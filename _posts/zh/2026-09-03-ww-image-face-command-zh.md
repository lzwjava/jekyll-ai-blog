---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ww 图像人脸命令
translated: true
type: note
---

完成。以下是我添加的内容：

## 新命令：`ww image face`

**模块：** `ww/image/face.py` — 一个灵活的、面部感知的照片裁剪工具，将你原先就业文件脚本中的逻辑移植到了 `ww` 工具集中。

**功能说明：**
1. 使用 macOS Vision（`VNDetectFaceRectanglesRequest`）检测最大面部。
2. 以面部为中心进行头部和肩部裁剪，面部中心位于距离顶部可配置的比例位置。
3. 限制在图像边界内，然后使用 LANCZOS 重采样到每个目标像素尺寸。

**默认预设**（当不指定 `--size`/`--preset` 时，会生成所有预设）：
- `square_600x600`、`rectangle_800x1000`、`qmas_visa_1500x2000`、`1inch_id_295x413`、`2inch_id_413x579`、`passport_413x531`

**灵活性参数：**
- `-o / --out` — 自定义输出目录（默认：源文件旁创建 `<源文件名>_face/`）
- `--size WxH`（可重复）— 临时指定目标尺寸；追加 `= 名称` 可为文件命名，例如 `--size 600x600 = profile`
- `--preset NAME`（可重复）— 仅生成这些命名的预设
- `--scale / --face-scale` — 裁剪高度 = N × 面部高度（默认为 2.7）
- `--top / --face-top` — 面部中心距顶部的垂直比例（默认为 0.40）
- `--quality` — JPEG 质量（默认为 95）
- `--dpi` — 输出 DPI（默认为 300）
- `--format JPEG|PNG`

**示例：**
```
ww image face ~/IMG_6127.JPG                          # 生成所有 6 个预设
ww image face ~/IMG_6127.JPG -o ./out                 # 自定义目录
ww image face ~/IMG_6127.JPG --size 600x600 --size 413x531
ww image face ~/IMG_6127.JPG --scale 2.5 --top 0.45 --quality 85
```

**已完成配置：**
- `pyproject.toml`：添加了 `pyobjc-framework-Vision>=9.0` 依赖（并运行了 `uv sync`）。
- `ww/main.py`：在 `image` 组中注册了 `face`（帮助文本 + 分发）。
- `~/.zsh/completions/_ww`：将 `face` 添加到了 `image_cmds` 中。运行 `autoload -Uz compinit && compinit` 以重新加载。

已使用 `IMG_6127.JPG` 验证——所有预设和自定义尺寸均正确裁剪。