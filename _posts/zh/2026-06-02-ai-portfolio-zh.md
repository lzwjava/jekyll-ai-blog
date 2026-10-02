---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 我的AI作品集——日常AI工作的证明
translated: true
---

我不只是谈论AI——我每天都在大规模使用它。这篇文章是我的AI工作视觉作品集：我构建的工具、消耗的token以及获得的认证。

---

## 🖥️ LLM训练与推理——我的硬件设置

于2023年搭建了我的机器学习工作站，并一直在进行训练和学习。

**硬件经验：**

| GPU | 显存 | 经验时长 | 使用场景 |
| ----- | ------ | ------------ | ------- |
| NVIDIA RTX 4070 | 12 GB | 3年 | 家庭工作站 |
| NVIDIA H200 | 141 GB | 3个月 | RunPod / DigitalOcean |
| AMD MI300X | 192 GB HBM3 | 3个月 | AMD开发者云 |

**我训练过的模型：**

- **GPT-2 124M** 从头开始在FineWeb数据集上训练（nanoGPT）——在RTX 4070、H200和MI300X上。
- **GPT-2 760M** 从头开始在AMD MI300X（192 GB HBM3）上训练——探索nanochat、DeepSeek v4 MoE。
- 各种关于超参数调优、学习率调度和数据集预处理的实验。

**工作站：**

![我的ML学习工作站——2023年搭建，RTX 4070 12GB，用于日常训练和实验](/assets/images/ai-portfolio/learning-station.jpg)

**AMD开发者云——MI300X 192GB HBM3：**

![AMD开发者云——用于大规模模型训练的MI300X实例](/assets/images/ai-portfolio/amd-dev-cloud.png)

---

## 🔧 GPU拆解——从坏卡中学习硬件

从二手市场购买了坏掉的GPU（**Quadro 401 / 2000 / 4000**等），拆解它们并研究电路板以了解组件——VRM电路（MOSFET、电感、电容）、内存芯片布局，以及每一代架构（Fermi → …）的不同之处。每一块PCB都是工程决策的蓝图。

![二手市场坏掉的GPU——Quadro拆解，研究VRM电路和PCB架构](/assets/images/ai-portfolio/gpu-teardown.jpg)

---

## 🖥️ 廉价AI工作站——特斯拉M40 12GB约1200元人民币

使用闲鱼上的二手零件，以大约1200元人民币（约165美元）搭建了一个**12 GB AI工作站**，为我的家庭设置添加了第二块CUDA GPU，与RTX 4070配合使用。

**配置清单：**

| 部件 | 成本（人民币） | 备注 |
| ------ | -----------: | ------ |
| 特斯拉M40 12GB | ~200–300 | 数据中心GPU，Maxwell架构，250W，被动散热 |
| MSI Z170A Gaming M5 | ~200–300 | LGA1151，3× PCIe x16，BIOS支持良好 |
| Intel i5-6500 / 电源 / 内存 / 机箱 | ~500–700 | 来自二手市场的标准ATX零件 |
| **总计** | **~1000–1300** | **~140–180美元获得12 GB CUDA算力** |

> 特斯拉M40是一张**12 GB GDDR5**显卡（也有24 GB版本）。它使用**8-pin EPS（CPU）电源接口**，而不是标准的PCIe电源线——这是一个常见的陷阱。该卡为**被动散热**，需要强制气流。

**突破——BIOS配置：**

在不同主板（华南B75、华硕A68HM-E、微星B150M）上经过大量试错后，最终在MSI Z170A Gaming M5上成功的关键设置是：

```
设置
  → 高级
    → Windows操作系统配置
      → Windows 10 WHQL支持 = 禁用
```

此外，在BIOS中：

- **Above 4G Decoding** = 启用（M40的大64位BAR需要）
- **CSM** = 禁用（纯UEFI模式，用于正确的PCIe资源分配）
- 将M40放入**PCI_E1**（最顶部的x16插槽，直接连接到CPU）

通过这些设置，显卡成功初始化——`nvidia-smi`显示完整的**11,520 MiB显存**（ECC保留剩余的512 MiB），满载压力测试确认**100%利用率，6.12 TFLOPS FP32，约理论峰值的90%**，温度保持在35–39°C。

**这意味着什么——影响：**

