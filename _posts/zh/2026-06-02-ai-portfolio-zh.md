---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 我的AI作品集——每日AI工作证据
translated: true
---

我不只是谈论AI——我每天都在大规模地使用它。这篇文章是我的AI作品视觉档案：我构建的工具、我消耗的Token，以及我获得的认证。

---

## 🖥️ LLM训练与推理——我的硬件设置

我于2023年搭建了我的机器学习工作站，并从此一直在进行训练和学习。

**硬件经验：**

| GPU | 显存 | 经验时长 | 使用平台 |
| ----- | ------ | ------------ | ------- |
| NVIDIA RTX 4070 | 12 GB | 3年 | 家庭工作站 |
| NVIDIA H200 | 141 GB | 3个月 | RunPod / DigitalOcean |
| AMD MI300X | 192 GB HBM3 | 3个月 | AMD开发者云 |

**我训练过的模型：**

- **GPT-2 124M** 从头开始在FineWeb数据集上训练（nanoGPT）——在RTX 4070、H200和MI300X上。
- **GPT-2 760M** 从头开始在AMD MI300X（192 GB HBM3）上训练——探索nanochat、DeepSeek v4 MoE。
- 各种超参数调优、学习率调度和数据集预处理的实验。

**工作站：**

![我的机器学习学习站——2023年搭建，RTX 4070 12GB，用于日常训练和实验](/assets/images/ai-portfolio/learning-station.jpg)

**AMD开发者云——MI300X 192GB HBM3：**

![AMD开发者云——用于大规模模型训练的MI300X实例](/assets/images/ai-portfolio/amd-dev-cloud.png)

---

## 🔧 GPU拆解——从坏卡上学习硬件知识

从二手市场购买坏掉的GPU（**Quadro 401 / 2000 / 4000**等），拆解它们并研究电路板以了解组件——VRM电路（MOSFET、电感、电容）、内存芯片布局，以及每一代架构（Fermi → …）的不同之处。每一块PCB都是工程决策的蓝图。

![来自二手市场的坏GPU——Quadro拆解收藏](/assets/images/ai-portfolio/gpu-teardown-collection.jpg)

![GPU维修工作台——诊断和修复坏卡](/assets/images/ai-portfolio/gpu-repair.jpg)

---

### 🏋️ 训练运行摘要

| # | 模型 | 框架 | 参数量 | 硬件 | 步骤数 | 状态 |
| --- | ------- | ----------- | -------- | ---------- | ------- | -------- |
| 1 | FineWeb 125M run1 | nanoGPT | 124M | RTX 4070 | 20K | 已完成 |
| 2 | FineWeb 125M run2 | nanoGPT | 124M | RTX 4070 | 6K | 已完成 |
| 3 | FineWeb 125M run3 | nanoGPT | 124M | RTX 4070 | 11K | 已完成 |
| 4 | OpenWebText 125M | nanoGPT | 124M | RTX 4070 | 6K | 已完成 |
| 5 | FineWeb 125M MI300X | nanoGPT | 124M | MI300X | 750 | 冒烟测试 |
| 6 | FineWeb 760M | nanoGPT | 760M | MI300X | 76K/445K | 提前停止 |
| 7 | fineweb-edu-d12 | nanochat | 286M | RTX 4070 | 10K | 基础预训练完成 |
| 8 | rtx4070-d12-chinchilla | nanochat | 286M | RTX 4070 | 87K | **完全完成** |
| 9 | code-sec-fineweb-d12 | nanochat | 286M | H200? | 50K | 已完成 |
| 10 | code-sec-sft | nanochat | ~140M | H200? | 8,985 | 已完成 |
| 11 | codeparrot-d12 | nanochat | 286M | RTX 4070 | ? | 仅脚本 |
| 12 | Notes SFT (Qwen3-4B) | trl/peft | 4B | RTX 4070 | ? | 仅脚本 |
| 13 | SPGISpeech (Whisper) | transformers | 可变 | ? | ? | 仅脚本 |

## 🧠 增强版nanoGPT——我的分支项目

