---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 我的AI作品集——每日AI工作证据
translated: true
---

我不只是谈论AI——我每天都在大规模使用它。这篇文章是我AI工作的可视化作品集：我构建的工具、消耗的token，以及获得的认证。

---

## 🖥️ LLM训练与推理——我的硬件配置

2023年搭建了我的机器学习工作站，并从此持续训练和学习。

**硬件经验：**

| GPU | VRAM | 经验时长 | 使用场景 |
|-----|------|---------|---------|
| NVIDIA RTX 4070 | 12 GB | 3年 | 家用工作站 |
| NVIDIA H200 | 141 GB | 3个月 | RunPod / DigitalOcean |
| AMD MI300X | 192 GB HBM3 | 3个月 | AMD开发者云 |

**我训练过的模型：**

- **GPT-2 124M** 从头开始在FineWeb数据集上训练（nanoGPT）——在RTX 4070、H200和MI300X上。
- **GPT-2 760M** 从头开始在AMD MI300X（192 GB HBM3）上训练——探索nanochat、DeepSeek v4 MoE。
- 超参数调优、学习率调度和数据集预处理的各种实验。

**工作站：**

![我的机器学习学习站——2023年搭建，RTX 4070 12GB，用于日常训练和实验](/assets/images/ai-portfolio/learning-station.jpg)

**AMD开发者云——MI300X 192GB HBM3：**

![AMD开发者云——MI300X实例，用于大规模模型训练](/assets/images/ai-portfolio/amd-dev-cloud.png)

---

## 🧠 增强版nanoGPT——我的Fork

Fork了[karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)并扩展了额外的数据集管道、扩展的训练配置以及用于学习的内联形状注释。45次提交，2025年11月至2026年4月。

**新增的数据集管道：**

| 数据集 | 路径 | 描述 |
|-------|------|------|
| FineWeb-Edu | `data/fineweb/` | HuggingFace FineWeb-Edu（100亿+ token）。基于分片的加载、分块处理、增量训练/验证分割。 |
| OpenWebText 10k | `data/openwebtext_10k/` | 快速10k子集，用于快速迭代。 |
| Wikipedia Local | `data/wikipedia_local/` | 直接对本地纯文本转储进行分词（无需HuggingFace下载）。 |

**新增的训练配置：**

| 配置 | 目标 | 备注 |
|------|------|------|
| `train_fineweb.py` | 125M on FineWeb | 针对RTX 4070 12 GB调优（n_embd=384, dropout=0.1）。 |
| `train_fineweb1_5b.py` | 1.5B on FineWeb | 用于H200 80 GB。 |
| `train_fineweb_gpt3.py` | GPT-3风格100亿 token | 基于分片的加载器，更宽的调度。 |
| `train_fineweb_760m.py` | 760M on FineWeb | 用于MI300X 192 GB HBM3。 |
| `train_gpt2_200m.py` | GPT-2 200M | 通用中等规模配置。 |
| `train_gpt2_200m_smoke.py` | 冒烟测试 | 快速200M完整性检查（约几分钟）。 |

**模型变更：**

- 在`model.py`的前向传播（CausalSelfAttention、MLP、GPT）中**内联张量形状注释**——以具体的GPT-2 XL示例展示每一步的精确形状，例如`# x: (B, T, C) e.g. (1, 5, 1600)`。有助于理解Transformer数据流。

![增强版nanoGPT——45次提交、数据集管道、扩展训练配置、内联形状注释](/assets/images/ai-portfolio/nanogpt-fork.png)

