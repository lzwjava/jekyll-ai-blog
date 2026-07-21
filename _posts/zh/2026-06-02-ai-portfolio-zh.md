---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 我的 AI 作品集 — 日常 AI 工作记录
translated: true
---

我不只是谈论AI——我每天都在大规模使用它。这篇文章是我AI工作的视觉作品集：我构建的工具、消耗的token以及获得的认证。

---

## 🖥️ LLM训练与推理——我的硬件配置

2023年搭建了我的机器学习工作站，此后一直在进行训练和学习。

**硬件经验：**

| GPU | 显存 | 经验时长 | 使用位置 |
| ----- | ------ | ------------ | ------- |
| NVIDIA RTX 4070 | 12 GB | 3年 | 家庭工作站 |
| NVIDIA H200 | 141 GB | 3个月 | RunPod / DigitalOcean |
| AMD MI300X | 192 GB HBM3 | 3个月 | AMD开发者云 |

**我训练过的内容：**

- **GPT-2 124M** 从零开始在FineWeb数据集上训练（nanoGPT）——分别在RTX 4070、H200和MI300X上。
- **GPT-2 760M** 从零开始在AMD MI300X（192 GB HBM3）上训练——探索nanochat、DeepSeek v4 MoE。
- 各种超参数调优、学习率调度和数据集预处理的实验。

**工作站：**

![我的ML学习站——2023年搭建，RTX 4070 12GB，用于日常训练和实验](/assets/images/ai-portfolio/learning-station.jpg)

**AMD开发者云——MI300X 192GB HBM3：**

![AMD开发者云——用于大规模模型训练的MI300X实例](/assets/images/ai-portfolio/amd-dev-cloud.png)

---

### 🏋️ 训练运行摘要

| # | 模型 | 框架 | 参数量 | 硬件 | 步数 | 状态 |
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

## 🧠 增强版nanoGPT——我的Fork

Fork了[karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)并进行扩展，增加了额外的数据集管线、规模化训练配置以及用于学习的内嵌形状注释。45次提交，2025年11月 – 2026年4月。

**新增数据集管线：**

| 数据集 | 路径 | 描述 |
| --------- | ------ | ------------- |
| FineWeb-Edu | `data/fineweb/` | HuggingFace FineWeb-Edu（100亿+ token）。基于分片的加载、分块处理、增量式训练/验证集划分。 |
| OpenWebText 10k | `data/openwebtext_10k/` | 快速10k子集，用于快速迭代。 |
| Wikipedia Local | `data/wikipedia_local/` | 直接对本地纯文本转储进行分词（无需HuggingFace下载）。 |

**新增训练配置：**

| 配置 | 目标 | 备注 |
| -------- | -------- | ------- |
| `train_fineweb.py` | 125M on FineWeb | 针对RTX 4070 12 GB优化（n_embd=384, dropout=0.1）。 |
| `train_fineweb1_5b.py` | 1.5B on FineWeb | 用于H200 80 GB。 |
| `train_fineweb_gpt3.py` | GPT-3风格 100亿 token | 基于分片的加载器，更宽泛的调度。 |
| `train_fineweb_760m.py` | 760M on FineWeb | 用于MI300X 192 GB HBM3。 |
| `train_gpt2_200m.py` | GPT-2 200M | 通用中型配置。 |
| `train_gpt2_200m_smoke.py` | 冒烟测试 | 快速200M sanity检查（约几分钟）。 |

**模型改动：**

- **内联张量形状注释** 贯穿 `model.py` 的前向传播（CausalSelfAttention, MLP, GPT）——精确展示每一步的形状，并给出具体的GPT-2 XL示例，例如 `# x: (B, T, C) e.g. (1, 5, 1600)`。有助于理解Transformer数据流。

![增强版nanoGPT——45次提交，数据集管线，规模化训练配置，内联形状注释](/assets/images/ai-portfolio/nanogpt-fork.png)

