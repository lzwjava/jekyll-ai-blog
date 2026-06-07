---
audio: false
generated: true
image: false
lang: en
layout: post
title: JPEG Beats PNG for Screenshots
translated: false
type: note
---

Two things at play:

**Resolution vs compression tradeoff.** The PNG was resized to 1000px — you permanently lost pixel data. The JPG kept the full original resolution but applied lossy compression at quality 50. More pixels + lossy > fewer pixels + lossless, visually.

**PNG is lossless but wasteful for screenshots.** A screenshot has gradients, anti-aliased text, and subtle color variations. PNG encodes every pixel exactly, which costs a lot of bits for that kind of content. JPG's DCT (discrete cosine transform) compresses 8×8 blocks by discarding high-frequency detail humans barely notice — so it packs far more visual information per kilobyte.

**The math roughly:**

- PNG at 1000px, lossless: 451KB for ~1M pixels
- JPG at full res (~2400px?), quality 50: 463KB for ~5.7M pixels

The JPG stores ~5x more pixels in roughly the same space. Even with lossy artifacts, 5.7M pixels at quality 50 beats 1M pixels at lossless quality every time for perceptual sharpness.

**For screenshots specifically**, JPG quality 50-70 is the sweet spot — text stays readable, UI elements stay sharp, and the DCT compression handles flat color regions very efficiently. PNG's lossless guarantee only wins when you need pixel-perfect accuracy (e.g., icons, pixel art, or images you'll re-edit).
