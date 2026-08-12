---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 我的AI作品集——日常AI工作证据
translated: true
---

我不仅仅谈论AI——我每天都在大规模使用它。这篇文章是我的AI成果视觉作品集：我构建的工具、消耗的token以及获得的认证。

---

## 🖥️ LLM训练与推理——我的硬件设置

2023年搭建了我的机器学习工作站，并从此持续训练和学习。

**硬件经验：**

| GPU | VRAM | 经验时间 | 位置 |
| ----- | ------ | ------------ | ------- |
| NVIDIA RTX 4070 | 12 GB | 3年 | 家庭工作站 |
| NVIDIA H200 | 141 GB | 3个月 | RunPod / DigitalOcean |
| AMD MI300X | 192 GB HBM3 | 3个月 | AMD Developer Cloud |

**我训练过的内容：**

- **GPT-2 124M** 从头开始，在FineWeb数据集上（nanoGPT）——在RTX 4070、H200和MI300X上。
- **GPT-2 760M** 从头开始，在AMD MI300X（192 GB HBM3）上——探索nanochat、DeepSeek v4 MoE。
- 各种超参数调优、学习率调度和数据集预处理的实验。

**工作站：**

![我的ML学习工作站——2023年搭建，RTX 4070 12GB，用于日常训练和实验](/assets/images/ai-portfolio/learning-station.jpg)

**AMD Developer Cloud — MI300X 192GB HBM3：**

![AMD Dev Cloud — 用于大规模模型训练的MI300X实例](/assets/images/ai-portfolio/amd-dev-cloud.png)

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
| 11 | codeparrot-d12 | nanochat | 286M | RTX 4070 | ? | 仅脚本 |
| 12 | Notes SFT (Qwen3-4B) | trl/peft | 4B | RTX 4070 | ? | 仅脚本 |
| 13 | SPGISpeech (Whisper) | transformers | 变化 | ? | ? | 仅脚本 |

## 🧠 增强版nanoGPT——我的分支

Fork了[karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)并扩展了额外的数据集管道、规模化训练配置以及用于学习的内联形状注释。45次提交，2025年11月 – 2026年4月。

**新增数据集管道：**

| 数据集 | 路径 | 描述 |
| --------- | ------ | ------------- |
| FineWeb-Edu | `data/fineweb/` | HuggingFace FineWeb-Edu（100亿+ token）。基于分片的加载，分块处理，增量训练/验证分割。 |
| OpenWebText 10k | `data/openwebtext_10k/` | 快速10k子集用于快速迭代。 |
| Wikipedia Local | `data/wikipedia_local/` | 直接对本地纯文本转储进行分词（无需HuggingFace下载）。 |

**新增训练配置：**

| 配置 | 目标 | 备注 |
| -------- | -------- | ------- |
| `train_fineweb.py` | 125M在FineWeb上 | 针对RTX 4070 12 GB优化（n_embd=384, dropout=0.1）。 |
| `train_fineweb1_5b.py` | 1.5B在FineWeb上 | 用于H200 80 GB。 |
| `train_fineweb_gpt3.py` | GPT-3风格100亿token | 基于分片的加载器，更宽的调度。 |
| `train_fineweb_760m.py` | 760M在FineWeb上 | 用于MI300X 192 GB HBM3。 |
| `train_gpt2_200m.py` | GPT-2 200M | 通用中规模配置。 |
| `train_gpt2_200m_smoke.py` | 烟雾测试 | 快速200M合理性检查（约几分钟）。 |

**模型变更：**

- **内联张量形状注释** 遍布 `model.py` 的前向传播（CausalSelfAttention, MLP, GPT）——显示每一步的精确形状，并附有具体GPT-2 XL示例，例如 `# x: (B, T, C) e.g. (1, 5, 1600)`。有助于理解Transformer数据流。

![增强版nanoGPT——45次提交，数据集管道，规模化训练配置，内联形状注释](/assets/images/ai-portfolio/nanogpt-fork.png)

