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
   The number multiplies the image's display area after its rung is picked. 1.0 is the
   default; 2.0 is twice the area, i.e. about 1.4x wider and taller; rungs are 4x apart
   in area, so 4.0 is exactly one rung bigger. Rough guide: dense table or chart
   2.0-2.5, tweet or meme with small text 1.5-2.0, photo or big-text poster nothing at
   all — leaving most images unhinted is what gives the page its range of sizes.

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
- Sizing follows [guzey.com/vibes](https://guzey.com/vibes/): each image is shown at
  1/1, 1/2, 1/4 or 1/8 of native resolution — the coarsest reduction that brings it
  under a 240,000 px² target. The quantization is the point. Two images 20% apart in
  native resolution can land a full rung apart, so the canvas holds a 614px-wide meme
  next to a 240px one instead of reading as a grid of equal tiles.
  [girl.surgery](https://girl.surgery/website_vibes/) normalises every image to one
  exact area instead; that page's images all come out the same size, and so did this
  one before.
- Pixel dimensions can't tell you how big an image *needs* to be — a 3000px photo of a
  poster reads fine small, a 2200px spreadsheet doesn't read at any size that fits on a
  canvas. That's what `vibes_sizes.yml` is for, and why every image links to its
  full-size file (or its source URL, if `vibes_sources.yml` has one) in a new tab.
- **Crop dead space before reaching for a size hint.** `tiktok_coding.png` was 41% black
  letterbox bars; cropping it to its content box made the caption readable while using
  *less* room on the canvas than bumping its weight did. When you do crop, lower the
  weight to match — `idle_doing_nothing.PNG` went from 2.0 to 1.5 after its bars came
  off, because the chart then filled the frame it was already being given.
- **Photos of screens usually need a white-point fix, not just a crop.** A projector or
  monitor shot rarely gets above ~70% brightness and skews blue, so it renders as a grey
  smudge next to memes that are actually white. `accountability_partner.jpg` was capped
  at RGB 178/161/179 before its channels were stretched onto the full range.

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
