---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 我的AI作品集——日常AI工作证据
translated: true
---

我不只是在谈论 AI——我每天都在大规模地使用它。这篇文章是我的 AI 努力成果的视觉作品集：我构建的工具、我消耗的 token，以及我获得的认证。

---

## 🖥️ LLM 训练与推理——我的硬件设置

我在 2023 年构建了自己的机器学习工作站，并从那时起一直在训练和学习。

**硬件经验：**

| GPU | VRAM | 经验时长 | 使用场景 |
|-----|------|----------|---------|
| NVIDIA RTX 4070 | 12 GB | 3 年 | 家用工作站 |
| NVIDIA H200 | 141 GB | 3 个月 | RunPod / DigitalOcean |
| AMD MI300X | 192 GB HBM3 | 3 个月 | AMD 开发者云 |

**我训练过的内容：**

- **GPT-2 124M** 从零开始在 FineWeb 数据集上训练（nanoGPT）——在 RTX 4070、H200 和 MI300X 上。
- **GPT-2 760M** 从零开始在 AMD MI300X（192 GB HBM3）上训练——探索 nanochat、DeepSeek v4 MoE。
- 各种关于超参数调优、学习率调度和数据集预处理的实验。

**工作站：**

![我的机器学习学习站——2023 年构建，RTX 4070 12GB，用于日常训练和实验](/assets/images/ai-portfolio/learning-station.jpg)

**AMD 开发者云——MI300X 192GB HBM3：**

![AMD 开发者云——用于大规模模型训练的 MI300X 实例](/assets/images/ai-portfolio/amd-dev-cloud.png)

---

## 🧠 增强版 nanoGPT——我的分支

Fork 了 [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT) 并扩展了额外的数据集管道、扩展的训练配置以及用于学习的内联形状注释。45 次提交，2025 年 11 月 – 2026 年 4 月。

**新增的数据集管道：**

| 数据集 | 路径 | 描述 |
|---------|------|------|
| FineWeb-Edu | `data/fineweb/` | HuggingFace FineWeb-Edu（100 亿+ token）。基于分片的加载、分块处理、增量训练/验证集划分。 |
| OpenWebText 10k | `data/openwebtext_10k/` | 快速 10k 子集，用于快速迭代。 |
| 本地 Wikipedia | `data/wikipedia_local/` | 直接对本地纯文本转储进行 tokenization（无需 HuggingFace 下载）。 |

**新增的训练配置：**

| 配置 | 目标 | 备注 |
|--------|--------|------|
| `train_fineweb.py` | 125M 在 FineWeb 上 | 针对 RTX 4070 12 GB 调整（n_embd=384, dropout=0.1）。 |
| `train_fineweb1_5b.py` | 1.5B 在 FineWeb 上 | 适用于 H200 80 GB。 |
| `train_fineweb_gpt3.py` | GPT-3 风格 100 亿 token | 基于分片的加载器，更宽的调度。 |
| `train_fineweb_760m.py` | 760M 在 FineWeb 上 | 适用于 MI300X 192 GB HBM3。 |
| `train_gpt2_200m.py` | GPT-2 200M | 通用中型配置。 |
| `train_gpt2_200m_smoke.py` | 烟雾测试 | 快速 200M 完整性检查（约几分钟）。 |

**模型变更：**

- **在整个 `model.py` 前向传播中添加了内联张量形状注释**（CausalSelfAttention、MLP、GPT）——以具体的 GPT-2 XL 示例显示每一步的精确形状，例如 `# x: (B, T, C) e.g. (1, 5, 1600)`。有助于理解 transformer 数据流。

![增强版 nanoGPT——45 次提交、数据集管道、扩展的训练配置、内联形状注释](/assets/images/ai-portfolio/nanogpt-fork.png)