分叉了[karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)，并扩展了额外的数据集管道、扩展训练配置和内联形状注释以方便学习。45次提交，2025年11月至2026年4月。

**新增数据集管道：**

| 数据集 | 路径 | 描述 |
| --------- | ------ | ------------- |
| FineWeb-Edu | `data/fineweb/` | HuggingFace FineWeb-Edu（100亿+ Token）。基于分片加载、分块处理、增量式训练/验证集划分。 |
| OpenWebText 10k | `data/openwebtext_10k/` | 用于快速迭代的10k子集。 |
| Wikipedia Local | `data/wikipedia_local/` | 直接对本地纯文本转储进行分词（无需HuggingFace下载）。 |

**新增训练配置：**

| 配置 | 目标 | 备注 |
| -------- | -------- | ------- |
| `train_fineweb.py` | 125M on FineWeb | 为RTX 4070 12 GB调优（n_embd=384，dropout=0.1）。 |
| `train_fineweb1_5b.py` | 1.5B on FineWeb | 适用于H200 80 GB。 |
| `train_fineweb_gpt3.py` | GPT-3风格的100亿Token | 基于分片的加载器，更宽的调度。 |
| `train_fineweb_760m.py` | 760M on FineWeb | 适用于MI300X 192 GB HBM3。 |
| `train_gpt2_200m.py` | GPT-2 200M | 通用中型配置。 |
| `train_gpt2_200m_smoke.py` | 冒烟测试 | 快速200M完整性检查（约几分钟）。 |

**模型变更：**

- 在整个`model.py`的前向传播（CausalSelfAttention、MLP、GPT）中加入了**内联张量形状注释**——在每一步都显示确切的形状，并附有具体的GPT-2 XL示例，例如`# x: (B, T, C) e.g. (1, 5, 1600)`。有助于理解Transformer数据流。

![增强版nanoGPT——45次提交，数据集管道，扩展训练配置，内联形状注释](/assets/images/ai-portfolio/nanogpt-fork.png)

