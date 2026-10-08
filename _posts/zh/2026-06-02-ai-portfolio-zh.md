---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 我的AI作品集——日常AI工作的证明
translated: true
---

我不仅谈论人工智能——我还每天大规模地使用它。这篇文章是我的 AI 努力的可视化作品集：我构建的工具、我消耗的令牌以及我获得的认证。

---

## 🖥️ LLM 训练与推理——我的硬件配置

于 2023 年构建了我的机器学习工作站，并从此一直在进行训练和学习。

**硬件经验：**

| GPU | 显存 | 经验时长 | 使用地点 |
| --- | --- | --- | --- |
| NVIDIA RTX 4070 | 12 GB | 3 年 | 家庭工作站 |
| NVIDIA H200 | 141 GB | 3 个月 | RunPod / DigitalOcean |
| AMD MI300X | 192 GB HBM3 | 3 个月 | AMD 开发者云 |

**我训练过的项目：**

- **GPT-2 124M**：从零开始在 FineWeb 数据集上训练（nanoGPT）——在 RTX 4070、H200 和 MI300X 上。
- **GPT-2 760M**：从零开始在 AMD MI300X（192 GB HBM3）上训练——探索 nanochat、DeepSeek v4 MoE。
- 各种关于超参数调优、学习率调度和数据集预处理的实验。

**工作站：**

![我的机器学习学习站——2023 年构建，RTX 4070 12GB，用于日常训练和实验](/assets/images/ai-portfolio/learning-station.jpg)

**AMD 开发者云——MI300X 192GB HBM3：**

![AMD 开发者云——用于大规模模型训练的 MI300X 实例](/assets/images/ai-portfolio/amd-dev-cloud.png)

---

## 🔧 GPU 拆解——从坏卡中学习硬件

从二手市场购买了损坏的 GPU（**Quadro 401 / 2000 / 4000** 等），将其拆解，并研究电路板以了解组件——VRM 电路（MOSFET、电感、电容）、内存芯片布局，以及每一代架构（Fermi → …）的不同之处。每个 PCB 都是工程决策的蓝图。

![来自二手市场的损坏 GPU——Quadro 拆解，研究 VRM 电路和 PCB 架构](/assets/images/ai-portfolio/gpu-teardown.jpg)

---

## 🖥️ 廉价 AI 工作站——M40 12GB / M40 24GB / P100

使用来自闲鱼的二手零件构建了**三个廉价的 AI 工作站**——在我的家庭设置中添加了**Tesla M40 12 GB**、**Tesla M40 24 GB**和**Tesla P100 16 GB**，与 RTX 4070 一起。这相当于**三个节点上总共 52 GB 的 CUDA 显存**，每个节点都运行日常训练和推理实验。

**设备列表：**

| 工作站 | GPU | 显存 | 架构 | FP16 | 构建成本 |
| --- | --- | --- | --- | --- | --- |
| M40 12 GB | Tesla M40 | 12 GB GDDR5 | Maxwell，2015，CC 5.2 | 弱（1/64 速率） | ~1000–1300 元 |
| M40 24 GB | Tesla M40 24 GB | 24 GB GDDR5 | Maxwell，2015，CC 5.2 | 弱（1/64 速率） | 二手零件 |
| P100 16 GB | Tesla P100 PCIe | 16 GB HBM2 | Pascal，2016，CC 6.0 | 快（~9.3 TFLOPS，2:1） | 二手零件 |

**M40 12 GB 构建：**

| 零件 | 成本（元） | 备注 |
| --- | --- | --- |
| Tesla M40 12GB | ~200–300 | 数据中心 GPU，Maxwell 架构，250W，被动散热 |
| MSI Z170A Gaming M5 | ~200–300 | LGA1151，3× PCIe x16，良好的 BIOS 支持 |
| Intel i5-6500 / PSU / 内存 / 机箱 | ~500–700 | 来自二手市场的标准 ATX 零件 |
| **总计** | **~1000–1300** | **~$140–180，获得 12 GB CUDA 算力** |

