---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 我的AI作品集——日常AI工作的证据
translated: true
---

我不只谈论AI——我每天都在大规模地使用它。这篇文章是我AI工作的可视化组合展示：包含我构建的工具、消耗的token以及获得的认证。

---

## 🖥️ LLM 训练与推理 — 我的硬件配置

我于2023年搭建了机器学习工作站，此后一直进行训练和学习。

**硬件经验：**

| GPU | VRAM | 经验 | 环境 |
| ----- | ------ | ------------ | ------- |
| NVIDIA RTX 4070 | 12 GB | 3 年 | 家庭工作站 |
| NVIDIA H200 | 141 GB | 3 个月 | RunPod / DigitalOcean |
| AMD MI300X | 192 GB HBM3 | 3 个月 | AMD Developer Cloud |

**训练过的模型：**

- 在FineWeb数据集上从零开始训练 **GPT-2 124M** (nanoGPT) — 分别在 RTX 4070、H200 和 MI300X 上。
- 在 AMD MI300X (192 GB HBM3) 上从零开始训练 **GPT-2 760M** — 探索 nanochat、DeepSeek v4 MoE。
- 关于超参数调优、学习率调度和数据集预处理的各种实验。

**工作站：**

![我的机器学习工作站——2023年搭建，RTX 4070 12GB，用于日常训练和实验](/assets/images/ai-portfolio/learning-station.jpg)

**AMD Developer Cloud — MI300X 192GB HBM3：**

![AMD Dev Cloud — 用于大规模模型训练的 MI300X 实例](/assets/images/ai-portfolio/amd-dev-cloud.png)

---

## 🔧 GPU 拆解 — 从损坏的显卡中学习硬件知识

从二手市场购买了损坏的GPU（Quadro 401 / 2000 / 4000等），进行拆解并研究电路板，以了解其组件——VRM电路（MOSFETs、电感、电容）、内存芯片布局，以及每一代架构（Fermi → …）的差异。每一块PCB都是一份工程决策的蓝图。

![从二手市场购买的损坏 GPU — Quadro 拆解，研究 VRM 电路和 PCB 架构](/assets/images/ai-portfolio/gpu-teardown.jpg)

---

## 🖥️ 廉价 AI 工作站 — M40 12GB / M40 24GB / P100

使用来自闲鱼 (Xianyu) 的二手零件搭建了**三台廉价AI工作站**——为家庭装备增加了 **Tesla M40 12 GB**、**Tesla M40 24 GB** 和 **Tesla P100 16 GB**，与 RTX 4070 协同工作。这意味着**在三个节点上拥有总计52 GB的CUDA VRAM**，每个节点都运行着日常训练和推理实验。

**工作站集群：**

| 工作站 | GPU | VRAM | 架构 | FP16 | 构建成本 |
| ------ | ------ | ------ | ------ | ------ | ------ |
| M40 12 GB | Tesla M40 | 12 GB GDDR5 | Maxwell, 2015, CC 5.2 | 弱 (1/64 速率) | ~1000–1300 CNY |
| M40 24 GB | Tesla M40 24 GB | 24 GB GDDR5 | Maxwell, 2015, CC 5.2 | 弱 (1/64 速率) | 二手零件 |
| P100 16 GB | Tesla P100 PCIe | 16 GB HBM2 | Pascal, 2016, CC 6.0 | 快 (~9.3 TFLOPS, 2:1) | 二手零件 |

**M40 12 GB 构建成本明细：**

| 配件 | 成本 (CNY) | 备注 |
| ------ | -----------: | ------ |
| Tesla M40 12GB | ~200–300 | 数据中心 GPU, Maxwell 架构, 250W, 被动散热 |
| MSI Z170A Gaming M5 | ~200–300 | LGA1151, 3× PCIe x16, BIOS 支持良好 |
| Intel i5-6500 / PSU / RAM / 机箱 | ~500–700 | 来自二手市场的标准 ATX 部件 |
| **总计** | **~1000–1300** | **~$140–180 获得 12 GB CUDA 算力** |