GitHub: [lzwjava/nanoGPT](https://github.com/lzwjava/nanoGPT)

---

## ⚙️ MoE与LLM推理——刚刚开始学习

在训练了密集GPT-2模型之后，我想了解LLM的架构和系统层面：**混合专家模型（MoE）** 和**推理引擎**。老实说，我才刚刚开始。我读过一些代码，运行过一些东西，并跟着学习过——但我无法从头编写这些代码，我仍然认为自己在这些方面主要是个初学者。

**我开始关注的内容：**

- **MoE架构**——路由+分发+专家计算+合并+负载均衡的高级概念。我粗略阅读过DeepSeek-MoE（细粒度+共享专家）、MegaBlocks（无丢弃块稀疏分发）、Tutel（全到全专家并行）和Mixtral（8×7B，top-2）作为参考实现——主要是让AI代理带我过代码。
- **前向传播**——路由（`router_logits` → `topk(softmax(...))`）、每个专家的计算，以及`token → 专家 → token`如何跨GPU高效进行。我能理解流程，但自己还不能推理其中的权衡。
- **KV缓存分页、预填充/解码调度、连续批处理、CUDA图、前缀缓存、张量并行**——我知道这些名字和大致概念，但服务栈很深，我仅触及表面。

**我的学习方式——使用代理进行探索：**

1. **阅读代码**——我使用编码代理（例如Hermes Agent）来帮助我在mini-sglang中端到端地追踪MoE：`路由器 (LinearReplicated) → MoELayer → FusedMoe (top-k路由 → 块对齐分发 → 2个融合GEMM → sum-reduce) → Triton grouped-GEMM内核`。当代理带我过时我能理解；但我自己还不能复现。
2. **运行并基准测试**——让nano-vLLM在我的RTX 4070上运行Qwen3-0.6B，使用flash-attention：**506 tok/s预填充**，解码约4–30 tok/s，在笔记本基准测试中约1434 tok/s。我把这些当作数据点，而不是任何事情的证明。
3. **从源码编译**——从源码构建了**SGLang**（`pip install -e "python"`，修复了torch/torchaudio CUDA版本不匹配到2.11.0+cu130，编译了它的3个PyO3 Rust扩展），并让一个Qwen2.5-0.5B服务器在`localhost:30010`提供服务并完成。也使用`flash-attn==2.8.3`预构建的wheel让nano-vLLM运行起来。能让东西跑起来是一回事，深刻理解是另一回事。

**我目前所学（仍然很浅）：**

| 概念 | 我的理解 |
| --------- | -------------------------------- |
| **分页KV缓存** | 固定256-token块、空闲列表、内容哈希前缀缓存、写时复制共享——仅限高级概念 |
| **调度器** | 长提示的分块预填充、解码步骤、KV缓存满时的抢占——大致了解 |
| **CUDA图** | 捕获解码批处理（`[1,2,4,…512]`）以减少CPU内核启动开销——动机而非细节 |
| **MoE分发** | `moe_align_block_size`排序+填充每个专家的token块以进行高效的Triton grouped-GEMM——跟着代码过了一次 |
| **张量并行** | 行并行层的`all_reduce`、LM头的`gather`、共享路由器`LinearReplicated`——现在明白了这些名字 |
| **融合MoE内核** | gate/up融合为一个GEMM，拆分SwiGLU激活，路由权重精确应用一次——读过，但记忆不完整 |

**我的方法**——老实说，我的很多“阅读”都是代理阅读代码并给我解释。循环大致是这样的：

```text
阅读 20% → 修改 30% → 搞坏东西 30% → 提交 20%
```

我只接触这个几周。我知道的刚好能跟上关于MoE推理的讨论——但不足以自己构建或改进这些系统。

---

## 📝 SEC-EDGAR-GPT——在SEC文件上从头训练GPT-2（124M）

在**15.5亿Token**的SEC EDGAR财务文件（10-K、10-Q和其他公司披露）上从头训练了一个**1.24亿参数的GPT-2**——在单个**RTX 4070**（12 GB显存）上训练了约8小时，验证损失收敛到2.28。

该模型能生成令人信服的SEC模板文本——风险因素、管理层讨论与分析（MD&A）部分、业务描述——并通过RunPod上的FastAPI服务器部署用于交互式聊天。

整个项目（模型训练、论文、聊天机器人和网站）在**3天内使用Hermes Agent**构建，展示了AI代理如何使LLM研究变得可及。

在银行内部共享后，该项目获得**200多次内部浏览**。一位首席工程师留下评论称其为*“不错”*。此外，受朋友在递归Transformer方面工作的启发，这个项目让我开始思考如何区分对待金融Token和自然语言Token以提高生成精度。

![SEC-EDGAR-GPT聊天机器人](/assets/images/sec-edgar-gpt/chatbot_web.png)

**代码：** [github.com/lzwjava/sec-edgar-gpt](https://github.com/lzwjava/sec-edgar-gpt) · **论文：** [sec-edgar-gpt.pdf](https://github.com/lzwjava/sec-edgar-gpt/raw/main/sec-edgar-gpt.pdf) · **模型：** [Hugging Face](https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf) · **聊天：** [sec-edgar-gpt.lzwjava.workers.dev](https://sec-edgar-gpt.lzwjava.workers.dev/)

---

## 📊 LLM API使用量——数据一览

### OpenRouter——过去一年

消耗了22.8亿Token，花费239美元，跨多个模型发出了15.5万次API请求。

![OpenRouter活动仪表板——过去一年22.8亿Token，239美元花费，15.5万次请求](/assets/images/ai-portfolio/openrouter-activity.png)

### DeepSeek——过去一年

过去一年通过DeepSeek平台消耗了6.29亿Token。

### 通过SSSAICode使用的Claude API——2026年4月

一个月花费171.53美元。2,555次请求。1.15亿+ Token。90.9%缓存命中率。

![SSSAICode Claude使用量——Opus 4.6, Opus 4.7, Sonnet 4.6, Haiku 4.5](/assets/images/ai-portfolio/sssaicode-usage.png)

### 小米MIMO订阅——已使用12.5亿Token

Pro每月计划，包含380亿主配额+87.5亿补偿配额（约46亿免费额度）。**2026年5月至6月期间消耗了12.5亿Token。**

![小米MIMO Pro计划——消耗12.5亿Token，约34亿免费额度剩余](/assets/images/ai-portfolio/xiaomi-mimo-usage.png)

#### 每月Token使用量明细

| 月份 | 模型 | 总Token数 | 输入（缓存命中） | 输入（缓存未命中） | 输出 | 请求数 |
| ------- | ------- | -------------: | -------------------: | --------------------: | -------: | ---------: |
| 2026-06 | mimo-v2.5 | 285,179 | 36,416 | 143,556 | 105,207 | 78 |
| 2026-06 | mimo-v2.5-pro | 734,873,374 | 710,036,672 | 21,617,131 | 3,219,571 | 10,704 |
| 2026-05 | mimo-v2.5 | 91,203 | 5,312 | 52,908 | 32,983 | 27 |
| 2026-05 | mimo-v2.5-pro | 508,851,211 | 488,291,136 | 17,725,731 | 2,834,344 | 8,649 |
| 2026-05 | mimo-v2-pro | 3,571,328 | 3,021,568 | 539,357 | 10,403 | 167 |

**每月总计：** 2026年5月：**5.125亿Token**（8,843次请求）· 2026年6月：**7.352亿Token**（10,782次请求）

> mimo-v2.5-pro占据主导地位（约占总量96%）。mimo-v2.5-pro上的缓存命中率约96.7%，保持了成本效率。6月Token量较5月增长43.5%。

### 摘要

| 平台 | Token数 | 周期 | 成本 |
| ---------- | -------- | -------- | ------ |
| OpenRouter | 22.8亿 | 过去一年 | 239美元 |
| DeepSeek | 6.29亿 | 过去一年 | — |
| SSSAICode (Claude) | 1.15亿+ | 2026年4月 | 171.53美元 |
| 小米MIMO | 12.5亿 | 2026年5-6月 | 46亿免费额度 |
| 其他 (GitHub Copilot等) | 7.26亿 | 过去一年 | — |
| **总计** | **约50亿** | **过去一年** | **—** |

---

## 🏢 企业AI应用——在一家英国环球银行

在一家英国环球银行（通过一家全球IT外包公司），我在一个编码助手之上构建了一个自主AI代理层，用于自动化脚本编写、日志记录、文档生成和测试。

**我构建的内容：**

- **20个定制化AI代理**——为不同的技术栈和工作流程配备了专门的提示和上下文。
- **400个可复用的编码助手编写的脚本**——跨Java、Spring、Python、Angular和DevOps工具的常见任务自动化。
- **1,800份编码助手编写的指南**——由AI在人类提示下生成的文档。
- **通过编码助手API自动生成约70个测试用例**——涵盖Spring过滤器、Python unittest、JSON截断、提示工程和区域端点。

**成果：**

- 在企业范围内，按高级请求衡量，编码助手使用率排名**前6%**。
- 因备受瞩目的AIPlayer项目获得**贡献奖**。
- 加入了银行的内部AI社区。

![AIPlayer贡献奖](/assets/images/ai-portfolio/aiplayer.jpg)

---

## 🎤 AI演讲——从神经网络到智能体

在一家英国环球银行向**80位参与者**进行了技术演讲——包括高级顾问、专家、副总监、软件工程师和合同工。

**演讲：** *“从神经网络到智能体”*——从最简单的神经网络（`y = wx`）出发，历经MNIST、Transformer、GPT、nanoGPT，直至构建个人AI代理。

**我涵盖的内容：**

- 从基本原理出发的神经网络——前向传播、反向传播、梯度下降
- Transformer架构——Q/K/V注意力、多头注意力、位置编码
- GPT内部机制——分词、嵌入、训练、生成
- nanoGPT——在H200/RTX 4070上从头训练GPT-2
- LLM代理——Claude Code、OpenClaw、Hermes、工具调用、代理循环
- 真实数据——消耗10亿Token，H200每小时3.44美元，钱花在了哪里
- 我的路径——从阅读Q/K/V到从头训练模型，用了3年

**反馈：**

- 一位初级工程师说：*“你就是我想成为的人”*——这次演讲开阔了他对AI可能性的视野
- 高级工程师赞赏这种从基本原理出发的方法——没有炒作，只有数学和代码
- 多次关于训练、代理和职业方向的后续讨论

**幻灯片：** 使用Claude Code和Marp，基于我的公开AI回答笔记构建。

幻灯片（Marp格式）：[PDF](/assets/marp/neural_networks_to_agents_public.pdf)

---

## 🛠️ ww——跨平台CLI工具箱

[ww](https://github.com/lzwjava/ww) 是我的旗舰CLI工具箱——255+次提交，10+个命令组，跨平台（macOS + Linux）。涵盖带有AI提交信息的git工作流、笔记管理、图片/PDF处理、网页搜索、GitHub Copilot聊天、系统工具和LLM驱动的助手。

```
lzwjava@lzw-mac ww % uv run ww --help
用法: ww <group> [command] [options]

Action:
  ww action [workflow.yml]  触发一个GitHub Actions工作流

AMD Dev Cloud:
  ww amd-dev-cloud snapshots    列出快照
  ww amd-dev-cloud start-train  创建GPU实例用于训练
  ww amd-dev-cloud end-train    对GPU实例进行快照并销毁

Copilot:
  ww copilot auth           通过GitHub OAuth进行身份验证
  ww copilot chat           与Copilot模型聊天

Git:
  ww git gpa            对所有仓库执行Git pull --all
  ww git squash <n>     压缩最近n次提交
  ww git amend-push     修改最后一次提交并强制推送

LLM:
  ww llm compare <prompt>   比较多个LLM响应
  ww llm query <question>   查询本地RAG文档

Note:
  ww note              剪贴板内容快速记笔记
  ww note process      处理笔记队列
  ww note watch        自动处理守护进程

Screenshot:
  ww screenshot               截屏并创建笔记
  ww screenshot interact-note 交互式截屏笔记

255+次提交。10+个命令组。跨平台 (macOS + Linux)。
```

![ww——GitHub上的跨平台CLI工具箱](/assets/images/ai-portfolio/ww1.png)

GitHub: [lzwjava/ww](https://github.com/lzwjava/ww)

---

## 📝 jekyll-ai-blog——AI驱动的博客平台

[jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog) 是 [lzwjava.github.io](https://lzwjava.github.io) 的源代码——一个通过AI自动化增强的Jekyll博客。超过10,000篇英文文章，超过10,000篇中文文章，超过9,700条AI回答笔记。过去一个月约70,000次页面浏览（Cloudflare分析）。

```
lzwjava@lzw-mac jekyll-ai-blog % ls README.md
README.md
```

**它与标准Jekyll博客的不同之处：**

- **AI驱动的翻译**——基于LLM的翻译管道通过GitHub Actions自动将每篇文章扩展到多种语言。
- **Google Cloud Text-to-Speech**——自动生成文章的音频版本以提高可访问性。
- **XeLaTeX PDF/EPUB生成**——从Markdown源文件生成高质量、可打印的PDF和电子书导出。
- **GitHub Actions CI/CD**——自动化构建、测试、翻译和部署工作流。
- **8,000+条AI回答笔记**——基于日常LLM辅助研究构建的知识库，可在博客上搜索。
- **MathJax、夜间模式、RSS、双语内容**——通过自定义CSS和主题增强的标准功能。

**规模：**

| 指标 | 数量 |
| -------- | ------- |
| 英文文章 | 10,264 |
| 中文文章 | 10,259 |
| AI回答笔记 | 9,794 |
| Python脚本 | 323 |
| 机器学习脚本 | 191 |
| 页面浏览量（过去一个月） | 约70,000 |

![jekyll-ai-blog——拥有10K+文章、翻译、TTS和PDF管道的AI驱动博客](/assets/images/ai-portfolio/blog.png)

![Cloudflare Web分析——38.9K访问量，45.2K页面浏览量，930ms加载时间，82%良好LCP](/assets/images/ai-portfolio/cloudflare-analytics.png)

GitHub: [lzwjava/jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog)

---

## 🎬 FluxReel——AMD黑客马拉松短视频工作室

[FluxReel](https://github.com/lzwjava/flux-reel) 可将一行主题转换为**15秒的垂直短视频**（1080×1920，9:16，30 fps）——核心图像生成运行在**AMD Radeon GPU（ROCm）** 上。为AMD AI DevMaster黑客马拉松2026年7月的**第一赛道——多模态内容创作工具**而构建。

**工作原理：**

1. **脚本**——LLM根据主题起草一份300–500词的Markdown文章，然后场景规划器精确生成5个场景，每个场景包含`title` / `subtitle` / `image_prompt`（双语，根据主题自动检测）。
2. **图像**——并行生成5个场景图像：通过diffusers（FLUX.1-schnell / dev / 2-dev）在AMD GPU上生成，或通过stable-diffusion.cpp（FLUX.1-schnell Q4_0 GGUF，低显存），或通过OpenRouter。
3. **合成**——PIL（Python Imaging Library）构建每个1080×1920的幻灯片，包含标题/副标题栏，字体自动缩小以适应，支持CJK（中日韩）文字换行。
4. **组装**——ffmpeg将每个幻灯片编码为3秒的H.264片段，无需重新编码即可拼接，并混合背景音乐。

**关键特性：**

- **主题到视频只需几分钟**：从提示到精美的MP4的完整管道，在本地AMD上运行。
- **双语字幕**——使用Noto Sans CJK字体和基于字符的换行自动检测英文/中文。
- **多种图像后端**——`local`（ROCm + diffusers FLUX）、`sdcpp`（GGUF 4-bit，低显存）、`openrouter`（云端备用）、`auto`（优先本地，回退至云端）。
- **Web UI + REST API**——FastAPI服务器，带有任务队列、进度轮询、视频预览和下载功能。
- **可选的YouTube上传**——通过LLM自动生成标题/描述/标签。
- **远程AMD GPU管理**——rc-tunnel，通过`hf-mirror.com`（适合中国用户）下载FLUX模型，GPU / ROCm / 磁盘信息。

**演示输出帧（1080×1920，9:16）：**

![FluxReel演示帧2——在AMD GPU上生成的15秒垂直短视频](https://raw.githubusercontent.com/lzwjava/flux-reel/main/submission/demo_frame_2.jpg)

**🏆 AMD AI DevMaster黑客马拉松——完成奖**（0121 Zhiwei Li）：

![AMD AI DevMaster黑客马拉松完成奖——FluxReel](/assets/images/ai-portfolio/fluxreel-award.png)

GitHub: [lzwjava/flux-reel](https://github.com/lzwjava/flux-reel)

---

## 🤖 iclaw——终端AI代理（REPL）

[iclaw](https://github.com/lzwjava/iclaw) 是一个可以自主编码、搜索和运行命令的终端AI代理——既能在个人机器上工作，也能在受限制的企业机器上工作。一个极简的openclaw实现，构建为纯Python CLI，无需浏览器扩展或IDE插件，由GitHub Copilot驱动。

```
lzwjava@lzw-mac iclaw % iclaw

  ██  █████  ██       █████  ██   ██
  ██ ██      ██      ██   ██ ██   ██
  ██ ██      ██      ███████ ██ █ ██
  ██ ██      ██      ██   ██ ██████
  ██  █████  ███████ ██   ██  ███ ██

可用命令：
  /provider_model      选择并验证模型提供商
  /model               从您的提供商处选择特定模型
  /search              网页搜索（用法：/search <query>）
  /provider_search     选择网页搜索提供商
  /proxy               设置HTTP/HTTPS代理（用法：/proxy [url|off]）
  /ca_bundle           设置HTTPS的CA证书包（用法：/ca_bundle [path|off]）
  /log                 设置日志详细程度（用法：/log [verbose|info]）
  /copy                复制上一条Copilot响应到剪贴板
  /read                将文件内容打印到终端（用法：/read <path>）
  /clear               清除对话历史
  /compact             使用LLM压缩对话历史
  /export              将完整对话历史导出为JSON文件
  /status              显示当前设置
  /help                显示可用命令
  /exit                退出REPL。
```

**关键特性：**

- **多轮对话**，在终端中使用GitHub Copilot或OpenRouter。
- **多个模型提供商**：GitHub Copilot（OAuth设备流）和OpenRouter（API密钥）。
- **原生工具调用**：模型自主调用网页搜索、执行Shell命令和编辑文件——无需人工介入。
- **多个搜索提供商**：DuckDuckGo、Startpage、Bing和Tavily。
- **企业友好**：无需IDE插件或浏览器扩展。支持在公司防火墙后使用代理和CA证书包。
- **默认模型**：GPT-5.2。

![iclaw——带有原生工具调用的终端AI代理REPL](/assets/images/ai-portfolio/iclaw.jpg)

![iclaw——显示自主编码和Shell命令的执行日志](/assets/images/ai-portfolio/iclaw-log.png)

GitHub: [lzwjava/iclaw](https://github.com/lzwjava/iclaw)

---

## ⚙️ zz——数据集处理与训练工具

[zz](https://github.com/lzwjava/zz) 是一个用于ML训练管道的工具箱——包含数据集下载、分词、提取和推理工具。在GPT-2 124M训练运行期间使用，涉及平台包括RunPod H200、DigitalOcean H100和家庭RTX 4070。也托管在[Hugging Face](https://huggingface.co/lzwjava/zz)上。

```
lzwjava@lzw-mac zz % tree -L 1
scripts/
  download/     # 数据集下载脚本 (FineWeb, Wikimedia, HF mirrors)
  extract/      # 数据提取、分词和重命名
  analysis/     # 训练时长和指标评估
  deepseek/     # LLM推理脚本 (DeepSeek-V2-Lite)
logs/           # 训练日志和输出
datasets/       # 已下载的数据集存储
```

**关键能力：**

- **FineWeb下载**——规划并下载分片以达到Token预算（100亿、1000亿+ Token），支持带进度跟踪的断点续传。
- **支持hf-mirror.com**——当HuggingFace被屏蔽时，使用wget脚本通过中国镜像站访问。
- **Parquet提取**——通过pyarrow的iter_batches实现内存安全的迭代。
- **分词**——将原始文本转换为训练就绪格式。
- **训练分析**——从训练日志计算时长和评估指标。
- **DeepSeek推理**——适用于DeepSeek-V2-Lite的LLM推理脚本。

![zz在Hugging Face上——数据集处理与训练工具，22次提交，3位贡献者](/assets/images/ai-portfolio/zz-huggingface.png)

GitHub: [lzwjava/zz](https://github.com/lzwjava/zz) · Hugging Face: [lzwjava/zz](https://huggingface.co/lzwjava/zz)

---

## 🎓 证书

### 机器学习专项课程 — DeepLearning.AI 与斯坦福大学

2023年11月完成。三门课程：监督式机器学习、高级学习算法、无监督学习、推荐系统、强化学习。

![Coursera机器学习专项课程证书——李智维，2023年11月](/assets/images/ai-portfolio/coursera-ml-1.png)

### 深度学习专项课程 — DeepLearning.AI

2023年12月完成。五门课程：神经网络、超参数调优、构建机器学习项目、卷积神经网络、序列模型。

![Coursera深度学习专项课程证书——李智维，2023年12月](/assets/images/ai-portfolio/coursera-dl-1.png)

---

- GitHub: [https://github.com/lzwjava](https://github.com/lzwjava)
- 博客: [https://lzwjava.github.io](https://lzwjava.github.io)

---