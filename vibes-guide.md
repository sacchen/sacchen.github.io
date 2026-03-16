# Adding images to the vibes page

## Setup (one-time)

```
pip3 install pillow pillow-heif
```

`pillow-heif` is optional — only needed for `.heic`/`.heif` images.

## Adding images

1. Drop screenshot files into `assets/vibes/`.
   Supported formats: `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.heic`, `.heif`, `.avif`

2. *(Optional)* Add source URLs to `vibes_sources.yml` in the repo root:
   ```yaml
   foo.png: https://example.com
   bar.png: https://another.com
   ```
   Images with a URL will be clickable links on the vibes page.

3. Regenerate the metadata JSON:
   ```
   python3 lister.py
   ```

4. Commit everything together:
   ```
   git add assets/vibes/ vibes_sources.yml
   git commit -m "Add vibes images"
   ```

## How it works

- `lister.py` reads every image in `assets/vibes/`, records its dimensions, merges any URLs from `vibes_sources.yml`, and writes `assets/vibes/image_widths_heights.json`.
- The vibes page (`/vibes/`) fetches that JSON at load time and places images in a collision-detected freeform layout (320px wide, height scaled proportionally).

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
