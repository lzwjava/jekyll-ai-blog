---
audio: false
generated: true
image: false
lang: zh
layout: post
title: sd-cpp 路线：两个新幻灯片
translated: true
type: note
---

完成。`submission/02_slides.md` 中的变更摘要如下：

**新增幻灯片（在 Pipeline Overview 之后）：**

1.  **“sd-cpp 路线 — 量化快速通道”**（第 4 张）
    -   原生 C++ `sd-cli` 引擎，无 torch/diffusers 介入
    -   四组件 FLUX 加载（GPU 上的 Q4_0 transformer + VAE，CPU 上的 CLIP-L/T5-XXL 文本编码器）
    -   每图全新进程设计、GPU 串行化互斥锁、后端无关的 `ImageProvider` API

2.  **“sd-cpp 优化”**（第 5 张）
    -   每标志收益表：Q4_0（→ 12 GB 上约 8.75 GB/次）、4 步蒸馏、`--vae-tiling`、`--max-vram 10`、后端卸载、`--cfg-scale 1.0`、4:3 960×720、固定种子
    -   诚实的权衡说明：以每张图像的模型加载成本换取零内存增长/崩溃隔离

**对现有幻灯片的细微调整：**
- 流水线图：`Q4_0 GGUF (4-bit)` → `Q4_0 GGUF · sd-cpp`
- 模型策略表：Q4_0 行现在显示“**4-bit GGUF** 通过 **sd-cpp**”
- AMD 优化幻灯片：新增指针 `> 项目 1–5 由 sd-cpp 路线实现 — 请参阅上面的深入探讨。`
- 演示流程步骤 7：“量化 Q4