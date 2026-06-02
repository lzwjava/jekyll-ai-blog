---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 我的AI作品集——每日AI工作的证据
translated: true
---

我不只是谈论AI——我每天都在大规模使用它。这篇文章是我的AI成果视觉集锦：我构建的工具、我消耗的token，以及我获得的证书。

---

## 🖥️ LLM训练与推理——我的硬件设置

2023年搭建了我的机器学习工作站，并从那时起持续训练和学习。

**硬件经验：**

| GPU | 显存 | 经验时长 | 使用场景 |
|-----|------|------------|-------|
| NVIDIA RTX 4070 | 12 GB | 3年 | 家庭工作站 |
| NVIDIA H200 | 141 GB | 3个月 | RunPod / DigitalOcean |
| AMD MI300X | 192 GB HBM3 | 3个月 | AMD开发者云 |

**我训练过的模型：**

- **GPT-2 124M** 从头训练，基于FineWeb数据集（nanoGPT）——在RTX 4070、H200和MI300X上。
- **GPT-2 760M** 从头训练，基于AMD MI300X（192 GB HBM3）——探索nanochat、DeepSeek v4 MoE。
- 各种关于超参数调优、学习率调度和数据集预处理的实验。

**工作站：**

![我的机器学习学习站——2023年搭建，RTX 4070 12GB，用于日常训练和实验](/assets/images/ai-portfolio/learning-station.jpg)

**AMD开发者云——MI300X 192GB HBM3：**

![AMD开发者云——用于大规模模型训练的MI300X实例](/assets/images/ai-portfolio/amd-dev-cloud.png)

---

## 🧠 增强版nanoGPT——我的分支

Fork了[karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)并进行了扩展，增加了额外的数据集管道、扩展训练配置和用于学习的内联形状注释。45次提交，2025年11月至2026年4月。

**新增数据集管道：**

| 数据集 | 路径 | 描述 |
|---------|------|-------------|
| FineWeb-Edu | `data/fineweb/` | HuggingFace FineWeb-Edu（10B+ token）。基于分片的加载、分块处理、增量训练/验证集划分。 |
| OpenWebText 10k | `data/openwebtext_10k/` | 快速10k子集，用于快速迭代。 |
| 本地Wikipedia | `data/wikipedia_local/` | 直接对本地纯文本dump进行分词（无需HuggingFace下载）。 |

**新增训练配置：**

| 配置 | 目标 | 备注 |
|--------|--------|-------|
| `train_fineweb.py` | 125M on FineWeb | 针对RTX 4070 12 GB优化（n_embd=384, dropout=0.1）。 |
| `train_fineweb1_5b.py` | 1.5B on FineWeb | 用于H200 80 GB。 |
| `train_fineweb_gpt3.py` | GPT-3风格10B token | 基于分片的加载器，更宽的调度。 |
| `train_fineweb_760m.py` | 760M on FineWeb | 用于MI300X 192 GB HBM3。 |
| `train_gpt2_200m.py` | GPT-2 200M | 通用中等规模配置。 |
| `train_gpt2_200m_smoke.py` | 冒烟测试 | 快速200M完整性检查（约几分钟）。 |

**模型改动：**

- **内联张量形状注释**，贯穿`model.py`前向传播（CausalSelfAttention, MLP, GPT）——每一步都显示具体形状，并附有GPT-2 XL的具体示例，例如`# x: (B, T, C) 例如 (1, 5, 1600)`。有助于理解Transformer数据流。

![增强版nanoGPT——45次提交、数据集管道、扩展训练配置、内联形状注释](/assets/images/ai-portfolio/nanogpt-fork.png)

