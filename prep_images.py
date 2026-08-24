#!/usr/bin/env python3
"""
prep_images.py — get images in assets/vibes/ ready to commit.

Run it after dropping new files in and before lister.py:

  uv run prep_images.py

Two different jobs, split by whether git already tracks the file.

Files git does not track yet are new drops, and they get the full treatment:
converted out of formats browsers can't show, re-encoded if that wins anything,
normalised to sRGB, and stripped of metadata. Files git does track have already
been through this, so they only ever get a lossless metadata strip — a committed
image is never re-encoded, because a second lossy generation buys nothing and
costs a little of the picture every time.

What it fixes, roughly in order of how badly it bites:

  HEIC. Safari renders it, Chrome and Firefox render nothing at all. Photos come
  off an iPhone this way and look fine locally, which is what makes it nasty.

  EXIF. Phone photos carry GPS coordinates. This is a public repo.

  Wide-gamut profiles. A Display P3 photo whose profile is merely deleted comes
  out oversaturated, so the pixels get converted to sRGB rather than the tag
  being dropped on its own. Committed files keep their profile untouched: it is
  colour data, not metadata, and removing it is not free.

  Orientation flags. lister.py reads dimensions off the file, which for a rotated
  photo are the *unrotated* ones — so the canvas reserves a landscape box for an
  image the browser draws portrait. Baking the rotation in makes the box match.

  Size. Screenshots land as multi-megabyte PNGs and phone photos as 12MP JPEGs.

Format is chosen per image by measuring, not by rule. Every plausible encoding is
tried and the smallest one that passes the quality gate wins, which is how a
palette PNG beats JPEG on a spreadsheet and loses to it on a photograph.

Nothing here may change how big an image appears on the canvas. The vibes layout
derives display size from native pixel dimensions via the power-of-two ladder in
_layouts/vibes.html, so a resize is only allowed when it lands on the same rung,
and that is asserted per file.
"""
# /// script
# dependencies = ["pillow", "pillow-heif", "numpy"]
# ///

import io
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageCms, ImageOps

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    sys.exit("pillow-heif not found — run: uv run prep_images.py")

VIBES = Path("assets/vibes")
EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".heic", ".heif", ".avif"}

# Formats every browser renders. Anything outside this has to be re-encoded even
# when the re-encode comes out larger, which for HEIC it sometimes does.
BROWSER_SAFE = {"PNG", "JPEG", "MPO", "GIF", "WEBP"}

SRGB = ImageCms.createProfile("sRGB")

GOAL_AREA = 600 * 400       # must match GOAL_AREA in _layouts/vibes.html
RUNGS = (1, 2, 4, 8)


def display_size(w, h):
    """Mirror of sizeFor() in _layouts/vibes.html, ignoring weights and clamping."""
    for r in RUNGS:
        if w * h / (r * r) <= GOAL_AREA:
            return round(w / r), round(h / r)
    return round(w / RUNGS[-1]), round(h / RUNGS[-1])


# --- lossless metadata strippers -------------------------------------------
#
# Three containers, three sets of byte surgery. Re-encoding would remove metadata
# too, but only these leave the pixels bit-for-bit identical, which is what lets
# a committed file be cleaned without being degraded.

def strip_jpeg(data, keep_icc=True):
    """Drop EXIF/XMP/IPTC/comments from a JPEG. APP0 (JFIF) and, optionally,
    APP2 (ICC) survive; everything else in the APPn range goes."""
    if data[:2] != b"\xff\xd8":
        return data
    keep_markers = {0xE0} | ({0xE2} if keep_icc else set())
    out, i = bytearray(b"\xff\xd8"), 2
    while i < len(data):
        if data[i] != 0xFF:
            out += data[i:]
            break
        marker = data[i + 1]
        if marker == 0xDA:                       # start of scan — rest is entropy data
            out += data[i:]
            break
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            out += data[i:i + 2]
            i += 2
            continue
        length = int.from_bytes(data[i + 2:i + 4], "big")
        drop = (0xE1 <= marker <= 0xEF or marker == 0xFE) and marker not in keep_markers
        if not drop:
            out += data[i:i + 2 + length]
        i += 2 + length
    return bytes(out)


