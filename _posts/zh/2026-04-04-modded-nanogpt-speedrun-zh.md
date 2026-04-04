---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 模改NanoGPT速通基准测试
translated: true
type: note
---

**modded-nanogpt** 是一个开源的 GitHub 仓库，旨在为训练小型 GPT 风格语言模型提供高性能的“速通”基准。它专注于以最快速度在 **8 块 NVIDIA H100 GPU** 上达到特定的性能目标——即在 **FineWeb** 数据集的前 10,485,760 个词元上实现 **3.28 的交叉熵验证损失**。

### 起源与传承
该项目直接建立在 Andrej Karpathy 的教育工作之上：
- 它源自 Karpathy 的极简 PyTorch GPT-2 实现 **nanoGPT**（约 1.24 亿参数）。
- 以 Karpathy **llm.c** 仓库中的 PyTorch GPT-2 训练器为起点。
- 最初 llm.c GPT-2 复现在 8 块 H100 上达到目标损失大约需要 **45 分钟**。通过 modded-nanogpt 中社区驱动的优化，这一时间大幅缩短至约 **2 分钟**（某些报告中的记录低至约 2 分 20 秒）。

“modded-nanogpt”这个名称反映了其演进历程：对原始的 nanoGPT 基线进行了大量修改（“modded”），以在现代硬件上实现极致的实际时钟速度。它主要由 Keller Jordan 维护，并由一个协作/竞争性的社区提供贡献。

### 核心目标：NanoGPT 速通
这不是一个通用训练框架，而是一项 **速通挑战**：
- **目标**：在恰好使用 8 块 H100 GPU 的情况下，以最短时间将约 1.24 亿参数的模型在 FineWeb（一个大型网络衍生数据集）上训练至 3.28 的验证损失。
- **规则/设置**：代码包含完整的端到端流程（数据加载、分词器处理、训练、评估）。一个 `speedrun.sh` 脚本（或 Docker 构建）可复现当前记录。
- **排行榜**：仓库随时间跟踪世界纪录，显示从数分钟到约 2 分钟的逐步改进。

它强调 **实际时钟时间** 而非数据效率或泛化等其他指标，尽管许多优化也顺便提高了效率。

### 关键创新与优化
速度的显著提升源于架构、算法、系统和数值改进的结合。值得注意的技术包括：

- **架构变更**：
  - Rotary 位置嵌入。
  - QK 归一化。
  - MLP 中使用 ReLU² 激活函数。
  - 注意力层中融入值嵌入。
  - 跳跃连接（例如，从嵌入层到每个模块，或特定的模块到模块跳跃）。
  - Flex Attention、长短注意力窗口、注意力窗口预热。
  - 自定义 FP8（8 位浮点）操作，特别是用于语言建模头部，并配合不对称重新缩放和逻辑值的软上限处理。

- **优化器**：
  - **Muon** 优化器（由 Keller Jordan 开发）用于线性层，在此特定场景下通常优于调优后的 AdamW。许多分支实验了其他替代方案，如 SOAP。

- **训练技术**：
  - 类 muP 初始化（投影层初始化为零）。
  - 文档对齐以改进数据打包。
  - 线性学习率冷却。
  - 用于梯度更新的归约-分散操作。
  - 参数库以及其他内存/吞吐量技巧。

- **系统级优化**：
  - 大量使用自定义 Triton 内核以提高 GPU 效率。
  - 编译器配置、torch.compile 集成以及低级 CUDA/FP8 调整。
  - 针对 8 块 H100 量身定制的并行策略（例如，具有优化通信的数据并行）。

这些改动针对特定硬件和目标进行了激进调优。并非所有改动都能完美地推广到更大的模型或不同的设置，但其中许多已影响了后续项目。

### 如何运行
仓库提供了直接的复现方法：
1. 克隆仓库：`git clone https://github.com/KellerJordan/modded-nanogpt.git`
2. 通过 Docker 构建并运行以复现当前记录：`sudo docker build -t modded-nanogpt .`，然后运行容器。
3. 或者直接执行脚本（例如 `speedrun.sh` 或 `train_gpt.py`）。

它包含 Wandb 日志记录、基准测试以及相关讨论中的生成能力。

### 影响与社区影响力
- **研究平台**：超越速通本身，它作为一个小规模实验平台，用于测试新的优化器、架构和内核。来自 modded-nanogpt 的创新已被“下游”应用于其他项目。
- **nanochat**：一个受 modded-nanogpt 启发的相关项目，融入了缩放定律、强化学习元素和聊天机器人聚焦功能。一些优化技巧已融入其中。
- **分支与变体**：存在许多针对不同硬件（例如 JAX/TPU 移植）、优化器（例如 SOAP）或基线（例如 RWKV 实验、用于更强基线比较的“混音”版本）的分支。例子包括 modded-nanogpt-rwkv、modded-nanogpt-SOAP 和 modded-nanogpt-jax。
- **更广泛的启示**：它展示了通过精细工程能从 Transformer 模型中榨取多少性能。它引发了关于数据效率、缩放定律乃至递归自我改进基准的讨论。Karpathy 本人称赞其将 nanoGPT 发展为一个小规模 LLM 研究工具。

### 教育价值
虽然为速度而非可读性进行了优化，但核心的 `train_gpt.py`（以及相关的文件如 Triton 内核）为深入了解现代 LLM 训练提供了深刻的洞见。网络上存在涵盖设置、FP8 操作、并行化、注意力机制和优化器的讲解。它比原始的 nanoGPT 更复杂，但相比 Hugging Face Transformers 等生产级框架，仍然易懂得多。

总之，modded-nanogpt 将一个简单的教育性 GPT 训练器转变为一个尖端的优化实验场。它突显了通过开源协作和底层工程在 LLM 训练中可能实现的快速进步，将曾经需要 45 分钟的任务转变为在高端硬件上不到 3 分钟的壮举。

参考文献：
- [https://github.com/KellerJordan/modded-nanogpt](https://github.com/KellerJordan/modded-nanogpt)
- [https://www.lesswrong.com/posts/j3gp8tebQiFJqzBgg/how-the-nanogpt-speedrun-wr-dropped-by-20-in-3-months](https://www.lesswrong.com/posts/j3gp8tebQiFJqzBgg/how-the-nanogpt-speedrun-wr-dropped-by-20-in-3-months)
- [https://damek.github.io/random/modded-nanogpt-walkthrough-i/](https://damek.github.io/random/modded-nanogpt-walkthrough-i/)
- [https://github.com/karpathy/llm.c](https://github.com/karpathy/llm.c)（原始基线背景）
- [https://kellerjordan.github.io/posts/muon/](https://kellerjordan.github.io/posts/muon/)（Muon 优化器详解文章）