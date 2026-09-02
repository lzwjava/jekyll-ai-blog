---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 六种照片尺寸生成成功
translated: true
type: note
---

所有 6 种照片尺寸已在 `/Users/lzwjava/projects/employment-files/image/` 中成功生成。每张均从横向源图的中心裁剪（使用完整高度，确保头部保持在画面内），并以 300 DPI 重新采样：

| # | 文件 | 尺寸 | 比例 | 用途 |
| --- | ------ | ----------- | ------- | ---------- |
| 1 | `photo_1_square_600x600.jpg` | 600 × 600 | 1:1 正方形 | 简历头像 / 社交 |
| 2 | `photo_2_rectangle_800x1000.jpg` | 800 × 1000 | 4:5 矩形 | 简历 / LinkedIn |
| 3 | `photo_3_qmas_visa_1500x2000.jpg` | 1500 × 2000 | 3:4 | **QMAS / 香港签证**（与你提供的参考一致） |
| 4 | `photo_4_1inch_id_295x413.jpg` | 295 × 413 | 25×35 mm | 中国一寸证件照 |
| 5 | `photo_5_2inch_id_413x579.jpg` | 413 × 579 | 35×53 mm | 中国二寸证件照 |
| 6 | `photo_6_passport_413x531.jpg` | 413 × 531 | 33×48 mm | 护照 / 签证 |

说明：

- #3 的 3:4 构图与你的 `IMG_6126_QMAS.jpg` 参考图（1500×2000）完全一致。
- 脚本 `make_sizes.py` 与图片保存在同一目录，如需重新生成或调整尺寸可复用。
- 由于源图为横向，我以完整图像高度为中心进行水平裁剪——因此被摄者头部保持在画面内。若人脸偏离中心，请告知，我可以调整水平裁剪偏移量。
