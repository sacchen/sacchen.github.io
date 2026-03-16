#!/usr/bin/env python3
"""
lister.py — scan assets/vibes/ and write assets/vibes/image_widths_heights.json.

Merge optional URL metadata from vibes_sources.yml:
  foo.png: https://example.com
  bar.png: https://another.com

Requirements:
  pip3 install pillow pillow-heif
"""

import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("pillow not found — run: pip3 install pillow pillow-heif")

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass  # HEIF support optional

VIBES_DIR = Path("assets/vibes")
OUTPUT = VIBES_DIR / "image_widths_heights.json"
SOURCES_FILE = Path("vibes_sources.yml")

EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".heic", ".heif", ".avif"}


def load_sources():
    if not SOURCES_FILE.exists():
        return {}
    # Minimal YAML parser for flat key: value mappings (no pyyaml dependency)
    sources = {}
    for line in SOURCES_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ": " in line:
            key, val = line.split(": ", 1)
            sources[key.strip()] = val.strip()
    return sources


def main():
    sources = load_sources()
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
        entries.append(entry)
        print(f"  {f.name}  {w}x{h}" + (f"  → {entry['url']}" if "url" in entry else ""))

    OUTPUT.write_text(json.dumps(entries, indent=2) + "\n")
    print(f"\nWrote {len(entries)} entries to {OUTPUT}")


if __name__ == "__main__":
    main()