> Tesla M40 有 **12 GB** 和 **24 GB GDDR5** 两种版本——24 GB版本将VRAM翻倍，可以运行更大的模型。两者都使用 **8-pin EPS (CPU) 电源连接器**，而非标准的 PCIe 电源线——这是一个常见的陷阱——并且是**被动散热**，因此需要强制气流。**Tesla P100** 是更新的 Pascal 架构显卡 (2016, CC 6.0)，配备 **16 GB HBM2**：使用相同的 8-pin EPS + 被动散热，但增加了真正的 **FP16 吞吐量 (~9.3 TFLOPS, 2:1)** 和更高的内存带宽——相比 Maxwell 架构的 M40，用于 LLM 推理是一次有意义的升级。

**关键突破——BIOS 配置：**

在尝试了多种不同主板（华南 B75、华硕 A68HM-E、微星 B150M）并经历了大量试错之后，最终在微星 Z170A Gaming M5 上成功的关键设置是：

```
Settings
  → Advanced
    → Windows OS Configuration
      → Windows 10 WHQL Support = Disabled
```

此外，在 BIOS 中：

- **Above 4G Decoding** = Enabled (M40 的大 64-bit BAR 所需)
- **CSM** = Disabled (纯 UEFI 模式，必需以正确分配 PCIe 资源)
- 将 M40 放在 **PCI_E1** 插槽 (最顶端的 x16 插槽，直接连接 CPU)

使用这些设置后，显卡成功初始化——`nvidia-smi` 显示全部 **11,520 MiB VRAM** (ECC 保留剩余的 512 MiB)，并且满载烧机测试证实了 **100% 利用率，6.12 TFLOPS FP32，约理论峰值的 90%**，温度保持在 35–39°C。

**这意味着什么——影响：**

这意义重大。只需大约 **1000–1200 CNY**，你就可以为家庭实验室增加 **12 GB 的 CUDA VRAM**。这足够运行：

- **7B–14B 的 LLM**，采用 Q4–Q8 量化，并具有合理的上下文长度
- **27B 的模型**，采用激进量化 (IQ1_M, ~6.3 GB)，具备 4k–8k 上下文
- **批量推理、LoRA 微调**和多 GPU 实验

M40 较老 (Maxwell, 2015, CC 5.2)，因此 FP16 性能较弱，你需要使用 `-DCMAKE_CUDA_ARCHITECTURES=52` 编译的 llama.cpp 构建。**M40 24 GB** 使用相同的构建参数，但 VRAM 翻倍，而 **P100 (CC 6.0)** 需要 `-DCMAKE_CUDA_ARCHITECTURES=60`，并增加了真正的 FP16 速度和 HBM2 带宽。以这个价格，很难被超越——**12 GB 构建大约每 GB VRAM 成本为 100 CNY**。

而且我并没有止步于一台。如今，家庭实验室运行着**三台这样的廉价二手数据中心工作站——M40 12 GB + M40 24 GB + P100 16 GB = 三个节点共 52 GB 的 CUDA VRAM**——在多台机器上扩展分布式推理和训练实验。

![Tesla M40 工作站 —— 使用 MSI Z170A Gaming M5 主板和 12 GB M40 GPU 的构建](/assets/images/ai-portfolio/m40-workstation.jpg)

![我的 AI 工作站 —— 三台由二手零件构建的工作站：Tesla M40 12GB, Tesla M40 24GB, 和 Tesla P100 16GB](/assets/images/ai-portfolio/ai-station.jpg)

---

### 🏋️ 训练运行总结

| # | 模型 | 框架 | 参数量 | 硬件 | 步数 | 状态 |
| --- | ------- | ----------- | -------- | ---------- | ------- | -------- |
| 1 | FineWeb 125M run1 | nanoGPT | 124M | RTX 4070 | 20K | 已完成 |
| 2 | FineWeb 125M run2 | nanoGPT | 124M | RTX 4070 | 6K | 已完成 |
| 3 | FineWeb 125M run3 | nanoGPT | 124M | RTX 4070 | 11K | 已完成 |
| 4 | OpenWebText 125M | nanoGPT | 124M | RTX 4070 | 6K | 已完成 |
| 5 | FineWeb 125M MI300X | nanoGPT | 124M | MI300X | 750 | 测试运行 |
| 6 | FineWeb 760M | nanoGPT | 760M | MI300X | 76K/445K | 提前停止 |
| 7 | fineweb-edu-d12 | nanochat | 286M | RTX 4070 | 10K | 基础预训练完成 |
| 8 | rtx4070-d12-chinchilla | nanochat | 286M | RTX 4070 | 87K | **完全完成** |
| 9 | code-sec-fineweb-d12 | nanochat | 286M | H200? | 50K | 已完成 |
| 10 | code-sec-sft | nanochat | ~140M | H200? | 8,985 | 已完成 |
| 11 | codeparrot-d12 | nanochat | 286M | RTX 4070 | ? | 仅脚本 |
| 12 | Notes SFT (Qwen3-4B) | trl/peft | 4B | RTX 4070 | ? | 仅脚本 |
| 13 | SPGISpeech (Whisper) | transformers | 可变 | ? | ? | 仅脚本 |

