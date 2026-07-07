---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 模型选项：AWQ或配额？
translated: true
type: note
---

LibreChat 之前已经成功克隆——无需任何操作。

对于模型，您希望选择哪个选项？快速总结：

1. **较小的 AWQ 模型（约 4 GB）** — 我会切换到类似 `Qwen2.5-7B-Instruct-AWQ` 的模型，这很容易适配。现在即可使用。

2. **增加 RunPod 存储卷配额至 20 GB 以上** — 如果您能在 RunPod 控制面板中增加配额，我将重新下载完整的 Gemma 4 26B AWQ 模型。

3. **从 HuggingFace 流式加载** — 启动 SGLang 并将模型路径指向 HuggingFace 原始仓库，这样按需加载，无需完整下载（但需要足够的 VRAM 来运行 FP16 模型，其大小为 50 GB——16 GB VRAM 无法容纳）。

4. **使用原始 Gemma 4 FP16 配合 SGLang 的量化功能** — 加载 `google/gemma-4-26B-A4B-it`，SGLang 会实时量化以适配 VRAM，但仍需先完整下载约 50 GB 的模型。

选项 1 或 2 最现实。您选哪个？