def strip_png(data):
    """Drop eXIf and the text/timestamp chunks from a PNG. iCCP is left alone."""
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return data
    drop = {b"eXIf", b"tEXt", b"zTXt", b"iTXt", b"tIME"}
    out, i = bytearray(data[:8]), 8
    while i + 8 <= len(data):
        length = int.from_bytes(data[i:i + 4], "big")
        chunk = data[i:i + 12 + length]
        if data[i + 4:i + 8] not in drop:
            out += chunk
        i += 12 + length
    return bytes(out)


def strip_webp(data):
    """Drop EXIF/XMP chunks from a RIFF/WebP container."""
    if data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return data
    body, i = bytearray(), 12
    while i + 8 <= len(data):
        tag = data[i:i + 4]
        length = int.from_bytes(data[i + 4:i + 8], "little")
        chunk = data[i:i + 8 + length + (length & 1)]
        if tag == b"VP8X":                       # clear the "EXIF/XMP present" flags
            patched = bytearray(chunk)
            patched[8] &= ~0b00001100
            chunk = bytes(patched)
        if tag not in (b"EXIF", b"XMP "):
            body += chunk
        i += 8 + length + (length & 1)
    return b"RIFF" + (len(body) + 4).to_bytes(4, "little") + b"WEBP" + bytes(body)


STRIPPERS = {"JPEG": strip_jpeg, "MPO": strip_jpeg, "PNG": strip_png, "WEBP": strip_webp}


# --- loading ----------------------------------------------------------------

def load(path):
    """Open an image as sRGB pixels with any rotation applied.

    Returns the image plus what had to be done to it, which is also what decides
    whether the original bytes are still usable.
    """
    im = Image.open(path)
    fmt = im.format
    exif_count = len(im.getexif())
    icc = im.info.get("icc_profile")
    profile = None
    if icc:
        profile = ImageCms.ImageCmsProfile(io.BytesIO(icc)).profile.profile_description

    im = ImageOps.exif_transpose(im)
    rotated = Image.open(path).size != im.size

    has_alpha = im.mode in ("RGBA", "LA", "PA") or "transparency" in im.info
    im = im.convert("RGBA" if has_alpha else "RGB")

    converted = False
    if icc and profile != "sRGB":
        alpha = im.getchannel("A") if has_alpha else None
        im = ImageCms.profileToProfile(
            im.convert("RGB"), ImageCms.ImageCmsProfile(io.BytesIO(icc)), SRGB,
            outputMode="RGB")
        if alpha is not None:
            im.putalpha(alpha)
        converted = True

    # The pixels are sRGB now. PNG save carries info["icc_profile"] straight
    # through quantize(), and leaving the old P3 tag on converted pixels makes a
    # browser apply the transform a second time.
    im.info.pop("icc_profile", None)
    return im, fmt, exif_count, converted, rotated, profile


def has_real_alpha(im):
    return im.mode == "RGBA" and im.getchannel("A").getextrema()[0] != 255


# --- quality measurement ----------------------------------------------------

def flat_mask(rgb):
    """Pixels whose 3x3 neighbourhood is one exact colour.

    This is where a lossy codec's ringing shows up as a halo, and it is the
    artifact you actually notice on this page — a caption on a white card with a
    grey mist around it. Error out in textured areas is invisible by comparison,
    so it gets a separate, much looser budget.
    """
    g = np.asarray(rgb.convert("L"), dtype=np.int16)
    hi = lo = g
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            shifted = np.roll(np.roll(g, dy, 0), dx, 1)
            hi = np.maximum(hi, shifted)
            lo = np.minimum(lo, shifted)
    return (hi - lo) == 0