这意义重大。大约**1000–1200元人民币**，你就可以为家庭实验室增加**12 GB的CUDA显存**。这足以运行：

- **7B–14B LLM** 在Q4–Q8量化下，具有合理的上下文长度
- **27B模型** 在激进量化下（IQ1_M，约6.3 GB），具有4k–8k上下文
- **批量推理、LoRA微调**以及多GPU实验

M40较老（Maxwell，2015年，计算能力5.2），因此FP16性能较弱，并且需要使用编译时添加`-DCMAKE_CUDA_ARCHITECTURES=52`的llama.cpp构建版本。但就价格而言，它很难被击败——**每GB显存约100元人民币**。

我计划再搭建几台这样的廉价工作站，在多个12 GB节点上扩展分布式推理和训练实验。

![特斯拉M40工作站——使用MSI Z170A Gaming M5和12 GB M40 GPU的配置](/assets/images/ai-portfolio/m40-workstation.jpg)

![特斯拉M40——nvidia-smi显示11,520 MiB显存，显卡完全初始化](/assets/images/ai-portfolio/m40-running.jpg)

---

### 🏋️ 训练运行总结

| # | 模型 | 框架 | 参数量 | 硬件 | 步数 | 状态 |
| --- | ------- | ----------- | -------- | ---------- | ------- | -------- |
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
| 11 | codeparrot-d12 | nanochat | 286M | RTX 4070 | ? | 仅有脚本 |
| 12 | Notes SFT (Qwen3-4B) | trl/peft | 4B | RTX 4070 | ? | 仅有脚本 |
| 13 | SPGISpeech (Whisper) | transformers | varies | ? | ? | 仅有脚本 |

## 🧠 增强版nanoGPT——我的分支

从[karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)派生，并扩展了额外的数据集管道、扩缩训练配置以及用于学习的内联形状注释。45次提交，2025年11月至2026年4月。

**新增数据集管道：**

| 数据集 | 路径 | 描述 |
| --------- | ------ | ------------- |
| FineWeb-Edu | `data/fineweb/` | HuggingFace FineWeb-Edu（100亿+ tokens）。基于分片的加载、分块处理、增量训练/验证拆分。 |
| OpenWebText 10k | `data/openwebtext_10k/` | 快速10k子集用于快速迭代。 |
| Wikipedia Local | `data/wikipedia_local/` | 直接对本地纯文本转储进行分词（无需HuggingFace下载）。 |

**新增训练配置：**

| 配置 | 目标 | 备注 |
| -------- | -------- | ------- |
| `train_fineweb.py` | 125M on FineWeb | 针对RTX 4070 12 GB调优（n_embd=384，dropout=0.1）。 |
| `train_fineweb1_5b.py` | 1.5B on FineWeb | 针对H200 80 GB。 |
| `train_fineweb_gpt3.py` | GPT-3风格100亿tokens | 基于分片的加载器，更宽的调度。 |
| `train_fineweb_760m.py` | 760M on FineWeb | 针对MI300X 192 GB HBM3。 |
| `train_gpt2_200m.py` | GPT-2 200M | 通用中型配置。 |
| `train_gpt2_200m_smoke.py` | 烟雾测试 | 快速200M sanity检查（约几分钟）。 |

**模型更改：**

- 在`model.py`前向传播（CausalSelfAttention、MLP、GPT）中添加**内联张量形状注释**——在每一步显示精确形状，并附有具体的GPT-2 XL示例，例如`# x: (B, T, C) e.g. (1, 5, 1600)`。有助于理解transformer数据流。

![增强版nanoGPT——45次提交、数据集管道、扩缩训练配置、内联形状注释](/assets/images/ai-portfolio/nanogpt-fork.png)