> Tesla M40 有 **12 GB** 和 **24 GB GDDR5** 两种版本——24 GB 版本将显存翻倍以支持更大的模型。两者都使用 **8 针 EPS（CPU）电源连接器**，而不是标准的 PCIe 电源线——这是一个常见的陷阱——并且是**被动散热**的，因此需要强制气流。**Tesla P100** 是一款更新的 Pascal 卡（2016 年，CC 6.0），具有 **16 GB HBM2**：相同的 8 针 EPS + 被动散热，但增加了真正的 **FP16 吞吐量（~9.3 TFLOPS，2:1）** 和更高的内存带宽——与 Maxwell M40 相比，在 LLM 推理方面有显著提升。

**突破——BIOS 配置：**

在不同主板（华南金牌 B75、华硕 A68HM-E、微星 B150M）上进行了大量尝试和错误之后，最终在 MSI Z170A Gaming M5 上使其工作的关键设置是：

```
Settings
  → Advanced
    → Windows OS Configuration
      → Windows 10 WHQL Support = Disabled
```

此外，在 BIOS 中：

- **Above 4G Decoding** = Enabled（M40 的大 64 位 BAR 所需）
- **CSM** = Disabled（纯 UEFI 模式，正确的 PCIe 资源分配所需）
- 将 M40 放在 **PCI_E1**（顶部 x16 插槽，直接连接到 CPU）

使用这些设置，卡成功初始化——`nvidia-smi` 显示完整的 **11,520 MiB 显存**（ECC 保留了剩余的 512 MiB），满载压力测试确认了 **100% 利用率，6.12 TFLOPS FP32，约理论峰值的 90%**，温度保持在 35–39°C。

**这意味着什么——影响：**

这意义重大。大约花费 **1000–1200 元**，您就可以为您的家庭实验室增加 **12 GB 的 CUDA 显存**。这足以运行：

- 在 Q4–Q8 量化下具有合理上下文的 **7B–14B LLM**
- 在激进量化（IQ1_M，~6.3 GB）下具有 4k–8k 上下文的 **27B 模型**
- **批量推理、LoRA 微调**和多 GPU 实验

M40 较旧（Maxwell，2015，CC 5.2），因此 FP16 性能较弱，并且需要使用 `-DCMAKE_CUDA_ARCHITECTURES=52` 编译的 llama.cpp 构建版本。**M40 24 GB** 使用相同的构建标志，但显存翻倍，而 **P100（CC 6.0）** 需要 `-DCMAKE_CUDA_ARCHITECTURES=60`，并增加了真正的 FP16 速度和 HBM2 带宽。就价格而言，它很难被击败——12 GB 构建版本约为 **每 GB 显存 100 元**。

而且我不止于一台。如今，家庭实验室运行着**三台廉价的二手数据中心工作站——M40 12 GB + M40 24 GB + P100 16 GB = 三个节点上 52 GB 的 CUDA 显存**——跨多台机器扩展分布式推理和训练实验。

![Tesla M40 工作站——使用 MSI Z170A Gaming M5 和 12 GB M40 GPU 的构建](/assets/images/ai-portfolio/m40-workstation.jpg)

![我的 AI 站——三台由二手零件构建的工作站：Tesla M40 12GB、Tesla M40 24GB 和 Tesla P100 16GB](/assets/images/ai-portfolio/ai-station.jpg)

---

### 🏋️ 训练运行总结