## 🧠 增强版 nanoGPT — 我的分支

复刻 (Fork) 了 [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)，并通过添加额外的数据集管道、扩展训练配置以及内联形状注释来扩展它以便学习。45 次提交，2025 年 11 月至 2026 年 4 月。

**新增数据集管道：**

| Dataset | Path | Description |
| --------- | ------ | ------------- |
| FineWeb-Edu | `data/fineweb/` | HuggingFace FineWeb-Edu (10B+ tokens). Shard-based loading, chunked processing, incremental train/val splits. |
| OpenWebText 10k | `data/openwebtext_10k/` | Quick 10k-subset for fast iteration. |
| Wikipedia Local | `data/wikipedia_local/` | Tokenize local plain-text dump directly (no HuggingFace download). |

**新增训练配置：**

| 配置 | 目标 | 备注 |
| -------- | -------- | ------- |
| `train_fineweb.py` | 125M on FineWeb | 针对 RTX 4070 12 GB 调优 (n_embd=384, dropout=0.1)。 |
| `train_fineweb1_5b.py` | 1.5B on FineWeb | 针对 H200 80 GB。 |
| `train_fineweb_gpt3.py` | GPT-3 style 10B tokens | Shard-based loader, wider schedule。 |
| `train_fineweb_760m.py` | 760M on FineWeb | 针对 MI300X 192 GB HBM3。 |
| `train_gpt2_200m.py` | GPT-2 200M | 通用中规模配置。 |
| `train_gpt2_200m_smoke.py` | Smoke test | 快速 200M 健全性检查 (~几分钟)。 |

**模型变更：**

- 在 `model.py` 的前向传播中加入了 **内联张量形状注释** (CausalSelfAttention, MLP, GPT) —— 显示每一步的精确形状，并附有具体的 GPT-2 XL 示例，例如 `# x: (B, T, C) e.g. (1, 5, 1600)`。有助于理解 Transformer 数据流。

![增强版 nanoGPT —— 45 次提交, 数据集管道, 扩展训练配置, 内联形状注释](/assets/images/ai-portfolio/nanogpt-fork.png)

