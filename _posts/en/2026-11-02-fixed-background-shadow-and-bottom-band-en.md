---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixed background shadow and bottom band
translated: false
type: note
---

Done. The photo `image/photo_6126_body_white_600.jpg` has been fixed and committed (`001e1ca`).

## What was wrong
The old whitening only flood-filled the light-gray backdrop (~222–226) from the borders. Two background defects remained:

1. **The gray shadow you saw around the head** — a mid-gray halo ring (~120–170, neutral gray) hugging the hair/face silhouette, especially visible along the lower sides of the head.
2. **The whole bottom band** was left un-whitened (dark bluish-gray studio corner + warm floor gradient) — this is what made the 背景色不均 (uneven color).

## What I did
Rewrote `image/whiten_bg_6126.py` to combine three border-connected flood fills + a person guard:

- **light fill** (distance ≤ 45 from white) — light-gray walls/top
- **mid-gray halo fill** — neutral, low-texture pixels with brightness 72–252, which catches the shadow ring beside the hair and under the chin
- **dark-bluish fill** — seeds the bottom edge, admits the bluish wall/floor strip (distance ≤ 80 of (95,118,140), low texture)
- **Apple Vision person segmentation guard** — pixels with high person probability in the head/shoulders zone are never whitened, so hair, face, collar are untouched

Also fixed two latent bugs in the rewrite (the flood fill's transposed coordinate order, and `np.roll`-wrapped texture that polluted the bottom rows).

## Verified result (before → after)
- bottom band: **0% → ~80% white** (remaining is invisible JPEG-level tone + the person's garment, which is kept)
- left/right margins: 100% / 97% white
- head halo ring: shadow removed
- person fully preserved: **0 hair pixels damaged**, head/face area 0% altered
- re-saved at JPEG quality 98 with 300 dpi

The person (including the tan garment visible below) is kept intact — only the background was normalized to pure white.