GitHub: [lzwjava/nanoGPT](https://github.com/lzwjava/nanoGPT)

---

## 📝 SEC-EDGAR-GPT——基于SEC申报文件从零训练的GPT-2（124M）

在 **15.5亿token** 的SEC EDGAR金融申报文件（10-K、10-Q及其他公司披露）上，从零训练了一个 **124M参数的GPT-2**——在单张 **RTX 4070**（12 GB显存）上训练约8小时，验证损失收敛至2.28。

该模型能生成令人信服的SEC套话——风险因素、MD&A部分、业务描述——并通过FastAPI服务器部署在RunPod上，支持交互式聊天。

整个项目——模型训练、论文、聊天机器人和网站——在 **3天内使用Hermes Agent** 构建完成，展示了AI代理如何让LLM研究变得人人可及。

该项目在一家全球银行内部共享后，内部获得了 **200多次浏览**。一位首席工程师留下评论称其 *“不错”*。此外，受一位朋友在循环Transformer方面工作的启发，该项目让我思考如何将金融token与自然语言token区别对待，以提高生成准确性。

![SEC-EDGAR-GPT 聊天机器人](/assets/images/sec-edgar-gpt/chatbot_web.png)

**代码：** [github.com/lzwjava/sec-edgar-gpt](https://github.com/lzwjava/sec-edgar-gpt) · **论文：** [sec-edgar-gpt.pdf](https://github.com/lzwjava/sec-edgar-gpt/raw/main/sec-edgar-gpt.pdf) · **模型：** [Hugging Face](https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf) · **聊天：** [sec-edgar-gpt.lzwjava.workers.dev](https://sec-edgar-gpt.lzwjava.workers.dev/)

---

## 📊 LLM API使用量——数据一览

### OpenRouter——过去一年

消耗11.5亿token，花费239美元，15.5万次API请求，覆盖多个模型。

![OpenRouter活动仪表板——1年消耗11.5亿token，花费239美元，15.5万次请求](/assets/images/ai-portfolio/openrouter-activity.png)

![OpenRouter模型花费分布——Claude 4 Sonnet $44.40，Claude 3.5 Sonnet $9.67，Grok 3，Mistral，Kimi](/assets/images/ai-portfolio/openrouter-spend.png)

![OpenRouter各模型Token使用量——MiniMax 2.4亿，Gemini 2.03亿，DeepSeek 1.1亿](/assets/images/ai-portfolio/openrouter-models.png)

### 通过SSSAICode的Claude API——2026年4月

单月花费171.53美元。2,555次请求。1.15亿+ token。缓存命中率90.9%。

![SSSAICode Claude使用情况——Opus 4.6，Opus 4.7，Sonnet 4.6，Haiku 4.5](/assets/images/ai-portfolio/sssaicode-usage.png)

### 小米MIMO订阅——已使用12.5亿Token

Pro月度套餐，包含380亿主配额 + 87.5亿补偿配额（约46亿免费额度）。**2026年5月至6月消耗12.5亿token。**

![小米MIMO Pro套餐——消耗12.5亿token，剩余约34亿免费额度](/assets/images/ai-portfolio/xiaomi-mimo-usage.png)

#### 月度Token使用明细

| 月份 | 模型 | 总Token | 输入（缓存命中） | 输入（缓存未命中） | 输出 | 请求数 |
| ------- | ------- | -------------: | -------------------: | --------------------: | -------: | ---------: |
| 2026-06 | mimo-v2.5 | 285,179 | 36,416 | 143,556 | 105,207 | 78 |
| 2026-06 | mimo-v2.5-pro | 734,873,374 | 710,036,672 | 21,617,131 | 3,219,571 | 10,704 |
| 2026-05 | mimo-v2.5 | 91,203 | 5,312 | 52,908 | 32,983 | 27 |
| 2026-05 | mimo-v2.5-pro | 508,851,211 | 488,291,136 | 17,725,731 | 2,834,344 | 8,649 |
| 2026-05 | mimo-v2-pro | 3,571,328 | 3,021,568 | 539,357 | 10,403 | 167 |

**月度合计：** 2026年5月：**5.125亿token**（8,843次请求）· 2026年6月：**7.352亿token**（10,782次请求）

> mimo-v2.5-pro 占据使用主导（占总量的约96%）。mimo-v2.5-pro 上缓存命中率约96.7%，保持了成本效率。6月token量较5月增长43.5%。

### 总结

| 平台 | Token | 时间段 | 成本 |
| ---------- | -------- | -------- | ------ |
| OpenRouter | 11.5亿 | 过去一年 | $239 |
| SSSAICode (Claude) | 1.15亿+ | 2026年4月 | $171.53 |
| 小米MIMO | 12.5亿 | 2026年5–6月 | 免费46亿额度 |
| 其他（GitHub Copilot等） | 5亿 | 过去一年 | — |
| **总计** | **~30亿+** | **过去一年** | **—** |

---

## 🏢 企业级AI使用——在一家英国全能银行

在一家英国全能银行（通过一家全球IT外包公司），我在一个编码助手之上构建了一个自主AI代理层，用于自动化脚本编写、日志记录、文档编写和测试。

**我构建的内容：**

- **20个定制AI代理**——针对不同的技术栈和工作流程设置了专用的提示词和上下文。
- **400个由编码助手编写的可复用脚本**——针对Java、Spring、Python、Angular和DevOps工具的常见任务自动化。
- **1,800份由编码助手编写的指南**——通过LLM输出生成并验证的文档，包含缓存和验证机制。
- **通过编码助手API自动生成约70个测试用例**——涵盖Spring Filter、Python unittest、JSON截断、提示工程和区域端点。

**成果：**

- 在整个企业的编码助手使用排名中，按照高级请求量计算，位列 **前6%**。
- 因备受瞩目的AIPlayer项目获得 **贡献奖**。
- 加入该银行的内部AI社区。

![AIPlayer贡献奖](/assets/images/ai-portfolio/aiplayer.jpg)

---

## 🎤 AI演讲——从神经网络到智能代理

在一家英国全能银行向 **80名参与者** 做了技术分享——包括高级顾问、专家、副董事、软件工程师和合同工。

**演讲主题：** *"从神经网络到智能代理"*——从最简单的神经网络（`y = wx`）出发，经过MNIST、Transformer、GPT、nanoGPT，直至构建个人AI代理。

**演讲内容：**

- 神经网络基础原理——前向传播、反向传播、梯度下降
- Transformer架构——Q/K/V注意力、多头注意力、位置编码
- GPT内部机制——分词、嵌入、训练、生成
- nanoGPT——在H200/RTX 4070上从零训练GPT-2
- LLM代理——Claude Code、OpenClaw、Hermes、工具调用、代理循环
- 真实数据——消耗10亿token，H200每小时$3.44，钱究竟花在哪里
- 我的路径——从阅读Q/K/V相关文章到从零训练模型的3年历程

**反馈：**

- 一位初级工程师说：*"你是我想要成为的人"*——这场演讲让他看到了AI可能性的崭新视角
- 资深工程师欣赏这种从基本原理出发的方法——没有炒作，只有数学和代码
- 多次就训练、代理和职业方向进行后续讨论

**幻灯片：** 使用Claude Code和Marp，基于我的公开AI回答笔记构建。

幻灯片（Marp）：[PDF](/assets/marp/neural_networks_to_agents_public.pdf)

---

## 🛠️ ww——跨平台CLI工具包

[ww](https://github.com/lzwjava/ww) 是我的旗舰CLI工具包——255+次提交，10+个命令组，跨平台（macOS + Linux）。涵盖带有AI提交信息的Git工作流、笔记管理、图像/PDF处理、网页搜索、GitHub Copilot聊天、系统工具和LLM辅助功能。

```
lzwjava@lzw-mac ww % uv run ww --help
用法: ww <group> [command] [options]

Action:
  ww action [workflow.yml]  触发GitHub Actions工作流

AMD Dev Cloud:
  ww amd-dev-cloud snapshots    列出快照
  ww amd-dev-cloud start-train  创建GPU实例用于训练
  ww amd-dev-cloud end-train    对GPU实例做快照并销毁

Copilot:
  ww copilot auth           通过GitHub OAuth进行身份验证
  ww copilot chat           与Copilot模型聊天

Git:
  ww git gpa            对所有仓库执行git pull --all
  ww git squash <n>     压缩最近n次提交
  ww git amend-push     修改最后一次提交并强制推送

LLM:
  ww llm compare <prompt>   比较多个LLM的响应
  ww llm query <question>   查询本地RAG文档

Note:
  ww note              剪贴板内容转为笔记（快速捕获）
  ww note process      清空笔记队列
  ww note watch        自动处理守护进程

Screenshot:
  ww screenshot               截图并创建笔记
  ww screenshot interact-note 交互式截图笔记

255+次提交。10+个命令组。跨平台（macOS + Linux）。
```

![ww——跨平台CLI工具包（GitHub）](/assets/images/ai-portfolio/ww1.png)

GitHub: [lzwjava/ww](https://github.com/lzwjava/ww)

---

## 📝 jekyll-ai-blog——AI驱动的博客平台

[jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog) 是 [lzwjava.github.io](https://lzwjava.github.io) 的源代码——一个通过AI自动化增强的Jekyll博客。10,000+篇英文文章，10,000+篇中文文章，9,700+条AI回答笔记。过去一个月页面浏览量约70,000次（Cloudflare分析）。

```
lzwjava@lzw-mac jekyll-ai-blog % ls README.md
README.md
```

**与标准Jekyll博客的不同之处：**

- **AI驱动翻译**——基于LLM的翻译管线，通过GitHub Actions自动将每篇文章扩展为多种语言。
- **Google Cloud Text-to-Speech**——自动生成文章的音频版本，提高可访问性。
- **XeLaTeX PDF/EPUB生成**——从Markdown源文件生成高质量、可直接打印的PDF和电子书导出。
- **GitHub Actions CI/CD**——自动化构建、测试、翻译和部署工作流。
- **8,000+条AI回答笔记**——通过日常LLM辅助研究构建的知识库，可在博客中搜索。
- **MathJax、夜间模式、RSS、双语内容**——通过自定义CSS和主题增强的标准功能。

**规模：**

| 指标 | 数量 |
| -------- | ------- |
| 英文文章 | 10,264 |
| 中文文章 | 10,259 |
| AI回答笔记 | 9,794 |
| Python脚本 | 323 |
| ML脚本 | 191 |
| 页面浏览量（过去一月） | ~70,000 |

![jekyll-ai-blog——AI驱动的博客，拥有10K+文章、翻译、TTS和PDF管线](/assets/images/ai-portfolio/blog.png)

![Cloudflare Web分析——38.9K访问，45.2K页面浏览量，930ms加载时间，82%良好LCP](/assets/images/ai-portfolio/cloudflare-analytics.png)

GitHub: [lzwjava/jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog)

---

## 🌳 Tree_Of_Thought——与一名高中生合作进行树状思维推理

[Tree_Of_Thought](https://github.com/Cerynitius/Tree_Of_Thought) 是一个朋友的项目——一个用于物理密集型问题求解的外部树状思维推理系统。它不依赖模型在一次不透明的生成中隐藏的思维链，而是将推理过程转化为一个显式的、可检查的、可控的树，包含实时状态、评分、剪枝和确定性工具支持。

该系统结合了：用于长时推理会话的FastAPI服务、用于检查和剪枝分支的浏览器UI、节点级FSM和树调度器、基于SymPy的技能层（用于精确符号计算），以及用于规划、建模、审查和评估的多模型路由。

**我的贡献（1个PR）：** 添加了一个兼容OpenAI的请求器和`python-dotenv`配置，使系统能够连接到任何兼容OpenAI的端点（本地或云端）。

**背景：** 我指导一名正在构建该系统的高中生。在一次会议中，他向我详细介绍了整个架构——推理树、基于FSM的审查、路径局部增量优化。我向他介绍了AI领域的博士生研究人员，并帮助他思考研究方向。他现在正在探索使用LLM进行物理问题求解，使用Codex（GPT-5.4）等工具，并构建多智能体协作编码系统。

![树状思维——终端树浏览器，支持节点检查、前沿管理和分支剪枝](/assets/images/ai-portfolio/tree-of-thought.jpg)

GitHub: [Cerynitius/Tree_Of_Thought](https://github.com/Cerynitius/Tree_Of_Thought)

---

## 🤖 iclaw——终端AI代理（REPL）

[iclaw](https://github.com/lzwjava/iclaw) 是一个终端AI代理，能够自主编码、搜索和执行命令——可在个人机器和受限制的企业机器上工作。一个极简的openclaw实现，作为纯Python CLI构建，无需浏览器扩展或IDE插件，由GitHub Copilot驱动。

```
lzwjava@lzw-mac iclaw % iclaw

  ██  █████  ██       █████  ██   ██
  ██ ██      ██      ██   ██ ██   ██
  ██ ██      ██      ███████ ██ █ ██
  ██ ██      ██      ██   ██ ██████
  ██  █████  ███████ ██   ██  ███ ██

可用命令:
  /provider_model      选择模型提供商并进行身份验证
  /model               从提供商选择特定模型
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

- **多轮对话** 在你的终端中与GitHub Copilot或OpenRouter进行。
- **多个模型提供商**：GitHub Copilot（OAuth设备流）和OpenRouter（API密钥）。
- **原生工具调用**：模型自主调用网页搜索、执行Shell命令和编辑文件——无需人工参与。
- **多个搜索提供商**：DuckDuckGo、Startpage、Bing和Tavily。
- **企业友好**：无需IDE插件或浏览器扩展。支持企业防火墙后使用，可设置代理和CA证书包。
- **默认模型**：GPT-5.2。

![iclaw——终端AI代理REPL，支持原生工具调用](/assets/images/ai-portfolio/iclaw.jpg)

![iclaw——显示自主编码和Shell命令的执行日志](/assets/images/ai-portfolio/iclaw-log.png)

GitHub: [lzwjava/iclaw](https://github.com/lzwjava/iclaw)

---

## ⚙️ zz——数据集处理与训练工具

[zz](https://github.com/lzwjava/zz) 是一个ML训练管线工具包——包括数据集下载、分词、提取和推理工具。在RunPod H200、DigitalOcean H100和家庭RTX 4070上进行GPT-2 124M训练时使用。也托管在 [Hugging Face](https://huggingface.co/lzwjava/zz) 上。

```
lzwjava@lzw-mac zz % tree -L 1
scripts/
  download/     # 数据集下载脚本（FineWeb, Wikimedia, HF镜像）
  extract/      # 数据提取、分词和重命名
  analysis/     # 训练时长和指标评估
  deepseek/     # LLM推理脚本（DeepSeek-V2-Lite）
logs/           # 训练日志和输出
datasets/       # 下载的数据集存储
```

**主要功能：**

- **FineWeb下载**——规划并下载分片以达到token预算（100亿、1000亿+ token），支持断点续传和进度跟踪。
- **支持hf-mirror.com**——当HuggingFace被屏蔽时，提供wget脚本以便中国用户访问。
- **Parquet提取**——通过pyarrow iter_batches进行内存安全的迭代。
- **分词**——将原始文本转换为训练就绪格式。
- **训练分析**——从训练日志计算时长和指标评估。
- **DeepSeek推理**——DeepSeek-V2-Lite的LLM推理脚本。

![zz在Hugging Face上——数据集处理与训练工具，22次提交，3个贡献者](/assets/images/ai-portfolio/zz-huggingface.png)

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