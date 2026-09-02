---
audio: false
generated: true
image: false
lang: en
layout: post
title: Six photo sizes generated successfully
translated: false
type: note
---

All 6 photo sizes have been generated successfully in `/Users/lzwjava/projects/employment-files/image/`. Each was cropped from the center of the landscape source (using the full height so the head stays in frame) and resampled at 300 DPI:

| # | File | Dimensions | Ratio | Use case |
| --- | ------ | ----------- | ------- | ---------- |
| 1 | `photo_1_square_600x600.jpg` | 600 × 600 | 1:1 square | Resume profile / social |
| 2 | `photo_2_rectangle_800x1000.jpg` | 800 × 1000 | 4:5 rectangle | Resume / LinkedIn |
| 3 | `photo_3_qmas_visa_1500x2000.jpg` | 1500 × 2000 | 3:4 | **QMAS / HK visa** (matches your reference) |
| 4 | `photo_4_1inch_id_295x413.jpg` | 295 × 413 | 25×35 mm | China 1-inch ID (一寸) |
| 5 | `photo_5_2inch_id_413x579.jpg` | 413 × 579 | 35×53 mm | China 2-inch ID (二寸) |
| 6 | `photo_6_passport_413x531.jpg` | 413 × 531 | 33×48 mm | Passport / visa |

Notes:

- #3 is exactly the same 3:4 framing as your `IMG_6126_QMAS.jpg` reference (1500×2000).
- The script `make_sizes.py` is saved alongside the images if you want to regenerate or tweak sizes.
- Since the source is landscape, I cropped from the horizontal center using the full image height — so the subject's head remains in frame. If the face is off-center, tell me and I can adjust the horizontal crop offset.