def measure(reference, candidate, mask):
    a = np.asarray(reference, dtype=np.int16)
    b = np.asarray(candidate.convert("RGB"), dtype=np.int16)
    d = np.abs(a - b).max(axis=2)
    # A high percentile rather than the max: one stray pixel in a smooth patch of
    # sky is not the artifact being screened for, and letting it veto sends whole
    # photographs to a lossless codec at three times the size.
    flat = float(np.percentile(d[mask], 99.9)) if mask.any() else 0.0
    return {"flat": round(flat, 1), "mean": float(d.mean()),
            "p999": float(np.percentile(d, 99.9))}


def acceptable(q, flat_fraction):
    """Whether an encoding is good enough to ship.

    Screening graphics on average error as well turned out to be redundant with
    the flat-region test, and only had the effect of pushing illustrations onto a
    lossless codec at three times the size.
    """
    if flat_fraction >= 0.02 and q["flat"] > 6:
        return False
    return q["mean"] <= 3.5 and q["p999"] <= 50


def classify(im):
    """Photograph or flat-colour graphic — they want opposite codecs."""
    rgb = im.convert("RGB")
    w = min(rgb.width, 900)
    small = rgb.resize((w, max(1, round(rgb.height * w / rgb.width))))
    colours = small.getcolors(maxcolors=200_000)
    if colours is None:
        return "photo"
    dominant = max(c for c, _ in colours) / (small.width * small.height)
    return "photo" if len(colours) > 40_000 and dominant < 0.20 else "graphic"


# --- encoding ---------------------------------------------------------------

def encode(im, kind, alpha):
    buf = io.BytesIO()
    if kind == "jpeg":
        im.convert("RGB").save(buf, "JPEG", quality=88, subsampling=0,
                               optimize=True, progressive=True)
    elif kind == "webp":
        im.save(buf, "WEBP", quality=90, method=4)
    elif kind == "webp95":
        im.save(buf, "WEBP", quality=95, method=4)
    elif kind == "webp_lossless":
        im.save(buf, "WEBP", lossless=True, method=4)
    elif kind == "palette":
        if alpha:
            im.quantize(colors=256, method=Image.Quantize.FASTOCTREE).save(
                buf, "PNG", optimize=True)
        else:
            im.convert("RGB").convert(
                "P", palette=Image.Palette.ADAPTIVE, colors=256).save(
                buf, "PNG", optimize=True)
    elif kind == "png":
        im.save(buf, "PNG", optimize=True)
    return buf.getvalue()


SUFFIX = {"jpeg": ".jpg", "webp": ".webp", "webp95": ".webp",
          "webp_lossless": ".webp", "palette": ".png", "png": ".png"}