GitHub：[lzwjava/nanoGPT](https://github.com/lzwjava/nanoGPT)

---

## ⚙️ MoE与LLM推理——刚刚开始学习

在训练了密集的GPT-2模型之后，我想研究LLM的架构和系统层面：**混合专家（MoE）**和**推理引擎**。老实说，我刚刚起步。我阅读了一些代码，运行了一些东西，并跟着学习——但我还无法从头写出这些东西，我仍然认为自己在这方面基本是初学者。

**我开始研究的内容：**

- **MoE架构**——路由+分发+专家计算+合并+负载均衡的高级概览。我浏览了DeepSeek-MoE（细粒度+共享专家）、MegaBlocks（无丢弃块稀疏分发）、Tutel（全到全专家并行）和Mixtral（8×7B，top-2）作为参考实现——主要通过AI代理为我讲解代码。
- **前向传播**——路由（`router_logits` → `topk(softmax(...))`）、每个专家的计算，以及如何使`tokens → experts → tokens`在GPU之间快速完成。我能跟上流程，但我还无法自己推理其中的权衡。
- **KV缓存分页、prefill/decode调度、连续批处理、CUDA图、前缀缓存、张量并行**——我知道这些名称和大致概念，但服务栈很深，我只触及了表面。

**我的学习方式——使用代理进行探索：**

1. **阅读代码**——我使用编码代理（例如Hermes Agent）帮助我在mini-sglang中端到端追踪MoE：`router (LinearReplicated) → MoELayer → FusedMoe (top-k routing → block-aligned dispatch → 2 fused GEMMs → sum-reduce) → Triton grouped-GEMM kernel`。当代理引导我时，我能理解；但我还无法自己重现。
2. **运行并基准测试**——让nano-vLLM在我的RTX 4070上运行Qwen3-0.6B，使用flash-attention：**506 tok/s prefill**，decode约4–30 tok/s，在笔记本电脑基准测试中约1434 tok/s。我将这些视为数据点，而不是任何事情的证据。
3. **从源码编译**——从源码构建了**SGLang**（`pip install -e "python"`，修复了torch/torchaudio CUDA不匹配到2.11.0+cu130，编译了它的3个PyO3 Rust扩展），并让Qwen2.5-0.5B服务器在`localhost:30010`提供补全服务。还让nano-vLLM使用预构建的`flash-attn==2.8.3` wheel运行。让东西能够构建是一回事；深入理解是另一回事。

**我目前学到的（仍然浅薄）：**

| 概念 | 我理解的内容 |
| --------- | -------------------------------- |
| **分页KV缓存** | 固定256-token块、空闲列表、内容哈希前缀缓存、写时复制共享——仅高级概念 |
| **调度器** | 针对长提示的分块prefill、decode步进、KV缓存满时的抢占——大致理解 |
| **CUDA图** | 捕获decode批次（`[1,2,4,…512]`）以减少CPU内核启动开销——动机而非细节 |
| **MoE分发** | `moe_align_block_size`排序+为每个专家填充token块以实现高效的Triton grouped-GEMM——曾跟随代码一次 |
| **张量并行** | 行并行层的`all_reduce`、LM头的`gather`、`LinearReplicated`共享路由器——这些名称现在有道理了 |
| **融合MoE内核** | gate/up融合为一个GEMM，SwiGLU激活拆分，路由权重仅应用一次——阅读过，保留不完整 |

**我的方法**——老实说，我很多“阅读”是代理阅读代码并向我解释。循环大致是：

```text
阅读20% → 修改30% → 破坏30% → 提交20%
```

我才开始这个领域几周。我了解得刚好足以跟上关于MoE推理的对话——但还不足以自己构建或改进这些系统。

---

## 📝 SEC-EDGAR-GPT——从头开始在SEC文件上训练GPT-2 (124M)

在**1.55B tokens**的SEC EDGAR财务文件（10-K、10-Q和其他公司披露文件）上从头训练了一个**124M参数的GPT-2**——在单个**RTX 4070**（12 GB显存）上训练约8小时，收敛到验证损失2.28。

该模型生成令人信服的SEC模板文本——风险因素、MD&A部分、业务描述——并通过RunPod上的FastAPI服务器部署用于交互式聊天。

整个项目——模型训练、论文、聊天机器人和网站——在**3天内使用Hermes Agent**构建，展示了AI代理如何使LLM研究变得可访问。

在一家全球银行内部共享后，该项目获得了**200多次内部浏览**。一位首席工程师留下了评论，称其为*“不错”*。此外，受一位朋友在循环transformer方面工作的启发，这个项目让我开始思考如何将金融tokens与自然语言tokens区别对待，以提高生成准确性。

![SEC-EDGAR-GPT聊天机器人](/assets/images/sec-edgar-gpt/chatbot_web.png)

**代码：** [github.com/lzwjava/sec-edgar-gpt](https://github.com/lzwjava/sec-edgar-gpt) · **论文：** [sec-edgar-gpt.pdf](https://github.com/lzwjava/sec-edgar-gpt/raw/main/sec-edgar-gpt.pdf) · **模型：** [Hugging Face](https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf) · **聊天：** [sec-edgar-gpt.lzwjava.workers.dev](https://sec-edgar-gpt.lzwjava.workers.dev/)

---

## 📊 LLM API使用量——数据

### OpenRouter——过去一年

消耗了22.8亿tokens，花费239美元，跨多个模型发送了15.5万次API请求。

![OpenRouter活动仪表盘——22.8亿tokens，239美元，过去一年15.5万次请求](/assets/images/ai-portfolio/openrouter-activity.png)

### DeepSeek——过去一年

通过DeepSeek平台在过去一年中消耗了6.29亿tokens。

### 通过SSSAICode的Claude API——2026年4月

一个月内花费171.53美元。2,555次请求。1.15亿+ tokens。缓存命中率90.9%。

![SSSAICode Claude使用情况——Opus 4.6、Opus 4.7、Sonnet 4.6、Haiku 4.5](/assets/images/ai-portfolio/sssaicode-usage.png)

### 小米MIMO订阅——使用了12.5亿tokens

Pro月付计划，包含380亿主配额 + 87.5亿补偿配额（约46亿免费额度）。**2026年5月至6月消耗了12.5亿tokens**。

![小米MIMO Pro计划——消耗12.5亿tokens，剩余约34亿免费额度](/assets/images/ai-portfolio/xiaomi-mimo-usage.png)

#### 每月Token使用明细

| 月份 | 模型 | 总Tokens | 输入（缓存命中） | 输入（缓存未命中） | 输出 | 请求数 |
| ------- | ------- | -------------: | -------------------: | --------------------: | -------: | ---------: |
| 2026-06 | mimo-v2.5 | 285,179 | 36,416 | 143,556 | 105,207 | 78 |
| 2026-06 | mimo-v2.5-pro | 734,873,374 | 710,036,672 | 21,617,131 | 3,219,571 | 10,704 |
| 2026-05 | mimo-v2.5 | 91,203 | 5,312 | 52,908 | 32,983 | 27 |
| 2026-05 | mimo-v2.5-pro | 508,851,211 | 488,291,136 | 17,725,731 | 2,834,344 | 8,649 |
| 2026-05 | mimo-v2-pro | 3,571,328 | 3,021,568 | 539,357 | 10,403 | 167 |

**月度总计：** 2026年5月：**5.125亿tokens**（8,843次请求）· 2026年6月：**7.352亿tokens**（10,782次请求）

> mimo-v2.5-pro占主导（约总使用量的96%）。mimo-v2.5-pro上的缓存命中率约96.7%，使成本保持高效。6月份tokens量比5月份增长43.5%。

### 总结

| 平台 | Tokens | 期间 | 成本 |
| ---------- | -------- | -------- | ------ |
| OpenRouter | 22.8亿 | 过去一年 | 239美元 |
| DeepSeek | 6.29亿 | 过去一年 | — |
| SSSAICode (Claude) | 1.15亿+ | 2026年4月 | 171.53美元 |
| 小米MIMO | 12.5亿 | 2026年5–6月 | 免费46亿额度 |
| 其他（GitHub Copilot等） | 7.26亿 | 过去一年 | — |
| **总计** | **约50亿** | **过去一年** | **—** |

---

## 🏢 企业AI使用——在英国一家环球银行

在一家英国环球银行（通过一家全球IT外包公司），我在编码助手之上构建了一个自主AI代理层，用于自动化脚本编写、日志记录、文档和测试。

**我构建的内容：**

- **20个定制化AI代理**——针对不同技术栈和工作流程的专用提示和上下文。
- **400个由编码助手编写的可重用脚本**——用于Java、Spring、Python、Angular和DevOps工具的常见任务自动化。
- **1,800份由编码助手编写的指南**——由AI在人类提示下生成的文档。
- **约70个通过编码助手API自动生成的测试用例**——涵盖Spring过滤器、Python unittest、JSON截断、提示工程和区域端点。

**结果：**

- 在企业范围内，编码助手使用量排名**前6%**（按高级请求衡量）。
- 因备受瞩目的AIPlayer项目获得了**贡献奖**。
- 加入了银行的内部AI社区。

![AIPlayer贡献奖](/assets/images/ai-portfolio/aiplayer.jpg)

---

## 🎤 AI讲座——从神经网络到代理

在英国一家环球银行向**80名参与者**进行了一场技术讲座——包括高级顾问、专家、副总监、软件工程师和承包商。

**讲座题目：** *“从神经网络到代理”*——从最简单的神经网络（`y = wx`）出发，经过MNIST、Transformers、GPT、nanoGPT，直到构建个人AI代理。

**涵盖内容：**

- 从基本原理出发的神经网络——前向传播、反向传播、梯度下降
- Transformer架构——Q/K/V注意力、多头注意力、位置编码
- GPT内部原理——分词、嵌入、训练、生成
- nanoGPT——在H200/RTX 4070上从头训练GPT-2
- LLM代理——Claude Code、OpenClaw、Hermes、工具调用、代理循环
- 真实数据——消耗10亿tokens、H200每小时3.44美元、钱实际花在哪里
- 我的路径——从阅读Q/K/V到从头训练模型的3年历程

**反馈：**

- 一位初级工程师说：*“你是我想要成为的人”*——这场讲座让他开阔了AI可能性的眼界
- 高级工程师赞赏从基本原理出发的方法——没有炒作，只有数学和代码
- 多次关于训练、代理和职业方向的后续对话

**幻灯片：** 使用Claude Code和Marp，基于我公开的AI回复笔记制作。

幻灯片（Marp）：[PDF](/assets/marp/neural_networks_to_agents_public.pdf)

---

## 🛠️ ww——跨平台CLI工具包

[ww](https://github.com/lzwjava/ww)是我的旗舰CLI工具包——255+次提交，10+个命令组，跨平台（macOS + Linux）。它涵盖了带AI提交消息的git工作流程、笔记管理、图像/PDF处理、网络搜索、GitHub Copilot聊天、系统实用程序和LLM驱动的辅助工具。

```
lzwjava@lzw-mac ww % uv run ww --help
Usage: ww <group> [command] [options]

Action:
  ww action [workflow.yml]  触发GitHub Actions工作流

AMD Dev Cloud:
  ww amd-dev-cloud snapshots    列出快照
  ww amd-dev-cloud start-train  创建用于训练的GPU droplet
  ww amd-dev-cloud end-train    快照并销毁GPU droplet

Copilot:
  ww copilot auth           通过GitHub OAuth进行身份验证
  ww copilot chat           与Copilot模型聊天

Git:
  ww git gpa            对所有仓库执行git pull --all
  ww git squash <n>     压缩最近n次提交
  ww git amend-push     修改上次提交并强制推送

LLM:
  ww llm compare <prompt>   比较多个LLM响应
  ww llm query <question>   查询本地RAG文档

Note:
  ww note              剪贴板到笔记（快速捕获）
  ww note process      清空笔记队列
  ww note watch        自动处理守护进程

Screenshot:
  ww screenshot               截图并创建笔记
  ww screenshot interact-note  交互式截图笔记

255+次提交。10+个命令组。跨平台（macOS + Linux）。
```

![ww——GitHub上的跨平台CLI工具包](/assets/images/ai-portfolio/ww1.png)

GitHub：[lzwjava/ww](https://github.com/lzwjava/ww)

---

## 📝 jekyll-ai-blog——AI驱动的博客平台

[jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog)是[lzwjava.github.io](https://lzwjava.github.io)的源代码——一个通过AI自动化增强的Jekyll博客。包含10,000+篇英文文章、10,000+篇中文文章、9,700+条AI答案笔记。过去一个月约10万页面浏览量（Cloudflare分析）。

```
lzwjava@lzw-mac jekyll-ai-blog % ls README.md
README.md
```

**它与标准Jekyll博客的不同之处：**

- **AI驱动的翻译**——基于LLM的翻译管道通过GitHub Actions自动将每篇文章扩展到多种语言。
- **Google Cloud Text-to-Speech**——自动生成文章的音频版本以提高可访问性。
- **XeLaTeX PDF/EPUB生成**——从Markdown源生成高质量、可打印的PDF和电子书导出。
- **GitHub Actions CI/CD**——自动化构建、测试、翻译和部署工作流。
- **8,000+条AI答案笔记**——基于日常LLM辅助研究构建的知识库，可在博客上搜索。
- **MathJax、夜间模式、RSS、双语内容**——通过自定义CSS和主题增强的标准功能。

**规模：**

| 指标 | 数量 |
| -------- | ------- |
| 英文文章 | 10,264 |
| 中文文章 | 10,259 |
| AI答案笔记 | 9,794 |
| Python脚本 | 323 |
| ML脚本 | 191 |
| 页面浏览量（过去一个月） | ~100,000 |

![jekyll-ai-blog——AI驱动的博客，拥有1万+文章、翻译、TTS和PDF管道](/assets/images/ai-portfolio/blog.png)

![页面浏览量（过去一个月）——约100,000](https://lzwjava.com/assets/images/analytics/pv.png)

GitHub：[lzwjava/jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog)

---

## 🎬 FluxReel——AMD黑客马拉松短视频工作室

[FluxReel](https://github.com/lzwjava/flux-reel)将一个单行主题转化为**15秒的竖屏短视频**（1080×1920，9:16，30 fps）——核心图像生成在**AMD Radeon GPU（ROCm）**上运行。为AMD AI DevMaster黑客马拉松2026-07的**赛道1——多模态内容创作工具**而构建。

**工作原理：**

1. **脚本**——LLM根据主题起草一篇300–500字的Markdown文章，然后场景规划器精确生成5个场景，包含`title` / `subtitle` / `image_prompt`（双语，自动从主题检测）。
2. **图像**——并行生成5个场景图像：通过diffusers（FLUX.1-schnell / dev / 2-dev）使用AMD GPU、stable-diffusion.cpp（FLUX.1-schnell Q4_0 GGUF，低显存）或OpenRouter。
3. **合成**——PIL构建每个1080×1920的幻灯片，带有标题/副标题栏，字体自动缩小以适应，支持CJK换行。
4. **组装**——ffmpeg将每个幻灯片编码为3秒的H.264片段，无需重新编码即可拼接，并混入背景音乐。

**关键特性：**

- **主题 → 视频只需几分钟**：从提示到精美的MP4的完整管道，在本地AMD上运行。
- **双语字幕**——自动检测英文/中文，使用Noto Sans CJK字体和基于字符的换行。
- **多个图像后端**——`local`（ROCm + diffusers FLUX）、`sdcpp`（GGUF 4-bit，低显存）、`openrouter`（云端回退）、`auto`（优先本地，回退到云端）。
- **Web UI + REST API**——FastAPI服务器，带有作业队列、进度轮询、视频预览和下载。
- **可选YouTube上传**——通过LLM自动生成标题/描述/标签。
- **远程AMD GPU管理**——rc-tunnel、通过`hf-mirror.com`（对中国友好）下载FLUX模型、GPU / ROCm /磁盘信息。

**演示输出帧（1080×1920，9:16）：**

![FluxReel演示帧2——在AMD GPU上生成的15秒竖屏短视频](https://raw.githubusercontent.com/lzwjava/flux-reel/main/submission/demo_frame_2.jpg)

**🏆 AMD AI DevMaster黑客马拉松——完成奖**（0121 李智维）：

![AMD AI DevMaster黑客马拉松完成奖——FluxReel](/assets/images/ai-portfolio/fluxreel-award.png)

GitHub：[lzwjava/flux-reel](https://github.com/lzwjava/flux-reel)

---

## 🤖 iclaw——终端AI代理（REPL）

[iclaw](https://github.com/lzwjava/iclaw)是一个终端AI代理，能够自主编写代码、搜索和执行命令——可在个人机器和受限制的企业机器上工作。一个最小化的openclaw实现，作为纯Python CLI构建，无需浏览器扩展或IDE插件，由GitHub Copilot驱动。

```
lzwjava@lzw-mac iclaw % iclaw

  ██  █████  ██       █████  ██   ██
  ██ ██      ██      ██   ██ ██   ██
  ██ ██      ██      ███████ ██ █ ██
  ██ ██      ██      ██   ██ ██████
  ██  █████  ███████ ██   ██  ███ ██

可用命令：
  /provider_model      选择并验证模型提供商
  /model               从你的提供商选择特定模型
  /search              网络搜索（用法：/search <query>）
  /provider_search     选择网络搜索提供商
  /proxy               设置HTTP/HTTPS代理（用法：/proxy [url|off]）
  /ca_bundle           设置HTTPS的CA包（用法：/ca_bundle [path|off]）
  /log                 设置日志详细程度（用法：/log [verbose|info]）
  /copy                将上次Copilot响应复制到剪贴板
  /read                将文件内容打印到终端（用法：/read <path>）
  /clear               清除对话历史
  /compact             使用LLM压缩对话历史
  /export              将完整对话历史导出为JSON文件
  /status              显示当前设置
  /help                显示可用命令
  /exit                退出REPL。
```

**关键特性：**

- 在终端中与GitHub Copilot或OpenRouter进行**多轮对话**。
- **多个模型提供商**：GitHub Copilot（OAuth设备流）和OpenRouter（API密钥）。
- **原生工具调用**：模型自主调用网络搜索、执行shell命令和编辑文件——无需人工干预。
- **多个搜索提供商**：DuckDuckGo、Startpage、Bing和Tavily。
- **企业友好**：无需IDE插件或浏览器扩展。在企业防火墙后通过代理和CA包支持工作。
- **默认模型**：GPT-5.2。

![iclaw——带有原生工具调用的终端AI代理REPL](/assets/images/ai-portfolio/iclaw.jpg)

![iclaw——显示自主编码和shell命令的执行日志](/assets/images/ai-portfolio/iclaw-log.png)

GitHub：[lzwjava/iclaw](https://github.com/lzwjava/iclaw)

---

## ⚙️ zz——数据集处理与训练工具

[zz](https://github.com/lzwjava/zz)是一个用于ML训练管道的工具包——数据集下载、分词、提取和推理实用程序。在RunPod H200、DigitalOcean H100和家庭RTX 4070上的GPT-2 124M训练运行中使用。也托管在[Hugging Face](https://huggingface.co/lzwjava/zz)上。

```
lzwjava@lzw-mac zz % tree -L 1
scripts/
  download/     # 数据集下载脚本（FineWeb、Wikimedia、HF镜像）
  extract/      # 数据提取、分词和重命名
  analysis/     # 训练时长和指标评估
  deepseek/     # LLM推理脚本（DeepSeek-V2-Lite）
logs/           # 训练日志和输出
datasets/       # 下载的数据集存储
```

**关键能力：**

- **FineWeb下载**——规划并下载分片以达到token预算（100亿、1000亿+ tokens），可恢复，带有进度跟踪。
- **hf-mirror.com支持**——当HuggingFace被屏蔽时，提供适用于中国的wget脚本。
- **Parquet提取**——通过pyarrow iter_batches进行内存安全迭代。
- **分词**——将原始文本转换为训练就绪格式。
- **训练分析**——从训练日志计算时长和指标评估。
- **DeepSeek推理**——用于DeepSeek-V2-Lite的LLM推理脚本。

![zz在Hugging Face上——数据集处理与训练工具，22次提交，3位贡献者](/assets/images/ai-portfolio/zz-huggingface.png)

GitHub：[lzwjava/zz](https://github.com/lzwjava/zz) · Hugging Face：[lzwjava/zz](https://huggingface.co/lzwjava/zz)

---

## 🎓 证书

### 机器学习专项课程——DeepLearning.AI & 斯坦福大学

2023年11月完成。三门课程：监督式机器学习、高级学习算法、无监督学习、推荐系统、强化学习。

![Coursera机器学习专项课程证书——李智维，2023年11月](/assets/images/ai-portfolio/coursera-ml-1.png)

### 深度学习专项课程——DeepLearning.AI

2023年12月完成。五门课程：神经网络、超参数调优、结构化机器学习项目、CNN、序列模型。

![Coursera深度学习专项课程证书——李智维，2023年12月](/assets/images/ai-portfolio/coursera-dl-1.png)

---

- GitHub：[https://github.com/lzwjava](https://github.com/lzwjava)
- 博客：[https://lzwjava.github.io](https://lzwjava.github.io)

---

AI翻译提示：British Universal Bank（英国环球银行）。
