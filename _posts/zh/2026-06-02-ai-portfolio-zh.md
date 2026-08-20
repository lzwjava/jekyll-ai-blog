---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 我的AI作品集——每日AI工作的证据
translated: true
---

我不只是谈论人工智能——我每天都在大规模使用它。这篇文章是我的AI工作视觉作品集：我构建的工具、消耗的token，以及获得的认证。

---

## 🖥️ LLM训练与推理——我的硬件配置

我在2023年搭建了自己的机器学习工作站，从此一直在训练和学习。

**硬件经验：**

| GPU | 显存 | 经验时长 | 使用场景 |
| ----- | ------ | ------------ | ------- |
| NVIDIA RTX 4070 | 12 GB | 3年 | 家庭工作站 |
| NVIDIA H200 | 141 GB | 3个月 | RunPod / DigitalOcean |
| AMD MI300X | 192 GB HBM3 | 3个月 | AMD 开发者云 |

**我训练过的模型：**

- **GPT-2 124M** —— 从零开始在FineWeb数据集上训练（nanoGPT）—— 在RTX 4070、H200和MI300X上完成。
- **GPT-2 760M** —— 从零开始在AMD MI300X（192 GB HBM3）上训练—— 探索nanochat、DeepSeek v4 MoE。
- 各种超参数调优、学习率调度和数据集预处理的实验。

**工作站：**

![我的ML学习站——2023年搭建，RTX 4070 12GB，用于日常训练和实验](/assets/images/ai-portfolio/learning-station.jpg)

**AMD 开发者云——MI300X 192GB HBM3：**

![AMD 开发者云——MI300X实例用于大规模模型训练](/assets/images/ai-portfolio/amd-dev-cloud.png)

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

Fork了[karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)并进行了扩展，增加了额外的数据集流水线、规模化训练配置以及用于学习的内联形状注释。45次提交，2025年11月至2026年4月。

**新增数据集流水线：**

| 数据集 | 路径 | 描述 |
| --------- | ------ | ------------- |
| FineWeb-Edu | `data/fineweb/` | HuggingFace FineWeb-Edu（100亿+ token）。基于分片的加载、分块处理、增量式训练/验证拆分。 |
| OpenWebText 10k | `data/openwebtext_10k/` | 快速10k子集用于快速迭代。 |
| Wikipedia Local | `data/wikipedia_local/` | 直接对本地纯文本转储进行分词（无需HuggingFace下载）。 |

**新增训练配置：**

| 配置 | 目标 | 说明 |
| -------- | -------- | ------- |
| `train_fineweb.py` | 125M on FineWeb | 针对RTX 4070 12 GB调优（n_embd=384, dropout=0.1）。 |
| `train_fineweb1_5b.py` | 1.5B on FineWeb | 用于H200 80 GB。 |
| `train_fineweb_gpt3.py` | GPT-3风格 100亿 token | 基于分片的加载器，更宽的调度。 |
| `train_fineweb_760m.py` | 760M on FineWeb | 用于MI300X 192 GB HBM3。 |
| `train_gpt2_200m.py` | GPT-2 200M | 通用中型配置。 |
| `train_gpt2_200m_smoke.py` | 烟雾测试 | 快速200M健全性检查（约几分钟）。 |

**模型改动：**

- 在 `model.py` 的前向传播中全面添加**内联张量形状注释**（CausalSelfAttention、MLP、GPT）—— 以具体GPT-2 XL示例展示每一步的精确形状，例如 `# x: (B, T, C) e.g. (1, 5, 1600)`。有助于理解Transformer数据流。

![增强版nanoGPT——45次提交，数据集流水线，规模化训练配置，内联形状注释](/assets/images/ai-portfolio/nanogpt-fork.png)

