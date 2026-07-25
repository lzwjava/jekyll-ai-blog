---
audio: false
generated: true
image: false
lang: en
layout: post
title: FLUX Generation on AMD Radeon
translated: false
type: note
---

Everything works! Here's the generated landscape image:

![Mountain Landscape](flux_output_1785005047.png)

### ✅ What we have now

**`ahl gen` command** — generate images with FLUX on the remote server:

```bash
# Basic usage
ahl gen "a cute cat" --download

# More options
ahl gen "cyberpunk city" --steps 8 --width 1024 --height 1024 --download

# Different model variant
ahl gen "portrait" --model dev --steps 4 --download

# Custom output name, no download
ahl gen "abstract art" --output my_art.png
```

**`infer_flux.py`** — standalone script with same functionality:
```bash
python3 infer_flux.py "a serene mountain landscape" --download
```

### Performance on AMD Radeon 48 GB

| Steps | Resolution | Time |
|-------|-----------|------|
| 2 | 1024×1024 | **26.2s** |
| 4 | 1024×1024 | **33.5s** |
| Max VRAM | — | **6.43 GB** (well within 48 GB) |
