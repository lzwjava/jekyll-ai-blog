---
audio: false
generated: true
image: false
lang: en
layout: post
title: Creating a Cooking Image Collage
translated: false
type: note
---

Here's how I did it, step by step:

## 1. Source Material Discovery

Read `original/2024-12-29-cooking-en.md` and found images in two directories:

- `assets/images/cooking/` — 22 files (c1, c2, cooking1-11, porridge1-9)
- `assets/images/airfryer/` — 7 files (s1-s7)

## 2. Image Selection (9 images, 3 categories)

Picked 9 images for diversity:

- **Stir-fry/dishes**: cooking1 (beef stir-fry), cooking2 (braised fish), cooking4 (pepper stir-fry in wok)
- **Porridge**: porridge1 (congee with meatballs), porridge2 (clay pot porridge), porridge3 (rice cooker fish)
- **Air fryer**: s1 (fries), s3 (chicken wings), s5 (roasted chicken)

## 3. Image Merging — ImageMagick `montage`

The key tool is ImageMagick's `montage` command. Two stages:

**Stage A — Resize all 9 to uniform 400x400:**

```bash
for img in cooking1.jpg cooking2.jpg cooking4.jpg porridge1.jpg porridge2.jpg porridge3.jpg s1.jpg s3.jpg s5.jpg; do
  magick "$img" -resize 400x400^ -gravity center -extent 400x400 "/tmp/cooking_tiles/$name"
done
```

- `-resize 400x400^` — scale so the **shorter** side hits 400px (the `^` means "at least this size")
- `-gravity center -extent 400x400` — crop from center to exactly 400x400

**Stage B — Combine into 3x3 grid:**

```bash
magick montage \
  tile1.jpg tile2.jpg ... tile9.jpg \
  -tile 3x3 -geometry 400x400+4+4 -background white \
  cooking_collage.jpg
```

- `-tile 3x3` — 3 columns, 3 rows
- `-geometry 400x400+4+4` — each cell is 400x400 with 4px gap between images
- `-background white` — white fill for gaps

**Why two stages?** The `montage` geometry parameter doesn't reliably resize source images on this ImageMagick build (the "Freetype delegate" warning). Pre-resizing guarantees uniform tiles.

## 4. Compression

The raw collage was 595KB — over the 500KB pre-commit limit. Fixed with:

```bash
magick cooking_collage.jpg -quality 80 cooking_collage.jpg
```

Result: 359KB, passes the check.

## 5. Writing the Section

Added to the portfolio between "Passed Courses" and "What's Next" — a concise section covering:

- The air fryer as primary tool
- Porridge and stir-fry skills
- Cooking-programming analogy (same process applies to similar items, order of operations matters)
- The collage image with Jekyll-compatible centered/caption markup

## Summary of Tools Used

| Step | Tool | Command |
| ------ | ------ | --------- |
| Resize | ImageMagick `magick` | `-resize 400x400^ -gravity center -extent 400x400` |
| Combine | ImageMagick `montage` | `-tile 3x3 -geometry 400x400+4+4` |
| Compress | ImageMagick `magick` | `-quality 80` |
| Edit | `patch` tool | find-and-replace in the .md file |
| Git | `gh` CLI | commit, push, `gh workflow run` |