| # | 模型 | 框架 | 参数 | 硬件 | 步数 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | FineWeb 125M run1 | nanoGPT | 124M | RTX 4070 | 20K | 已完成 |
| 2 | FineWeb 125M run2 | nanoGPT | 124M | RTX 4070 | 6K | 已完成 |
| 3 | FineWeb 125M run3 | nanoGPT | 124M | RTX 4070 | 11K | 已完成 |
| 4 | OpenWebText 125M | nanoGPT | 124M | RTX 4070 | 6K | 已完成 |
| 5 | FineWeb 125M MI300X | nanoGPT | 124M | MI300X | 750 | 烟雾测试 |
| 6 | FineWeb 760M | nanoGPT | 760M | MI300X | 76K/445K | 提前停止 |
| 7 | fineweb-edu-d12 | nanochat | 286M | RTX 4070 | 10K | 基础预训练完成 |
| 8 | rtx4070-d12-chinchilla | nanochat | 286M | RTX 4070 | 87K | **完全完成** |
| 9 | code-sec-fineweb-d12 | nanochat | 286M | H200? | 50K | 已完成 |
| 10 | code-sec-sft | nanochat | ~140M | H200? | 8,985 | 已完成 |
| 11 | codeparrot-d12 | nanochat | 286M | RTX 4070 | ? | 仅脚本 |
| 12 | Notes SFT (Qwen3-4B) | trl/peft | 4B | RTX 4070 | ? | 仅脚本 |
| 13 | SPGISpeech (Whisper) | transformers | varies | ? | ? | 仅脚本 |

## 🧠 增强版 nanoGPT——我的分支

派生自 [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT) 并进行了扩展，添加了额外的数据集管道、规模化训练配置和内联形状注释以便学习。45 次提交，2025 年 11 月 – 2026 年 4 月。

**新数据集管道：**

| 数据集 | 路径 | 描述 |
| --- | --- | --- |
| FineWeb-Edu | `data/fineweb/` | HuggingFace FineWeb-Edu（10B+ tokens）。基于分片的加载、分块处理、增量式训练/验证分割。 |
| OpenWebText 10k | `data/openwebtext_10k/` | 用于快速迭代的 10k 子集。 |
| Wikipedia Local | `data/wikipedia_local/` | 直接对本地纯文本转储进行分词（无需 HuggingFace 下载）。 |

**新增训练配置：**

| 配置 | 目标 | 备注 |
| --- | --- | --- |
| `train_fineweb.py` | 125M on FineWeb | 为 RTX 4070 12 GB 调优（n_embd=384，dropout=0.1）。 |
| `train_fineweb1_5b.py` | 1.5B on FineWeb | 用于 H200 80 GB。 |
| `train_fineweb_gpt3.py` | GPT-3 风格 10B tokens | 基于分片的加载器，更宽的调度。 |
| `train_fineweb_760m.py` | 760M on FineWeb | 用于 MI300X 192 GB HBM3。 |
| `train_gpt2_200m.py` | GPT-2 200M | 通用中等规模配置。 |
| `train_gpt2_200m_smoke.py` | 烟雾测试 | 快速 200M 健全性检查（约几分钟）。 |

**模型变更：**

- 在 `model.py` 的前向传播（CausalSelfAttention、MLP、GPT）中添加了**内联张量形状注释**——使用具体的 GPT-2 XL 示例显示每一步的精确形状，例如 `# x: (B, T, C) e.g. (1, 5, 1600)`。有助于理解 Transformer 数据流。

![增强版 nanoGPT——45 次提交、数据集管道、规模化训练配置、内联形状注释](/assets/images/ai-portfolio/nanogpt-fork.png)

