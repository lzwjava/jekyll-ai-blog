---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 我的AI作品集——日常AI工作的证据
translated: true
---

我不仅谈论AI——我每天都在大规模使用它。这篇文章是我的AI成果视觉作品集：我构建的工具、我消耗的Token数，以及我获得的认证。

---

## 🖥️ LLM训练与推理——我的硬件设置

2023年搭建了我的机器学习工作站，此后一直在进行训练和学习。

**硬件经验：**

| GPU | 显存 | 经验时间 | 使用场景 |
|-----|------|------------|-------|
| NVIDIA RTX 4070 | 12 GB | 3 年 | 家庭工作站 |
| NVIDIA H200 | 141 GB | 3 个月 | RunPod / DigitalOcean |
| AMD MI300X | 192 GB HBM3 | 3 个月 | AMD 开发者云 |

**我训练过的模型：**

- **GPT-2 124M** —— 从零开始在 FineWeb 数据集上训练（nanoGPT）—— 在 RTX 4070、H200 和 MI300X 上完成。
- **GPT-2 760M** —— 从零开始在 AMD MI300X（192 GB HBM3）上训练 —— 探索 nanochat、DeepSeek v4 MoE。
- 关于超参数调优、学习率调度和数据集预处理的各种实验。

**工作站：**

![我的机器学习学习站 —— 2023年搭建，RTX 4070 12GB，用于日常训练和实验](/assets/images/ai-portfolio/learning-station.jpg)

**AMD 开发者云 —— MI300X 192GB HBM3：**

![AMD 开发者云 —— 用于大规模模型训练的 MI300X 实例](/assets/images/ai-portfolio/amd-dev-cloud.png)

---

## 🧠 增强版 nanoGPT —— 我的分支

复刻了 [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT) 并进行了扩展，添加了额外的数据集流水线、规模化训练配置以及用于学习的在线形状注释。45次提交，2025年11月至2026年4月。

**新增的数据集流水线：**

| 数据集 | 路径 | 描述 |
|---------|------|-------------|
| FineWeb-Edu | `data/fineweb/` | HuggingFace FineWeb-Edu（100亿+ Token）。基于分片的加载、分块处理、增量训练/验证集划分。 |
| OpenWebText 10k | `data/openwebtext_10k/` | 用于快速迭代的10k子集。 |
| Wikipedia Local | `data/wikipedia_local/` | 直接对本地纯文本转储进行分词（无需 HuggingFace 下载）。 |

**新增的训练配置：**

| 配置 | 目标 | 备注 |
|--------|--------|-------|
| `train_fineweb.py` | FineWeb上的125M模型 | 针对RTX 4070 12 GB进行了调优（n_embd=384, dropout=0.1）。 |
| `train_fineweb1_5b.py` | FineWeb上的1.5B模型 | 适用于H200 80 GB。 |
| `train_fineweb_gpt3.py` | GPT-3风格的10B Token | 基于分片的加载器，更宽泛的调度。 |
| `train_fineweb_760m.py` | FineWeb上的760M模型 | 适用于MI300X 192 GB HBM3。 |
| `train_gpt2_200m.py` | GPT-2 200M | 通用型中等规模配置。 |
| `train_gpt2_200m_smoke.py` | 冒烟测试 | 快速的200M完整性检查（约几分钟）。 |

**模型改动：**

- 在整个 `model.py` 前向传播（CausalSelfAttention, MLP, GPT）中添加了**在线张量形状注释** —— 以具体的 GPT-2 XL 示例展示每一步的精确形状，例如 `# x: (B, T, C) e.g. (1, 5, 1600)`。有助于理解Transformer数据流。

![增强版 nanoGPT —— 45次提交，数据集流水线，规模化训练配置，在线形状注释](/assets/images/ai-portfolio/nanogpt-fork.png)

