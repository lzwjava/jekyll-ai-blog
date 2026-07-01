---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 我的AI作品集 — 日常AI工作的证明
translated: true
---

我不只是谈论AI——我每天都在大规模地使用它。这篇文章是我AI工作的视觉作品集：我构建的工具、我消耗的Token，以及我获得的认证。

---

## 🖥️ LLM训练与推理——我的硬件设置

2023年搭建了我的机器学习工作站，并一直进行训练和学习至今。

**硬件经验：**

| GPU | 显存 | 经验时长 | 使用场景 |
| ----- | ------ | ---------- | ---------- |
| NVIDIA RTX 4070 | 12 GB | 3年 | 家庭工作站 |
| NVIDIA H200 | 141 GB | 3个月 | RunPod / DigitalOcean |
| AMD MI300X | 192 GB HBM3 | 3个月 | AMD Developer Cloud |

**我训练过的内容：**

- **GPT-2 124M** 从头开始在FineWeb数据集上训练（nanoGPT）—— 在RTX 4070、H200和MI300X上完成。
- **GPT-2 760M** 从头开始在AMD MI300X（192 GB HBM3）上训练 —— 探索了nanochat、DeepSeek v4 MoE。
- 各种超参数调优、学习率调度和数据集预处理的实验。

**工作站：**

![我的机器学习学习工作站——2023年搭建，RTX 4070 12GB，日常训练和实验使用](/assets/images/ai-portfolio/learning-station.jpg)

**AMD Developer Cloud —— MI300X 192GB HBM3：**

![AMD Dev Cloud —— 用于大规模模型训练的MI300X实例](/assets/images/ai-portfolio/amd-dev-cloud.png)

---

## 🧠 增强版nanoGPT —— 我的分支

Fork了 [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT) 并扩展了额外的数据集管道、扩展的训练配置以及用于学习的内联形状注释。45次提交，2025年11月 – 2026年4月。

**新增数据集管道：**

| 数据集 | 路径 | 描述 |
| -------- | ------ | ------ |
| FineWeb-Edu | `data/fineweb/` | HuggingFace FineWeb-Edu（100亿+ Token）。基于分片的加载、分块处理、增量训练/验证集划分。 |
| OpenWebText 10k | `data/openwebtext_10k/` | 快速10k子集，用于快速迭代。 |
| Wikipedia Local | `data/wikipedia_local/` | 直接对本地纯文本dump进行分词（无需HuggingFace下载）。 |

**新增的训练配置：**

| 配置 | 目标 | 备注 |
| ------ | ------ | ------ |
| `train_fineweb.py` | 125M on FineWeb | 针对RTX 4070 12 GB调优（n_embd=384，dropout=0.1）。 |
| `train_fineweb1_5b.py` | 1.5B on FineWeb | 用于H200 80 GB。 |
| `train_fineweb_gpt3.py` | GPT-3风格100亿Token | 基于分片的加载器，更宽的调度。 |
| `train_fineweb_760m.py` | 760M on FineWeb | 用于MI300X 192 GB HBM3。 |
| `train_gpt2_200m.py` | GPT-2 200M | 通用中型配置。 |
| `train_gpt2_200m_smoke.py` | 冒烟测试 | 快速200M sanity检查（约几分钟）。 |

**模型改动：**

- **内联张量形状注释** 贯穿 `model.py` 的前向传播（CausalSelfAttention， MLP, GPT） —— 每一步都展示具体形状，并附带具体的GPT-2 XL示例，例如 `# x: (B, T, C) e.g. (1, 5, 1600)`。有助于理解Transformer数据流。

![增强版nanoGPT —— 45次提交，数据集管道，扩展训练配置，内联形状注释](/assets/images/ai-portfolio/nanogpt-fork.png)