GitHub: [lzwjava/nanoGPT](https://github.com/lzwjava/nanoGPT)

---

## ⚙️ MoE 与 LLM 推理——刚刚开始学习

在训练了密集的 GPT-2 模型之后，我想看看 LLM 的架构和系统方面：**混合专家（Mixture-of-Experts, MoE）** 和**推理引擎**。老实说，我还处于最初的阶段。我读过一些代码，运行过一些东西，并跟着做过——但我无法从头开始编写任何这些内容，我仍然认为自己在这方面基本上是个初学者。

**我开始关注的内容：**

- **MoE 架构**——路由 + 分发 + 专家计算 + 合并 + 负载均衡的高级概览。我粗略地看了 DeepSeek-MoE（细粒度 + 共享专家）、MegaBlocks（无丢弃的块稀疏分发）、Tutel（全到全专家并行）和 Mixtral（8×7B，top-2）作为参考实现——主要是让 AI agents 带我过一遍代码。
- **前向传播**——路由（`router_logits` → `topk(softmax(...))`）、每个专家的计算，以及 `tokens → experts → tokens` 如何跨 GPU 加速。我能理解流程，但还不能自己权衡利弊。
- **KV 缓存分页、prefill/decode 调度、连续批处理、CUDA graphs、前缀缓存、张量并行**——我知道这些名称和大致概念，但服务栈很深，我只触及了皮毛。

**我如何学习——使用 agents 探索：**

1. **阅读代码**——我使用编码 agents（例如 Hermes Agent）来帮助我端到端地追踪 mini-sglang 中的 MoE：`router (LinearReplicated) → MoELayer → FusedMoe (top-k routing → block-aligned dispatch → 2 fused GEMMs → sum-reduce) → Triton grouped-GEMM kernel`。当 agent 带我过一遍时，我能理解；但我还不能自己复现。
2. **运行并基准测试**——在我的 RTX 4070 上使用 flash-attention 运行了 nano-vLLM 上的 Qwen3-0.6B：**506 tok/s prefill**，解码约 4–30 tok/s，在笔记本电脑基准测试中约为 1434 tok/s。我将这些视为数据点，而不是任何事物的证明。
3. **从源码编译**——从源码构建了 **SGLang**（`pip install -e "python"`，修复了 torch/torchaudio CUDA 不匹配问题至 2.11.0+cu130，编译了其 3 个 PyO3 Rust 扩展），并让 Qwen2.5-0.5B 服务器在 `localhost:30010` 上提供补全服务。还使用 `flash-attn==2.8.3` 预构建 wheels 运行了 nano-vLLM。让东西能编译是一回事；深入理解是另一回事。

**我目前学到的东西（仍然浅显）：**

| 概念 | 我理解的内容 |
| --- | --- |
| **分页 KV 缓存** | 固定的 256 令牌块、空闲列表、内容哈希前缀缓存、写时复制共享——仅高层次概念 |
| **调度器** | 长提示的分块 prefill、解码步进、KV 缓存满时的抢占——大致了解 |
| **CUDA graphs** | 捕获解码批次（`[1,2,4,…512]`）以减少 CPU 内核启动开销——动机，而非细节 |
| **MoE 分发** | `moe_align_block_size` 排序 + 按专家填充令牌块以实现高效的 Triton grouped-GEMMs——跟着代码看过一次 |
| **张量并行** | 行并行层的 `all_reduce`、LM 头的 `gather`、 `LinearReplicated` 共享路由器——现在理解了这些名称 |
| **融合 MoE 内核** | gate/up 融合为一个 GEMM，SwiGLU 激活拆分，路由权重精确应用一次——读过相关内容，保留不完整 |

**我的处理方式**——老实说，我的很多“阅读”都是 agent 阅读代码并行解释给我听。循环大致如下：

```text
阅读 20% → 修改 30% → 破坏 30% → 提交 20%
```

我只接触这个几周。我所知道的刚好足以跟上关于 MoE 推理的讨论——但还不足以自己构建或改进这些系统之一。

---

## 📝 SEC-EDGAR-GPT——在 SEC 文件上从零训练的 GPT-2（124M）

在 **1.55B tokens** 的 SEC EDGAR 财务文件（10-K、10-Q 和其他公司披露）上从零训练了一个 **1.24 亿参数的 GPT-2**——在单个 **RTX 4070**（12 GB 显存）上训练了约 8 小时，验证损失收敛至 2.28。

该模型能生成令人信服的 SEC 标准文本——风险因素、MD&A 部分、业务描述——并通过 RunPod 上的 FastAPI 服务器部署用于交互式聊天。

整个项目——模型训练、论文、聊天机器人和网站——在 **3 天内使用 Hermes Agent 构建**，展示了 AI agents 如何使 LLM 研究变得可及。

在一家全球银行内部共享后，该项目获得了 **200 多次内部浏览**。一位首席工程师留下评论称其为 *“nice”*。此外，受一位朋友关于循环 Transformer 工作的启发，这个项目让我开始思考如何将金融令牌与自然语言令牌区别对待，以提高生成准确性。

![SEC-EDGAR-GPT 聊天机器人](/assets/images/sec-edgar-gpt/chatbot_web.png)

**代码：** [github.com/lzwjava/sec-edgar-gpt](https://github.com/lzwjava/sec-edgar-gpt) · **论文：** [sec-edgar-gpt.pdf](https://github.com/lzwjava/sec-edgar-gpt/raw/main/sec-edgar-gpt.pdf) · **模型：** [Hugging Face](https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf) · **聊天：** [sec-edgar-gpt.lzwjava.workers.dev](https://sec-edgar-gpt.lzwjava.workers.dev/)

---

## 📊 LLM API 使用量——数据

### OpenRouter——过去一年

消耗了 22.8 亿 tokens，花费 239 美元，跨多个模型进行了 15.5 万次 API 请求。

![OpenRouter 活动仪表板——过去一年 22.8 亿 tokens、239 美元花费、15.5 万次请求](/assets/images/ai-portfolio/openrouter-activity.png)

### DeepSeek——过去一年

过去一年通过 DeepSeek 平台消耗了 6.29 亿 tokens。

### 通过 SSSAICode 的 Claude API——2026 年 4 月

一个月内花费 171.53 美元。2,555 次请求。超过 1.15 亿 tokens。90.9% 缓存命中率。

![SSSAICode Claude 使用量——Opus 4.6、Opus 4.7、Sonnet 4.6、Haiku 4.5](/assets/images/ai-portfolio/sssaicode-usage.png)

### 小米 MIMO 订阅——已使用 12.5 亿 Tokens

Pro 月度套餐，包含 380 亿主配额 + 87.5 亿补偿配额（约 46 亿免费额度）。2026 年 5 月至 6 月期间消耗了 **12.5 亿 tokens**。

![小米 MIMO Pro 计划——已消耗 12.5 亿 tokens，剩余约 34 亿免费额度](/assets/images/ai-portfolio/xiaomi-mimo-usage.png)

#### 月度 Token 使用量明细

| 月份 | 模型 | Token 总数 | 输入（缓存命中） | 输入（缓存未命中） | 输出 | 请求数 |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-06 | mimo-v2.5 | 285,179 | 36,416 | 143,556 | 105,207 | 78 |
| 2026-06 | mimo-v2.5-pro | 734,873,374 | 710,036,672 | 21,617,131 | 3,219,571 | 10,704 |
| 2026-05 | mimo-v2.5 | 91,203 | 5,312 | 52,908 | 32,983 | 27 |
| 2026-05 | mimo-v2.5-pro | 508,851,211 | 488,291,136 | 17,725,731 | 2,834,344 | 8,649 |
| 2026-05 | mimo-v2-pro | 3,571,328 | 3,021,568 | 539,357 | 10,403 | 167 |

**月度总计：** 2026 年 5 月：**5.125 亿 tokens**（8,843 次请求）· 2026 年 6 月：**7.352 亿 tokens**（10,782 次请求）

> mimo-v2.5-pro 占主导地位（约占总数的 96%）。mimo-v2.5-pro 上约 96.7% 的缓存命中率保持了成本效益。6 月份 token 量较 5 月份增长 43.5%。

### 总结

| 平台 | Tokens | 时间段 | 成本 |
| --- | --- | --- | --- |
| OpenRouter | 228 亿 | 过去一年 | $239 |
| DeepSeek | 629M | 过去一年 | — |
| SSSAICode (Claude) | 1.15亿+ | 2026年4月 | $171.53 |
| 小米 MIMO | 125亿 | 2026年5–6月 | 46亿免费额度 |
| 其他 (GitHub Copilot 等) | 726M | 过去一年 | — |
| **总计** | **约 500亿** | **过去一年** | **—** |

---

## 🏢 企业 AI 使用——在一家英国环球银行

在一家英国环球银行（通过一家全球 IT 外包公司），我在编码助手之上构建了一个自主 AI agent 层，用于自动化脚本编写、日志记录、文档和测试。

**我构建的内容：**

- **20 个定制化的 AI agents**——为不同的技术栈和工作流程提供专用的提示和上下文。
- **400 个由编码助手编写的可重用脚本**——跨 Java、Spring、Python、Angular 和 DevOps 工具的常见任务自动化。
- **1,800 份由编码助手编写的指南**——由 AI 在人类提示下生成的文档。
- **约 70 个自动生成的测试用例**——通过编码助手 API，涵盖 Spring Filters、Python unittest、JSON 截断、提示工程和区域端点。

**成果：**

- 在整个企业范围内，按高级请求衡量，**编码助手使用率排名前 6%**。
- 因高知名度的 AIPlayer 项目获得**贡献奖**。
- 加入了银行的内部 AI 社区。

![AIPlayer 贡献奖](/assets/images/ai-portfolio/aiplayer.jpg)

---

## 🎤 AI 讲座——从神经网络到 Agents

在一家英国环球银行向 **80 名参与者**做了一场技术讲座——包括高级顾问、专家、助理总监、软件工程师和承包商。

**讲座：** *"从神经网络到 Agents"*——从最简单的神经网络（`y = wx`）开始，历经 MNIST、Transformers、GPT、nanoGPT，直至构建个人 AI agents 的旅程。

**我涵盖的内容：**

- 从第一性原理出发的神经网络——前向传播、反向传播、梯度下降
- Transformer 架构——Q/K/V 注意力、多头注意力、位置编码
- GPT 内部机制——分词、嵌入、训练、生成
- nanoGPT——在 H200/RTX 4070 上从零训练 GPT-2
- LLM agents——Claude Code、OpenClaw、Hermes、工具调用、agent 循环
- 真实数据——消耗 10 亿 tokens，H200 成本 $3.44/小时，资金实际流向
- 我的路径——3 年，从阅读 Q/K/V 到从零训练模型

**反馈：**

- 一位初级工程师说：*"你是我想要成为的人"*——这个讲座让他开阔了眼界，看到了 AI 的可能性
- 高级工程师赞赏第一性原理的方法——没有炒作，只有数学和代码
- 多次关于训练、agents 和职业方向的后续讨论

**幻灯片：** 使用 Claude Code 和 Marp 构建，基于我的公开 AI 回复笔记。

幻灯片 (Marp)：[PDF](/assets/marp/neural_networks_to_agents_public.pdf)

---

## 🛠️ ww——跨平台 CLI 工具箱

[ww](https://github.com/lzwjava/ww) 是我的旗舰级 CLI 工具箱——255 次以上提交，10 个以上命令组，支持跨平台（macOS + Linux）。它涵盖了带有 AI 提交信息的 git 工作流、笔记管理、图像/PDF 处理、网络搜索、GitHub Copilot 聊天、系统实用程序和 LLM 驱动的辅助工具。

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

![ww——GitHub 上的跨平台 CLI 工具箱](/assets/images/ai-portfolio/ww1.png)

GitHub: [lzwjava/ww](https://github.com/lzwjava/ww)

---

## 📝 jekyll-ai-blog——AI 驱动博客平台

[jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog) 是 [lzwjava.github.io](https://lzwjava.github.io) 的源代码——一个由 AI 自动化增强的 Jekyll 博客。包含 10,000 多篇英文文章、10,000 多篇中文文章、9,700 多条 AI 问答笔记。过去一个月约有 10 万次页面浏览量（Cloudflare Analytics）。

```
lzwjava@lzw-mac jekyll-ai-blog % ls README.md
README.md
```

**它与标准 Jekyll 博客的不同之处：**

- **AI 驱动翻译**——基于 LLM 的翻译管道通过 GitHub Actions 自动将每篇文章扩展到多种语言。
- **Google Cloud Text-to-Speech**——自动生成文章的音频版本以提高可访问性。
- **XeLaTeX PDF/EPUB 生成**——从 Markdown 源生成高质量、可直接打印的 PDF 和电子书导出文件。
- **GitHub Actions CI/CD**——自动化的构建、测试、翻译和部署工作流。
- **8,000+ 条 AI 问答笔记**——基于日常 LLM 辅助研究构建的知识库，可在博客上搜索。
- **MathJax、夜间模式、RSS、双语内容**——通过自定义 CSS 和主题增强的标准功能。

**规模：**

| 指标 | 数量 |
| --- | --- |
| 英文文章 | 10,264 |
| 中文文章 | 10,259 |
| AI 问答笔记 | 9,794 |
| Python 脚本 | 323 |
| ML 脚本 | 191 |
| 页面浏览量（过去一个月） | 约 100,000 |

![jekyll-ai-blog——拥有 10K+ 文章、翻译、TTS 和 PDF 管道的 AI 驱动博客](/assets/images/ai-portfolio/blog.png)

![页面浏览量（过去一个月）——约 100,000](https://lzwjava.com/assets/images/analytics/pv.png)

GitHub: [lzwjava/jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog)

---

## 🎬 FluxReel——AMD 黑客马拉松短视频工作室

[FluxReel](https://github.com/lzwjava/flux-reel) 将一个一行主题转化为 **15 秒的竖屏短视频**（1080×1920、9:16、30 fps）——核心图像生成在 **AMD Radeon GPU（ROCm）** 上运行。为 AMD AI DevMaster 黑客马拉松 2026-07 的 **赛道 1——多模态内容创作工具** 而构建。

**工作原理：**

1. **脚本**——LLM 根据主题起草一篇 300–500 字的 Markdown 文章，然后场景规划器精确生成 5 个场景，每个场景包含 `title` / `subtitle` / `image_prompt`（双语，自动从主题检测）。
2. **图像**——5 个场景图像并行生成：通过 AMD GPU 使用 diffusers（FLUX.1-schnell / dev / 2-dev）、stable-diffusion.cpp（FLUX.1-schnell Q4_0 GGUF，低显存）或 OpenRouter。
3. **合成**——PIL 构建每个 1080×1920 的幻灯片，包含标题/副标题栏，字体自动缩小以适应，支持 CJK 感知换行。
4. **组装**——ffmpeg 将每个幻灯片编码为 3 秒的 H.264 片段，无需重新编码即可连接，并混合背景音乐。

**主要特点：**

- **主题 → 几分钟内出视频**：从提示到精美 MP4 的完整管道，在本地 AMD 上运行。
- **双语字幕**——使用 Noto Sans CJK 字体和基于字符的换行自动检测 EN/中文。
- **多个图像后端**——`local`（ROCm + diffusers FLUX）、`sdcpp`（GGUF 4-bit，低显存）、`openrouter`（云端回退）、`auto`（优先本地，回退云端）。
- **Web UI + REST API**——带有作业队列、进度轮询、视频预览和下载功能的 FastAPI 服务器。
- **可选的 YouTube 上传**——通过 LLM 自动生成标题/描述/标签。
- **远程 AMD GPU 管理**——rc-tunnel、通过 `hf-mirror.com`（适合中国）下载 FLUX 模型、GPU/ROCm/磁盘信息。

**演示输出帧（1080×1920，9:16）：**

![FluxReel 演示帧 2——在 AMD GPU 上生成的 15 秒竖屏短视频](https://raw.githubusercontent.com/lzwjava/flux-reel/main/submission/demo_frame_2.jpg)

**🏆 AMD AI DevMaster 黑客马拉松——完成奖**（证书编号 0121 Zhiwei Li）：

![AMD AI DevMaster 黑客马拉松完成奖——FluxReel](/assets/images/ai-portfolio/fluxreel-award.png)

GitHub: [lzwjava/flux-reel](https://github.com/lzwjava/flux-reel)

---

## 🤖 iclaw——终端 AI Agent (REPL)

[iclaw](https://github.com/lzwjava/iclaw) 是一个终端 AI agent，可以自主编码、搜索和运行命令——适用于个人机器和受限制的企业机器。一个最小的 openclaw 实现，构建为纯 Python CLI，无需浏览器扩展或 IDE 插件，由 GitHub Copilot 提供支持。

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

- 在您的终端中与 GitHub Copilot 或 OpenRouter 进行**多轮对话**。
- **多个模型提供商**：GitHub Copilot（OAuth 设备流）和 OpenRouter（API 密钥）。
- **原生工具调用**：模型自主调用网络搜索、执行 shell 命令和编辑文件——无需人工介入。
- **多个搜索提供商**：DuckDuckGo、Startpage、Bing 和 Tavily。
- **企业友好**：无需 IDE 插件或浏览器扩展。在支持代理和 CA 捆绑包的企业防火墙后方可工作。
- **默认模型**：GPT-5.2。

![iclaw——具有原生工具调用功能的终端 AI agent REPL](/assets/images/ai-portfolio/iclaw.jpg)

![iclaw——显示自主编码和 shell 命令的执行日志](/assets/images/ai-portfolio/iclaw-log.png)

GitHub: [lzwjava/iclaw](https://github.com/lzwjava/iclaw)

---

## ⚙️ zz——数据集处理与训练实用工具

[zz](https://github.com/lzwjava/zz) 是一个用于 ML 训练管道的工具箱——数据集下载、分词、提取和推理实用程序。在 RunPod H200、DigitalOcean H100 和家庭 RTX 4070 上训练 GPT-2 124M 期间使用。也托管在 [Hugging Face](https://huggingface.co/lzwjava/zz) 上。

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

- **FineWeb 下载**——规划并下载分片以达到 token 预算（100 亿、1000 亿+ tokens），支持断点续传并带有进度跟踪。
- **hf-mirror.com 支持**——当 HuggingFace 被屏蔽时，用于中国地区访问的 wget 脚本。
- **Parquet 提取**——通过 pyarrow iter_batches 进行内存安全迭代。
- **分词**——将原始文本转换为训练就绪格式。
- **训练分析**——从训练日志中计算持续时间、评估指标。
- **DeepSeek 推理**——用于 DeepSeek-V2-Lite 的 LLM 推理脚本。

![zz 在 Hugging Face 上——数据集处理与训练实用工具，22 次提交，3 个贡献者](/assets/images/ai-portfolio/zz-huggingface.png)

GitHub: [lzwjava/zz](https://github.com/lzwjava/zz) · Hugging Face: [lzwjava/zz](https://huggingface.co/lzwjava/zz)

---

## 🎓 证书

### 机器学习专项课程——DeepLearning.AI 与斯坦福大学

于 2023 年 11 月完成。三门课程：监督式机器学习、高级学习算法、无监督学习、推荐系统、强化学习。

![Coursera 机器学习专项课程证书——李智维，2023 年 11 月](/assets/images/ai-portfolio/coursera-ml-1.png)

### 深度学习专项课程——DeepLearning.AI

于 2023 年 12 月完成。五门课程：神经网络、超参数调优、结构化机器学习项目、CNN、序列模型。

![Coursera 深度学习专项课程证书——李智维，2023 年 12 月](/assets/images/ai-portfolio/coursera-dl-1.png)

---

- GitHub: [https://github.com/lzwjava](https://github.com/lzwjava)
- 博客: [https://lzwjava.github.io](https://lzwjava.github.io)

---

AI 翻译提示：英国环球银行(British Universal Bank)。