GitHub: [lzwjava/nanoGPT](https://github.com/lzwjava/nanoGPT)

---

## 📝 SEC-EDGAR-GPT——在SEC文件上从头训练GPT-2（124M）

在SEC EDGAR财务文件（10-K、10-Q及其他公司披露）的**15.5亿 token**上从头训练了一个**1.24亿参数的GPT-2**——在单个**RTX 4070**（12 GB VRAM）上训练约8小时，收敛到验证损失2.28。

该模型能生成令人信服的SEC模板——风险因素、MD&A部分、业务描述——并通过RunPod上的FastAPI服务器部署为交互式聊天。

整个项目——模型训练、论文、聊天机器人和网站——在**3天内使用Hermes Agent**构建，展示了AI代理如何使LLM研究变得易于访问。

在全球一家银行内部共享后，该项目在内网获得了**200多次浏览**。一位首席工程师留下评论称其*"nice"*，同事们讨论了金融域token和自然语言token之间的差异——这场对话塑造了我对金融LLM领域特定分词的想法。

![SEC-EDGAR-GPT聊天机器人](/assets/images/sec-edgar-gpt/chatbot_web.png)

**代码：**[github.com/lzwjava/sec-edgar-gpt](https://github.com/lzwjava/sec-edgar-gpt) · **论文：**[sec-edgar-gpt.pdf](https://github.com/lzwjava/sec-edgar-gpt/raw/main/sec-edgar-gpt.pdf) · **模型：**[Hugging Face](https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf) · **聊天：**[sec-edgar-gpt.lzwjava.workers.dev](https://sec-edgar-gpt.lzwjava.workers.dev/)

---

## 📊 LLM API使用情况——数据

### OpenRouter——过去一年

消耗11.5亿 token，花费239美元，跨多个模型完成15.5万次API请求。

![OpenRouter活动仪表盘——1年内11.5亿 token、239美元花费、15.5万次请求](/assets/images/ai-portfolio/openrouter-activity.png)

![OpenRouter按模型花费明细——Claude 4 Sonnet $44.40、Claude 3.5 Sonnet $9.67、Grok 3、Mistral、Kimi](/assets/images/ai-portfolio/openrouter-spend.png)

![OpenRouter按模型token使用——MiniMax 2.4亿、Gemini 2.03亿、DeepSeek 1.1亿](/assets/images/ai-portfolio/openrouter-models.png)

### 通过SSSAICode使用Claude API——2026年4月

一个月内171.53美元。2555次请求。超过1.15亿 token。缓存命中率90.9%。

![SSSAICode Claude使用情况——Opus 4.6、Opus 4.7、Sonnet 4.6、Haiku 4.5](/assets/images/ai-portfolio/sssaicode-usage.png)

### 小米MIMO订阅——已使用12.5亿 Token

Pro月付方案，包含380亿主配额 + 87.5亿补偿配额（约46亿免费额度）。2026年5月至6月期间**消耗了12.5亿 token**。

![小米MIMO Pro方案——消耗12.5亿 token，剩余约34亿免费额度](/assets/images/ai-portfolio/xiaomi-mimo-usage.png)

#### 月度Token使用明细

| 月份 | 模型 | 总Token | 输入（缓存命中） | 输入（缓存未命中） | 输出 | 请求数 |
|------|------|--------:|-----------------:|-------------------:|-----:|-------:|
| 2026-06 | mimo-v2.5 | 285,179 | 36,416 | 143,556 | 105,207 | 78 |
| 2026-06 | mimo-v2.5-pro | 734,873,374 | 710,036,672 | 21,617,131 | 3,219,571 | 10,704 |
| 2026-05 | mimo-v2.5 | 91,203 | 5,312 | 52,908 | 32,983 | 27 |
| 2026-05 | mimo-v2.5-pro | 508,851,211 | 488,291,136 | 17,725,731 | 2,834,344 | 8,649 |
| 2026-05 | mimo-v2-pro | 3,571,328 | 3,021,568 | 539,357 | 10,403 | 167 |

**月度总计：** 2026年5月：**5.125亿 token**（8,843次请求）· 2026年6月：**7.352亿 token**（10,782次请求）

> mimo-v2.5-pro 占据绝大部分使用量（约总量的96%）。mimo-v2.5-pro 上缓存命中率约96.7%，有效控制成本。6月token量较5月增长43.5%。

### 总结

| 平台 | Token | 时段 | 成本 |
|------|-------|------|------|
| OpenRouter | 11.5亿 | 过去一年 | 239美元 |
| SSSAICode (Claude) | 1.15亿+ | 2026年4月 | 171.53美元 |
| 小米MIMO | 12.5亿 | 2026年5-6月 | 免费46亿额度 |
| 其他（GitHub Copilot等） | 5亿 | 过去一年 | — |
| **总计** | **~30亿+** | **过去一年** | **—** |

---

## 🏢 企业AI使用——汇丰银行

在汇丰银行（通过TEKsystems），我在GitHub Copilot之上构建了一个自主AI代理层，用于自动化脚本编写、日志记录、文档和测试。

**我构建的内容：**

- **20个定制化AI代理**——针对不同技术栈和工作流的专用提示词和上下文。
- **400个可复用的Copilot编写脚本**——跨Java、Spring、Python、Angular和DevOps工具的常见任务自动化。
- **1,100份Copilot编写的指南**——通过LLM输出生成并通过缓存和验证的文档。
- **通过Copilot API自动生成约70个测试用例**——涵盖Spring过滤器、Python单元测试、JSON截断、提示工程和区域端点。

**成果：**

- 在企业范围内Copilot使用排名**前6%**（按高级请求衡量）。
- 因备受瞩目的AIPlayer项目获得**贡献奖**。
- 加入了汇丰内部AI社区。

<div align="center">

<img src="/assets/images/ai-portfolio/copilot.png" width="100%" /><img/>

<p><a href="https://marketplace.visualstudio.com/items?itemName=GitHub.copilot">图片来源：GitHub Copilot — Visual Studio Code Marketplace</a></p>

</div>

![汇丰AIPlayer贡献奖](/assets/images/ai-portfolio/aiplayer.jpg)

---

## 🎤 汇丰AI讲座——从神经网络到智能体

在汇丰银行面向**80位参与者**进行了一场技术讲座——包括资深顾问、专家、副总监、软件工程师和合同工。

**讲座：** *"从神经网络到智能体"* ——从最简单的神经网络（`y = wx`）出发，历经MNIST、Transformer、GPT、nanoGPT，直至构建个人AI智能体。

**我涵盖的内容：**

- 神经网络第一性原理——前向传播、反向传播、梯度下降
- Transformer架构——Q/K/V注意力、多头注意力、位置编码
- GPT内部机制——分词、嵌入、训练、生成
- nanoGPT——在H200/RTX 4070上从头训练GPT-2
- LLM智能体——Claude Code、OpenClaw、Hermes、工具调用、智能体循环
- 真实数据——消耗10亿 token、H200每小时3.44美元、钱到底花在哪里
- 我的路径——从阅读Q/K/V到从头训练模型，历时3年

**反馈：**

- 一位初级工程师说：*"你就是我想成为的人"* ——这次讲座让他看到了AI的可能性
- 资深工程师赞赏第一性原理方法——不炒作，只有数学和代码
- 随后进行了多次关于训练、智能体和职业方向的讨论

**幻灯片：** 使用Claude Code和Marp根据我的公开AI回答笔记制作。

幻灯片（Marp）：[PDF](/assets/marp/neural_networks_to_agents_public.pdf)

---

## 🛠️ ww——跨平台CLI工具包

[ww](https://github.com/lzwjava/ww)是我的旗舰CLI工具包——255+次提交、10+个命令组、跨平台（macOS + Linux）。涵盖带AI提交信息的git工作流、笔记管理、图像/PDF处理、网页搜索、GitHub Copilot聊天、系统工具和LLM辅助工具。

```
lzwjava@lzw-mac ww % uv run ww --help
Usage: ww <group> [command] [options]

Action:
  ww action [workflow.yml]  触发GitHub Actions工作流

AMD Dev Cloud:
  ww amd-dev-cloud snapshots    列出快照
  ww amd-dev-cloud start-train  创建用于训练的GPU实例
  ww amd-dev-cloud end-train    创建快照并销毁GPU实例

Copilot:
  ww copilot auth           通过GitHub OAuth进行身份验证
  ww copilot chat           与Copilot模型聊天

Git:
  ww git gpa            对所有仓库执行git pull --all
  ww git squash <n>     压缩最近n次提交
  ww git amend-push     修改最后一次提交并强制推送

LLM:
  ww llm compare <prompt>   比较多个LLM响应
  ww llm query <question>   查询本地RAG文档

Note:
  ww note              剪贴板到笔记（快速捕获）
  ww note process      清空笔记队列
  ww note watch        自动处理守护进程

Screenshot:
  ww screenshot              截屏并创建笔记
  ww screenshot interact-note  交互式截屏笔记

255+次提交。10+个命令组。跨平台（macOS + Linux）。
```

![ww——GitHub上的跨平台CLI工具包](/assets/images/ai-portfolio/ww1.png)

GitHub: [lzwjava/ww](https://github.com/lzwjava/ww)

---

## 📝 jekyll-ai-blog——AI驱动的博客平台

[jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog)是[lzwjava.github.io](https://lzwjava.github.io)的源代码——一个由AI自动化增强的Jekyll博客。10,000+英文文章、10,000+中文文章、9,700+ AI回答笔记。过去一个月约70,000次页面浏览（Cloudflare Analytics）。

```
lzwjava@lzw-mac jekyll-ai-blog % ls README.md
README.md
```

**与标准Jekyll博客的不同之处：**

- **AI驱动翻译**——基于LLM的翻译管道通过GitHub Actions自动将每篇文章扩展为多种语言。
- **Google Cloud Text-to-Speech**——自动生成文章音频版本以提高无障碍性。
- **XeLaTeX PDF/EPUB生成**——从Markdown源生成高质量打印就绪PDF和电子书导出。
- **GitHub Actions CI/CD**——自动化构建、测试、翻译和部署工作流。
- **8,000+ AI回答笔记**——通过日常LLM辅助研究构建的知识库，可在博客上搜索。
- **MathJax、夜间模式、RSS、双语内容**——通过自定义CSS和主题增强的标准功能。

**规模：**

| 指标 | 数量 |
|------|------|
| 英文文章 | 10,264 |
| 中文文章 | 10,259 |
| AI回答笔记 | 9,794 |
| Python脚本 | 323 |
| ML脚本 | 191 |
| 页面浏览（上月） | ~70,000 |

![jekyll-ai-blog——AI驱动博客，10K+文章，翻译、TTS和PDF管道](/assets/images/ai-portfolio/blog.png)

![Cloudflare Web Analytics——38.9K访问、45.2K页面浏览、930ms加载时间、82%良好LCP](/assets/images/ai-portfolio/cloudflare-analytics.png)

GitHub: [lzwjava/jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog)

---

## 🌳 Tree_Of_Thought——与一位高中生合作思维树推理

[Tree_Of_Thought](https://github.com/Cerynitius/Tree_Of_Thought)是一个朋友的项目——一个用于物理密集型问题求解的外部思维树推理系统。它不是依赖模型在一次不透明补全中的隐藏思维链，而是将推理过程显式化为一个可检查、可控的树，具有实时状态、评分、剪枝和确定性工具支持。

该系统结合了用于长时间推理会话的FastAPI服务、用于检查和剪枝分支的浏览器UI、节点级FSM和树调度器、用于精确符号计算的SymPy支持技能层，以及用于规划、建模、审查和评估的多模型路由。

**我的贡献（1个PR）：** 添加了一个兼容OpenAI的请求者和`python-dotenv`配置，使系统能够连接到任何兼容OpenAI的端点（本地或云端）。

**背景：** 我指导一位构建了该系统的高中生。在一次会议中，他带我理解了整个架构——推理树、基于FSM的审查、路由-局部增量细化。我把他介绍给了AI博士研究员，并帮助他思考研究方向。他现在正在探索使用LLM解决物理问题，使用Codex（GPT-5.4）等工具，并构建多智能体协作编码系统。

![思维树——终端树资源管理器，带有节点检查、前沿管理和分支剪枝](/assets/images/ai-portfolio/tree-of-thought.jpg)

GitHub: [Cerynitius/Tree_Of_Thought](https://github.com/Cerynitius/Tree_Of_Thought)

---

## 🤖 iclaw——终端AI智能体（REPL）

[iclaw](https://github.com/lzwjava/iclaw)是一个终端AI智能体，能自主编写代码、搜索和执行命令——可在个人机器和受限制的企业机器上运行。一个最小化的openclaw实现，构建为纯Python CLI，无需浏览器扩展或IDE插件，由GitHub Copilot驱动。

```
lzwjava@lzw-mac iclaw % iclaw

  ██  █████  ██       █████  ██   ██
  ██ ██      ██      ██   ██ ██   ██
  ██ ██      ██      ███████ ██ █ ██
  ██ ██      ██      ██   ██ ██████
  ██  █████  ███████ ██   ██  ███ ██

可用命令：
  /provider_model      选择模型提供商并进行身份验证
  /model               从提供商中选择特定模型
  /search              网页搜索（用法：/search <查询>）
  /provider_search     选择网页搜索提供商
  /proxy               设置HTTP/HTTPS代理（用法：/proxy [url|off]）
  /ca_bundle           设置HTTPS的CA绑定（用法：/ca_bundle [path|off]）
  /log                 设置日志详细程度（用法：/log [verbose|info]）
  /copy                将最近的Copilot响应复制到剪贴板
  /read                将文件内容打印到终端（用法：/read <路径>）
  /clear               清除对话历史
  /compact             使用LLM压缩对话历史
  /export              将完整对话历史导出为JSON文件
  /status              显示当前设置
  /help                显示可用命令
  /exit                退出REPL。
```

**关键功能：**

- **多轮对话**——在终端中使用GitHub Copilot或OpenRouter。
- **多模型提供商**：GitHub Copilot（OAuth设备流）和OpenRouter（API密钥）。
- **原生工具调用**：模型自主调用网页搜索、执行shell命令和编辑文件——无需人工干预。
- **多个搜索提供商**：DuckDuckGo、Startpage、Bing和Tavily。
- **企业友好**：无需IDE插件或浏览器扩展。支持企业防火墙（代理和CA绑定）。
- **默认模型**：GPT-5.2。

![iclaw——终端AI智能体REPL，支持原生工具调用](/assets/images/ai-portfolio/iclaw.jpg)

![iclaw——显示自主编码和shell命令的执行日志](/assets/images/ai-portfolio/iclaw-log.png)

GitHub: [lzwjava/iclaw](https://github.com/lzwjava/iclaw)

---

## ⚙️ zz——数据集处理与训练工具

[zz](https://github.com/lzwjava/zz)是一个用于ML训练管道的工具包——数据集下载、分词、提取和推理工具。在RunPod H200、DigitalOcean H100和家用RTX 4070上运行GPT-2 124M训练时使用。也托管在[Hugging Face](https://huggingface.co/lzwjava/zz)上。

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

- **FineWeb下载**——计划并下载分片以达到token预算（100亿、1000亿+ token），可恢复，带进度跟踪。
- **hf-mirror.com支持**——当HuggingFace被屏蔽时，使用wget脚本访问中国镜像。
- **Parquet提取**——通过pyarrow iter_batches进行内存安全迭代。
- **分词**——将原始文本转换为训练就绪格式。
- **训练分析**——从训练日志中计算时长、指标评估。
- **DeepSeek推理**——DeepSeek-V2-Lite的LLM推理脚本。

![zz on Hugging Face——数据集处理与训练工具，22次提交，3位贡献者](/assets/images/ai-portfolio/zz-huggingface.png)

GitHub: [lzwjava/zz](https://github.com/lzwjava/zz) · Hugging Face: [lzwjava/zz](https://huggingface.co/lzwjava/zz)

---

## 🎓 证书

### 机器学习专项课程——DeepLearning.AI & Stanford University

2023年11月完成。三门课程：监督式机器学习、高级学习算法、无监督学习、推荐系统、强化学习。

![Coursera机器学习专项课程证书——李智维，2023年11月](/assets/images/ai-portfolio/coursera-ml-1.png)

### 深度学习专项课程——DeepLearning.AI

2023年12月完成。五门课程：神经网络、超参数调优、结构化ML项目、CNN、序列模型。

![Coursera深度学习专项课程证书——李智维，2023年12月](/assets/images/ai-portfolio/coursera-dl-1.png)

---

- GitHub: [https://github.com/lzwjava](https://github.com/lzwjava)
- 博客: [https://lzwjava.github.io](https://lzwjava.github.io)