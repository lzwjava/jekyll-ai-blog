---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 我的AI作品集——日常AI工作的证据
translated: true
---

我不只是谈论 AI——我每天都在大规模使用它。这篇文章是我的 AI 工作视觉作品集：我构建的工具、消耗的 token 以及获得的认证。

---

## 🖥️ LLM 训练与推理——我的硬件配置

2023 年搭建了我的机器学习工作站，并一直进行训练和学习。

**硬件经验：**

| GPU | VRAM | 经验时长 | 使用场景 |
|-----|------|----------|----------|
| NVIDIA RTX 4070 | 12 GB | 3 年 | 家庭工作站 |
| NVIDIA H200 | 141 GB | 3 个月 | RunPod / DigitalOcean |
| AMD MI300X | 192 GB HBM3 | 3 个月 | AMD Developer Cloud |

**我训练过的模型：**

- **GPT-2 124M** 从零开始在 FineWeb 数据集上训练（nanoGPT）——在 RTX 4070、H200 和 MI300X 上完成。
- **GPT-2 760M** 从零开始在 AMD MI300X（192 GB HBM3）上训练——探索 nanochat、DeepSeek v4 MoE。
- 各种关于超参数调优、学习率调度和数据集预处理的实验。

**工作站：**

![我的机器学习学习站——2023 年搭建，RTX 4070 12GB，用于日常训练和实验](/assets/images/ai-portfolio/learning-station.jpg)

**AMD Developer Cloud — MI300X 192GB HBM3：**

![AMD Dev Cloud — 用于大规模模型训练的 MI300X 实例](/assets/images/ai-portfolio/amd-dev-cloud.png)

---

## 🧠 增强版 nanoGPT——我的分支

Fork 了 [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT) 并扩展了额外的数据集流水线、扩展的训练配置以及用于学习的内联形状注释。45 次提交，2025 年 11 月 – 2026 年 4 月。

**新增的数据集流水线：**

| 数据集 | 路径 | 描述 |
|--------|------|------|
| FineWeb-Edu | `data/fineweb/` | HuggingFace FineWeb-Edu（100 亿+ token）。基于分片的加载、分块处理、增量训练/验证集划分。 |
| OpenWebText 10k | `data/openwebtext_10k/` | 用于快速迭代的 10k 子集。 |
| Wikipedia Local | `data/wikipedia_local/` | 直接对本地纯文本转储进行分词（无需 HuggingFace 下载）。 |

**新增的训练配置：**

| 配置 | 目标 | 备注 |
|------|------|------|
| `train_fineweb.py` | 在 FineWeb 上训练 125M | 针对 RTX 4070 12 GB 调优（n_embd=384, dropout=0.1）。 |
| `train_fineweb1_5b.py` | 在 FineWeb 上训练 1.5B | 适用于 H200 80 GB。 |
| `train_fineweb_gpt3.py` | GPT-3 风格 10B token | 基于分片的加载器，更宽的调度。 |
| `train_fineweb_760m.py` | 在 FineWeb 上训练 760M | 适用于 MI300X 192 GB HBM3。 |
| `train_gpt2_200m.py` | GPT-2 200M | 通用中型配置。 |
| `train_gpt2_200m_smoke.py` | 冒烟测试 | 快速 200M 完整性检查（约几分钟）。 |

**模型更改：**

- **内联张量形状注释** 贯穿 `model.py` 的前向传播（CausalSelfAttention, MLP, GPT）——每一步都显示精确的形状，并附有具体的 GPT-2 XL 示例，例如 `# x: (B, T, C) e.g. (1, 5, 1600)`。有助于理解 Transformer 数据流。

![增强版 nanoGPT——45 次提交，数据集流水线，扩展的训练配置，内联形状注释](/assets/images/ai-portfolio/nanogpt-fork.png)

