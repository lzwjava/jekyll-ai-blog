---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 我的AI作品集——日常AI工作的证明
translated: true
---

我不只是谈论AI——我每天都在大规模使用它。这篇博文是我的AI成果视觉作品集：我构建的工具、消耗的令牌以及获得的认证。

---

## 🖥️ LLM训练与推理——我的硬件配置

2023年搭建了我的机器学习工作站，此后一直进行训练和学习。

**硬件经验：**

| GPU | 显存 | 经验时长 | 使用平台 |
| --- | --- | --- | --- |
| NVIDIA RTX 4070 | 12 GB | 3年 | 家庭工作站 |
| NVIDIA H200 | 141 GB | 3个月 | RunPod / DigitalOcean |
| AMD MI300X | 192 GB HBM3 | 3个月 | AMD开发者云 |

**我训练过的模型：**

- **GPT-2 124M** 从零开始在FineWeb数据集上训练（nanoGPT）——在RTX 4070、H200和MI300X上完成。
- **GPT-2 760M** 从零开始在AMD MI300X（192 GB HBM3）上训练——探索nanochat、DeepSeek v4 MoE。
- 各种超参数调优、学习率调度和数据集预处理实验。

**工作站：**

![我的ML学习站——2023年搭建，RTX 4070 12GB，用于日常训练和实验](/assets/images/ai-portfolio/learning-station.jpg)

**AMD开发者云——MI300X 192GB HBM3：**

![AMD开发云——用于大规模模型训练的MI300X实例](/assets/images/ai-portfolio/amd-dev-cloud.png)

---

### 🏋️ 训练运行摘要

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
| 11 | codeparrot-d12 | nanochat | 286M | RTX 4070 | ? | 仅有脚本 |
| 12 | Notes SFT (Qwen3-4B) | trl/peft | 4B | RTX 4070 | ? | 仅有脚本 |
| 13 | SPGISpeech (Whisper) | transformers | varies | ? | ? | 仅有脚本 |

## 🧠 增强版nanoGPT——我的分支

Fork了[karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)并进行了扩展，添加了额外的数据集管道、扩展的训练配置以及用于学习的内联形状注释。45次提交，2025年11月至2026年4月。

**新增数据集管道：**

| 数据集 | 路径 | 描述 |
| --- | --- | --- |
| FineWeb-Edu | `data/fineweb/` | HuggingFace FineWeb-Edu（100亿+令牌）。基于分片加载、分块处理、增量训练/验证分割。 |
| OpenWebText 10k | `data/openwebtext_10k/` | 用于快速迭代的10k子集。 |
| Wikipedia Local | `data/wikipedia_local/` | 直接对本地纯文本转储进行分词（无需HuggingFace下载）。 |

**添加的训练配置：**

| 配置 | 目标 | 备注 |
| --- | --- | --- |
| `train_fineweb.py` | FineWeb上的125M | 针对RTX 4070 12 GB优化（n_embd=384, dropout=0.1）。 |
| `train_fineweb1_5b.py` | FineWeb上的1.5B | 用于H200 80 GB。 |
| `train_fineweb_gpt3.py` | GPT-3风格100亿令牌 | 基于分片的加载器，更宽的调度。 |
| `train_fineweb_760m.py` | FineWeb上的760M | 用于MI300X 192 GB HBM3。 |
| `train_gpt2_200m.py` | GPT-2 200M | 通用中型配置。 |
| `train_gpt2_200m_smoke.py` | 烟雾测试 | 快速200M健全性检查（约几分钟）。 |

**模型更改：**

- **内联张量形状注释** 贯穿`model.py`的前向传播（CausalSelfAttention, MLP, GPT）——在每个步骤显示精确形状，并附有具体的GPT-2 XL示例，例如`# x: (B, T, C) 例如 (1, 5, 1600)`。有助于理解Transformer数据流。

![增强版nanoGPT——45次提交，数据集管道，扩展训练配置，内联形状注释](/assets/images/ai-portfolio/nanogpt-fork.png)