GitHub: [lzwjava/nanoGPT](https://github.com/lzwjava/nanoGPT)

---

## 📊 LLM API 使用情况——数据

### OpenRouter——过去一年

消耗了 11.5 亿 token，花费 239 美元，跨多个模型发出了 15.5 万次 API 请求。

![OpenRouter 活动仪表板——1 年内消耗 11.5 亿 token、花费 239 美元、15.5 万次请求](/assets/images/ai-portfolio/openrouter-activity.png)

![OpenRouter 模型花费明细——Claude 4 Sonnet $44.40, Claude 3.5 Sonnet $9.67, Grok 3, Mistral, Kimi](/assets/images/ai-portfolio/openrouter-spend.png)

![OpenRouter 按模型划分的 Token 使用量——MiniMax 2.4 亿, Gemini 2.03 亿, DeepSeek 1.1 亿](/assets/images/ai-portfolio/openrouter-models.png)

### 通过 SSSAICode 使用 Claude API——2026 年 4 月

一个月内花费 171.53 美元。2555 次请求。1.15 亿+ token。缓存命中率 90.9%。

![SSSAICode Claude 使用情况——Opus 4.6, Opus 4.7, Sonnet 4.6, Haiku 4.5](/assets/images/ai-portfolio/sssaicode-usage.png)

### 小米 MIMO 订阅——已使用 12.5 亿 Token

Pro 月度计划，包含 380 亿主配额 + 87.5 亿补偿配额（约 46 亿免费额度）。2026 年 5 月至 6 月期间消耗了 **12.5 亿 token**。

![小米 MIMO Pro 计划——已消耗 12.5 亿 token，剩余约 34 亿免费额度](/assets/images/ai-portfolio/xiaomi-mimo-usage.png)

#### 月度 Token 使用明细

| 月份 | 模型 | Token 总数 | 输入（缓存命中） | 输入（缓存未命中） | 输出 | 请求次数 |
|-------|-------|-------------:|-------------------:|--------------------:|-------:|---------:|
| 2026-06 | mimo-v2.5 | 285,179 | 36,416 | 143,556 | 105,207 | 78 |
| 2026-06 | mimo-v2.5-pro | 734,873,374 | 710,036,672 | 21,617,131 | 3,219,571 | 10,704 |
| 2026-05 | mimo-v2.5 | 91,203 | 5,312 | 52,908 | 32,983 | 27 |
| 2026-05 | mimo-v2.5-pro | 508,851,211 | 488,291,136 | 17,725,731 | 2,834,344 | 8,649 |
| 2026-05 | mimo-v2-pro | 3,571,328 | 3,021,568 | 539,357 | 10,403 | 167 |

**月度总计：** 2026 年 5 月：**5.125 亿 token**（8,843 次请求）· 2026 年 6 月：**7.352 亿 token**（10,782 次请求）

> mimo-v2.5-pro 占主导地位（约占总额的 96%）。mimo-v2.5-pro 上的缓存命中率约 96.7%，保持了成本效率。6 月份 token 量较 5 月份增长了 43.5%。

### 总结

| 平台 | Token 数量 | 时间段 | 费用 |
|----------|--------|--------|------|
| OpenRouter | 11.5 亿 | 过去一年 | $239 |
| SSSAICode (Claude) | 1.15 亿+ | 2026 年 4 月 | $171.53 |
| 小米 MIMO | 12.5 亿 | 2026 年 5 月至 6 月 | 免费 46 亿额度 |
| 其他（GitHub Copilot 等） | 5 亿 | 过去一年 | — |
| **总计** | **~30 亿+** | **过去一年** | **—** |

---

## 🏢 企业 AI 使用——汇丰银行

在汇丰银行（通过 TEKsystems），我在 GitHub Copilot 之上构建了一个自主 AI 代理层，用于自动化脚本编写、日志记录、文档和测试。

**我构建的内容：**

- **20 个定制 AI 代理**——针对不同技术栈和工作流的专用提示和上下文。
- **400 个可重复使用的 Copilot 编写的脚本**——跨 Java、Spring、Python、Angular 和 DevOps 工具的常见任务自动化。
- **1,100 份 Copilot 编写的指南**——通过 LLM 输出生成并验证的文档，带有缓存和验证功能。
- **通过 Copilot API 自动生成了约 70 个测试用例**——涵盖 Spring Filters、Python unittest、JSON 截断、提示工程和区域端点。

**成果：**

- 在整个企业中，根据高级请求衡量，**Copilot 使用量排名前 6%**。
- 因高知名度的 AIPlayer 项目获得了 **贡献奖**。
- 加入了汇丰银行的内部 AI 社区。

<div align="center">

<img src="/assets/images/ai-portfolio/copilot.png" width="100%" /><img/>

<p><a href="https://marketplace.visualstudio.com/items?itemName=GitHub.copilot">图片来源：GitHub Copilot — Visual Studio Code Marketplace</a></p>

</div>

![汇丰银行 AIPlayer 贡献奖](/assets/images/ai-portfolio/aiplayer.jpg)

---

## 🎤 在汇丰银行的 AI 演讲——从神经网络到代理

在汇丰银行向 **80 名参与者** 进行了技术演讲——包括高级顾问、专家、副总监、软件工程师和合同工。

**演讲：** *"从神经网络到代理"*——从最简单的神经网络（`y = wx`）开始，经过 MNIST、Transformer、GPT、nanoGPT，一直到构建个人 AI 代理的旅程。

**我涵盖的内容：**

- 从第一性原理出发的神经网络——前向传播、反向传播、梯度下降
- Transformer 架构——Q/K/V 注意力、多头注意力、位置编码
- GPT 内部机制——分词、嵌入、训练、生成
- nanoGPT——在 H200/RTX 4070 上从零开始训练 GPT-2
- LLM 代理——Claude Code、OpenClaw、Hermes、工具调用、代理循环
- 实际数据——消耗 10 亿 token、H200 每小时 $3.44、钱究竟花在哪里
- 我的路径——从阅读 Q/K/V 到从零开始训练模型的 3 年

**反馈：**

- 一位初级工程师说：*"你就是我想成为的人"*——这场演讲开拓了他对 AI 可能性的认识
- 高级工程师赞赏第一性原理的方法——没有炒作，只有数学和代码
- 多次后续对话涉及训练、代理和职业方向

**幻灯片：** 使用 Claude Code 和 Marp 构建，源自我的公开 AI 回复笔记。

---

## 🛠️ ww——跨平台 CLI 工具包

[ww](https://github.com/lzwjava/ww) 是我的旗舰 CLI 工具包——255+ 次提交、10+ 命令组、跨平台（macOS + Linux）。它涵盖了带有 AI 提交消息的 git 工作流、笔记管理、图像/PDF 处理、网络搜索、GitHub Copilot 聊天、系统工具和 LLM 驱动的辅助功能。

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

![ww——GitHub 上的跨平台 CLI 工具包](/assets/images/ai-portfolio/ww1.png)

GitHub: [lzwjava/ww](https://github.com/lzwjava/ww)

---

## 📝 jekyll-ai-blog——AI 驱动的博客平台

[jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog) 是 [lzwjava.github.io](https://lzwjava.github.io) 的源代码——一个通过 AI 自动化增强的 Jekyll 博客。10,000+ 篇英文文章、10,000+ 篇中文文章、9,700+ 条 AI 回答笔记。过去一个月约 70,000 次页面浏览量（Cloudflare Analytics）。

```
lzwjava@lzw-mac jekyll-ai-blog % ls README.md
README.md
```

**它与标准 Jekyll 博客的不同之处：**

- **AI 驱动的翻译**——基于 LLM 的翻译管道，通过 GitHub Actions 自动将每篇文章扩展到多种语言。
- **Google Cloud Text-to-Speech**——自动生成文章音频版本，提高可访问性。
- **XeLaTeX PDF/EPUB 生成**——从 Markdown 源生成高质量、适合打印的 PDF 和电子书导出。
- **GitHub Actions CI/CD**——自动化构建、测试、翻译和部署工作流。
- **8,000+ 条 AI 回答笔记**——通过日常 LLM 辅助研究构建的知识库，可在博客上搜索。
- **MathJax、夜间模式、RSS、双语内容**——通过自定义 CSS 和主题增强的标准功能。

**规模：**

| 指标 | 数量 |
|--------|-------|
| 英文文章 | 10,264 |
| 中文文章 | 10,259 |
| AI 回答笔记 | 9,794 |
| Python 脚本 | 323 |
| ML 脚本 | 191 |
| 页面浏览量（过去一个月） | ~70,000 |

![jekyll-ai-blog——AI 驱动的博客，拥有 10K+ 篇文章、翻译、TTS 和 PDF 管道](/assets/images/ai-portfolio/blog.png)

![Cloudflare Web Analytics——38.9K 访问量、45.2K 页面浏览量、930ms 加载时间、82% 良好 LCP](/assets/images/ai-portfolio/cloudflare-analytics.png)

GitHub: [lzwjava/jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog)

---

## 🌳 Tree_Of_Thought——与一名高中生合作进行思维树推理

[Tree_Of_Thought](https://github.com/Cerynitius/Tree_Of_Thought) 是一个朋友的项目——一个用于解决重度物理问题的外部思维树推理系统。它不是依赖模型在一个不透明的补全中的隐藏思维链，而是将推理转化为一个显式、可检查、可控的树，具有实时状态、评分、剪枝和确定性工具支持。

该系统结合了一个用于长时推理会话的 FastAPI 服务、一个用于检查和剪枝分支的浏览器 UI、一个节点级 FSM 和树调度器、一个支持精确符号计算的 SymPy 技能层，以及用于规划、建模、审查和评估的多模型路由。

**我的贡献（1 个 PR）：** 添加了一个兼容 OpenAI 的请求器和 `python-dotenv` 配置，使系统可以连接到任何兼容 OpenAI 的端点（本地或云端）。

**背景：** 我指导一名构建了该系统的高中生。在一次会议中，他向我详细介绍了完整的架构——推理树、基于 FSM 的审查、路线局部增量改进。我向他介绍了 AI 博士研究员，并帮助他思考研究方向。他现在正在探索使用 LLM 解决物理问题，使用 Codex (GPT-5.4) 等工具，并构建多智能体协作编码系统。

![思维树——终端树探索器，具有节点检查、前沿管理和分支剪枝功能](/assets/images/ai-portfolio/tree-of-thought.jpg)

GitHub: [Cerynitius/Tree_Of_Thought](https://github.com/Cerynitius/Tree_Of_Thought)

---

## 🤖 iclaw——终端 AI 代理（REPL）

[iclaw](https://github.com/lzwjava/iclaw) 是一个终端 AI 代理，可以自主编码、搜索和运行命令——可在个人机器和受限制的企业机器上工作。一个最小的 openclaw 实现，构建为纯 Python CLI，无需浏览器扩展或 IDE 插件，由 GitHub Copilot 驱动。

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

- 在终端中与 GitHub Copilot 或 OpenRouter 进行**多轮对话**。
- **多个模型提供者**：GitHub Copilot（OAuth 设备流）和 OpenRouter（API 密钥）。
- **原生工具调用**：模型自主调用网络搜索、执行 shell 命令和编辑文件——无需人工介入。
- **多个搜索提供者**：DuckDuckGo、Startpage、Bing 和 Tavily。
- **企业友好**：无需 IDE 插件或浏览器扩展。在企业防火墙后通过代理和 CA 包支持工作。
- **默认模型**：GPT-5.2。

![iclaw——具有原生工具调用功能的终端 AI 代理 REPL](/assets/images/ai-portfolio/iclaw.jpg)

![iclaw——显示自主编码和 shell 命令的执行日志](/assets/images/ai-portfolio/iclaw-log.png)

GitHub: [lzwjava/iclaw](https://github.com/lzwjava/iclaw)

---

## ⚙️ zz——数据集处理与训练工具

[zz](https://github.com/lzwjava/zz) 是一个用于 ML 训练管道的工具包——数据集下载、分词、提取和推理工具。在 RunPod H200、DigitalOcean H100 和家用 RTX 4070 上的 GPT-2 124M 训练运行期间使用。也托管在 [Hugging Face](https://huggingface.co/lzwjava/zz) 上。

```
lzwjava@lzw-mac zz % tree -L 1
scripts/
  download/     # 数据集下载脚本（FineWeb、Wikimedia、HF 镜像）
  extract/      # 数据提取、分词和重命名
  analysis/     # 训练时长和指标评估
  deepseek/     # LLM 推理脚本（DeepSeek-V2-Lite）
logs/           # 训练日志和输出
datasets/       # 下载的数据集存储
```

**主要功能：**

- **FineWeb 下载**——规划并下载分片以达到 token 预算（100 亿、1000 亿+ token），可断点续传并带有进度跟踪。
- **hf-mirror.com 支持**——当 HuggingFace 被屏蔽时，针对中国访问的 wget 脚本。
- **Parquet 提取**——通过 pyarrow iter_batches 进行内存安全的迭代。
- **分词**——将原始文本转换为训练就绪格式。
- **训练分析**——从训练日志计算时长和指标评估。
- **DeepSeek 推理**——用于 DeepSeek-V2-Lite 的 LLM 推理脚本。

![zz 在 Hugging Face 上——数据集处理与训练工具，22 次提交，3 位贡献者](/assets/images/ai-portfolio/zz-huggingface.png)

GitHub: [lzwjava/zz](https://github.com/lzwjava/zz) · Hugging Face: [lzwjava/zz](https://huggingface.co/lzwjava/zz)

---

## 🎓 证书

### 机器学习专项课程——DeepLearning.AI & 斯坦福大学

2023 年 11 月完成。三门课程：监督式机器学习、高级学习算法、无监督学习、推荐系统、强化学习。

![Coursera 机器学习专项课程证书——李智维，2023 年 11 月](/assets/images/ai-portfolio/coursera-ml-1.png)

### 深度学习专项课程——DeepLearning.AI

2023 年 12 月完成。五门课程：神经网络、超参数调优、构建机器学习项目、CNN、序列模型。

![Coursera 深度学习专项课程证书——李智维，2023 年 12 月](/assets/images/ai-portfolio/coursera-dl-1.png)

---

- GitHub: [https://github.com/lzwjava](https://github.com/lzwjava)
- 博客: [https://lzwjava.github.io](https://lzwjava.github.io)