GitHub: [lzwjava/nanoGPT](https://github.com/lzwjava/nanoGPT)

---

## 📊 LLM API 使用量——数据

### OpenRouter——过去一年

消耗 11.5 亿 token，花费 239 美元，跨多个模型的 API 请求 15.5 万次。

![OpenRouter 活动仪表板——11.5 亿 token，239 美元，一年内 15.5 万次请求](/assets/images/ai-portfolio/openrouter-activity.png)

![OpenRouter 模型花费明细——Claude 4 Sonnet 44.40 美元，Claude 3.5 Sonnet 9.67 美元，Grok 3, Mistral, Kimi](/assets/images/ai-portfolio/openrouter-spend.png)

![OpenRouter 各模型 token 使用量——MiniMax 2.4 亿，Gemini 2.03 亿，DeepSeek 1.1 亿](/assets/images/ai-portfolio/openrouter-models.png)

### 通过 SSSAICode 使用 Claude API——2026 年 4 月

一个月内花费 171.53 美元。2,555 次请求。1.15 亿+ token。缓存命中率 90.9%。

![SSSAICode Claude 使用量——Opus 4.6, Opus 4.7, Sonnet 4.6, Haiku 4.5](/assets/images/ai-portfolio/sssaicode-usage.png)

### 小米 MIMO 订阅——已使用 5 亿 token

Pro 月度计划，主配额 380 亿 + 补偿配额 87.5 亿（约 46 亿免费额度）。目前已消耗 5 亿 token。

![小米 MIMO Pro 计划——已消耗 5 亿 token，剩余约 46 亿免费额度](/assets/images/ai-portfolio/xiaomi-mimo-usage.png)

#### 2026 年 5 月每日 token 使用量

![小米 MIMO 2026 年 5 月——mimo-v2.5、mimo-v2.5-pro、mimo-v2-pro 每日 token 使用详情](/assets/images/ai-portfolio/xiaomi-mimo-may2026.png)

| 日期 | 模型 | 总 token | 输入（缓存命中） | 输入（缓存未命中） | 输出 |
|------|-------|-------------:|-------------------:|--------------------:|-------:|
| 2026-05-31 | mimo-v2.5 | 1,498 | 192 | 943 | 363 |
| 2026-05-31 | mimo-v2.5-pro | 132,198,274 | 128,108,096 | 3,478,691 | 611,487 |
| 2026-05-30 | mimo-v2.5 | 70,745 | 3,200 | 39,429 | 28,116 |
| 2026-05-30 | mimo-v2.5-pro | 124,459,514 | 120,774,848 | 3,111,678 | 572,988 |
| 2026-05-29 | mimo-v2.5-pro | 17,534,693 | 16,141,184 | 1,204,155 | 189,354 |
| 2026-05-28 | mimo-v2.5 | 14,217 | 1,344 | 9,589 | 3,284 |
| 2026-05-28 | mimo-v2.5-pro | 10,946,159 | 8,842,496 | 2,010,722 | 92,941 |
| 2026-05-28 | mimo-v2-pro | 3,389,424 | 2,860,224 | 522,989 | 6,211 |
| 2026-05-27 | mimo-v2.5 | 1,631 | 192 | 945 | 494 |
| 2026-05-27 | mimo-v2.5-pro | 12,646,146 | 12,001,216 | 580,332 | 64,598 |

> mimo-v2.5-pro 占主导地位（5 天内约 3 亿 token）。高缓存命中率（约 96% on mimo-v2.5-pro）保持成本高效。

### 总结

| 平台 | Token | 时间周期 | 费用 |
|----------|--------|--------|------|
| OpenRouter | 11.5 亿 | 过去一年 | 239 美元 |
| SSSAICode (Claude) | 1.15 亿+ | 2026 年 4 月 | 171.53 美元 |
| 小米 MIMO | 5 亿 | 当前计划 | 免费 46 亿额度 |
| 其他 (GitHub Copilot 等) | 5 亿 | 过去一年 | — |
| **总计** | **约 23 亿+** | **过去一年** | **—** |

---

## 🏢 企业 AI 应用——汇丰银行

在汇丰银行（通过 TEKsystems），我在 GitHub Copilot 之上构建了一个自主 AI 代理层，用于自动化脚本编写、日志记录、文档编写和测试。

**我构建的内容：**

- **20 个定制的 AI 代理**——针对不同技术栈和工作流的专用提示和上下文。
- **400 个可复用的 Copilot 编写的脚本**——跨 Java、Spring、Python、Angular 和 DevOps 工具的常见任务自动化。
- **1,100 份 Copilot 编写的指南**——通过 LLM 输出生成并验证的文档，带有缓存和验证。
- **通过 Copilot API 自动生成约 70 个测试用例**——涵盖 Spring Filters、Python unittest、JSON 截断、提示工程和区域端点。

**成果：**

- 在企业范围内，基于 premium 请求量排名 **前 6% 的 Copilot 使用量**。
- 因备受瞩目的 AIPlayer 项目获得 **贡献奖**。
- 加入汇丰内部 AI 社区。

<div align="center">

<img src="/assets/images/ai-portfolio/copilot.png" width="100%" /><img/>

<p><a href="https://marketplace.visualstudio.com/items?itemName=GitHub.copilot">图片出处：GitHub Copilot — Visual Studio Code 市场</a></p>

</div>

![汇丰 AIPlayer 贡献奖](/assets/images/ai-portfolio/aiplayer.jpg)

---

## 🎤 汇丰 AI 讲座——从神经网络到智能代理

在汇丰银行面向 **80 位参与者** 做了一场技术讲座——包括高级顾问、专家、副总监、软件工程师和承包商。

**讲座：** *"从神经网络到智能代理"*——一个从最简单的神经网络（`y = wx`）出发，经过 MNIST、Transformers、GPT、nanoGPT，再到构建个人 AI 代理的旅程。

**我涵盖的内容：**

- 神经网络基本原理——前向传播、反向传播、梯度下降
- Transformer 架构——Q/K/V 注意力、多头注意力、位置编码
- GPT 内部机制——分词、嵌入、训练、生成
- nanoGPT——在 H200/RTX 4070 上从头训练 GPT-2
- LLM 代理——Claude Code、OpenClaw、Hermes、工具调用、代理循环
- 真实数据——消耗 10 亿 token，H200 每小时 3.44 美元，钱到底花在哪
- 我的路径——3 年，从了解 Q/K/V 到从头训练模型

**反馈：**

- 一位初级工程师说：*"你就是我想成为的人"*——这次讲座开阔了他对 AI 可能性的认知
- 高级工程师赞赏这种从基本原理出发的方法——没有炒作，只有数学和代码
- 多次关于训练、代理和职业方向的后续讨论

**幻灯片：** 使用 Claude Code 和 Marp 构建，基于我的公开 AI 回复笔记。

---

## 🛠️ ww——跨平台 CLI 工具集

[ww](https://github.com/lzwjava/ww) 是我的旗舰 CLI 工具集——255+ 次提交，10+ 个命令组，跨平台（macOS + Linux）。涵盖带 AI 提交消息的 git 工作流、笔记管理、图像/PDF 处理、网页搜索、GitHub Copilot 聊天、系统工具和 LLM 驱动的辅助工具。

```
lzwjava@lzw-mac ww % uv run ww --help
用法: ww <group> [command] [options]

Action:
  ww action [workflow.yml]  触发一个 GitHub Actions 工作流

AMD Dev Cloud:
  ww amd-dev-cloud snapshots    列出快照
  ww amd-dev-cloud start-train  创建用于训练的 GPU 实例
  ww amd-dev-cloud end-train    创建快照并销毁 GPU 实例

Copilot:
  ww copilot auth           通过 GitHub OAuth 认证
  ww copilot chat           与 Copilot 模型聊天

Git:
  ww git gpa            对所有仓库执行 git pull --all
  ww git squash <n>     压缩最近 n 次提交
  ww git amend-push     修改最后一次提交并强制推送

LLM:
  ww llm compare <prompt>   比较多个 LLM 响应
  ww llm query <question>   查询本地 RAG 文档

Note:
  ww note              剪贴板内容保存为笔记（快速捕捉）
  ww note process      清空笔记队列
  ww note watch        自动处理守护进程

Screenshot:
  ww screenshot               截屏并创建笔记
  ww screenshot interact-note  交互式截屏笔记

255+ 次提交。10+ 个命令组。跨平台（macOS + Linux）。
```

![ww——跨平台 CLI 工具集 on GitHub](/assets/images/ai-portfolio/ww1.png)

GitHub: [lzwjava/ww](https://github.com/lzwjava/ww)

---

## 📝 jekyll-ai-blog——AI 驱动的博客平台

[jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog) 是 [lzwjava.github.io](https://lzwjava.github.io) 的源码——一个通过 AI 自动化增强的 Jekyll 博客。10,000+ 英文文章，10,000+ 中文文章，9,700+ AI 回答笔记。过去一个月约 70,000 次页面浏览（Cloudflare Analytics）。

```
lzwjava@lzw-mac jekyll-ai-blog % ls README.md
README.md
```

**它与标准 Jekyll 博客的不同之处：**

- **AI 驱动的翻译**——基于 LLM 的翻译流水线，通过 GitHub Actions 自动将每篇文章扩展到多种语言。
- **Google Cloud Text-to-Speech**——自动生成文章的音频版本，增强可访问性。
- **XeLaTeX PDF/EPUB 生成**——从 Markdown 源生成高质量、可打印的 PDF 和电子书导出。
- **GitHub Actions CI/CD**——自动化的构建、测试、翻译和部署工作流。
- **8,000+ AI 回答笔记**——通过日常 LLM 辅助研究构建的知识库，可在博客中搜索。
- **MathJax、夜间模式、RSS、双语内容**——通过自定义 CSS 和主题增强的标准功能。

**规模：**

| 指标 | 数量 |
|--------|-------|
| 英文文章 | 10,264 |
| 中文文章 | 10,259 |
| AI 回答笔记 | 9,794 |
| Python 脚本 | 323 |
| ML 脚本 | 191 |
| 页面浏览（过去一个月） | 约 70,000 |

![jekyll-ai-blog——AI 驱动的博客，拥有 10K+ 文章、翻译、TTS 和 PDF 流水线](/assets/images/ai-portfolio/blog.png)

![Cloudflare 网站分析——38.9K 访问次数，45.2K 页面浏览量，930ms 加载时间，82% 良好的 LCP](/assets/images/ai-portfolio/cloudflare-analytics.png)

GitHub: [lzwjava/jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog)

---

## 🌳 Tree_Of_Thought——与高中生合作“思维树”推理

[Tree_Of_Thought](https://github.com/Cerynitius/Tree_Of_Thought) 是一个朋友的项目——一个用于重物理问题解决的外部“思维树”推理系统。它不依赖于模型在一次不透明的生成中隐藏的思维链，而是将推理转化为一个显式、可检查、可控的树结构，带有实时状态、评分、剪枝和确定性工具支持。

该系统结合了：用于持久推理会话的 FastAPI 服务、用于检查和剪枝分支的浏览器 UI、节点级 FSM 和树调度器、用于精确符号计算的 SymPy 后端技能层，以及用于规划、建模、审查和评估的多模型路由。

**我的贡献（1 个 PR）：** 添加了一个兼容 OpenAI 的请求器和 `python-dotenv` 配置，使系统能够连接到任何兼容 OpenAI 的端点（本地或云端）。

**背景：** 我指导了一名构建该系统的中学生。在一次会议中，他向我展示了完整的架构——推理树、基于 FSM 的审查、路由本地增量优化。我向他介绍了 AI 博士研究员，并帮助他思考研究方向。他现在正在探索使用 LLM 解决物理问题，使用 Codex（GPT-5.4）等工具，并构建多智能体协作编码系统。

![思维树——终端树探索器，具有节点检查、前沿管理和分支剪枝功能](/assets/images/ai-portfolio/tree-of-thought.jpg)

GitHub: [Cerynitius/Tree_Of_Thought](https://github.com/Cerynitius/Tree_Of_Thought)

---

## 🤖 iclaw——终端 AI 代理（REPL）

[iclaw](https://github.com/lzwjava/iclaw) 是一个终端 AI 代理，可以自主编写代码、搜索和执行命令——适用于个人机器和受限制的企业环境。一个极简的 openclaw 实现，构建为纯 Python CLI，无需浏览器扩展或 IDE 插件，由 GitHub Copilot 驱动。

```
lzwjava@lzw-mac iclaw % iclaw

  ██  █████  ██       █████  ██   ██
  ██ ██      ██      ██   ██ ██   ██
  ██ ██      ██      ███████ ██ █ ██
  ██ ██      ██      ██   ██ ██████
  ██  █████  ███████ ██   ██  ███ ██

可用命令：
  /provider_model      选择并认证模型提供商
  /model               从提供商中选择特定模型
  /search              网页搜索（用法：/search <query>）
  /provider_search     选择网页搜索提供商
  /proxy               设置 HTTP/HTTPS 代理（用法：/proxy [url|off]）
  /ca_bundle           设置 HTTPS 的 CA 包（用法：/ca_bundle [path|off]）
  /log                 设置日志级别（用法：/log [verbose|info]）
  /copy                复制上一条 Copilot 响应到剪贴板
  /read                将文件内容打印到终端（用法：/read <path>）
  /clear               清除对话历史
  /compact             使用 LLM 压缩对话历史
  /export              将完整对话历史导出为 JSON 文件
  /status              显示当前设置
  /help                显示可用命令
  /exit                退出 REPL。
```

**关键特性：**

- **多轮对话** 在终端中与 GitHub Copilot 或 OpenRouter 进行。
- **多种模型提供商**：GitHub Copilot（OAuth 设备流）和 OpenRouter（API key）。
- **原生工具调用**：模型自主调用网页搜索、执行 Shell 命令、编辑文件——无需人工干预。
- **多种搜索提供商**：DuckDuckGo、Startpage、Bing 和 Tavily。
- **企业友好**：无需 IDE 插件或浏览器扩展。支持在企业防火墙后使用代理和 CA 包。
- **默认模型**：GPT-5.2。

![iclaw——带有原生工具调用的终端 AI 代理 REPL](/assets/images/ai-portfolio/iclaw.jpg)

![iclaw——显示自主编码和 Shell 命令的执行日志](/assets/images/ai-portfolio/iclaw-log.png)

GitHub: [lzwjava/iclaw](https://github.com/lzwjava/iclaw)

---

## ⚙️ zz——数据集处理与训练工具

[zz](https://github.com/lzwjava/zz) 是一个用于 ML 训练流水线的工具集——数据集下载、分词、提取和推理工具。用于 RunPod H200、DigitalOcean H100 和家庭 RTX 4070 上的 GPT-2 124M 训练运行。也托管在 [Hugging Face](https://huggingface.co/lzwjava/zz)。

```
lzwjava@lzw-mac zz % tree -L 1
scripts/
  download/     # 数据集下载脚本 (FineWeb, Wikimedia, HF mirrors)
  extract/      # 数据提取、分词和重命名
  analysis/     # 训练时长和指标评估
  deepseek/     # LLM 推理脚本 (DeepSeek-V2-Lite)
logs/           # 训练日志和输出
datasets/       # 下载的数据集存储
```

**关键能力：**

- **FineWeb 下载**——规划并下载分片以达到 token 预算（10B、100B+ token），可中断恢复并带有进度追踪。
- **hf-mirror.com 支持**——当 HuggingFace 被屏蔽时提供 wget 脚本用于中国访问。
- **Parquet 提取**——通过 pyarrow iter_batches 进行内存安全的迭代。
- **分词**——将原始文本转换为训练就绪格式。
- **训练分析**——从训练日志计算时长和指标评估。
- **DeepSeek 推理**——用于 DeepSeek-V2-Lite 的 LLM 推理脚本。

![zz on Hugging Face——数据集处理与训练工具，22 次提交，3 位贡献者](/assets/images/ai-portfolio/zz-huggingface.png)

GitHub: [lzwjava/zz](https://github.com/lzwjava/zz) · Hugging Face: [lzwjava/zz](https://huggingface.co/lzwjava/zz)

---

## 🎓 证书

### 机器学习专项课程——DeepLearning.AI 与斯坦福大学

2023 年 11 月完成。三门课程：监督式机器学习、高级学习算法、无监督学习、推荐系统、强化学习。

![Coursera 机器学习专项课程证书——李智维，2023 年 11 月](/assets/images/ai-portfolio/coursera-ml-1.png)

### 深度学习专项课程——DeepLearning.AI

2023 年 12 月完成。五门课程：神经网络、超参数调优、结构化机器学习项目、卷积神经网络、序列模型。

![Coursera 深度学习专项课程证书——李智维，2023 年 12 月](/assets/images/ai-portfolio/coursera-dl-1.png)

---

- GitHub: [https://github.com/lzwjava](https://github.com/lzwjava)
- 博客: [https://lzwjava.github.io](https://lzwjava.github.io)
