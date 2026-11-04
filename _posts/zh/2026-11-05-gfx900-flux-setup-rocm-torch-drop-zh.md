---
audio: false
generated: true
image: false
lang: zh
layout: post
title: gfx900 FLUX 设置：ROCm Torch Drop
translated: true
type: note
---

目前状态：

**已完成**
| 步骤 | 结果 |
|---|---|
| 环境 | `.venv` (py3.12) + `fluxreel -e .` 已安装 |
| ffmpeg | 通过 `imageio-ffmpeg` → `~/.local/bin/ffmpeg` (包含 libx264) |
| 管线冒烟测试 | ✅ 通过 — 1080×1920, 30 fps, 15.00 s, H.264+AAC, 已渲染 CJK 幻灯片 |
| 服务器 | ✅ `fluxreel server --port 8000` → `/health` 正常, `/` 24 KB SPA |
| 检测到 GPU | AMD Radeon Pro WX 9100 (gfx900, Vega 10), 17.2 GB VRAM, ROCm 7.1 |
| ROCm torch | ✅ torch 2.2.2+rocm5.7 可在 gfx900 上运行 (需要 execstack 修复); torch 2.13+rocm7.1 **失败** — 无 gfx900 内核 |
| gfx900 上的 HIP | ✅ `hipcc --offload-arch=gfx900` 编译 + 运行正常 |
| sd.cpp Vulkan | ✅ 已构建, 识别为 `AMD Radeon Pro WX 9100 (RADV VEGA10)` |
| sd.cpp HIP | 🔄 构建中 (59%) |
| 模型 | 🔄 flux1-schnell-Q4_0 3.2/6.8 GB, t5-xxl-Q4 2.8/3.1 GB; ae + clip_l 已完成 |

**关键发现：** PyTorch 当前的 ROCm wheels (6.3/6.4/7.x) 放弃了对 gfx900 的支持，因此 `local` diffusers provider 无法在此显卡上配合现代 torch 运行。仍有两条可行路径：基于 **HIP/ROCm** 的 sd.cpp（正在构建中），或基于 **Vulkan** 的 sd.cpp（已构建完毕），两者均使用该仓库的 `sdcpp` provider。

下一步：完成 HIP 构建 + FLUX 下载，然后运行 `tests/smoke_test.py --provider sdcpp` 进行真实的 GPU 图像生成测试。