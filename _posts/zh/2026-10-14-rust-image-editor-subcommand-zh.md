---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Rust图像编辑器子命令
translated: true
type: note
---

已完成。我添加了一个完整的 **迷你 Photoshop / ImageMagick 风格的图像编辑器**，作为 `ll image` 子命令，使用纯 Rust 实现（无需外部 `convert` 二进制文件）。

## 更改的文件

| 文件 | 更改 |
| --- | --- |
| `src/image_ops.rs` | **新增**约 2230 行 — 30 个命令、24 个已注册操作、单元测试 |
| `src/main.rs` | `image` 分发、用法行、干净的 `error: …` + exit 1 |
| `README.md` | 新增“图像编辑器”部分 |
| `Cargo.toml` / `Cargo.lock` | 添加 `image` 0.25（png、jpg、webp、gif、bmp、tiff、ico、pnm、qoi、tga） |

## 命令（`ll image list`）

- **几何**：`crop`（`-g 400x300+50+50`、百分比、`-10-10` 从远边缘开始）、`resize`（`-p 50%` / `-w/-h`、5 种滤镜、`fit|fill|stretch`）、`thumbnail`（绝不放大）、`rotate`（任意角度、alpha 感知填充；90/180/270 快速路径）、`flip`、`pad`（画布 + 9 方向 gravity）、`border`、`trim`（自动裁剪均匀边缘）
- **颜色**：`grayscale`、`invert`、`sepia`、`brightness`、`contrast`、`saturate`、`hue`、`opacity`、`posterize`
- **滤镜**：`blur`（+`--fast`）、`sharpen`（unsharp mask）、`pixelate`、`grain`、`edge`（Sobel）、`emboss`
- **文件/工具**：`info [--json]`、`slice`（`--cols/--rows` 网格 **或** `--tile 512x512`，`{r}`/`{c}` 名称模式）、`montage`（contact sheet，接受目录）、`convert`（包括 `--out-dir` 批处理）、`view`（truecolor ANSI half-block 终端预览）、`apply`（单次处理中链式操作）
- 颜色接受 `#rrggbb`、`r,g,b`、名称（`red`、`gold`、`transparent`…）；`--quality` 用于 jpeg；对于不支持 alpha 的格式，alpha 会被自动展平；输出目录自动创建。

```bash
ll image crop photo.png out.png -g 400x300+50+50
ll image slice photo.png tiles/part --cols 3 --rows 2
ll image apply photo.png out.webp crop:80%x80% resize:1200x_ grayscale sharpen:2 -q 85
ll image view photo.png
```

## 验证

- `cargo test`：**20/20 通过**（几何/颜色解析、所有操作行为、文件往返）
- 与 ImageMagick 交叉验证：负偏移裁剪、`rotate 90`、`flop` → **RMSE 0**；`resize 50%` 对比 IM Lanczos → 0.11%；`saturate -100` 等于我们的 grayscale（RMSE 0）
- 对所有 30 个命令进行了端到端冒烟测试；`cargo clippy` 对新模块无警告