GitHub：[lzwjava/nanoGPT](https://github.com/lzwjava/nanoGPT)

---

## 📊 LLM API使用情况——数据

### OpenRouter——过去一年

消耗1.15B token，花费$239，15.5万次API请求，覆盖多个模型。

![OpenRouter活动仪表盘——1.15B token，消费$239，15.5万次请求（过去一年）](/assets/images/ai-portfolio/openrouter-activity.png)

![OpenRouter模型花费明细——Claude 4 Sonnet $44.40，Claude 3.5 Sonnet $9.67，Grok 3，Mistral，Kimi](/assets/images/ai-portfolio/openrouter-spend.png)

![OpenRouter各模型Token用量——MiniMax 240M，Gemini 203M，DeepSeek 110M](/assets/images/ai-portfolio/openrouter-models.png)

### 通过SSSAICode使用Claude API——2026年4月

一个月内$171.53。2,555次请求。1.15亿+ token。90.9%缓存命中率。

![SSSAICode Claude使用情况——Opus 4.6，Opus 4.7，Sonnet 4.6，Haiku 4.5](/assets/images/ai-portfolio/sssaicode-usage.png)

### 小米MIMO订阅——已使用5亿Token

Pro月度套餐，38B主配额 + 8.75B补偿配额（约4.6B免费额度）。目前已使用5亿Token。

![小米MIMO Pro套餐——已消耗5亿Token，剩余约4.6B免费额度](/assets/images/ai-portfolio/xiaomi-mimo-usage.png)

### 总计

| 平台 | Token | 时间段 | 费用 |
|----------|--------|--------|------|
| OpenRouter | 1.15B | 过去一年 | $239 |
| SSSAICode (Claude) | 1.15亿+ | 2026年4月 | $171.53 |
| 小米MIMO | 5亿 | 当前套餐 | 免费4.6B额度 |
| 其他 (GitHub Copilot等) | 5亿 | 过去一年 | — |
| **总计** | **约2.3B+** | **过去一年** | **—** |

---

## 🏢 企业级AI使用——汇丰银行

在汇丰银行（通过TEKsystems），我在GitHub Copilot之上构建了一个自主AI智能体层，用于自动化脚本编写、日志记录、文档编写和测试。

**我构建的内容：**

- **20个定制化AI智能体**——针对不同技术栈和工作流程的专用提示词和上下文。
- **400个可复用的Copilot编写脚本**——自动化常见的Java、Spring、Python、Angular和DevOps工具任务。
- **1,100份Copilot编写的指南**——通过LLM输出生成并验证的文档，包含缓存和验证机制。
- **通过Copilot API自动生成约70个测试用例**——覆盖Spring过滤器、Python unittest、JSON截断、提示词工程和区域端点。

**成果：**

- 在全企业Copilot使用量中排名**前6%**（按高级请求计算）。
- 因高影响力的AIPlayer项目获得**贡献奖**。
- 加入汇丰银行内部AI社区。

<div align="center">

<img src="/assets/images/ai-portfolio/copilot.png" width="100%" /><img/>

<p><a href="https://marketplace.visualstudio.com/items?itemName=GitHub.copilot">图片来源：GitHub Copilot——Visual Studio Code Marketplace</a></p>

</div>

![汇丰银行AIPlayer贡献奖](/assets/images/ai-portfolio/aiplayer.jpg)

---

## 🎤 汇丰银行AI讲座——从神经网络到智能体

在汇丰银行面向**80名参与者**进行了一场技术讲座——包括高级顾问、专家、副总监、软件工程师和承包商。

**讲座主题：** *"从神经网络到智能体"* ——从最简单的神经网络（`y = wx`）出发，经历MNIST、Transformer、GPT、nanoGPT，直至构建个人AI智能体的旅程。

**涵盖内容：**

- 神经网络基本原理——前向传播、反向传播、梯度下降
- Transformer架构——Q/K/V注意力、多头注意力、位置编码
- GPT内部机制——分词、嵌入、训练、生成
- nanoGPT——在H200/RTX 4070上从头训练GPT-2
- LLM智能体——Claude Code、OpenClaw、Hermes、工具调用、智能体循环
- 真实数据——消耗1B token，H200每小时$3.44，钱到底花在哪里
- 我的路径——从3年前阅读Q/K/V到如今从头训练模型

**反馈：**

- 一位初级工程师说：*"你就是我想成为的人"*——这场讲座开阔了他对AI可能性的认知
- 高级工程师欣赏其基于第一性原理的方法——没有炒作，只有数学和代码
- 多次后续交流，关于训练、智能体和职业方向

**幻灯片：** 使用Claude Code & Marp构建，基于我的公开AI回复笔记。

---

## 🛠️ ww——跨平台CLI工具包

[ww](https://github.com/lzwjava/ww)是我的旗舰CLI工具包——255+次提交，10+个命令组，跨平台（macOS + Linux）。涵盖带有AI提交信息的git工作流、笔记管理、图像/PDF处理、网页搜索、GitHub Copilot聊天、系统工具和LLM辅助功能。

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

![ww——GitHub上的跨平台CLI工具包](/assets/images/ai-portfolio/ww1.png)

GitHub：[lzwjava/ww](https://github.com/lzwjava/ww)

---

## 📝 jekyll-ai-blog——AI驱动博客平台

[jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog)是[lzwjava.github.io](https://lzwjava.github.io)的源代码——一个由AI自动化增强的Jekyll博客。10,000+篇英文文章，10,000+篇中文文章，9,700+条AI回答笔记。过去一个月约70,000次页面浏览（Cloudflare Analytics）。

```
lzwjava@lzw-mac jekyll-ai-blog % ls README.md
README.md
```

**它与标准Jekyll博客的不同之处：**

- **AI驱动翻译**——基于LLM的翻译管道通过GitHub Actions自动将每篇文章扩展到多种语言。
- **Google Cloud Text-to-Speech**——自动生成文章的音频版本，提升可访问性。
- **XeLaTeX PDF/EPUB生成**——从Markdown源生成高质量、可打印的PDF和电子书导出。
- **GitHub Actions CI/CD**——自动化构建、测试、翻译和部署工作流。
- **8,000+条AI回答笔记**——基于日常LLM辅助研究构建的知识库，可在博客上搜索。
- **MathJax、夜间模式、RSS、双语内容**——通过自定义CSS和主题增强的标准功能。

**规模：**

| 指标 | 数量 |
|--------|-------|
| 英文文章 | 10,264 |
| 中文文章 | 10,259 |
| AI回答笔记 | 9,794 |
| Python脚本 | 323 |
| 机器学习脚本 | 191 |
| 页面浏览（过去一个月） | ~70,000 |

![jekyll-ai-blog——AI驱动博客，包含10K+篇文章、翻译、TTS和PDF管道](/assets/images/ai-portfolio/blog.png)

GitHub：[lzwjava/jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog)

---

## 🌳 Tree_Of_Thought——与一名高中生合作进行树状思维推理

[Tree_Of_Thought](https://github.com/Cerynitius/Tree_Of_Thought)是一个朋友的项目——一个面向物理密集型问题解决的外部树状思维推理系统。它不依赖模型在单个不透明完成中的隐藏思维链，而是将推理转化为一个显式、可检查、可控的树，包含实时状态、评分、剪枝和确定性工具支持。

该系统结合了用于长时间推理会话的FastAPI服务、用于检查和剪枝分支的浏览器UI、节点级FSM和树调度器、基于SymPy的技能层用于精确符号计算，以及用于规划、建模、审查和评估的多模型路由。

**我的贡献（1个PR）：** 添加了一个兼容OpenAI的请求器和`python-dotenv`配置，使系统能够连接到任何兼容OpenAI的端点（本地或云端）。

**背景：** 我指导一名构建该系统的中学生。在一次会议中，他向我展示了完整的架构——推理树、基于FSM的审查、路由局部增量优化。我将他介绍给AI博士研究员，并帮助他思考研究方向。他现在正在探索使用LLM解决物理问题，使用Codex（GPT-5.4）等工具，并构建多智能体协作编码系统。

![树状思维——终端树形探索器，支持节点检查、前沿管理和分支剪枝](/assets/images/ai-portfolio/tree-of-thought.jpg)

GitHub：[Cerynitius/Tree_Of_Thought](https://github.com/Cerynitius/Tree_Of_Thought)

---

## 🤖 iclaw——终端AI智能体（REPL）

[iclaw](https://github.com/lzwjava/iclaw)是一个终端AI智能体，能够自主编码、搜索和运行命令——可运行在个人机器和严格限制的企业机器上。一个最小化的openclaw实现，作为纯Python CLI构建，无需浏览器扩展或IDE插件，由GitHub Copilot驱动。

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

**主要特性：**

- **多轮对话**，在终端中使用GitHub Copilot或OpenRouter。
- **多个模型提供商**：GitHub Copilot（OAuth设备流）和OpenRouter（API密钥）。
- **原生工具调用**：模型自主调用网络搜索、执行shell命令、编辑文件——无需人工介入。
- **多个搜索提供商**：DuckDuckGo、Startpage、Bing和Tavily。
- **对企业友好**：无需IDE插件或浏览器扩展。支持代理和CA包配置，可在企业防火墙后运行。
- **默认模型**：GPT-5.2。

![iclaw——带原生工具调用的终端AI智能体REPL](/assets/images/ai-portfolio/iclaw.jpg)

![iclaw——显示自主编码和shell命令的执行日志](/assets/images/ai-portfolio/iclaw-log.png)

GitHub：[lzwjava/iclaw](https://github.com/lzwjava/iclaw)

---

## ⚙️ zz——数据集处理与训练工具

[zz](https://github.com/lzwjava/zz)是一个面向ML训练管道的工具包——数据集下载、分词、提取和推理工具。用于在RunPod H200、DigitalOcean H100和家庭RTX 4070上训练GPT-2 124M。也托管在[Hugging Face](https://huggingface.co/lzwjava/zz)上。

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

- **FineWeb下载**——规划并下载分片以达到token预算（10B、100B+ token），支持断点续传和进度跟踪。
- **hf-mirror.com支持**——当HuggingFace被屏蔽时，提供用于中国的wget脚本。
- **Parquet提取**——通过pyarrow iter_batches进行内存安全的迭代。
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

2023年12月完成。五门课程：神经网络、超参数调优、结构化机器学习项目、卷积神经网络、序列模型。

![Coursera深度学习专项课程证书——李智维，2023年12月](/assets/images/ai-portfolio/coursera-dl-1.png)

---

- GitHub：[https://github.com/lzwjava](https://github.com/lzwjava)
- 博客：[https://lzwjava.github.io](https://lzwjava.github.io)