GitHub: [lzwjava/nanoGPT](https://github.com/lzwjava/nanoGPT)

---

## ⚙️ MoE与LLM推理——刚刚开始学习

在训练了密集的GPT-2模型后，我想看看LLM的架构和系统方面：**混合专家模型（MoE）** 和**推理引擎**。老实说，我还处于非常初级的阶段。我阅读了一些代码，运行了一些东西，并跟着学习——但我无法从头编写这些内容，我仍然认为自己在这里主要是个初学者。

**我开始了解的内容：**

- **MoE架构**——路由、分发、专家计算、合并、负载均衡的高级视图。我粗略浏览了DeepSeek-MoE（细粒度+共享专家）、MegaBlocks（无丢弃块稀疏分发）、Tutel（全到全专家并行）和Mixtral（8×7B，top-2）作为参考实现——主要是通过AI代理带我阅读代码。
- **前向传播**——路由（`router_logits` → `topk(softmax(...))`）、每个专家的计算，以及如何让`令牌 → 专家 → 令牌`跨GPU快速完成。我能理解流程，但还无法自己权衡取舍。
- **KV缓存分页、预填充/解码调度、连续批处理、CUDA图、前缀缓存、张量并行**——我知道名称和大体概念，但服务栈很深，我只触及了表面。

**我的学习方式——使用代理进行探索：**

1. **阅读代码**——我使用编码代理（例如Hermes Agent）帮助我在mini-sglang中端到端追踪MoE：`router (LinearReplicated) → MoELayer → FusedMoe (top-k routing → block-aligned dispatch → 2 fused GEMMs → sum-reduce) → Triton grouped-GEMM kernel`。当代理带我走一遍时我能理解；但我还无法独自复现。
2. **运行并基准测试**——让nano-vLLM在我的RTX 4070上运行Qwen3-0.6B，使用flash-attention：**506 tok/s预填充**，解码约4-30 tok/s，在笔记本电脑基准测试中约1434 tok/s。我把这些视为数据点，而不是任何事情的证明。
3. **从源码编译**——从源码构建了**SGLang**（`pip install -e "python"`，将torch/torchaudio CUDA不匹配修复为2.11.0+cu130，编译了它的3个PyO3 Rust扩展），并在`localhost:30010`上运行了一个提供补全服务的Qwen2.5-0.5B服务器。还使用`flash-attn==2.8.3`预构建wheel让nano-vLLM运行起来。让东西能编译是一回事；深入理解它们是另一回事。

**我目前学到的（仍然浅显）：**

| 概念 | 我理解的内容 |
| --- | --- |
| **分页KV缓存** | 固定256令牌块、空闲列表、内容哈希前缀缓存、写时复制共享——仅高级概念 |
| **调度器** | 长提示的分块预填充、解码步进、KV缓存满时的抢占——大致理解 |
| **CUDA图** | 捕获解码批次（`[1,2,4,…512]`）以减少CPU内核启动开销——动机理解，细节不了解 |
| **MoE分发** | `moe_align_block_size`排序 + 为每个专家填充令牌块以实现高效的Triton grouped-GEMM——跟读过一次代码 |
| **张量并行** | 行并行层的`all_reduce`、LM头的`gather`、`LinearReplicated`共享路由器——现在明白这些名称的含义 |
| **融合MoE内核** | 门/上融合为一个GEMM、SwiGLU激活分割、路由权重恰好应用一次——阅读过，记忆不完整 |

**我的处理方法**——老实说，我的很多“阅读”是代理阅读代码然后解释给我听。循环大致是：

```text
阅读20% → 修改30% → 破坏30% → 提交20%
```

我接触这个才几周。我了解得刚好能跟得上关于MoE推理的对话——还不足以自己构建或改进这些系统。

---

## 📝 SEC-EDGAR-GPT——在SEC文件上从零训练的GPT-2（124M）

从零训练了一个**124M参数的GPT-2**，使用**15.5亿令牌**的SEC EDGAR财务文件（10-K、10-Q和其他公司披露文件）——在单个**RTX 4070**（12 GB显存）上训练了约8小时，验证损失收敛到2.28。

该模型生成令人信服的SEC标准文本——风险因素、管理层讨论与分析部分、业务描述——并通过RunPod上的FastAPI服务器部署为交互式聊天。

整个项目——模型训练、论文、聊天机器人和网站——在**3天内使用Hermes Agent**构建完成，展示了AI代理如何使LLM研究变得可及。

在一家全球银行内部共享后，该项目获得了**200多次内部查看**。一位首席工程师留言称其为*“不错”*。此外，受一位朋友关于循环Transformer研究的启发，这个项目让我思考如何区别对待财务令牌和自然语言令牌以提高生成准确性。

![SEC-EDGAR-GPT聊天机器人](/assets/images/sec-edgar-gpt/chatbot_web.png)

**代码：** [github.com/lzwjava/sec-edgar-gpt](https://github.com/lzwjava/sec-edgar-gpt) · **论文：** [sec-edgar-gpt.pdf](https://github.com/lzwjava/sec-edgar-gpt/raw/main/sec-edgar-gpt.pdf) · **模型：** [Hugging Face](https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf) · **聊天：** [sec-edgar-gpt.lzwjava.workers.dev](https://sec-edgar-gpt.lzwjava.workers.dev/)

---

## 📊 LLM API使用量——数据

### OpenRouter——过去一年

消耗了11.5亿令牌，花费239美元，跨多个模型发出了15.5万次API请求。

![OpenRouter活动仪表板——11.5亿令牌，239美元花费，1年内15.5万次请求](/assets/images/ai-portfolio/openrouter-activity.png)

![OpenRouter模型花费明细——Claude 4 Sonnet $44.40，Claude 3.5 Sonnet $9.67，Grok 3，Mistral，Kimi](/assets/images/ai-portfolio/openrouter-spend.png)

![OpenRouter按模型划分的令牌使用量——MiniMax 2.4亿，Gemini 2.03亿，DeepSeek 1.1亿](/assets/images/ai-portfolio/openrouter-models.png)

### 通过SSSAICode使用Claude API——2026年4月

一个月内花费171.53美元。2555次请求。超过1.15亿令牌。90.9%缓存命中率。

![SSSAICode Claude使用量——Opus 4.6，Opus 4.7，Sonnet 4.6，Haiku 4.5](/assets/images/ai-portfolio/sssaicode-usage.png)

### 小米MIMO订阅——使用了12.5亿令牌

专业月付计划，包含380亿主配额+87.5亿补偿配额（约46亿免费信用额度）。2026年5月至6月期间**消耗了12.5亿令牌**。

![小米MIMO专业计划——消耗12.5亿令牌，剩余约34亿免费信用额度](/assets/images/ai-portfolio/xiaomi-mimo-usage.png)

#### 月度令牌使用明细

| 月份 | 模型 | 总令牌数 | 输入（缓存命中） | 输入（缓存未命中） | 输出 | 请求数 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 2026-06 | mimo-v2.5 | 285,179 | 36,416 | 143,556 | 105,207 | 78 |
| 2026-06 | mimo-v2.5-pro | 734,873,374 | 710,036,672 | 21,617,131 | 3,219,571 | 10,704 |
| 2026-05 | mimo-v2.5 | 91,203 | 5,312 | 52,908 | 32,983 | 27 |
| 2026-05 | mimo-v2.5-pro | 508,851,211 | 488,291,136 | 17,725,731 | 2,834,344 | 8,649 |
| 2026-05 | mimo-v2-pro | 3,571,328 | 3,021,568 | 539,357 | 10,403 | 167 |

**月度总计：** 2026年5月：**5.125亿令牌**（8,843次请求）· 2026年6月：**7.352亿令牌**（10,782次请求）

> mimo-v2.5-pro主导使用（约占总量96%）。mimo-v2.5-pro上的缓存命中率约96.7%保持成本高效。6月令牌量较5月增长43.5%。

### 总结

| 平台 | 令牌数 | 时间段 | 成本 |
| --- | --- | --- | --- |
| OpenRouter | 11.5亿 | 过去一年 | $239 |
| SSSAICode (Claude) | 超过1.15亿 | 2026年4月 | $171.53 |
| 小米MIMO | 12.5亿 | 2026年5-6月 | 免费46亿信用额度 |
| 其他（GitHub Copilot等） | 5亿 | 过去一年 | — |
| **总计** | **约30亿+** | **过去一年** | **—** |

---

## 🏢 企业AI使用——在英资环球银行

在一家英资环球银行（通过一家全球IT外包公司），我在编程助手之上构建了一个自主AI代理层，用于自动化脚本编写、日志记录、文档和测试。

**我构建的内容：**

- **20个定制AI代理**——针对不同技术栈和工作流程的专用提示和上下文。
- **400个可复用的编程助手编写脚本**——跨Java、Spring、Python、Angular和DevOps工具的常见任务自动化。
- **1,800份编程助手编写的指南**——在人工提示下由AI生成的文档。
- **通过编程助手API自动生成约70个测试用例**——涵盖Spring Filters、Python unittest、JSON截断、提示工程和区域端点。

**成果：**

- 在整个企业中排名**前6%的编程助手使用量**，以高级请求衡量。
- 因高调项目AIPlayer获得**贡献奖**。
- 加入银行内部AI社区。

![AIPlayer贡献奖](/assets/images/ai-portfolio/aiplayer.jpg)

---

## 🎤 AI讲座——从神经网络到代理

在英资环球银行向**80名参与者**做了技术讲座——高级顾问、专家、副总监、软件工程师和承包商。

**讲座：** *“从神经网络到代理”*——从最简单的神经网络（`y = wx`）出发，经过MNIST、Transformer、GPT、nanoGPT，到构建个人AI代理的旅程。

**我涵盖的内容：**

- 神经网络基本原理——前向传播、反向传播、梯度下降
- Transformer架构——Q/K/V注意力、多头注意力、位置编码
- GPT内部机制——分词、嵌入、训练、生成
- nanoGPT——在H200/RTX 4070上从零训练GPT-2
- LLM代理——Claude Code、OpenClaw、Hermes、工具调用、代理循环
- 真实数据——消耗10亿令牌、H200每小时$3.44、钱花在哪里
- 我的路径——从阅读Q/K/V相关知识到从零训练模型的3年

**反馈：**

- 一位初级工程师说：*“你是我想要成为的人”*——这次讲座开阔了他对AI可能性的视野
- 高级工程师欣赏从基本原理出发的方法——没有炒作，只有数学和代码
- 关于训练、代理和职业方向的多次后续对话

**幻灯片：** 使用Claude Code和Marp构建，基于我的公开AI回复笔记。

幻灯片（Marp）：[PDF](/assets/marp/neural_networks_to_agents_public.pdf)

---

## 🛠️ ww——跨平台CLI工具包

[ww](https://github.com/lzwjava/ww)是我的旗舰CLI工具包——255+次提交，10+个命令组，跨平台（macOS + Linux）。它涵盖带有AI提交信息的git工作流、笔记管理、图像/PDF处理、网络搜索、GitHub Copilot聊天、系统实用程序和LLM驱动的助手。

```
智维@lzw-mac ww % uv run ww --help
Usage: ww <group> [command] [options]

Action:
  ww action [workflow.yml]  触发GitHub Actions工作流

AMD Dev Cloud:
  ww amd-dev-cloud snapshots    列出快照
  ww amd-dev-cloud start-train  创建GPU云主机进行训练
  ww amd-dev-cloud end-train    快照并销毁GPU云主机

Copilot:
  ww copilot auth           通过GitHub OAuth进行身份验证
  ww copilot chat           与Copilot模型聊天

Git:
  ww git gpa            对所有仓库执行git pull --all
  ww git squash <n>     压缩最近n次提交
  ww git amend-push     修改上次提交并强制推送

LLM:
  ww llm compare <prompt>    比较多个LLM响应
  ww llm query <question>    查询本地RAG文档

Note:
  ww note              剪贴板内容到笔记（快速捕获）
  ww note process      清空笔记队列
  ww note watch        自动处理守护进程

Screenshot:
  ww screenshot               捕获并创建笔记
  ww screenshot interact-note  交互式截图笔记

255+次提交。10+个命令组。跨平台（macOS + Linux）。
```

![ww——GitHub上的跨平台CLI工具包](/assets/images/ai-portfolio/ww1.png)

GitHub: [lzwjava/ww](https://github.com/lzwjava/ww)

---

## 📝 jekyll-ai-blog——AI驱动的博客平台

[jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog)是[lzwjava.github.io](https://lzwjava.github.io)的源代码——一个通过AI自动化增强的Jekyll博客。超过10,000篇英文文章，超过10,000篇中文文章，超过9,700篇AI回答笔记。过去一个月约70,000次页面浏览量（Cloudflare Analytics）。

```
智维@lzw-mac jekyll-ai-blog % ls README.md
README.md
```

**它与标准Jekyll博客的不同之处：**

- **AI驱动翻译**——基于LLM的翻译管道通过GitHub Actions自动将每篇文章扩展到多种语言。
- **Google Cloud Text-to-Speech**——自动生成文章的音频版本以提高可访问性。
- **XeLaTeX PDF/EPUB生成**——从Markdown源生成高质量的可打印PDF和电子书导出。
- **GitHub Actions CI/CD**——自动化构建、测试、翻译和部署工作流。
- **8,000+ AI回答笔记**——从日常LLM辅助研究中构建的知识库，可在博客上搜索。
- **MathJax、夜间模式、RSS、双语内容**——通过自定义CSS和主题增强的标准功能。

**规模：**

| 指标 | 数量 |
| --- | ---: |
| 英文文章 | 10,264 |
| 中文文章 | 10,259 |
| AI回答笔记 | 9,794 |
| Python脚本 | 323 |
| ML脚本 | 191 |
| 页面浏览量（过去一个月） | ~70,000 |

![jekyll-ai-blog——拥有10K+文章、翻译、TTS和PDF管道的AI驱动博客](/assets/images/ai-portfolio/blog.png)

![Cloudflare Web Analytics——38.9K访问量，45.2K页面浏览量，930ms加载时间，82%良好LCP](/assets/images/ai-portfolio/cloudflare-analytics.png)

GitHub: [lzwjava/jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog)

---

## 🎬 FluxReel——AMD黑客马拉松短视频工作室

[FluxReel](https://github.com/lzwjava/flux-reel)将一个单行主题转化为**15秒竖屏短视频**（1080×1920，9:16，30 fps）——在**AMD Radeon GPU（ROCm）** 上运行核心图像生成。为AMD AI DevMaster黑客马拉松2026-07的**赛道1——多模态内容创作工具**而构建。

**工作原理：**

1. **脚本**——LLM从主题起草一篇300-500词的Markdown文章，然后场景规划器生成恰好5个场景，包含`title` / `subtitle` / `image_prompt`（双语，自动从主题检测）。
2. **图像**——并行生成5个场景图像：通过diffusers（FLUX.1-schnell / dev / 2-dev）在AMD GPU上运行，stable-diffusion.cpp（FLUX.1-schnell Q4_0 GGUF，低显存），或OpenRouter。
3. **合成**——PIL构建每个1080×1920的幻灯片，包含标题/副标题栏，字体自动缩小以适应，支持CJK换行。
4. **组装**——ffmpeg将每个幻灯片编码为3秒H.264片段，无需重新编码即可拼接，并混入背景音乐。

**关键特性：**

- **主题→视频只需几分钟**：从提示到精良MP4的完整管道，在AMD上本地运行。
- **双语字幕**——自动检测EN / 中文，使用Noto Sans CJK字体和基于字符的换行。
- **多图像后端**——`local`（ROCm + diffusers FLUX）、`sdcpp`（GGUF 4-bit，低显存）、`openrouter`（云端回退）、`auto`（优先本地，回退云端）。
- **Web UI + REST API**——FastAPI服务器，具有作业队列、进度轮询、视频预览和下载功能。
- **可选YouTube上传**——通过LLM自动生成标题/描述/标签。
- **远程AMD GPU管理**——rc-tunnel、通过`hf-mirror.com`（中国友好）下载FLUX模型、GPU / ROCm / 磁盘信息。

**演示输出帧（1080×1920，9:16）：**

![FluxReel演示帧2——在AMD GPU上生成的15秒竖屏短视频](https://raw.githubusercontent.com/lzwjava/flux-reel/main/submission/demo_frame_2.jpg)

GitHub: [lzwjava/flux-reel](https://github.com/lzwjava/flux-reel)

---

## 🤖 iclaw——终端AI代理（REPL）

[iclaw](https://github.com/lzwjava/iclaw)是一个终端AI代理，能够自主编码、搜索和运行命令——适用于个人机器和受限制的企业机器。一个最小化的openclaw实现，构建为纯Python CLI，无需浏览器扩展或IDE插件，由GitHub Copilot驱动。

```
智维@lzw-mac iclaw % iclaw

  ██  █████  ██       █████  ██   ██
  ██ ██      ██      ██   ██ ██   ██
  ██ ██      ██      ███████ ██ █ ██
  ██ ██      ██      ██   ██ ██████
  ██  █████  ███████ ██   ██  ███ ██

可用命令：
  /provider_model      选择并认证模型提供商
  /model               从您的提供商中选择特定模型
  /search              网络搜索（用法：/search <query>）
  /provider_search     选择网络搜索提供商
  /proxy               设置HTTP/HTTPS代理（用法：/proxy [url|off]）
  /ca_bundle           设置HTTPS的CA捆绑包（用法：/ca_bundle [path|off]）
  /log                 设置日志详细程度（用法：/log [verbose|info]）
  /copy                将最后一次Copilot响应复制到剪贴板
  /read                将文件内容打印到终端（用法：/read <path>）
  /clear               清除对话历史
  /compact             使用LLM压缩对话历史
  /export              将完整对话历史导出到JSON文件
  /status              显示当前设置
  /help                显示可用命令
  /exit                退出REPL。
```

**关键特性：**

- **多轮对话**，在终端中使用GitHub Copilot或OpenRouter。
- **多模型提供商**：GitHub Copilot（OAuth设备流）和OpenRouter（API密钥）。
- **原生工具调用**：模型自主调用网络搜索、执行Shell命令和编辑文件——无需人工干预。
- **多搜索提供商**：DuckDuckGo、Startpage、Bing和Tavily。
- **企业友好**：无需IDE插件或浏览器扩展。在企业防火墙后支持代理和CA捆绑包。
- **默认模型**：GPT-5.2。

![iclaw——带有原生工具调用的终端AI代理REPL](/assets/images/ai-portfolio/iclaw.jpg)

![iclaw——显示自主编码和Shell命令的执行日志](/assets/images/ai-portfolio/iclaw-log.png)

GitHub: [lzwjava/iclaw](https://github.com/lzwjava/iclaw)

---

## ⚙️ zz——数据集处理与训练工具

[zz](https://github.com/lzwjava/zz)是一个用于ML训练管道的工具包——数据集下载、分词、提取和推理工具。在RunPod H200、DigitalOcean H100和家庭RTX 4070上进行GPT-2 124M训练运行期间使用。也托管在[Hugging Face](https://huggingface.co/lzwjava/zz)上。

```
智维@lzw-mac zz % tree -L 1
scripts/
  download/     # 数据集下载脚本（FineWeb, Wikimedia, HF镜像）
  extract/      # 数据提取、分词和重命名
  analysis/     # 训练时长和指标评估
  deepseek/     # LLM推理脚本（DeepSeek-V2-Lite）
logs/           # 训练日志和输出
datasets/       # 下载的数据集存储
```

**关键能力：**

- **FineWeb下载**——规划和下载分片以达到令牌预算（100亿、1000亿+令牌），支持进度跟踪和断点续传。
- **hf-mirror.com支持**——当HuggingFace被屏蔽时，用于中国访问的wget脚本。
- **Parquet提取**——通过pyarrow iter_batches进行内存安全的迭代。
- **分词**——将原始文本转换为训练就绪格式。
- **训练分析**——从训练日志计算时长、评估指标。
- **DeepSeek推理**——DeepSeek-V2-Lite的LLM推理脚本。

![zz在Hugging Face上——数据集处理与训练工具，22次提交，3位贡献者](/assets/images/ai-portfolio/zz-huggingface.png)

GitHub: [lzwjava/zz](https://github.com/lzwjava/zz) · Hugging Face: [lzwjava/zz](https://huggingface.co/lzwjava/zz)

---

## 🎓 证书

### 机器学习专项课程——DeepLearning.AI & 斯坦福大学

2023年11月完成。三门课程：监督式机器学习、高级学习算法、无监督学习、推荐系统、强化学习。

![Coursera机器学习专项课程证书——李智维，2023年11月](/assets/images/ai-portfolio/coursera-ml-1.png)

### 深度学习专项课程——DeepLearning.AI

2023年12月完成。五门课程：神经网络、超参数调优、结构化机器学习项目、卷积神经网络、序列模型。

![Coursera深度学习专项课程证书——李智维，2023年12月](/assets/images/ai-portfolio/coursera-dl-1.png)

---

- GitHub: [https://github.com/lzwjava](https://github.com/lzwjava)
- 博客: [https://lzwjava.github.io](https://lzwjava.github.io)

---

AI翻译提示：British Universal Bank（英国环球银行）。