GitHub: [lzwjava/nanoGPT](https://github.com/lzwjava/nanoGPT)

---

## 📝 SEC-EDGAR-GPT —— 在SEC文件上从零训练的 GPT-2（124M）

在 **15.5亿 Token** 的 SEC EDGAR 金融文件（10-K、10-Q 及其他公司披露文件）上，从零训练了一个 **1.24亿参数的 GPT-2** 模型 —— 在单个 **RTX 4070**（12 GB 显存）上训练了约8小时，验证损失收敛至2.28。

该模型能生成逼真的 SEC 样板文件 —— 风险因素、MD&A 章节、业务描述 —— 并通过 RunPod 上的 FastAPI 服务器部署为交互式聊天。

整个项目（模型训练、论文、聊天机器人和网站）在 **3天内使用 Hermes Agent 完成**，展示了 AI Agent 如何让 LLM 研究变得更加触手可及。

该项目在某个全球银行内部共享，获得了 **200多次** 内部浏览量。一位首席工程师留言称其 *“不错”*，同事们讨论了金融领域 Token 与自然语言 Token 之间的差异 —— 这场对话影响了我对金融领域LLM特化分词的理解。

![SEC-EDGAR-GPT 聊天机器人](/assets/images/sec-edgar-gpt/chatbot_web.png)

**代码：** [github.com/lzwjava/sec-edgar-gpt](https://github.com/lzwjava/sec-edgar-gpt) · **论文：** [sec-edgar-gpt.pdf](https://github.com/lzwjava/sec-edgar-gpt/raw/main/sec-edgar-gpt.pdf) · **模型：** [Hugging Face](https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf) · **聊天：** [sec-edgar-gpt.lzwjava.workers.dev](https://sec-edgar-gpt.lzwjava.workers.dev/)

---

## 📊 LLM API 使用量 —— 数据

### OpenRouter —— 过去一年

消耗了11.5亿 Token，花费239美元，跨多个模型发出了15.5万次 API 请求。

![OpenRouter 活动仪表板 —— 1年内11.5亿 Token、239美元花费、15.5万次请求](/assets/images/ai-portfolio/openrouter-activity.png)

![OpenRouter 模型花费细分 —— Claude 4 Sonnet $44.40, Claude 3.5 Sonnet $9.67, Grok 3, Mistral, Kimi](/assets/images/ai-portfolio/openrouter-spend.png)

![OpenRouter 各模型 Token 使用量 —— MiniMax 240M, Gemini 203M, DeepSeek 110M](/assets/images/ai-portfolio/openrouter-models.png)

### 通过 SSSAICode 使用 Claude API —— 2026年4月

一个月花费171.53美元。2555次请求。超过1.15亿 Token。90.9% 缓存命中率。

![SSSAICode Claude 使用量 —— Opus 4.6, Opus 4.7, Sonnet 4.6, Haiku 4.5](/assets/images/ai-portfolio/sssaicode-usage.png)

### 小米 MIMO 订阅 —— 已使用12.5亿 Token

Pro 月度套餐，包含380亿主配额 + 87.5亿补偿配额（约46亿免费额度）。**2026年5月至6月期间消耗了12.5亿 Token**。

![小米 MIMO Pro 套餐 —— 消耗12.5亿 Token，剩余约34亿免费额度](/assets/images/ai-portfolio/xiaomi-mimo-usage.png)

#### 月度 Token 使用细分

| 月份 | 模型 | 总 Token | 输入（缓存命中） | 输入（缓存未命中） | 输出 | 请求数 |
|-------|-------|-------------:|-------------------:|--------------------:|-------:|---------:|
| 2026-06 | mimo-v2.5 | 285,179 | 36,416 | 143,556 | 105,207 | 78 |
| 2026-06 | mimo-v2.5-pro | 734,873,374 | 710,036,672 | 21,617,131 | 3,219,571 | 10,704 |
| 2026-05 | mimo-v2.5 | 91,203 | 5,312 | 52,908 | 32,983 | 27 |
| 2026-05 | mimo-v2.5-pro | 508,851,211 | 488,291,136 | 17,725,731 | 2,834,344 | 8,649 |
| 2026-05 | mimo-v2-pro | 3,571,328 | 3,021,568 | 539,357 | 10,403 | 167 |

**月度总计：** 2026年5月: **5.125亿 Token**（8,843次请求）· 2026年6月: **7.352亿 Token**（10,782次请求）

> mimo-v2.5-pro 占主导地位（约占总量的96%）。mimo-v2.5-pro 上约96.7% 的缓存命中率保持了成本效益。6月的 Token 量比5月增长了43.5%。

### 总结

| 平台 | Token 数 | 时间段 | 成本 |
|----------|--------|--------|------|
| OpenRouter | 11.5亿 | 过去一年 | $239 |
| SSSAICode (Claude) | 1.15亿+ | 2026年4月 | $171.53 |
| 小米 MIMO | 12.5亿 | 2026年5-6月 | 46亿免费额度 |
| 其他（GitHub Copilot 等） | 5亿 | 过去一年 | — |
| **总计** | **~30亿+** | **过去一年** | **—** |

---

## 🏢 企业级 AI 应用 —— 汇丰银行

在汇丰银行（通过 TEKsystems），我在 GitHub Copilot 之上构建了一个自主 AI Agent 层，用于自动化脚本编写、日志记录、文档编写和测试。

**我构建的内容：**

- **20个定制化 AI Agent** —— 为不同技术栈和工作流设计了专用提示和上下文。
- **400个可复用的 Copilot 编写脚本** —— 针对跨 Java、Spring、Python、Angular 和 DevOps 工具的常见任务进行自动化。
- **1,100份 Copilot 编写指南** —— 通过 LLM 输出生成并验证的文档，包含缓存和验证机制。
- **约70个自动生成的测试用例** —— 通过 Copilot API 生成，涵盖 Spring Filters、Python unittest、JSON 截断、提示工程和区域端点。

**成果：**

- 以高级请求衡量，在整个企业中 Copilot 使用量排名**前6%**。
- 因备受瞩目的 AIPlayer 项目获得**贡献奖**。
- 加入了汇丰银行内部 AI 社区。

<div align="center">

<img src="/assets/images/ai-portfolio/copilot.png" width="100%" /><img/>

<p><a href="https://marketplace.visualstudio.com/items?itemName=GitHub.copilot">图片来源：GitHub Copilot — Visual Studio Code Marketplace</a></p>

</div>

![汇丰银行 AIPlayer 贡献奖](/assets/images/ai-portfolio/aiplayer.jpg)

---

## 🎤 汇丰银行 AI 讲座 —— 从神经网络到 Agent

在汇丰银行面向 **80名参与者** 进行了一场技术讲座 —— 包括高级顾问、专家、副总监、软件工程师和合同工。

**讲座：** *“从神经网络到 Agent”* —— 一场从最简单的神经网络（`y = wx`）开始，历经 MNIST、Transformers、GPT、nanoGPT，再到构建个人 AI Agent 的旅程。

**我涵盖的内容：**

- 从基本原理出发的神经网络 —— 前向传播、反向传播、梯度下降
- Transformer 架构 —— Q/K/V 注意力、多头注意力、位置编码
- GPT 内部机制 —— 分词、嵌入、训练、生成
- nanoGPT —— 在 H200/RTX 4070 上从零训练 GPT-2
- LLM Agent —— Claude Code、OpenClaw、Hermes、工具调用、Agent 循环
- 真实数据 —— 消耗10亿 Token，H200 每小时 $3.44，钱实际花在了哪里
- 我的路径 —— 从阅读 Q/K/V 相关知识到从零训练模型，历时3年

**反馈：**

- 一位初级工程师说：*“你就是我想成为的人”* —— 这场讲座开阔了他对 AI 可能性的认知
- 高级工程师欣赏这种从基本原理入手的方法 —— 没有炒作，只有数学和代码
- 后续进行了多次关于训练、Agent 和职业方向的讨论

**幻灯片：** 使用 Claude Code 和 Marp 基于我的公开 AI 回复笔记构建。

---

## 🛠️ ww —— 跨平台 CLI 工具集

[ww](https://github.com/lzwjava/ww) 是我的旗舰 CLI 工具集 —— 255+ 次提交，10+ 个命令组，跨平台（macOS + Linux）。它涵盖了带 AI 提交信息的 git 工作流、笔记管理、图像/PDF 处理、网络搜索、GitHub Copilot 聊天、系统实用程序和 LLM 驱动的助手。

```
lzwjava@lzw-mac ww % uv run ww --help
用法: ww <group> [command] [options]

操作:
  ww action [workflow.yml]  触发一个 GitHub Actions 工作流

AMD 开发者云:
  ww amd-dev-cloud snapshots    列出快照
  ww amd-dev-cloud start-train  创建用于训练的 GPU 实例
  ww amd-dev-cloud end-train    创建快照并销毁 GPU 实例

Copilot:
  ww copilot auth           通过 GitHub OAuth 进行身份验证
  ww copilot chat           与 Copilot 模型聊天

Git:
  ww git gpa            对所有仓库执行 git pull --all
  ww git squash <n>     压缩最近 n 次提交
  ww git amend-push     修改最后一次提交并强制推送

LLM:
  ww llm compare <prompt>   比较多个 LLM 的响应
  ww llm query <question>   查询本地 RAG 文档

笔记:
  ww note              将剪贴板内容保存为笔记（快速捕获）
  ww note process      清空笔记队列
  ww note watch        自动处理守护进程

截图:
  ww screenshot               截图并创建笔记
  ww screenshot interact-note 交互式截图笔记

255+ 次提交。10+ 个命令组。跨平台（macOS + Linux）。
```

![ww —— GitHub 上的跨平台 CLI 工具集](/assets/images/ai-portfolio/ww1.png)

GitHub: [lzwjava/ww](https://github.com/lzwjava/ww)

---

## 📝 jekyll-ai-blog —— AI 驱动的博客平台

[jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog) 是 [lzwjava.github.io](https://lzwjava.github.io) 的源代码 —— 一个通过 AI 自动化增强的 Jekyll 博客。包含10,000+ 篇英文文章，10,000+ 篇中文文章，9,700+ 条 AI 回答笔记。过去一个月约70,000次页面浏览量（Cloudflare Analytics）。

```
lzwjava@lzw-mac jekyll-ai-blog % ls README.md
README.md
```

**它区别于标准 Jekyll 博客的特点：**

- **AI 驱动翻译** —— 基于 LLM 的翻译流水线通过 GitHub Actions 自动将每篇文章扩展到多种语言。
- **Google Cloud Text-to-Speech** —— 自动生成文章的音频版本以提高可访问性。
- **XeLaTeX PDF/EPUB 生成** —— 从 Markdown 源生成高质量的可打印 PDF 和电子书导出文件。
- **GitHub Actions CI/CD** —— 自动化构建、测试、翻译和部署工作流。
- **8,000+ 条 AI 回答笔记** —— 从日常 LLM 辅助研究中构建的知识库，可在博客中搜索。
- **MathJax、夜间模式、RSS、双语内容** —— 通过自定义 CSS 和主题增强的标准功能。

**规模：**

| 指标 | 数量 |
|--------|-------|
| 英文文章 | 10,264 |
| 中文文章 | 10,259 |
| AI 回答笔记 | 9,794 |
| Python 脚本 | 323 |
| ML 脚本 | 191 |
| 页面浏览量（过去一个月） | ~70,000 |

![jekyll-ai-blog —— 拥有10K+ 文章、翻译、TTS 和 PDF 流水线的 AI 驱动博客](/assets/images/ai-portfolio/blog.png)

![Cloudflare Web Analytics —— 38.9K 次访问，45.2K 次页面浏览，930ms 加载时间，82% 良好 LCP](/assets/images/ai-portfolio/cloudflare-analytics.png)

GitHub: [lzwjava/jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog)

---

## 🌳 Tree_Of_Thought —— 与一位高中生合作进行思维树推理

[Tree_Of_Thought](https://github.com/Cerynitius/Tree_Of_Thought) 是一个朋友的项目 —— 一个用于物理密集型问题求解的外部思维树推理系统。它不依赖模型在单次不透明的补全中隐藏的思维链，而是将推理过程转化为一个显式、可检查、可控的树，包含实时状态、评分、剪枝和确定性工具支持。

该系统结合了一个用于长时间推理会话的 FastAPI 服务、一个用于检查和剪枝分支的浏览器 UI、一个节点级 FSM 和树调度器、一个用于精确符号计算的 SymPy 支持技能层，以及用于规划、建模、审查和评估的多模型路由。

**我的贡献（1个 PR）：** 添加了一个兼容 OpenAI 的请求器和 `python-dotenv` 配置，使系统能够连接到任何兼容 OpenAI 的端点（本地或云端）。

**背景：** 我指导一名高中生构建了这个系统。在一次会议中，他向我讲解了整个架构 —— 推理树、基于 FSM 的审查、路线-本地增量细化。我把他介绍给了一些 AI 博士研究人员，并帮助他思考研究方向。他现在正在探索使用 LLM 解决物理问题，使用 Codex（GPT-5.4）等工具，并构建多 Agent 协作编码系统。

![思维树 —— 带有节点检查、前沿管理和分支剪枝的终端树浏览器](/assets/images/ai-portfolio/tree-of-thought.jpg)

GitHub: [Cerynitius/Tree_Of_Thought](https://github.com/Cerynitius/Tree_Of_Thought)

---

## 🤖 iclaw —— 终端 AI Agent（REPL）

[iclaw](https://github.com/lzwjava/iclaw) 是一个终端 AI Agent，能够自主编码、搜索和运行命令 —— 可在个人电脑和受严格管控的企业电脑上运行。一个极简的 openclaw 实现，构建为一个纯 Python CLI，无需浏览器扩展或 IDE 插件，由 GitHub Copilot 驱动。

```
lzwjava@lzw-mac iclaw % iclaw

  ██  █████  ██       █████  ██   ██
  ██ ██      ██      ██   ██ ██   ██
  ██ ██      ██      ███████ ██ █ ██
  ██ ██      ██      ██   ██ ██████
  ██  █████  ███████ ██   ██  ███ ██

可用命令：
  /provider_model      选择模型提供商并进行身份验证
  /model               从您的提供商中选择特定模型
  /search              网络搜索（用法：/search <query>）
  /provider_search     选择网络搜索提供商
  /proxy               设置 HTTP/HTTPS 代理（用法：/proxy [url|off]）
  /ca_bundle           设置 HTTPS 的 CA 包（用法：/ca_bundle [path|off]）
  /log                 设置日志详细程度（用法：/log [verbose|info]）
  /copy                将上一条 Copilot 响应复制到剪贴板
  /read                将文件内容打印到终端（用法：/read <path>）
  /clear               清除对话历史
  /compact             使用 LLM 压缩对话历史
  /export              将完整对话历史导出为 JSON 文件
  /status              显示当前设置
  /help                显示可用命令
  /exit                退出 REPL。
```

**主要特性：**

- 在终端中与 **GitHub Copilot 或 OpenRouter** 进行 **多轮对话**。
- **多个模型提供商**：GitHub Copilot（OAuth 设备流）和 OpenRouter（API 密钥）。
- **原生工具调用**：模型自主调用网络搜索、执行 shell 命令和编辑文件 —— 无需人工介入。
- **多个搜索提供商**：DuckDuckGo、Startpage、Bing 和 Tavily。
- **企业友好**：无需 IDE 插件或浏览器扩展。支持在公司防火墙后使用，并支持代理和 CA 包配置。
- **默认模型**：GPT-5.2。

![iclaw —— 具有原生工具调用功能的终端 AI Agent REPL](/assets/images/ai-portfolio/iclaw.jpg)

![iclaw —— 显示自主编码和 shell 命令的执行日志](/assets/images/ai-portfolio/iclaw-log.png)

GitHub: [lzwjava/iclaw](https://github.com/lzwjava/iclaw)

---

## ⚙️ zz —— 数据集处理与训练工具

[zz](https://github.com/lzwjava/zz) 是一个用于 ML 训练流水线的工具集 —— 包含数据集下载、分词、提取和推理工具。在 RunPod H200、DigitalOcean H100 和家庭 RTX 4070 上的 GPT-2 124M 训练运行期间使用。也托管在 [Hugging Face](https://huggingface.co/lzwjava/zz)。

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

- **FineWeb 下载** —— 规划并下载分片以达到 Token 预算（100亿、1000亿+ Token），支持带进度跟踪的断点续传。
- **hf-mirror.com 支持** —— 当 HuggingFace 被屏蔽时，提供用于在中国访问的 wget 脚本。
- **Parquet 提取** —— 通过 pyarrow iter_batches 进行内存安全迭代。
- **分词** —— 将原始文本转换为训练就绪格式。
- **训练分析** —— 从训练日志进行时长计算、指标评估。
- **DeepSeek 推理** —— 用于 DeepSeek-V2-Lite 的 LLM 推理脚本。

![zz on Hugging Face —— 数据集处理与训练工具，22次提交，3位贡献者](/assets/images/ai-portfolio/zz-huggingface.png)

GitHub: [lzwjava/zz](https://github.com/lzwjava/zz) · Hugging Face: [lzwjava/zz](https://huggingface.co/lzwjava/zz)

---

## 🎓 证书

### 机器学习专项课程 —— DeepLearning.AI 与斯坦福大学

2023年11月完成。三门课程：监督式机器学习、高级学习算法、无监督学习、推荐系统、强化学习。

![Coursera 机器学习专项课程证书 —— 李智维，2023年11月](/assets/images/ai-portfolio/coursera-ml-1.png)

### 深度学习专项课程 —— DeepLearning.AI

2023年12月完成。五门课程：神经网络、超参数调优、结构化机器学习项目、卷积神经网络、序列模型。

![Coursera 深度学习专项课程证书 —— 李智维，2023年12月](/assets/images/ai-portfolio/coursera-dl-1.png)

---

- GitHub: [https://github.com/lzwjava](https://github.com/lzwjava)
- 博客: [https://lzwjava.github.io](https://lzwjava.github.io)