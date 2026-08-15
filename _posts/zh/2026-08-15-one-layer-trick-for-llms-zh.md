---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLMs的单层技巧
translated: true
type: note
---

这是 **AirLLM** —— 一种在小型 GPU 上运行超大 LLM 的技巧，无需量化/蒸馏/剪枝。以下是核心思路来自代码（`air_llm/airllm/airllm_base.py`）：

## 单层技巧

70B 模型的内存问题在于通常需要把所有 70B 参数加载到 GPU 上。AirLLM 的做法是 **每次只在 GPU 上保留一层**，因此所需显存 ≈ *一层* 的大小，而不是整个模型。这就是 671B DeepSeek-V3 能在约 12GB 显存上运行、Kimi K3（2.8T）能在 <4GB 显存上运行的原因。

该机制由四部分组成：

**1. 先在磁盘上按层切分 checkpoint**（`utils.split_and_save_layers`）——原始权重文件被分解为每层一个分片并缓存。这就是 README 中警告的磁盘占用步骤。

**2. 在 `meta` 设备上实例化模型** —— `init_empty_weights()` 构建完整的 transformers 模型，包含所有参数 *形状*，但不占用内存。模型在“代码层面”是完整的（拥有所有注意力/旋转位置编码/生成逻辑），只是没有权重。

**3. 使用 forward hooks 流式加载权重**：
- 每个大模块（embedding → 每个 decoder layer → final norm → lm_head）都挂上 pre-hook 和 post-hook。
- **Pre-hook**：在模块运行前，将该层的分片从磁盘加载到 GPU。
- **Post-hook**：一旦该层完成，立即把权重移回 `meta` 并调用 `clean_memory()`。
- **预取**：一个 worker 线程在当前层计算时加载 *下一层*，让磁盘 I/O 与数学计算重叠（约 10% 的速度提升）。

**4. 针对 MoE 模型的逐专家流式加载**（`_setup_expert_streaming`）——近期的一大改进。一个稀疏 MoE 层（DeepSeek、Kimi K3）包含数百个专家，但每个 token 只会路由到其中少数几个。由于 transformers 会把每个被选中的专家当作独立模块来调用，AirLLM 挂钩 *单个专家*，只加载实际运行的专家——因此 K3 一层完整展开约 55GB，但一个 token 触及的只有约 1GB。显存需求降到 *单个专家* 的大小。

## 额外功能

- **压缩**：可为磁盘分片选用 bitsandbytes 4bit/8bit；FP8/MXFP4 预量化 checkpoint 将 *打包后* 的字节流式传到 GPU（PCIe 流量减少 4 倍），并在 GPU 上解压。
- **AutoModel** 自动检测架构——大多数新模型发布当天就能用，因为前向传播完全委托给 transformers（`forward`/`generate` 只是调用 `self.model`）。

**权衡**：用显存换速度——每一层都要经历一次 磁盘→GPU 的往返，所以比常规的全内存推理慢很多。它面向的是爱好者级显卡，而非生产环境吞吐量。