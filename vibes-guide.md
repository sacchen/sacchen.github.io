# Adding images to the vibes page

## Setup (one-time)

None — uses `uv` to manage dependencies inline.

## Adding images

1. Drop screenshot files into `assets/vibes/`.
   Supported formats: `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.heic`, `.heif`, `.avif`

2. *(Optional)* Add source URLs to `vibes_sources.yml` in the repo root:
   ```yaml
   foo.png: https://example.com
   bar.png: https://another.com
   ```
   Images with a URL will be clickable links on the vibes page.

3. *(Optional)* If the image is too small to read at its default size, add a size
   hint to `vibes_sizes.yml` in the repo root:
   ```yaml
   dense_spreadsheet.png: 2.4
   ```
   The number multiplies the image's display area. 1.0 is the default; 2.0 is twice
   the area, i.e. about 1.4x wider and taller. Rough guide: dense table or diagram
   2.0-2.5, tweet or meme with small text 1.3-1.5, photo or big-text poster 1.0.

4. Regenerate the metadata JSON:
   ```
   uv run --with pillow lister.py
   ```

5. Commit everything together:
   ```
   git add assets/vibes/ vibes_sources.yml vibes_sizes.yml
   git commit -m "Add vibes images"
   ```

## How it works

- `lister.py` reads every image in `assets/vibes/`, records its dimensions, merges any URLs from `vibes_sources.yml` and size hints from `vibes_sizes.yml`, and writes `assets/vibes/image_widths_heights.json`.
- The vibes page (`/vibes/`) fetches that JSON at load time and places images in a collision-detected freeform layout.
- Sizing follows [guzey.com/vibes](https://guzey.com/vibes/): each image gets a scale
  factor that pulls it toward a common display area (126,000 px², matching guzey's
  median), bounded to never shrink past 1/8 of native or upscale past 1x, and capped so
  nothing dominates the canvas. Anchoring to native resolution rather than forcing a
  fixed size is what keeps the page from reading as a uniform grid.
- Pixel dimensions can't tell you how big an image *needs* to be — a 3000px photo of a
  poster reads fine small, a 2200px spreadsheet doesn't read at any size that fits on a
  canvas. That's what `vibes_sizes.yml` is for, and why every image links to its
  full-size file (or its source URL, if `vibes_sources.yml` has one) in a new tab.
- **Crop dead space before reaching for a size hint.** `tiktok_coding.png` was 41% black
  letterbox bars; cropping it to its content box made the caption readable while using
  *less* room on the canvas than bumping its weight did.

## Adding a new wide page

Any page that needs more than 800px can use `layout: wide` (1400px max-width):

```yaml
---
layout: wide
title: My Page
---
```

Add it to the nav by appending to `_data/navigation.yml`:

```yaml
- name: My Page
  url: /my-page/
```