GitHub: [lzwjava/nanoGPT](https://github.com/lzwjava/nanoGPT)

---

## 📝 SEC-EDGAR-GPT —— 基于SEC文件从头训练的GPT-2（124M）

从头开始在 **15.5亿Token** 的SEC EDGAR财务文件（10-K，10-Q及其他公司披露文件）上训练了一个 **1.24亿参数的GPT-2** —— 在单个 **RTX 4070**（12 GB显存）上训练了约8小时，验证损失收敛到2.28。

该模型能生成令人信服的SEC模板文本 —— 风险因素、MD&A部分、业务描述 —— 并通过RunPod上的FastAPI服务器部署用于交互式聊天。

整个项目 —— 模型训练、论文、聊天机器人和网站 —— 在 **3天内使用Hermes Agent** 构建完成，展示了AI Agent如何让LLM研究变得可及。

该项目在全球性银行内部共享后，获得了 **200+次内部浏览**。一位首席工程师留下了评论，称其为 *"nice"*。此外，受一位朋友在循环Transformer方面工作的启发，这个项目让我开始思考将金融Token与自然语言Token区别对待，以提高生成准确性。

![SEC-EDGAR-GPT 聊天机器人](/assets/images/sec-edgar-gpt/chatbot_web.png)

**代码：** [github.com/lzwjava/sec-edgar-gpt](https://github.com/lzwjava/sec-edgar-gpt) · **论文：** [sec-edgar-gpt.pdf](https://github.com/lzwjava/sec-edgar-gpt/raw/main/sec-edgar-gpt.pdf) · **模型：** [Hugging Face](https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf) · **聊天：** [sec-edgar-gpt.lzwjava.workers.dev](https://sec-edgar-gpt.lzwjava.workers.dev/)

---

## 📊 LLM API使用情况 —— 数据

### OpenRouter —— 过去一年

消耗11.5亿Token，花费239美元，跨多个模型共155K次API请求。

![OpenRouter活动面板 —— 1.15B Token，$239消费，1年内155K请求](/assets/images/ai-portfolio/openrouter-activity.png)

![OpenRouter按模型消费细分 —— Claude 4 Sonnet $44.40，Claude 3.5 Sonnet $9.67，Grok 3，Mistral，Kimi](/assets/images/ai-portfolio/openrouter-spend.png)

![OpenRouter按模型Token使用量 —— MiniMax 240M，Gemini 203M，DeepSeek 110M](/assets/images/ai-portfolio/openrouter-models.png)

### 通过SSSAICode使用的Claude API —— 2026年4月

一个月内花费171.53美元。2,555次请求。1.15亿+ Token。缓存命中率90.9%。

![SSSAICode Claude使用情况 —— Opus 4.6，Opus 4.7，Sonnet 4.6，Haiku 4.5](/assets/images/ai-portfolio/sssaicode-usage.png)

### 小米MIMO订阅 —— 已使用12.5亿Token

Pro月度计划，主配额380亿+补偿配额87.5亿（约46亿免费额度）。**2026年5月至6月消耗12.5亿Token**。

![小米MIMO Pro计划 —— 消耗1.25B Token，剩余约3.4B免费额度](/assets/images/ai-portfolio/xiaomi-mimo-usage.png)

#### 月度Token使用量细分

| 月份 | 模型 | 总Token | 输入（缓存命中） | 输入（缓存未命中） | 输出 | 请求数 |
| ------ | ------ | ---------: | ------------------: | --------------------: | -----: | ------: |
| 2026-06 | mimo-v2.5 | 285,179 | 36,416 | 143,556 | 105,207 | 78 |
| 2026-06 | mimo-v2.5-pro | 734,873,374 | 710,036,672 | 21,617,131 | 3,219,571 | 10,704 |
| 2026-05 | mimo-v2.5 | 91,203 | 5,312 | 52,908 | 32,983 | 27 |
| 2026-05 | mimo-v2.5-pro | 508,851,211 | 488,291,136 | 17,725,731 | 2,834,344 | 8,649 |
| 2026-05 | mimo-v2-pro | 3,571,328 | 3,021,568 | 539,357 | 10,403 | 167 |

**月度总计：** 2026年5月：**5.125亿Token**（8,843次请求）· 2026年6月：**7.352亿Token**（10,782次请求）

> mimo-v2.5-pro 占主导地位（约占总量的96%）。mimo-v2.5-pro上的缓存命中率约为96.7%，保持了成本效率。6月与5月相比，Token量增长了43.5%。

### 摘要

| 平台 | Token数 | 周期 | 成本 |
| -------- | --------- | ------ | ------ |
| OpenRouter | 11.5亿 | 过去一年 | $239 |
| SSSAICode (Claude) | 1.15亿+ | 2026年4月 | $171.53 |
| 小米MIMO | 12.5亿 | 2026年5-6月 | 46亿免费额度 |
| 其他（GitHub Copilot等） | 5亿 | 过去一年 | — |
| **总计** | **约30亿+** | **过去一年** | **—** |

---

## 🏢 企业级AI使用 —— 汇丰银行

在汇丰银行（通过TEKsystems），我在GitHub Copilot之上构建了一个自主AI Agent层，用于自动化脚本编写、日志记录、文档编写和测试。

**我构建的内容：**

- **20个定制化AI Agent** —— 针对不同技术栈和工作流的专用提示词和上下文。
- **400个可复用的Copilot编写脚本** —— 针对Java、Spring、Python、Angular和DevOps工具的常见任务自动化。
- **1,100份Copilot编写的指南** —— 通过LLM输出生成并验证的文档，带有缓存和验证。
- **约70个自动生成的测试用例** —— 通过Copilot API生成，涵盖Spring Filter、Python unittest、JSON截断、提示词工程和区域端点。

**结果：**

- 在企业整体Copilot使用量中排名 **前6%**（按高级请求衡量）。
- 因备受关注的项目AIPlayer获得 **贡献奖**。
- 加入汇丰内部AI社区。

<div align="center">

<img src="/assets/images/ai-portfolio/copilot.png" width="100%" /><img/>

<p><a href="https://marketplace.visualstudio.com/items?itemName=GitHub.copilot">图片来源：GitHub Copilot —— Visual Studio Code Marketplace</a></p>

</div>

![汇丰AIPlayer贡献奖](/assets/images/ai-portfolio/aiplayer.jpg)

---

## 🎤 汇丰AI演讲 —— 从神经网络到Agent

在汇丰银行向 **80位参与者** 进行了技术演讲 —— 高级顾问、专家、副总监、软件工程师和承包商。

**演讲：** *"从神经网络到Agent"* —— 从最简单的神经网络（`y = wx`）出发，经过MNIST、Transformer、GPT、nanoGPT，到构建个人AI Agent的旅程。

**我涵盖的内容：**

- 神经网络基本原理 —— 前向传播、反向传播、梯度下降
- Transformer架构 —— Q/K/V注意力、多头注意力、位置编码
- GPT内部机制 —— 分词、嵌入、训练、生成
- nanoGPT —— 在H200/RTX 4070上从头训练GPT-2
- LLM Agent —— Claude Code、OpenClaw、Hermes、工具调用、Agent循环
- 真实数据 —— 10亿Token消耗，H200每小时3.44美元，钱到底花在哪里
- 我的路线 —— 从阅读Q/K/V到从头训练模型，历时3年

**反馈：**

- 一位初级工程师说：*"你就是我想成为的人"* —— 这次演讲让他看到了AI的可能性
- 高级工程师赞赏基于第一性原理的方法 —— 没有炒作，只有数学和代码
- 多次后续对话，涉及训练、Agent和职业方向

**幻灯片：** 使用Claude Code和Marp构建，基于我的公开AI回答笔记。

幻灯片（Marp）：[PDF](/assets/marp/neural_networks_to_agents_public.pdf)

---

## 🛠️ ww —— 跨平台CLI工具包

[ww](https://github.com/lzwjava/ww) 是我的旗舰CLI工具包——255+次提交，10+个命令组，跨平台（macOS + Linux）。它涵盖了带AI提交信息的Git工作流、笔记管理、图片/PDF处理、网页搜索、GitHub Copilot聊天、系统工具和LLM辅助功能。

```
lzwjava@lzw-mac ww % uv run ww --help
Usage: ww <group> [command] [options]

Action:
  ww action [workflow.yml]  触发GitHub Actions工作流

AMD Dev Cloud:
  ww amd-dev-cloud snapshots    列出快照
  ww amd-dev-cloud start-train  创建用于训练的GPU云主机
  ww amd-dev-cloud end-train    创建快照并销毁GPU云主机

Copilot:
  ww copilot auth           通过GitHub OAuth认证
  ww copilot chat           与Copilot模型聊天

Git:
  ww git gpa            对所有仓库执行git pull --all
  ww git squash <n>     压缩最近n次提交
  ww git amend-push     修改最近一次提交并强制推送

LLM:
  ww llm compare <prompt>   比较多个LLM的回答
  ww llm query <question>   查询本地RAG文档

Note:
  ww note              剪贴板内容存为笔记（快速捕获）
  ww note process      清空笔记队列
  ww note watch        自动处理守护进程

Screenshot:
  ww screenshot              截屏并创建笔记
  ww screenshot interact-note  交互式截图笔记

255+次提交。10+个命令组。跨平台（macOS + Linux）。
```

![ww —— 跨平台CLI工具包（GitHub）](/assets/images/ai-portfolio/ww1.png)

GitHub: [lzwjava/ww](https://github.com/lzwjava/ww)

---

## 📝 jekyll-ai-blog —— AI驱动的博客平台

[jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog) 是 [lzwjava.github.io](https://lzwjava.github.io) 的源代码 —— 一个由AI自动化增强的Jekyll博客。10,000+篇英文文章，10,000+篇中文文章，9,700+条AI回答笔记。过去一个月约70,000次页面浏览量（Cloudflare Analytics）。

```
lzwjava@lzw-mac jekyll-ai-blog % ls README.md
README.md
```

**它与标准Jekyll博客的不同之处：**

- **AI驱动的翻译** —— 基于LLM的翻译管道，通过GitHub Actions自动将每篇文章扩展到多种语言。
- **Google Cloud Text-to-Speech** —— 自动生成文章的音频版本，用于无障碍访问。
- **XeLaTeX PDF/EPUB生成** —— 从Markdown源生成高质量的可打印PDF和电子书导出。
- **GitHub Actions CI/CD** —— 自动构建、测试、翻译和部署工作流。
- **8,000+条AI回答笔记** —— 基于日常LLM辅助研究构建的知识库，可在博客中搜索。
- **MathJax、夜间模式、RSS、双语内容** —— 标准功能通过自定义CSS和主题增强。

**规模：**

| 指标 | 数量 |
| ------ | ------ |
| 英文文章 | 10,264 |
| 中文文章 | 10,259 |
| AI回答笔记 | 9,794 |
| Python脚本 | 323 |
| 机器学习脚本 | 191 |
| 页面浏览量（过去一个月） | ~70,000 |

![jekyll-ai-blog —— AI驱动博客，10K+文章，翻译，TTS和PDF管道](/assets/images/ai-portfolio/blog.png)

![Cloudflare Web Analytics —— 38.9K访问量，45.2K页面浏览量，930ms加载时间，82%的良好LCP](/assets/images/ai-portfolio/cloudflare-analytics.png)

GitHub: [lzwjava/jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog)

---

## 🌳 Tree_Of_Thought —— 与一名高中生合作研究树状推理

[Tree_Of_Thought](https://github.com/Cerynitius/Tree_Of_Thought) 是一个朋友的项目 —— 一个用于解决高难度物理问题的外部树状推理系统。它不依赖于模型在一次不透明生成中的隐藏思维链，而是将推理转化为一个显式、可检查、可控的树，带有实时状态、评分、剪枝和确定性工具支持。

该系统结合了一个用于长时间推理会话的FastAPI服务、一个用于检查和剪枝分支的浏览器UI、一个节点级FSM和树调度器、一个支持SymPy的技能层用于精确符号计算，以及用于规划、建模、审查和评估的多模型路由。

**我的贡献（1个PR）：** 添加了一个兼容OpenAI的请求器和`python-dotenv`配置，使系统可以连接到任何兼容OpenAI的端点（本地或云端）。

**背景：** 我指导一名构建了这个系统的高中生。在一次会议上，他向我解释了完整的架构 —— 推理树、基于FSM的审查、路径局部增量细化。我把他介绍给AI博士研究人员，并帮助他思考研究方向。他现在正在探索使用LLM解决物理问题，使用Codex (GPT-5.4)等工具，并构建多智能体协作编码系统。

![Tree of Thought —— 终端树资源管理器，带有节点检查、前沿管理和分支剪枝](/assets/images/ai-portfolio/tree-of-thought.jpg)

GitHub: [Cerynitius/Tree_Of_Thought](https://github.com/Cerynitius/Tree_Of_Thought)

---

## 🤖 iclaw —— 终端AI Agent (REPL)

[iclaw](https://github.com/lzwjava/iclaw) 是一个终端AI Agent，能够自主编程、搜索和执行命令 —— 可用于个人机器和受限的企业机器。一个极简的openclaw实现，以纯Python CLI的形式构建，无需浏览器扩展或IDE插件，由GitHub Copilot驱动。

```
lzwjava@lzw-mac iclaw % iclaw

  ██  █████  ██       █████  ██   ██
  ██ ██      ██      ██   ██ ██   ██
  ██ ██      ██      ███████ ██ █ ██
  ██ ██      ██      ██   ██ ██████
  ██  █████  ███████ ██   ██  ███ ██

可用命令：
  /provider_model      选择并认证模型提供商
  /model               从你的提供商中选择特定模型
  /search              网页搜索（用法：/search <query>）
  /provider_search     选择网页搜索提供商
  /proxy               设置HTTP/HTTPS代理（用法：/proxy [url|off]）
  /ca_bundle           设置HTTPS的CA包（用法：/ca_bundle [path|off]）
  /log                 设置日志级别（用法：/log [verbose|info]）
  /copy                将最后一次Copilot回复复制到剪贴板
  /read                将文件内容打印到终端（用法：/read <path>）
  /clear               清除对话历史
  /compact             使用LLM压缩对话历史
  /export              将完整的对话历史导出为JSON文件
  /status              显示当前设置
  /help                显示可用命令
  /exit                退出REPL。
```

**主要特性：**

- **多轮对话** 在终端中与GitHub Copilot或OpenRouter进行。
- **多个模型提供商**：GitHub Copilot（OAuth设备流）和OpenRouter（API Key）。
- **原生工具调用**：模型自主调用网页搜索、执行shell命令和编辑文件 —— 无需人类介入。
- **多个搜索提供商**：DuckDuckGo、Startpage、Bing和Tavily。
- **企业友好**：无需IDE插件或浏览器扩展。支持带有代理和CA包的企业防火墙环境。
- **默认模型**：GPT-5.2。

![iclaw —— 终端AI Agent REPL，原生工具调用](/assets/images/ai-portfolio/iclaw.jpg)

![iclaw —— 执行日志，显示自主编程和shell命令](/assets/images/ai-portfolio/iclaw-log.png)

GitHub: [lzwjava/iclaw](https://github.com/lzwjava/iclaw)

---

## ⚙️ zz —— 数据集处理与训练工具

[zz](https://github.com/lzwjava/zz) 是一个用于ML训练管道的工具包 —— 数据集下载、分词、提取和推理工具。在GPT-2 124M训练期间使用，涉及RunPod H200、DigitalOcean H100和家用RTX 4070。也托管在 [Hugging Face](https://huggingface.co/lzwjava/zz) 上。

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

**主要能力：**

- **FineWeb下载** —— 规划并下载分片以达到Token预算（100亿、1000亿+ Token），支持进度跟踪和断点续传。
- **hf-mirror.com 支持** —— 当HuggingFace被屏蔽时，提供wget脚本用于中国访问。
- **Parquet提取** —— 通过pyarrow的iter_batches实现内存安全的迭代。
- **分词** —— 将原始文本转换为训练就绪格式。
- **训练分析** —— 从训练日志计算时长、评估指标。
- **DeepSeek推理** —— DeepSeek-V2-Lite的LLM推理脚本。

![zz on Hugging Face —— 数据集处理与训练工具，22次提交，3位贡献者](/assets/images/ai-portfolio/zz-huggingface.png)

GitHub: [lzwjava/zz](https://github.com/lzwjava/zz) · Hugging Face: [lzwjava/zz](https://huggingface.co/lzwjava/zz)

---

## 🎓 证书

### 机器学习专项课程 —— DeepLearning.AI & 斯坦福大学

2023年11月完成。三门课程：监督式机器学习、高级学习算法、无监督学习、推荐系统、强化学习。

![Coursera机器学习专项课程证书 —— 李智维，2023年11月](/assets/images/ai-portfolio/coursera-ml-1.png)

### 深度学习专项课程 —— DeepLearning.AI

2023年12月完成。五门课程：神经网络、超参数调优、结构化机器学习项目、卷积神经网络、序列模型。

![Coursera深度学习专项课程证书 —— 李智维，2023年12月](/assets/images/ai-portfolio/coursera-dl-1.png)

---

- GitHub: [https://github.com/lzwjava](https://github.com/lzwjava)
- 博客: [https://lzwjava.github.io](https://lzwjava.github.io)