GitHub: [lzwjava/nanoGPT](https://github.com/lzwjava/nanoGPT)

---

## 📝 SEC-EDGAR-GPT — 基于SEC文件从头训练的GPT-2 (124M)

在**1.55B token**的SEC EDGAR金融文件（10-K、10-Q及其他公司披露）上从头训练了一个**124M参数的GPT-2**——在单个**RTX 4070**（12 GB VRAM）上训练约8小时，收敛到验证损失2.28。

该模型能生成令人信服的SEC模板——风险因素、MD&A章节、业务描述——并通过RunPod上的FastAPI服务器部署为交互式聊天。

整个项目——模型训练、论文、聊天机器人和网站——在**3天内使用Hermes Agent**构建，展示了AI代理如何使LLM研究变得易于访问。

在全球银行内部共享后，该项目获得了**200+次内部浏览**。一位首席工程师留下了评论，称之为*“不错”*。此外，受一位朋友在循环Transformer方面的工作启发，该项目让我思考如何将金融token与自然语言token区别对待，以提高生成准确性。

![SEC-EDGAR-GPT聊天机器人](/assets/images/sec-edgar-gpt/chatbot_web.png)

**代码：** [github.com/lzwjava/sec-edgar-gpt](https://github.com/lzwjava/sec-edgar-gpt) · **论文：** [sec-edgar-gpt.pdf](https://github.com/lzwjava/sec-edgar-gpt/raw/main/sec-edgar-gpt.pdf) · **模型：** [Hugging Face](https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf) · **聊天：** [sec-edgar-gpt.lzwjava.workers.dev](https://sec-edgar-gpt.lzwjava.workers.dev/)

---

## 📊 LLM API使用量——数据

### OpenRouter — 过去一年

消耗1.15B token，花费239美元，跨多个模型共155K次API请求。

![OpenRouter活动仪表盘——1.15B token，239美元花费，1年内155K次请求](/assets/images/ai-portfolio/openrouter-activity.png)

![OpenRouter模型花费细分——Claude 4 Sonnet 44.40美元，Claude 3.5 Sonnet 9.67美元，Grok 3，Mistral，Kimi](/assets/images/ai-portfolio/openrouter-spend.png)

![OpenRouter按模型划分的Token使用量——MiniMax 240M，Gemini 203M，DeepSeek 110M](/assets/images/ai-portfolio/openrouter-models.png)

### Claude API via SSSAICode — 2026年4月

一个月内171.53美元。2,555次请求。1.15亿+ token。90.9%缓存命中率。

![SSSAICode Claude使用量——Opus 4.6，Opus 4.7，Sonnet 4.6，Haiku 4.5](/assets/images/ai-portfolio/sssaicode-usage.png)

### 小米MIMO订阅——已使用12.5亿Token

Pro月度计划，包含38B主配额 + 8.75B补偿配额（约4.6B免费额度）。2026年5月至6月期间**消耗了1.25B token**。

![小米MIMO Pro计划——已消耗1.25B token，剩余约3.4B免费额度](/assets/images/ai-portfolio/xiaomi-mimo-usage.png)

#### 月度Token使用量细分

| 月份 | 模型 | 总Token数 | 输入（缓存命中） | 输入（缓存未命中） | 输出 | 请求数 |
| ------- | ------- | -------------: | -------------------: | --------------------: | -------: | ---------: |
| 2026-06 | mimo-v2.5 | 285,179 | 36,416 | 143,556 | 105,207 | 78 |
| 2026-06 | mimo-v2.5-pro | 734,873,374 | 710,036,672 | 21,617,131 | 3,219,571 | 10,704 |
| 2026-05 | mimo-v2.5 | 91,203 | 5,312 | 52,908 | 32,983 | 27 |
| 2026-05 | mimo-v2.5-pro | 508,851,211 | 488,291,136 | 17,725,731 | 2,834,344 | 8,649 |
| 2026-05 | mimo-v2-pro | 3,571,328 | 3,021,568 | 539,357 | 10,403 | 167 |

**月度合计：** 2026年5月：**512.5M token**（8,843次请求）· 2026年6月：**735.2M token**（10,782次请求）

> mimo-v2.5-pro占主导地位（约占总量的96%）。mimo-v2.5-pro的缓存命中率约96.7%，保持了成本效益。6月Token量较5月增长43.5%。

### 总结

| 平台 | Token数 | 时间段 | 成本 |
| ---------- | -------- | -------- | ------ |
| OpenRouter | 1.15B | 过去一年 | 239美元 |
| SSSAICode (Claude) | 1.15亿+ | 2026年4月 | 171.53美元 |
| 小米MIMO | 1.25B | 2026年5月–6月 | 免费4.6B额度 |
| 其他（GitHub Copilot等） | 500M | 过去一年 | — |
| **总计** | **~3.0B+** | **过去一年** | **—** |

---

## 🏢 企业级AI使用——在英国环球银行

在一家英国环球银行（通过一家全球IT外包公司），我在编码助手之上构建了一个自主AI代理层，用于自动化脚本编写、日志记录、文档编制和测试。

**我构建的内容：**

- **20个定制化AI代理**——针对不同技术栈和工作流设置了专用提示词和上下文。
- **400个由编码助手编写的可重用脚本**——针对Java、Spring、Python、Angular和DevOps工具的常见任务自动化。
- **1,800份由编码助手编写的指南**——由AI生成、人工提示的文档。
- **通过编码助手API自动生成约70个测试用例**——涵盖Spring Filters、Python unittest、JSON截断、提示工程和区域端点。

**结果：**

- 在整个企业的编码助手使用量中排名**前6%**（按高级请求衡量）。
- 因备受瞩目的AIPlayer项目获得**贡献奖**。
- 加入了银行的内部AI社区。

![AIPlayer贡献奖](/assets/images/ai-portfolio/aiplayer.jpg)

---

## 🎤 AI讲座——从神经网络到代理

在英国环球银行向**80名参与者**进行了一场技术讲座——包括高级顾问、专家、副总监、软件工程师和承包商。

**讲座主题：** *"从神经网络到代理"*——从最简单的神经网络（`y = wx`）出发，经过MNIST、Transformer、GPT、nanoGPT，再到构建个人AI代理。

**涵盖内容：**

- 从基本原理出发的神经网络——前向传播、反向传播、梯度下降
- Transformer架构——Q/K/V注意力、多头注意力、位置编码
- GPT内部机制——分词、嵌入、训练、生成
- nanoGPT——在H200/RTX 4070上从头训练GPT-2
- LLM代理——Claude Code、OpenClaw、Hermes、工具调用、代理循环
- 真实数据——消耗1B token，H200每小时3.44美元，资金实际流向
- 我的路径——从阅读Q/K/V到从头训练模型，历时3年

**反馈：**

- 一位初级工程师说：*"你就是我想成为的人"*——讲座让他开阔了AI可能性的眼界
- 高级工程师赞赏从第一性原理出发的方法——没有炒作，只有数学和代码
- 多次关于训练、代理和职业方向的后续讨论

**幻灯片：** 使用Claude Code & Marp基于我的公开AI回答笔记构建。

幻灯片（Marp）：[PDF](/assets/marp/neural_networks_to_agents_public.pdf)

---

## 🛠️ ww——跨平台CLI工具包

[ww](https://github.com/lzwjava/ww) 是我的旗舰CLI工具包——255+次提交，10+个命令组，跨平台（macOS + Linux）。涵盖带有AI提交信息的Git工作流、笔记管理、图像/PDF处理、网页搜索、GitHub Copilot聊天、系统实用程序和LLM驱动的助手。

```
lzwjava@lzw-mac ww % uv run ww --help
用法: ww <group> [command] [options]

Action:
  ww action [workflow.yml]  触发 GitHub Actions 工作流

AMD Dev Cloud:
  ww amd-dev-cloud snapshots    列出快照
  ww amd-dev-cloud start-train  创建用于训练的GPU实例
  ww amd-dev-cloud end-train    快照并销毁GPU实例

Copilot:
  ww copilot auth           通过GitHub OAuth进行身份验证
  ww copilot chat           与Copilot模型聊天

Git:
  ww git gpa            对所有仓库执行 git pull --all
  ww git squash <n>     压缩最近n次提交
  ww git amend-push     修改最后一次提交并强制推送

LLM:
  ww llm compare <prompt>   比较多个LLM响应
  ww llm query <question>   查询本地RAG文档

Note:
  ww note              剪贴板内容到笔记（快速捕获）
  ww note process      清空笔记队列
  ww note watch        自动处理守护进程

Screenshot:
  ww screenshot               截图并创建笔记
  ww screenshot interact-note 交互式截图笔记

255+次提交。10+个命令组。跨平台（macOS + Linux）。
```

![ww — GitHub上的跨平台CLI工具包](/assets/images/ai-portfolio/ww1.png)

GitHub: [lzwjava/ww](https://github.com/lzwjava/ww)

---

## 📝 jekyll-ai-blog——AI驱动的博客平台

[jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog) 是 [lzwjava.github.io](https://lzwjava.github.io) 的源代码——一个通过AI自动化增强的Jekyll博客。10,000+篇英文文章，10,000+篇中文文章，9,700+条AI回答笔记。过去一个月约70,000次页面浏览量（Cloudflare Analytics）。

```
lzwjava@lzw-mac jekyll-ai-blog % ls README.md
README.md
```

**与标准Jekyll博客的不同之处：**

- **AI驱动的翻译**——基于LLM的翻译管道，通过GitHub Actions自动将每篇文章扩展到多种语言。
- **Google Cloud Text-to-Speech**——为无障碍访问自动生成文章的音频版本。
- **XeLaTeX PDF/EPUB生成**——从Markdown源生成高质量的可打印PDF和电子书导出。
- **GitHub Actions CI/CD**——自动化的构建、测试、翻译和部署工作流。
- **8,000+条AI回答笔记**——基于日常LLM辅助研究构建的知识库，可在博客中搜索。
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

![jekyll-ai-blog——AI驱动的博客，拥有10K+文章、翻译、TTS和PDF管道](/assets/images/ai-portfolio/blog.png)

![Cloudflare Web Analytics——38.9K访问量，45.2K页面浏览量，930ms加载时间，82%良好LCP](/assets/images/ai-portfolio/cloudflare-analytics.png)

GitHub: [lzwjava/jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog)

---

## 🤖 iclaw——终端AI代理（REPL）

[iclaw](https://github.com/lzwjava/iclaw) 是一个终端AI代理，可以自主编码、搜索和运行命令——适用于个人机器和受限制的企业机器。一个最小化的openclaw实现，作为纯Python CLI构建，无需浏览器扩展或IDE插件，由GitHub Copilot驱动。

```
lzwjava@lzw-mac iclaw % iclaw

  ██  █████  ██       █████  ██   ██
  ██ ██      ██      ██   ██ ██   ██
  ██ ██      ██      ███████ ██ █ ██
  ██ ██      ██      ██   ██ ██████
  ██  █████  ███████ ██   ██  ███ ██

可用命令：
  /provider_model      选择模型提供商并进行身份验证
  /model               从你的提供商选择特定模型
  /search              网页搜索（用法: /search <query>）
  /provider_search     选择网页搜索提供商
  /proxy               设置HTTP/HTTPS代理（用法: /proxy [url|off]）
  /ca_bundle           设置HTTPS的CA证书包（用法: /ca_bundle [path|off]）
  /log                 设置日志详细程度（用法: /log [verbose|info]）
  /copy                将最后一条Copilot响应复制到剪贴板
  /read                将文件内容打印到终端（用法: /read <path>）
  /clear               清除对话历史
  /compact             使用LLM压缩对话历史
  /export              将完整对话历史导出为JSON文件
  /status              显示当前设置
  /help                显示可用命令
  /exit                退出REPL。
```

**主要功能：**

- **多轮对话** 与GitHub Copilot或OpenRouter在终端中。
- **多个模型提供商**：GitHub Copilot（OAuth设备流）和OpenRouter（API密钥）。
- **原生工具调用**：模型自主调用网页搜索、执行shell命令和编辑文件——无需人工介入。
- **多个搜索提供商**：DuckDuckGo、Startpage、Bing和Tavily。
- **企业友好**：无需IDE插件或浏览器扩展。支持代理和CA证书包，可在企业防火墙后工作。
- **默认模型**：GPT-5.2。

![iclaw——带有原生工具调用的终端AI代理REPL](/assets/images/ai-portfolio/iclaw.jpg)

![iclaw——显示自主编码和shell命令的执行日志](/assets/images/ai-portfolio/iclaw-log.png)

GitHub: [lzwjava/iclaw](https://github.com/lzwjava/iclaw)

---

## ⚙️ zz——数据集处理与训练工具

[zz](https://github.com/lzwjava/zz) 是一个用于ML训练管道的工具包——数据集下载、分词、提取和推理工具。在GPT-2 124M训练运行期间使用，运行于RunPod H200、DigitalOcean H100和家庭RTX 4070。也托管在 [Hugging Face](https://huggingface.co/lzwjava/zz) 上。

```
lzwjava@lzw-mac zz % tree -L 1
scripts/
  download/     # 数据集下载脚本（FineWeb, Wikimedia, HF镜像）
  extract/      # 数据提取、分词和重命名
  analysis/     # 训练持续时间和指标评估
  deepseek/     # LLM推理脚本（DeepSeek-V2-Lite）
logs/           # 训练日志和输出
datasets/       # 下载的数据集存储
```

**主要能力：**

- **FineWeb下载**——规划并下载分片以达到Token预算（10B, 100B+ token），可续传并带有进度跟踪。
- **支持hf-mirror.com**——当HuggingFace被屏蔽时，为中国用户提供wget脚本。
- **Parquet提取**——通过pyarrow iter_batches进行内存安全迭代。
- **分词**——将原始文本转换为训练就绪格式。
- **训练分析**——从训练日志计算持续时间、评估指标。
- **DeepSeek推理**——DeepSeek-V2-Lite的LLM推理脚本。

![zz on Hugging Face——数据集处理与训练工具，22次提交，3位贡献者](/assets/images/ai-portfolio/zz-huggingface.png)

GitHub: [lzwjava/zz](https://github.com/lzwjava/zz) · Hugging Face: [lzwjava/zz](https://huggingface.co/lzwjava/zz)

---

## 🎓 证书

### 机器学习专项课程 — DeepLearning.AI & Stanford University

2023年11月完成。三门课程：监督式机器学习、高级学习算法、无监督学习、推荐系统、强化学习。

![Coursera机器学习专项课程证书——李智维，2023年11月](/assets/images/ai-portfolio/coursera-ml-1.png)

### 深度学习专项课程 — DeepLearning.AI

2023年12月完成。五门课程：神经网络、超参数调优、结构化机器学习项目、CNN、序列模型。

![Coursera深度学习专项课程证书——李智维，2023年12月](/assets/images/ai-portfolio/coursera-dl-1.png)

---

- GitHub: [https://github.com/lzwjava](https://github.com/lzwjava)
- 博客: [https://lzwjava.github.io](https://lzwjava.github.io)

---

AI翻译提示：British Universal Bank(英国环球银行)。