GitHub: [lzwjava/nanoGPT](https://github.com/lzwjava/nanoGPT)

---

## ⚙️ MoE与LLM推理——刚刚开始学习

在训练了密集GPT-2模型之后，我想了解LLM的架构和系统层面：**混合专家模型（MoE）**和**推理引擎**。老实说，我在这方面刚刚起步。我读过一些代码，运行过一些东西，跟着走过一遍——但我无法从零写出任何这样的代码，我仍然认为自己在这方面基本上是个初学者。

**我开始关注的内容：**

- **MoE架构**——路由、分发、专家计算、合并、负载均衡的高层次图景。我粗略浏览了DeepSeek-MoE（细粒度+共享专家）、MegaBlocks（无丢弃块稀疏分发）、Tutel（全到全专家并行）和Mixtral（8×7B，top-2）作为参考实现——主要是通过AI代理带我阅读代码。
- **前向传播**——路由（`router_logits` → `topk(softmax(...))`）、每个专家的计算，以及如何使`tokens → experts → tokens`在GPU间快速进行。我能跟上流程，但自己还无法权衡利弊。
- **KV缓存分页、prefill/decode调度、连续批处理、CUDA图、前缀缓存、张量并行**——我知道这些名称和大体概念，但服务栈很深，我只触及了表面。

**我的学习方式——使用代理进行探索：**

1. **阅读代码**——我使用编码代理（例如Hermes Agent）帮助我在mini-sglang中端到端地追踪MoE：`router (LinearReplicated) → MoELayer → FusedMoe (top-k routing → block-aligned dispatch → 2 fused GEMMs → sum-reduce) → Triton grouped-GEMM kernel`。当代理带我走过时我能理解；但还不能独立重现。
2. **运行并基准测试**——让nano-vLLM在我的RTX 4070上运行Qwen3-0.6B，使用flash-attention：**506 tok/s prefill**，解码约4–30 tok/s，在笔记本基准测试中约1434 tok/s。我把这些当作数据点，而不是任何证明。
3. **从源码编译**——从源码构建了**SGLang**（`pip install -e "python"`，修复了torch/torchaudio CUDA不匹配问题至2.11.0+cu130，编译了它的3个PyO3 Rust扩展），并在`localhost:30010`运行了Qwen2.5-0.5B服务器提供completions。还使用`flash-attn==2.8.3`预编译wheel运行了nano-vLLM。让东西能构建是一回事，深入理解是另一回事。

**我目前学到的东西（仍然很浅）：**

| 概念 | 我理解的内容 |
| --------- | -------------------------------- |
| **分页KV缓存** | 固定256 token块、空闲列表、内容哈希前缀缓存、写时复制共享——仅高层次概念 |
| **调度器** | 长提示的分块prefill、解码步进、KV缓存满时的抢占——大致了解 |
| **CUDA图** | 捕获解码批次（`[1,2,4,…512]`）以减少CPU内核启动开销——动机，而非细节 |
| **MoE分发** | `moe_align_block_size`排序+填充每个专家的token块以实现高效Triton grouped-GEMM——跟着代码走过一次 |
| **张量并行** | 行并行层的`all_reduce`、LM头的`gather`、`LinearReplicated`共享路由——现在能理解这些名称 |
| **融合MoE内核** | gate/up融合为一个GEMM、SwiGLU激活拆分、路由权重仅应用一次——读过，记忆不完整 |

**我的处理方式**——老实说，我的很多“阅读”是代理读代码并解释给我听。循环大致是：

```text
读20% → 改30% → 搞砸30% → 提交20%
```

我只做了几周。我知道的刚好能跟上关于MoE推理的对话——还不足以自己构建或改进这样的系统。

---

## 📝 SEC-EDGAR-GPT——从零在SEC文件上训练的GPT-2（124M）

从零训练了一个**1.24亿参数的GPT-2**，使用**15.5亿token**的SEC EDGAR财务文件（10-K、10-Q及其他公司披露文件）——在单个**RTX 4070**（12 GB显存）上训练了约8小时，验证损失收敛至2.28。

该模型能生成令人信服的SEC套话——风险因素、MD&A章节、业务描述——并通过RunPod上的FastAPI服务器以交互式聊天方式部署。

整个项目——模型训练、论文、聊天机器人和网站——在**3天内使用Hermes Agent**完成，展示了AI代理如何让LLM研究变得可及。

在环球银行内部共享后，该项目获得了**200多次内部浏览**。一位首席工程师评论说“不错”。此外，受朋友在循环变换器方面工作的启发，这个项目让我思考如何区别对待金融token和自然语言token，以提高生成准确性。

![SEC-EDGAR-GPT聊天机器人](/assets/images/sec-edgar-gpt/chatbot_web.png)

**代码：**[github.com/lzwjava/sec-edgar-gpt](https://github.com/lzwjava/sec-edgar-gpt) · **论文：**[sec-edgar-gpt.pdf](https://github.com/lzwjava/sec-edgar-gpt/raw/main/sec-edgar-gpt.pdf) · **模型：**[Hugging Face](https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf) · **聊天：**[sec-edgar-gpt.lzwjava.workers.dev](https://sec-edgar-gpt.lzwjava.workers.dev/)

---

## 📊 LLM API使用量——数字说话

### OpenRouter——过去一年

消耗22.8亿token，花费239美元，15.5万次API请求，涵盖多个模型。

![OpenRouter活动仪表盘——22.8亿token，239美元，15.5万次请求，1年期间](/assets/images/ai-portfolio/openrouter-activity.png)

### DeepSeek——过去一年

通过DeepSeek平台在过去一年消耗了6.29亿token。

### 通过SSSAICode使用Claude API——2026年4月

一个月内171.53美元。2,555次请求。1.15亿+ token。90.9%缓存命中率。

![SSSAICode Claude使用量——Opus 4.6, Opus 4.7, Sonnet 4.6, Haiku 4.5](/assets/images/ai-portfolio/sssaicode-usage.png)

### 小米MIMO订阅——已使用12.5亿token

专业月付计划，38亿主配额+87.5亿补偿配额（约46亿免费额度）。**2026年5月–6月期间消耗12.5亿token**。

![小米MIMO专业版——消耗12.5亿token，剩余约34亿免费额度](/assets/images/ai-portfolio/xiaomi-mimo-usage.png)

#### 月度Token使用量明细

| 月份 | 模型 | 总Token | 输入（缓存命中） | 输入（缓存未命中） | 输出 | 请求数 |
| ------- | ------- | -------------: | -------------------: | --------------------: | -------: | ---------: |
| 2026-06 | mimo-v2.5 | 285,179 | 36,416 | 143,556 | 105,207 | 78 |
| 2026-06 | mimo-v2.5-pro | 734,873,374 | 710,036,672 | 21,617,131 | 3,219,571 | 10,704 |
| 2026-05 | mimo-v2.5 | 91,203 | 5,312 | 52,908 | 32,983 | 27 |
| 2026-05 | mimo-v2.5-pro | 508,851,211 | 488,291,136 | 17,725,731 | 2,834,344 | 8,649 |
| 2026-05 | mimo-v2-pro | 3,571,328 | 3,021,568 | 539,357 | 10,403 | 167 |

**月度总计：** 2026年5月：**5.125亿token**（8,843次请求）· 2026年6月：**7.352亿token**（10,782次请求）

> mimo-v2.5-pro占主导（约总量96%）。mimo-v2.5-pro缓存命中率约96.7%，保持成本高效。6月token量较5月增长43.5%。

### 总结

| 平台 | Token | 时间段 | 花费 |
| ---------- | -------- | -------- | ------ |
| OpenRouter | 22.8亿 | 过去一年 | 239美元 |
| DeepSeek | 6.29亿 | 过去一年 | — |
| SSSAICode (Claude) | 1.15亿+ | 2026年4月 | 171.53美元 |
| 小米MIMO | 12.5亿 | 2026年5–6月 | 免费46亿额度 |
| 其他（GitHub Copilot等） | 7.26亿 | 过去一年 | — |
| **总计** | **约50亿** | **过去一年** | **—** |

---

## 🏢 企业AI应用——在环球银行

在一家英国环球银行（通过一家全球IT外包公司），我在编码助手之上构建了一个自治AI代理层，用于自动化脚本编写、日志记录、文档和测试。

**我构建的内容：**

- **20个定制化AI代理**——针对不同技术栈和工作流程的专用提示词和上下文。
- **400个可复用的编码助手编写脚本**——涵盖Java、Spring、Python、Angular和DevOps工具的常见任务自动化。
- **1,800份编码助手编写的指南**——由人类提示、AI生成的文档。
- **约70个自动生成的测试用例**——通过编码助手API生成，涵盖Spring过滤器、Python unittest、JSON截断、提示工程和区域端点。

**成果：**

- 在整个企业中，编码助手使用量排名**前6%**（按高级请求衡量）。
- 因高关注度的AIPlayer项目获得**贡献奖**。
- 加入银行内部AI社区。

![AIPlayer贡献奖](/assets/images/ai-portfolio/aiplayer.jpg)

---

## 🎤 AI演讲——从神经网络到智能体

在一家英国环球银行面向**80名参与者**进行了一场技术演讲——包括高级顾问、专家、副总监、软件工程师和合同工。

**演讲标题：**《从神经网络到智能体》——从最简单的神经网络（`y = wx`）出发，经过MNIST、Transformer、GPT、nanoGPT，一直到构建个人AI智能体。

**我涵盖的内容：**

- 神经网络基本原理——前向传播、反向传播、梯度下降
- Transformer架构——Q/K/V注意力、多头注意力、位置编码
- GPT内部机制——分词、嵌入、训练、生成
- nanoGPT——从零在H200/RTX 4070上训练GPT-2
- LLM智能体——Claude Code、OpenClaw、Hermes、工具调用、智能体循环
- 真实数字——10亿token消耗、H200每小时3.44美元、钱到底花在哪里
- 我的路径——从阅读Q/K/V到从零训练模型，历时3年

**反馈：**

- 一位初级工程师说：“你就是我想成为的人”——这次演讲让他看到了AI的可能性
- 高级工程师欣赏这种从基本原理出发的方式——没有炒作，只有数学和代码
- 多次后续对话关于训练、智能体和职业方向

**幻灯片：** 使用Claude Code和Marp，基于我的公开AI回答笔记制作。

幻灯片（Marp）：[PDF](/assets/marp/neural_networks_to_agents_public.pdf)

---

## 🛠️ ww——跨平台CLI工具包

[ww](https://github.com/lzwjava/ww) 是我的旗舰CLI工具包——255+次提交，10+个命令组，跨平台（macOS + Linux）。涵盖带有AI提交信息的git工作流、笔记管理、图像/PDF处理、网络搜索、GitHub Copilot聊天、系统工具和LLM辅助功能。

```
lzwjava@lzw-mac ww % uv run ww --help
用法: ww <group> [command] [options]

Action:
  ww action [workflow.yml]  触发GitHub Actions工作流

AMD Dev Cloud:
  ww amd-dev-cloud snapshots    列出快照
  ww amd-dev-cloud start-train  创建用于训练的GPU droplet
  ww amd-dev-cloud end-train    快照并销毁GPU droplet

Copilot:
  ww copilot auth           通过GitHub OAuth认证
  ww copilot chat           与Copilot模型聊天

Git:
  ww git gpa            对所有仓库执行git pull --all
  ww git squash <n>     压缩最近n个提交
  ww git amend-push     修改最后一次提交并强制推送

LLM:
  ww llm compare <prompt>   比较多个LLM响应
  ww llm query <question>   查询本地RAG文档

Note:
  ww note              剪贴板到笔记（快速捕获）
  ww note process      清空笔记队列
  ww note watch        自动处理守护进程

Screenshot:
  ww screenshot              捕获并创建笔记
  ww screenshot interact-note  交互式截图笔记

255+提交。10+命令组。跨平台（macOS + Linux）。
```

![ww——跨平台CLI工具包在GitHub上](/assets/images/ai-portfolio/ww1.png)

GitHub: [lzwjava/ww](https://github.com/lzwjava/ww)

---

## 📝 jekyll-ai-blog——AI驱动的博客平台

[jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog) 是[lzwjava.github.io](https://lzwjava.github.io)的源码——一个由AI自动化增强的Jekyll博客。超过10,000篇英文文章，超过10,000篇中文文章，超过9,700条AI回答笔记。过去一个月约70,000页面浏览量（Cloudflare Analytics）。

```
lzwjava@lzw-mac jekyll-ai-blog % ls README.md
README.md
```

**与标准Jekyll博客的不同之处：**

- **AI驱动的翻译**——基于LLM的翻译流水线通过GitHub Actions自动将每篇文章扩展到多种语言。
- **Google Cloud Text-to-Speech**——自动生成文章的音频版本，便于无障碍访问。
- **XeLaTeX PDF/EPUB生成**——从Markdown源码生成高质量的可打印PDF和电子书导出。
- **GitHub Actions CI/CD**——自动化构建、测试、翻译和部署工作流。
- **8,000+ AI回答笔记**——通过日常LLM辅助研究构建的知识库，可在博客中搜索。
- **MathJax、夜间模式、RSS、双语内容**——通过自定义CSS和主题增强的标准功能。

**规模：**

| 指标 | 数量 |
| -------- | ------- |
| 英文文章 | 10,264 |
| 中文文章 | 10,259 |
| AI回答笔记 | 9,794 |
| Python脚本 | 323 |
| ML脚本 | 191 |
| 页面浏览量（过去一个月） | ~70,000 |

![jekyll-ai-blog——AI驱动的博客，10K+文章，翻译，TTS和PDF流水线](/assets/images/ai-portfolio/blog.png)

![Cloudflare Web Analytics——38.9K次访问，45.2K页面浏览量，930ms加载时间，82%良好LCP](/assets/images/ai-portfolio/cloudflare-analytics.png)

GitHub: [lzwjava/jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog)

---

## 🎬 FluxReel——AMD黑客马拉松短视频工作室

[FluxReel](https://github.com/lzwjava/flux-reel) 将一行主题转化为**15秒竖屏短视频**（1080×1920，9:16，30 fps）——核心图像生成运行在**AMD Radeon GPU（ROCm）**上。为AMD AI DevMaster黑客马拉松2026年7月**赛道1——多模态内容创作工具**而构建。

**工作原理：**

1. **剧本**——LLM根据主题起草一篇300–500词的markdown文章，然后场景规划器精确生成5个场景，包含`title` / `subtitle` / `image_prompt`（双语，自动根据主题检测）。
2. **图像**——5个场景图像并行生成：通过diffusers（FLUX.1-schnell / dev / 2-dev）在AMD GPU上生成，或使用stable-diffusion.cpp（FLUX.1-schnell Q4_0 GGUF，低显存），或OpenRouter。
3. **合成**——PIL构建每个1080×1920幻灯片，包含标题/副标题栏，字体自动缩小以适应，支持CJK换行。
4. **组装**——ffmpeg将每个幻灯片编码为3秒H.264片段，无需重新编码即可拼接，并混入背景音乐。

**主要特点：**

- **主题到视频只需几分钟**：从提示到精修MP4的完整流水线，在AMD上本地运行。
- **双语字幕**——自动检测EN/中文，使用Noto Sans CJK字体和基于字符的换行。
- **多个图像后端**——`local`（ROCm + diffusers FLUX）、`sdcpp`（GGUF 4-bit，低显存）、`openrouter`（云备选）、`auto`（优先本地，失败后切换到云）。
- **Web UI + REST API**——FastAPI服务器，带有任务队列、进度轮询、视频预览和下载。
- **可选YouTube上传**——通过LLM自动生成标题/描述/标签。
- **远程AMD GPU管理**——rc-tunnel、通过`hf-mirror.com`下载FLUX模型（中国友好）、GPU/ROCm/磁盘信息。

**演示输出帧（1080×1920，9:16）：**

![FluxReel演示帧2——在AMD GPU上生成的15秒竖屏短视频](https://raw.githubusercontent.com/lzwjava/flux-reel/main/submission/demo_frame_2.jpg)

GitHub: [lzwjava/flux-reel](https://github.com/lzwjava/flux-reel)

---

## 🤖 iclaw——终端AI代理（REPL）

[iclaw](https://github.com/lzwjava/iclaw) 是一个终端AI代理，能够自主编码、搜索和运行命令——可在个人机器和受限制的企业机器上工作。一个极简的openclaw实现，作为纯Python CLI构建，无需浏览器扩展或IDE插件，由GitHub Copilot驱动。

```
lzwjava@lzw-mac iclaw % iclaw

  ██  █████  ██       █████  ██   ██
  ██ ██      ██      ██   ██ ██   ██
  ██ ██      ██      ███████ ██ █ ██
  ██ ██      ██      ██   ██ ██████
  ██  █████  ███████ ██   ██  ███ ██

可用命令:
  /provider_model      选择并认证模型提供商
  /model               从提供商中选择特定模型
  /search              网络搜索（用法: /search <query>）
  /provider_search     选择网络搜索提供商
  /proxy               设置HTTP/HTTPS代理（用法: /proxy [url|off]）
  /ca_bundle           设置HTTPS的CA包（用法: /ca_bundle [path|off]）
  /log                 设置日志详细程度（用法: /log [verbose|info]）
  /copy                复制上一个Copilot响应到剪贴板
  /read                将文件内容打印到终端（用法: /read <path>）
  /clear               清除对话历史
  /compact             使用LLM压缩对话历史
  /export              将完整对话历史导出为JSON文件
  /status              显示当前设置
  /help                显示可用命令
  /exit                退出REPL。
```

**主要特点：**

- **多轮对话**——在终端中使用GitHub Copilot或OpenRouter。
- **多个模型提供商**：GitHub Copilot（OAuth设备流）和OpenRouter（API密钥）。
- **原生工具调用**：模型自主调用网络搜索、执行shell命令和编辑文件——无需人工介入。
- **多个搜索提供商**：DuckDuckGo、Startpage、Bing和Tavily。
- **企业友好**：无需IDE插件或浏览器扩展。支持代理和CA包，可在企业防火墙后工作。
- **默认模型**：GPT-5.2。

![iclaw——带有原生工具调用的终端AI代理REPL](/assets/images/ai-portfolio/iclaw.jpg)

![iclaw——显示自主编码和shell命令的执行日志](/assets/images/ai-portfolio/iclaw-log.png)

GitHub: [lzwjava/iclaw](https://github.com/lzwjava/iclaw)

---

## ⚙️ zz——数据集处理与训练工具

[zz](https://github.com/lzwjava/zz) 是一个用于ML训练流水线的工具包——数据集下载、分词、提取和推理工具。在RunPod H200、DigitalOcean H100和家庭RTX 4070上的GPT-2 124M训练运行期间使用。也托管在[Hugging Face](https://huggingface.co/lzwjava/zz)上。

```
lzwjava@lzw-mac zz % tree -L 1
scripts/
  download/     # 数据集下载脚本 (FineWeb, Wikimedia, HF镜像)
  extract/      # 数据提取、分词和重命名
  analysis/     # 训练时长和指标评估
  deepseek/     # LLM推理脚本 (DeepSeek-V2-Lite)
logs/           # 训练日志和输出
datasets/       # 下载的数据集存储
```

**主要能力：**

- **FineWeb下载**——计划并下载分片以达到token预算（10B、100B+ token），可续传带进度追踪。
- **hf-mirror.com支持**——当HuggingFace被屏蔽时，使用wget脚本实现中国访问。
- **Parquet提取**——通过pyarrow iter_batches实现内存安全迭代。
- **分词**——将原始文本转换为训练就绪格式。
- **训练分析**——从训练日志计算时长和指标评估。
- **DeepSeek推理**——DeepSeek-V2-Lite的LLM推理脚本。

![zz在Hugging Face上——数据集处理与训练工具，22次提交，3位贡献者](/assets/images/ai-portfolio/zz-huggingface.png)

GitHub: [lzwjava/zz](https://github.com/lzwjava/zz) · Hugging Face: [lzwjava/zz](https://huggingface.co/lzwjava/zz)

---

## 🎓 证书

### 机器学习专业课程——DeepLearning.AI & 斯坦福大学

2023年11月完成。三门课程：监督式机器学习、高级学习算法、无监督学习、推荐系统、强化学习。

![Coursera机器学习专业课程证书——李智维，2023年11月](/assets/images/ai-portfolio/coursera-ml-1.png)

### 深度学习专业课程——DeepLearning.AI

2023年12月完成。五门课程：神经网络、超参数调优、结构化ML项目、CNN、序列模型。

![Coursera深度学习专业课程证书——李智维，2023年12月](/assets/images/ai-portfolio/coursera-dl-1.png)

---

- GitHub: [https://github.com/lzwjava](https://github.com/lzwjava)
- 博客: [https://lzwjava.github.io](https://lzwjava.github.io)
