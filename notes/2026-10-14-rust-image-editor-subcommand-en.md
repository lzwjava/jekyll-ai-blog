---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rust Image Editor Subcommand
translated: false
type: note
---

Done. I added a full **mini-Photoshop / ImageMagick-style image editor** as the `ll image` subcommand, implemented in pure Rust (no external `convert` binary needed).

## Files changed

| File | Change |
| --- | --- |
| `src/image_ops.rs` | **new** ~2230 lines — 30 commands, 24 registered operators, unit tests |
| `src/main.rs` | `image` dispatch, usage line, clean `error: …` + exit 1 |
| `README.md` | new "Image editor" section |
| `Cargo.toml` / `Cargo.lock` | added `image` 0.25 (png, jpg, webp, gif, bmp, tiff, ico, pnm, qoi, tga) |

## Commands (`ll image list`)

- **Geometry**: `crop` (`-g 400x300+50+50`, percentages, `-10-10` from far edge), `resize` (`-p 50%` / `-w/-h`, 5 filters, `fit|fill|stretch`), `thumbnail` (never enlarges), `rotate` (any angle, alpha-aware fill; fast paths for 90/180/270), `flip`, `pad` (canvas + 9-way gravity), `border`, `trim` (auto-crop uniform edges)
- **Color**: `grayscale`, `invert`, `sepia`, `brightness`, `contrast`, `saturate`, `hue`, `opacity`, `posterize`
- **Filters**: `blur` (+`--fast`), `sharpen` (unsharp mask), `pixelate`, `grain`, `edge` (Sobel), `emboss`
- **Files/tools**: `info [--json]`, `slice` (`--cols/--rows` grid **or** `--tile 512x512`, `{r}`/`{c}` name patterns), `montage` (contact sheet, accepts directories), `convert` (incl. `--out-dir` batch), `view` (truecolor ANSI half-block terminal preview), `apply` (chain ops in one pass)
- Colors accept `#rrggbb`, `r,g,b`, names (`red`, `gold`, `transparent`…); `--quality` for jpeg; alpha auto-flattened for formats without it; output dirs auto-created.

```bash
ll image crop photo.png out.png -g 400x300+50+50
ll image slice photo.png tiles/part --cols 3 --rows 2
ll image apply photo.png out.webp crop:80%x80% resize:1200x_ grayscale sharpen:2 -q 85
ll image view photo.png
```

## Verification

- `cargo test`: **20/20 pass** (geometry/color parsing, all operator behaviors, file round-trip)
- Cross-checked against ImageMagick: negative-offset crop, `rotate 90`, `flop` → **RMSE 0**; `resize 50%` vs IM Lanczos → 0.11%; `saturate -100` == our grayscale (RMSE 0)
- Smoke-tested every one of the 30 commands end-to-end; `cargo clippy` is clean for the new module
