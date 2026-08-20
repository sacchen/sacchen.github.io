#!/usr/bin/env python3
"""
lister.py — scan assets/vibes/ and write assets/vibes/image_widths_heights.json.

Merge optional URL metadata from vibes_sources.yml:
  foo.png: https://example.com
  bar.png: https://another.com

Merge optional size hints from vibes_sizes.yml (area multiplier, default 1.0):
  foo.png: 2.0

Requirements:
  uv run --with pillow lister.py
"""

import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("pillow not found — run: uv run --with pillow lister.py")

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass  # HEIF support optional

VIBES_DIR = Path("assets/vibes")
OUTPUT = VIBES_DIR / "image_widths_heights.json"
SOURCES_FILE = Path("vibes_sources.yml")
SIZES_FILE = Path("vibes_sizes.yml")

EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".heic", ".heif", ".avif"}


def load_mapping(path):
    """Minimal YAML parser for flat key: value mappings (no pyyaml dependency)."""
    if not path.exists():
        return {}
    mapping = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ": " in line:
            key, val = line.split(": ", 1)
            mapping[key.strip()] = val.strip()
    return mapping


def load_weights():
    weights = {}
    for name, val in load_mapping(SIZES_FILE).items():
        try:
            weights[name] = float(val)
        except ValueError:
            print(f"  skip size hint {name}: {val!r} is not a number", file=sys.stderr)
    return weights


def main():
    sources = load_mapping(SOURCES_FILE)
    weights = load_weights()
    entries = []

    files = sorted(
        f for f in VIBES_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in EXTENSIONS
    )

    for f in files:
        try:
            with Image.open(f) as img:
                w, h = img.size
        except Exception as e:
            print(f"  skip {f.name}: {e}", file=sys.stderr)
            continue

        entry = {"filename": f.name, "width": w, "height": h}
        if f.name in sources:
            entry["url"] = sources[f.name]
        if f.name in weights:
            entry["weight"] = weights[f.name]
        entries.append(entry)
        note = ""
        if "weight" in entry:
            note += f"  x{entry['weight']}"
        if "url" in entry:
            note += f"  → {entry['url']}"
        print(f"  {f.name}  {w}x{h}{note}")

    OUTPUT.write_text(json.dumps(entries, indent=2) + "\n")
    print(f"\nWrote {len(entries)} entries to {OUTPUT}")


if __name__ == "__main__":
    main()