def process_new(path):
    """Full pipeline for a file that isn't committed yet."""
    raw = path.read_bytes()
    im, fmt, exif_count, converted, rotated, profile = load(path)
    alpha = has_real_alpha(im)
    if not alpha and im.mode == "RGBA":
        im = im.convert("RGB")

    target = display_size(*im.size)

    # A 12MP phone photo shown at 504px carries eight times the pixels the
    # click-through needs. Halving drops it one rung, and since rungs are 4x
    # apart in area the ladder renders the result at exactly the same size.
    resized = ""
    if im.width * im.height >= 8_000_000 and display_size(im.width // 2, im.height // 2) == target:
        im = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
        resized = f"{im.width}x{im.height}"
    assert display_size(*im.size) == target, f"{path.name} changed rung"

    reference = im.convert("RGB")
    mask = flat_mask(reference)
    flat_fraction = float(mask.mean())
    kind = classify(im)

    # Lossless encoders never win on a photograph and are slow on a 12MP one, so
    # only the codec family that can plausibly win gets tried.
    kinds = ["webp", "webp95"] if kind == "photo" else \
            ["palette", "png", "webp_lossless", "webp", "webp95"]
    if not alpha:
        kinds.append("jpeg")

    candidates = {}
    for k in kinds:
        data = encode(im, k, alpha)
        q = {"flat": 0.0, "mean": 0.0, "p999": 0.0} if k in ("png", "webp_lossless") \
            else measure(reference, Image.open(io.BytesIO(data)), mask)
        candidates[k] = (data, q)

    # Keeping the original bytes is only on the table for a format every browser
    # renders, and only when nothing about the pixels had to change.
    keep = None
    if fmt in BROWSER_SAFE and not converted and not rotated and not resized:
        stripper = STRIPPERS.get(fmt)
        stripped = stripper(raw) if stripper else raw
        keep = (stripped, path.suffix if fmt != "MPO" else ".jpg")

    passing = {k: v for k, v in candidates.items() if acceptable(v[1], flat_fraction)}
    if not passing:
        passing = {"png": (encode(im, "png", alpha), {"flat": 0.0, "mean": 0.0, "p999": 0.0})}
    pick, (data, q) = min(passing.items(), key=lambda kv: len(kv[1][0]))
    suffix = SUFFIX[pick]

    # Don't spend a lossy generation on a re-encode that barely pays, and never
    # write a bigger file than we were handed when the original is usable.
    if keep and len(data) > 0.90 * len(keep[0]) - 25 * 1024:
        data, suffix, pick, q = keep[0], keep[1], "keep", {"flat": 0.0, "mean": 0.0, "p999": 0.0}

    notes = []
    if converted:
        notes.append(f"{profile}->sRGB")
    if rotated:
        notes.append("rotation baked in")
    if resized:
        notes.append(f"halved to {resized}")
    if fmt not in BROWSER_SAFE:
        notes.append(f"{fmt} is Safari-only")
    if exif_count:
        notes.append(f"{exif_count} EXIF tags")
    return path.stem + suffix, data, pick, notes


def process_tracked(path):
    """Lossless metadata strip for a file that's already committed."""
    raw = path.read_bytes()
    fmt = Image.open(path).format
    stripper = STRIPPERS.get(fmt)
    if not stripper:
        return None
    stripped = stripper(raw)
    if stripped == raw:
        return None
    exif_count = len(Image.open(path).getexif())
    return path.name, stripped, "strip", [f"{exif_count} EXIF tags"]


def main():
    dry_run = "--dry-run" in sys.argv
    everything = "--all" in sys.argv

    untracked = {Path(f) for f in subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", str(VIBES)],
        capture_output=True, text=True).stdout.split()}

    files = sorted(f for f in VIBES.iterdir()
                   if f.is_file() and f.suffix.lower() in EXTENSIONS)
    if not files:
        sys.exit(f"no images found in {VIBES}")

    before = after = 0
    changed = 0
    for path in files:
        original = path.stat().st_size
        try:
            result = process_new(path) if (path in untracked or everything) \
                     else process_tracked(path)
        except Exception as e:
            print(f"  skip {path.name}: {e}", file=sys.stderr)
            continue
        if result is None:
            before += original
            after += original
            continue

        name, data, pick, notes = result
        before += original
        after += len(data)
        if name == path.name and data == path.read_bytes():
            continue

        changed += 1
        arrow = f"{path.name} -> {name}" if name != path.name else path.name
        print(f"  {arrow}\n      {original // 1024}K -> {len(data) // 1024}K"
              f"  [{pick}]{('  ' + ', '.join(notes)) if notes else ''}")
        if not dry_run:
            if name != path.name:
                path.unlink()
            (VIBES / name).write_bytes(data)

    verb = "would change" if dry_run else "changed"
    print(f"\n{verb} {changed} of {len(files)} files, "
          f"{before / 1024 / 1024:.1f} MB -> {after / 1024 / 1024:.1f} MB")
    if changed and not dry_run:
        print("now run: uv run --with pillow --with pillow-heif lister.py")


if __name__ == "__main__":
    main()