GitHub: [lzwjava/nanoGPT](https://github.com/lzwjava/nanoGPT)

---

## ⚙️ MoE 与 LLM 推理 — 初学入门

在训练了密集型的 GPT-2 模型之后，我想要探索 LLM 架构和系统层面：**混合专家模型 (MoE)** 和**推理引擎**。坦白说，我在这方面才刚刚起步。我读过一些代码，运行过一些东西，并跟着学习——但我无法从头写出任何这些内容，我仍然认为自己在这个领域基本还是个初学者。

**已经开始关注的领域：**

- **MoE 架构** —— 路由 + 分发 + 专家计算 + 合并 + 负载均衡的整体架构。我粗略阅读过 DeepSeek-MoE (细粒度 + 共享专家)、MegaBlocks (无丢弃块稀疏分发)、Tutel (全对全专家并行) 和 Mixtral (8×7B, top-2) 的参考实现——主要是让 AI 智能体带我过一遍代码。
- **前向传播** —— 路由 (`router_logits` → `topk(softmax(...))`)、每个专家的计算，以及 `tokens → experts → tokens` 如何在 GPU 间高效完成。我能理解这个流程，但还无法自己权衡利弊。
- **KV 缓存分页、prefill/decode 调度、continuous batching、CUDA graphs、prefix caching、tensor parallelism** —— 我知道这些名词和大致概念，但服务栈很深，我仅仅触及了皮毛。

**我的学习方法——使用智能体进行探索：**

1. **阅读代码** —— 我使用编码智能体（例如 Hermes Agent）来帮助我追踪 mini-sglang 中 MoE 的端到端流程：`router (LinearReplicated) → MoELayer → FusedMoe (top-k routing → block-aligned dispatch → 2 fused GEMMs → sum-reduce) → Triton grouped-GEMM kernel`。当智能体带我过一遍时我能理解；但我还不能独立复现它。
2. **运行并基准测试** —— 在 RTX 4070 上使用 flash-attention 运行了 nano-vLLM Qwen3-0.6B：**506 tok/s prefill**，decode 约 4–30 tok/s，在笔记本基准测试中达到约 1434 tok/s。我把这些当作数据点，而不是任何结论的证据。
3. **从源码编译** —— 从源码构建了 **SGLang** (`pip install -e "python"`，修复了 torch/torchaudio CUDA 版本不匹配问题至 2.11.0+cu130，编译了它的 3 个 PyO3 Rust 扩展)，并让 Qwen2.5-0.5B 服务器在 `localhost:30010` 上提供补全服务。还运行了使用 `flash-attn==2.8.3` 预编译 wheel 的 nano-vLLM。能让东西编译起来是一回事；深入理解它们则是另一回事。

**目前所学（深度尚浅）：**

| 概念 | 我已理解的程度 |
| --------- | -------------------------------- |
| **Paged KV cache** | 固定的 256-token 块、空闲列表、content-hash prefix caching、copy-on-write 共享 —— 仅高级概念 |
| **Scheduler** | 长提示的分块 prefill、decode 步进、KV 缓存满时的抢占 —— 大致了解 |
| **CUDA graphs** | 捕捉 decode 批次 (`[1,2,4,…512]`) 以减少 CPU 内核启动开销 —— 理解了动机，而非细节 |
| **MoE dispatch** | `moe_align_block_size` 排序 + 填充每个专家的 token 块，以实现高效的 Triton grouped-GEMMs —— 跟着代码看过一次 |
| **Tensor parallelism** | 行并行层的 `all_reduce`、LM 头的 `gather`、共享路由器的 `LinearReplicated` —— 这些名字现在能理解了 |
| **Fused MoE kernel** | gate/up 融合为一个 GEMM，SwiGLU 激活拆分，路由权重恰好应用一次 —— 阅读过相关内容，保留得不完整 |

**我的方法** —— 坦白说，我的很多“阅读”是智能体阅读代码然后向我解释。大致的循环是：

```text
read 20% → modify 30% → break things 30% → submit 20%
```

我涉足这个领域只有几周时间。我目前掌握的知识刚好足以理解关于 MoE 推理的对话——还不足以自行构建或改进这些系统。

---

## 📝 SEC-EDGAR-GPT — 在 SEC 文件上从零开始训练的 GPT-2 (124M)

在 **15.5 亿个 SEC EDGAR 财务申报文件词元**（10-K、10-Q 及其他公司披露文件）上从零开始训练了一个 **1.24 亿参数的 GPT-2** 模型——在单个 **RTX 4070** (12 GB VRAM) 上训练了约 **8 小时**，验证损失收敛至 **2.28**。

该模型能生成逼真的 SEC 套话——风险因素、MD&A 章节、业务描述——并通过 RunPod 上的 FastAPI 服务器以交互式聊天方式部署。

使用 **Hermes Agent** 在 **3 天内**构建了整个项目——模型训练、论文、聊天机器人和网站——展示了 AI 智能体如何让 LLM 研究变得人人可及。

在一家全球银行内部共享后，该项目获得了 **200 多次**内部浏览。一位首席工程师留下了 **"不错 (nice)"** 的评论。此外，受一位朋友关于循环 Transformer 的工作启发，这个项目让我思考如何将金融 token 与自然语言 token 区别对待，以提高生成准确性。

![SEC-EDGAR-GPT 聊天机器人](/assets/images/sec-edgar-gpt/chatbot_web.png)

**代码：** [github.com/lzwjava/sec-edgar-gpt](https://github.com/lzwjava/sec-edgar-gpt) · **论文：** [sec-edgar-gpt.pdf](https://github.com/lzwjava/sec-edgar-gpt/raw/main/sec-edgar-gpt.pdf) · **模型：** [Hugging Face](https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf) · **聊天：** [sec-edgar-gpt.lzwjava.workers.dev](https://sec-edgar-gpt.lzwjava.workers.dev/)

---

## 📊 LLM API 使用量 — 具体数字

### OpenRouter — 过去一年

消耗了 3.35B 个词元，花费 239 美元，跨多个模型共计 155K 次 API 请求。

![OpenRouter 活动仪表板 —— 1 年内 3.35B 词元, $239 开销, 155K 请求](/assets/images/ai-portfolio/openrouter-activity.png)

### DeepSeek — 过去一年

过去一年通过 DeepSeek 平台消耗了 629M 个词元。

### Claude API (通过 SSSAICode) — 2026 年 4 月

一个月内花费 $171.53。2,555 次请求。超过 115M 个词元。90.9% 缓存命中率。

![SSSAICode Claude 使用情况 —— Opus 4.6, Opus 4.7, Sonnet 4.6, Haiku 4.5](/assets/images/ai-portfolio/sssaicode-usage.png)

### 小米 MIMO 订阅 — 使用了 12.5 亿词元

Pro 月费套餐，包含 38B 主额度 + 8.75B 补偿额度（约 4.6B 免费额度）。2026 年 5 月至 6 月期间消耗了 **1.25B 词元**。

![小米 MIMO Pro 套餐 —— 消耗 1.25B 词元, 剩余约 3.4B 免费额度](/assets/images/ai-portfolio/xiaomi-mimo-usage.png)

#### 月度词元使用量细分

| 月份 | 模型 | 词元总计 | 输入 (缓存命中) | 输入 (缓存未命中) | 输出 | 请求数 |
| ------- | ------- | -------------: | -------------------: | --------------------: | -------: | ---------: |
| 2026-06 | mimo-v2.5 | 285,179 | 36,416 | 143,556 | 105,207 | 78 |
| 2026-06 | mimo-v2.5-pro | 734,873,374 | 710,036,672 | 21,617,131 | 3,219,571 | 10,704 |
| 2026-05 | mimo-v2.5 | 91,203 | 5,312 | 52,908 | 32,983 | 27 |
| 2026-05 | mimo-v2.5-pro | 508,851,211 | 488,291,136 | 17,725,731 | 2,834,344 | 8,649 |
| 2026-05 | mimo-v2-pro | 3,571,328 | 3,021,568 | 539,357 | 10,403 | 167 |

**月度总计：** 2026 年 5 月：**512.5M 词元** (8,843 次请求) · 2026 年 6 月：**735.2M 词元** (10,782 次请求)

> mimo-v2.5-pro 占主导地位（约占总量的 96%）。mimo-v2.5-pro 上约 96.7% 的缓存命中率使成本保持高效。6 月相比 5 月在词元量上显示出 43.5% 的增长。

### 总结

| 平台 | 词元量 | 时期 | 成本 |
| ---------- | -------- | -------- | ------ |
| OpenRouter | 3.35B | 过去一年 | $239 |
| DeepSeek | 629M | 过去一年 | — |
| SSSAICode (Claude) | 115M+ | 2026 年 4 月 | $171.53 |
| 小米 MIMO | 1.25B | 2026 年 5–6 月 | 免费 4.6B 额度 |
| 其他 (GitHub Copilot 等) | 726M | 过去一年 | — |
| **总计** | **约 6.1B** | **过去一年** | **—** |

---

## 🏢 企业 AI 应用——在英国环球银行

在一家英国环球银行（通过一家全球 IT 外包公司），我在编码助手之上构建了一个自主 AI 智能体层，用于自动化脚本编写、日志记录、文档编制和测试。

**我的成果：**

- **20 个定制化 AI 智能体** —— 针对不同技术栈和工作流程的专用提示和上下文。
- **400 个由编码助手编写的可重用脚本** —— 跨 Java、Spring、Python、Angular 和 DevOps 工具的常见任务自动化。
- **1,800 份由编码助手编写的指南** —— 由 AI 在人类提示下生成的文档。
- **约 70 个通过编码助手 API 自动生成的测试用例** —— 涵盖 Spring Filters、Python unittest、JSON 截断、提示工程和区域端点。

**结果：**

- 在全公司的编码助手使用率中排名 **前 6%**（以高级请求衡量）。
- 因备受瞩目的 **AIPlayer 项目**获得了 **贡献奖**。
- 加入了银行的内部 AI 社区。

![AIPlayer 贡献奖](/assets/images/ai-portfolio/aiplayer.jpg)

---

## 🎤 AI 演讲——从神经网络到 AI 智能体

在英国环球银行向 **80 位参与者**发表了一场技术演讲——其中包括高级顾问、专家、副总监、软件工程师和合同工。

**演讲主题：** *"从神经网络到 AI 智能体"* —— 一段从最简单的神经网络 (`y = wx`) 出发，历经 MNIST、Transformers、GPT、nanoGPT，直到构建个人 AI 智能体的旅程。

**涵盖内容：**

- 从第一性原理出发讲解神经网络——前向传播、反向传播、梯度下降
- Transformer 架构——Q/K/V 注意力、多头注意力、位置编码
- GPT 内部机制——分词、嵌入、训练、生成
- nanoGPT——在 H200/RTX 4070 上从零开始训练 GPT-2
- LLM 智能体——Claude Code、OpenClaw、Hermes、工具调用、智能体循环
- 真实数据——消耗 1B 词元、H200 每小时 $3.44、钱到底花在哪里
- 我的历程——从阅读 Q/K/V 相关知识到从零开始训练模型，历时 3 年

**反馈：**

- 一位初级工程师说：*"你就是我想成为的那种人"* —— 这场演讲开阔了他对 AI 可能性的眼界
- 高级工程师们欣赏从第一性原理出发的方法——没有炒作，只有数学和代码
- 关于训练、智能体和职业发展方向的多次后续交流

**幻灯片：** 使用 Claude Code 与 Marp 构建，内容源自我的公开 AI 回答笔记。

幻灯片 (Marp)： [PDF](/assets/marp/neural_networks_to_agents_public.pdf)

---

## 🛠️ ww — 跨平台 CLI 工具集

[ww](https://github.com/lzwjava/ww) 是我的旗舰 CLI 工具集——255+ 次提交，10+ 个命令组，跨平台（macOS + Linux）。涵盖带有 AI 提交消息的 Git 工作流程、笔记管理、图片/PDF 处理、网页搜索、GitHub Copilot 聊天、系统工具和 LLM 驱动的助手。

```
lzwjava@lzw-mac ww % uv run ww --help
Usage: ww <group> [command] [options]

Action:
  ww action [workflow.yml]  Trigger a GitHub Actions workflow

AMD Dev Cloud:
  ww amd-dev-cloud snapshots    List snapshots
  ww amd-dev-cloud start-train  Create GPU droplet for training
  ww amd-dev-cloud end-train    Snapshot and destroy a GPU droplet

Copilot:
  ww copilot auth           Authenticate via GitHub OAuth
  ww copilot chat           Chat with a Copilot model

Git:
  ww git gpa            Git pull --all for all repos
  ww git squash <n>     Squash last n commits
  ww git amend-push     Amend last commit and force push

LLM:
  ww llm compare <prompt>   Compare multiple LLM responses
  ww llm query <question>   Query local RAG documents

Note:
  ww note              Clipboard to note (fast capture)
  ww note process      Drain the note queue
  ww note watch        Auto-process daemon

Screenshot:
  ww screenshot              Capture and create a note
  ww screenshot interact-note  Interactive screenshot note

255+ commits. 10+ command groups. Cross-platform (macOS + Linux).
```

![ww —— GitHub 上的跨平台 CLI 工具集](/assets/images/ai-portfolio/ww1.png)

GitHub: [lzwjava/ww](https://github.com/lzwjava/ww)

---

## 📝 jekyll-ai-blog — AI 驱动博客平台

[jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog) 是 [lzwjava.github.io](https://lzwjava.github.io) 的源代码——一个由 AI 自动化增强的 Jekyll 博客。10,000+ 篇英文文章、10,000+ 篇中文文章、9,700+ 条 AI 问答笔记。过去一个月约 100,000 次页面浏览（Cloudflare Analytics）。

```
lzwjava@lzw-mac jekyll-ai-blog % ls README.md
README.md
```

**区别于标准 Jekyll 博客的特点：**

- **AI 驱动翻译** —— 基于 LLM 的翻译管道通过 GitHub Actions 自动将每篇文章扩展到多种语言。
- **Google Cloud Text-to-Speech** —— 自动生成文章的音频版本，以提高可访问性。
- **XeLaTeX PDF/EPUB 生成** —— 从 Markdown 源生成高质量、适合印刷的 PDF 和电子书导出文件。
- **GitHub Actions CI/CD** —— 自动化构建、测试、翻译和部署工作流程。
- **8,000+ 条 AI 问答笔记** —— 基于日常 LLM 辅助研究构建的知识库，可在博客上搜索。
- **MathJax、夜间模式、RSS、双语内容** —— 通过自定义 CSS 和主题增强的标准功能。

**规模：**

| 指标 | 数量 |
| -------- | ------- |
| 英文文章 | 10,264 |
| 中文文章 | 10,259 |
| AI 问答笔记 | 9,794 |
| Python 脚本 | 323 |
| ML 脚本 | 191 |
| 页面浏览（过去一个月） | ~100,000 |

![jekyll-ai-blog —— 拥有 10K+ 文章、翻译、TTS 和 PDF 管道的 AI 驱动博客](/assets/images/ai-portfolio/blog.png)

![页面浏览（过去一个月）—— ~100,000](https://lzwjava.com/assets/images/analytics/pv.png)

GitHub: [lzwjava/jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog)

---

## 🎬 FluxReel — AMD 黑客松短视频工作室

[FluxReel](https://github.com/lzwjava/flux-reel) 将一行主题转化为 **15 秒的竖屏短视频**（1080×1920, 9:16, 30 fps）——核心图像生成在 **AMD Radeon GPU (ROCm)** 上运行。专为 **2026 年 7 月 AMD AI DevMaster 黑客松赛道 1——多模态内容创作工具** 构建。

**工作原理：**

1. **脚本** —— LLM 根据主题起草一篇 300–500 字的 Markdown 文章，然后场景规划器精确生成 5 个场景，每个场景包含 `title` / `subtitle` / `image_prompt`（双语，根据主题自动检测）。
2. **图像** —— 并行生成 5 个场景图像：通过 diffusers（FLUX.1-schnell / dev / 2-dev）使用 AMD GPU、stable-diffusion.cpp（FLUX.1-schnell Q4_0 GGUF，低 VRAM）或 OpenRouter。
3. **合成** —— PIL 构建每张 1080×1920 的幻灯片，包含标题/副标题栏，字体自动缩小以适配，支持 CJK 感知换行。
4. **组装** —— ffmpeg 将每张幻灯片编码为 3 秒的 H.264 片段，串接无需重新编码，并混入背景音乐。

**主要特点：**

- **主题到视频只需几分钟**：从提示到精美的 MP4 的完整管道，在本地 AMD 硬件上运行。
- **双语字幕** —— 使用 Noto Sans CJK 字体和基于字符的换行自动检测 EN / 中文。
- **多种图像后端** —— `local` (ROCm + diffusers FLUX)、`sdcpp` (GGUF 4-bit, 低 VRAM)、`openrouter` (云端备选)、`auto` (优先本地，备选云端)。
- **Web UI + REST API** —— 带有作业队列、进度轮询、视频预览和下载功能的 FastAPI 服务器。
- **可选 YouTube 上传** —— 通过 LLM 自动生成标题/描述/标签。
- **远程 AMD GPU 管理** —— rc-tunnel、通过 `hf-mirror.com` 下载 FLUX 模型（对中国友好）、GPU / ROCm / 磁盘信息。

**演示输出帧 (1080×1920, 9:16)：**

![FluxReel 演示帧 2 —— 在 AMD GPU 上生成的 15 秒竖屏短视频](https://raw.githubusercontent.com/lzwjava/flux-reel/main/submission/demo_frame_2.jpg)

**🏆 AMD AI DevMaster 黑客松 — 完成奖** (0121 Zhiwei Li)：

![AMD AI DevMaster 黑客松完成奖 —— FluxReel](/assets/images/ai-portfolio/fluxreel-award.png)

GitHub: [lzwjava/flux-reel](https://github.com/lzwjava/flux-reel)

---

## 🤖 iclaw — 终端 AI 智能体 (REPL)

[iclaw](https://github.com/lzwjava/iclaw) 是一个终端 AI 智能体，可以自主编码、搜索和运行命令——可在个人机器和受严格限制的企业机器上工作。一个最小化的 openclaw 实现，作为纯 Python CLI 构建，无需浏览器扩展或 IDE 插件，由 GitHub Copilot 驱动。

```
lzwjava@lzw-mac iclaw % iclaw

  ██  █████  ██       █████  ██   ██
  ██ ██      ██      ██   ██ ██   ██
  ██ ██      ██      ███████ ██ █ ██
  ██ ██      ██      ██   ██ ██████
  ██  █████  ███████ ██   ██  ███ ██

Available commands:
  /provider_model      Select and authenticate with the model provider
  /model               Select specific model from your provider
  /search              Web search (usage: /search <query>)
  /provider_search     Select the web search provider
  /proxy               Set HTTP/HTTPS proxy (usage: /proxy [url|off])
  /ca_bundle           Set CA bundle for HTTPS (usage: /ca_bundle [path|off])
  /log                 Set log verbosity (usage: /log [verbose|info])
  /copy                Copy last Copilot response to clipboard
  /read                Print file contents to terminal (usage: /read <path>)
  /clear               Clear conversation history
  /compact             Compact conversation history using LLM
  /export              Export full conversation history to JSON file
  /status              Show current settings
  /help                Show available commands
  /exit                Quit the REPL.
```

**主要特点：**

- **多轮对话** —— 在终端中与 GitHub Copilot 或 OpenRouter 对话。
- **多个模型提供商**：GitHub Copilot (OAuth 设备授权流程) 和 OpenRouter (API 密钥)。
- **原生工具调用**：模型自主调用网页搜索、执行 shell 命令和编辑文件——无需人工参与。
- **多个搜索提供商**：DuckDuckGo、Startpage、Bing 和 Tavily。
- **企业友好**：无需 IDE 插件或浏览器扩展。可在企业防火墙后使用，支持代理和 CA bundle。
- **默认模型**：GPT-5.2。

![iclaw —— 终端 AI 智能体 REPL，支持原生工具调用](/assets/images/ai-portfolio/iclaw.jpg)

![iclaw —— 显示自主编码和 shell 命令的执行日志](/assets/images/ai-portfolio/iclaw-log.png)

GitHub: [lzwjava/iclaw](https://github.com/lzwjava/iclaw)

---

## ⚙️ zz — 数据集处理与训练工具

[zz](https://github.com/lzwjava/zz) 是一个用于 ML 训练管道的工具集——数据集下载、分词、提取和推理工具。用于在 RunPod H200、DigitalOcean H100 和家庭 RTX 4070 上进行的 GPT-2 124M 训练运行。同时也托管在 [Hugging Face](https://huggingface.co/lzwjava/zz) 上。

```
lzwjava@lzw-mac zz % tree -L 1
scripts/
  download/     # Dataset download scripts (FineWeb, Wikimedia, HF mirrors)
  extract/      # Data extraction, tokenization, and renaming
  analysis/     # Training duration and metric evaluation
  deepseek/     # LLM inference scripts (DeepSeek-V2-Lite)
logs/           # Training logs and outputs
datasets/       # Downloaded dataset storage
```

**关键能力：**

- **FineWeb 下载** —— 规划并下载分片以达到 token 预算（10B, 100B+ tokens），可恢复并带有进度跟踪。
- **hf-mirror.com 支持** —— 当 HuggingFace 被屏蔽时，为中国用户提供 wget 脚本。
- **Parquet 提取** —— 通过 pyarrow iter_batches 进行内存安全迭代。
- **分词** —— 将原始文本转换为训练就绪格式。
- **训练分析** —— 从训练日志计算持续时间、评估指标。
- **DeepSeek 推理** —— DeepSeek-V2-Lite 的 LLM 推理脚本。

![zz on Hugging Face —— 数据集处理与训练工具, 22 次提交, 3 位贡献者](/assets/images/ai-portfolio/zz-huggingface.png)

GitHub: [lzwjava/zz](https://github.com/lzwjava/zz) · Hugging Face: [lzwjava/zz](https://huggingface.co/lzwjava/zz)

---

## 🎓 证书

### 机器学习专项课程 — DeepLearning.AI & 斯坦福大学

2023 年 11 月完成。三门课程：有监督学习、高级学习算法、无监督学习、推荐系统、强化学习。

![Coursera 机器学习专项课程证书 —— Zhiwei Li, 2023 年 11 月](/assets/images/ai-portfolio/coursera-ml-1.png)

### 深度学习专项课程 — DeepLearning.AI

2023 年 12 月完成。五门课程：神经网络、超参数调优、结构化机器学习项目、卷积神经网络、序列模型。

![Coursera 深度学习专项课程证书 —— Zhiwei Li, 2023 年 12 月](/assets/images/ai-portfolio/coursera-dl-1.png)

---

- GitHub: [https://github.com/lzwjava](https://github.com/lzwjava)
- Blog: [https://lzwjava.github.io](https://lzwjava.github.io)

---
