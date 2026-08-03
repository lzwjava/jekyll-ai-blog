---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSpec：推测性解码框架
translated: true
type: note
---

这是**DeepSpec**——来自**DeepSeek AI**（https://github.com/deepseek-ai/DeepSpec）的开源研究代码库，用于训练和评估**用于投机解码的草稿模型**。它是**DSpark论文**（"DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation", arXiv:2607.05147）的官方实现。

## 功能

投机解码通过让一个小型“草稿”模型提出tokens，然后由大型“目标”模型并行验证，从而加速LLM推理。DeepSpec提供了完整的流水线，用于针对目标模型（Qwen3或Gemma 4系列）训练这些草稿模型，并在基准测试上评估由此产生的加速/接受率。

## 结构

**入口点**
- `train.py` — 为每个可见GPU生成一个训练工作进程（不使用torchrun；使用`torch.multiprocessing.spawn`）
- `eval.py` — 在9个基准测试（gsm8k, math500, aime25, humaneval, mbpp, livecodebench, mt-bench, alpaca, arena-hard-v2）上评估训练好的草稿检查点与目标模型对比
- `config/` — 12个按算法/模型配置的配置文件（dspark, dflash, eagle3 × Qwen3 4B/8B/14B, Gemma 12B）

**`deepspec/` 包（约10.8k行，65个Python文件）**
- `modeling/` — 三种草稿模型架构：
  - **DSpark**（新算法）：基于块（block-wise）的半自回归草稿模型，具有多层“锚定”注意力机制，关注目标隐藏状态；一个**Markov head**用于token级偏差；一个**confidence head**用于提前停止
  - **DFlash** — 移除Markov/confidence head的DSpark（仅CE）
  - **Eagle3** — 改编自SpecForge
- `trainer/` — 分布式训练器（`base_trainer`, `dspark_trainer`, `eagle3_trainer`），检查点管理器，带有原子性的`step_latest`符号链接
- `eval/` — 投机解码评估器，包含草稿提案/验证循环，confidence head校准记录器
- `data/` — 目标缓存数据集加载器，CUDA预取器，JSONL数据集，解析器
- `utils/` — 采样，融合优化器，分布式初始化，配置解析，指标，HFAI暂停支持

**`scripts/`** — 三阶段工作流：
1. `data/` — 下载/分割`open-perfectblend`，通过SGLang服务器用目标模型重新生成答案，并预计算每个token的隐藏状态**目标缓存**（⚠️ 默认Qwen3-4B设置下约38TB——一个实际限制）
2. `train/` — `train.sh`启动训练，使用缓存；检查点存放在`~/checkpoints/<project>/<exp>/step_*`
3. `eval/` — `eval.sh`运行接受率评估

## 值得注意的细节
- **训练数据**：草稿模型被训练用于从缓存的目标隐藏状态预测*目标模型*的输出，采用混合损失（CE + 隐藏状态的L1损失 + confidence head损失，并带有token距离衰减）
- **归属**：Eagle3代码改编自SpecForge（Apache-2.0）；DFlash设计来自z-lab/dflash（MIT）——参见`NOTICE`
- **已发布的检查点**：`deepseek-ai/dspark_qwen3_4b_block7`、`deepseek-ai/eagle3_*`等在HuggingFace上
- **硬件假设**：单节点，8个GPU；每GPU batch size为1，全局batch为512

简而言之：这是一个研究级别的投机解码草稿模型训练+评估框架的实现，其中DSpark是主要贡献。