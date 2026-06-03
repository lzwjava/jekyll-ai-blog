---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 我的AI作品集——每日AI工作证据
translated: true
---

我不只是谈论人工智能——我每天都在大规模使用它。这篇文章是我的AI工作视觉作品集：我构建的工具、消耗的令牌以及获得的认证。

---

## 🖥️ LLM训练与推理——我的硬件设置

2023年构建了我的机器学习工作站，此后一直在训练和学习。

**硬件经验：**

| GPU | VRAM | 经验时长 | 使用场景 |
|-----|------|------------|-------|
| NVIDIA RTX 4070 | 12 GB | 3年 | 家庭工作站 |
| NVIDIA H200 | 141 GB | 3个月 | RunPod / DigitalOcean |
| AMD MI300X | 192 GB HBM3 | 3个月 | AMD开发者云 |

**我训练过的内容：**

- **GPT-2 124M** 从零开始基于FineWeb数据集（nanoGPT）——在RTX 4070、H200和MI300X上。
- **GPT-2 760M** 从零开始基于AMD MI300X（192 GB HBM3）——探索nanochat、DeepSeek v4 MoE。
- 关于超参数调优、学习率调度和数据集预处理的各种实验。

**工作站：**

![我的机器学习学习站——2023年搭建，RTX 4070 12GB，用于日常训练和实验](/assets/images/ai-portfolio/learning-station.jpg)

**AMD开发者云——MI300X 192GB HBM3：**

![AMD Dev Cloud——用于大规模模型训练的MI300X实例](/assets/images/ai-portfolio/amd-dev-cloud.png)

---

## 🧠 增强版nanoGPT——我的分支

Fork了[karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)并扩展了额外的数据集管道、规模化训练配置以及用于学习的内联形状注释。45个提交，2025年11月至2026年4月。

**新增数据集管道：**

| 数据集 | 路径 | 描述 |
|---------|------|-------------|
| FineWeb-Edu | `data/fineweb/` | HuggingFace FineWeb-Edu（100亿+令牌）。基于分片的加载、分块处理、增量训练/验证集划分。 |
| OpenWebText 10k | `data/openwebtext_10k/` | 用于快速迭代的10k子集。 |
| 维基百科本地版 | `data/wikipedia_local/` | 直接对本地纯文本转储进行分词（无需HuggingFace下载）。 |

**新增训练配置：**

| 配置 | 目标 | 备注 |
|--------|--------|-------|
| `train_fineweb.py` | 125M on FineWeb | 针对RTX 4070 12 GB调优（n_embd=384, dropout=0.1）。 |
| `train_fineweb1_5b.py` | 1.5B on FineWeb | 适用于H200 80 GB。 |
| `train_fineweb_gpt3.py` | GPT-3风格100亿令牌 | 基于分片的加载器，更宽的调度。 |
| `train_fineweb_760m.py` | 760M on FineWeb | 适用于MI300X 192 GB HBM3。 |
| `train_gpt2_200m.py` | GPT-2 200M | 通用中型配置。 |
| `train_gpt2_200m_smoke.py` | 冒烟测试 | 快速200M完整性检查（约几分钟）。 |

**模型变更：**

- 在`model.py`的前向传播中（CausalSelfAttention、MLP、GPT）添加了**内联张量形状注释**——每一步都显示精确形状，并附有具体的GPT-2 XL示例，例如`# x: (B, T, C) e.g. (1, 5, 1600)`。有助于理解Transformer数据流。

![增强版nanoGPT——45个提交，数据集管道，规模化训练配置，内联形状注释](/assets/images/ai-portfolio/nanogpt-fork.png)

GitHub: [lzwjava/nanoGPT](https://github.com/lzwjava/nanoGPT)

---

## 📊 LLM API使用量——数据

### OpenRouter——过去一年

消耗了11.5亿令牌，花费239美元，跨多个模型共155K次API请求。

![OpenRouter活动仪表板——过去一年11.5亿令牌，239美元花费，155K次请求](/assets/images/ai-portfolio/openrouter-activity.png)

![OpenRouter模型花费细分——Claude 4 Sonnet 44.40美元，Claude 3.5 Sonnet 9.67美元，Grok 3、Mistral、Kimi](/assets/images/ai-portfolio/openrouter-spend.png)

![OpenRouter按模型划分的令牌使用量——MiniMax 2.4亿，Gemini 2.03亿，DeepSeek 1.1亿](/assets/images/ai-portfolio/openrouter-models.png)

### 通过SSSAICode使用Claude API——2026年4月

一个月内171.53美元。2,555次请求。超过1.15亿令牌。90.9%缓存命中率。

![SSSAICode Claude使用情况——Opus 4.6、Opus 4.7、Sonnet 4.6、Haiku 4.5](/assets/images/ai-portfolio/sssaicode-usage.png)

### 小米MIMO订阅——已使用5亿令牌

Pro月付计划，包含380亿主配额+87.5亿补偿配额（约46亿免费额度）。目前已消耗5亿令牌。

![小米MIMO Pro计划——已消耗5亿令牌，剩余约46亿免费额度](/assets/images/ai-portfolio/xiaomi-mimo-usage.png)

### 总结

| 平台 | 令牌数 | 时间周期 | 成本 |
|----------|--------|--------|------|
| OpenRouter | 11.5亿 | 过去一年 | 239美元 |
| SSSAICode (Claude) | 1.15亿+ | 2026年4月 | 171.53美元 |
| 小米MIMO | 5亿 | 当前计划 | 免费46亿额度 |
| 其他（GitHub Copilot等） | 5亿 | 过去一年 | — |
| **总计** | **~23亿+** | **过去一年** | **—** |

---

## 🏢 企业AI使用——汇丰银行

在汇丰银行（通过TEKsystems），我在GitHub Copilot之上构建了一个自主AI代理层，用于自动化脚本编写、日志记录、文档编写和测试。

**我构建的内容：**

- **20个定制化AI代理**——针对不同技术栈和工作流的专用提示词和上下文。
- **400个可复用的Copilot编写的脚本**——跨Java、Spring、Python、Angular和DevOps工具的常见任务自动化。
- **1,100份Copilot编写的指南**——通过LLM输出生成并经缓存和验证的文档。
- **通过Copilot API自动生成了约70个测试用例**——涵盖Spring过滤器、Python unittest、JSON截断、提示工程和区域端点。

**成果：**

- 按高级请求计算，在企业内**Copilot使用量排名前6%**。
- 因高知名度项目AIPlayer获得**贡献奖**。
- 加入汇丰内部AI社区。

<div align="center">

<img src="/assets/images/ai-portfolio/copilot.png" width="100%" /><img/>

<p><a href="https://marketplace.visualstudio.com/items?itemName=GitHub.copilot">图片来源：GitHub Copilot——Visual Studio Code Marketplace</a></p>

</div>

![汇丰AIPlayer贡献奖](/assets/images/ai-portfolio/aiplayer.jpg)

---

## 🎤 汇丰AI讲座——从神经网络到智能代理

在汇丰银行向**80名参与者**进行了技术讲座——包括高级顾问、专家、副总监、软件工程师和承包商。

**讲座内容：**《从神经网络到智能代理》——从最简单的神经网络（`y = wx`）出发，历经MNIST、Transformer、GPT、nanoGPT，直至构建个人AI代理。

**我涵盖的主题：**

- 神经网络基本原理——前向传播、反向传播、梯度下降
- Transformer架构——Q/K/V注意力、多头注意力、位置编码
- GPT内部机制——分词、嵌入、训练、生成
- nanoGPT——在H200/RTX 4070上从零开始训练GPT-2
- LLM代理——Claude Code、OpenClaw、Hermes、工具调用、代理循环
- 真实数据——消耗10亿令牌，H200每小时3.44美元，资金实际去向
- 我的路径——从了解Q/K/V到从零训练模型的3年历程

**反馈：**

- 一位初级工程师说：“你是我想要成为的人”——这场讲座让他开阔了眼界，看到了AI的可能性
- 高级工程师欣赏这种从头开始的方法——没有炒作，只有数学和代码
- 后续多次关于训练、代理和职业方向的讨论

**幻灯片：**使用Claude Code和Marp构建，基于我的公开AI响应笔记。

---

## 🛠️ ww——跨平台CLI工具包

[ww](https://github.com/lzwjava/ww)是我的旗舰CLI工具包——255+提交，10+命令组，跨平台（macOS + Linux）。涵盖带有AI提交消息的Git工作流、笔记管理、图像/PDF处理、网络搜索、GitHub Copilot聊天、系统工具及LLM辅助功能。

```
lzwjava@lzw-mac ww % uv run ww --help
Usage: ww <group> [command] [options]

Action:
  ww action [workflow.yml]  触发一个GitHub Actions工作流

AMD Dev Cloud:
  ww amd-dev-cloud snapshots    列出快照
  ww amd-dev-cloud start-train  创建用于训练的GPU droplet
  ww amd-dev-cloud end-train    快照并销毁GPU droplet

Copilot:
  ww copilot auth           通过GitHub OAuth进行身份验证
  ww copilot chat           与Copilot模型聊天

Git:
  ww git gpa            对所有仓库执行git pull --all
  ww git squash <n>     压缩最后n个提交
  ww git amend-push     修改最后一个提交并强制推送

LLM:
  ww llm compare <prompt>   比较多个LLM响应
  ww llm query <question>   查询本地RAG文档

Note:
  ww note              剪贴板内容保存为笔记（快速捕获）
  ww note process      清空笔记队列
  ww note watch        自动处理守护进程

Screenshot:
  ww screenshot               截图并创建笔记
  ww screenshot interact-note 交互式截图笔记

255+提交。10+命令组。跨平台（macOS + Linux）。
```

![ww——GitHub上的跨平台CLI工具包](/assets/images/ai-portfolio/ww1.png)

GitHub: [lzwjava/ww](https://github.com/lzwjava/ww)

---

## 📝 jekyll-ai-blog——AI驱动的博客平台

[jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog)是[lzwjava.github.io](https://lzwjava.github.io)的源代码——一个经过AI自动化增强的Jekyll博客。10,000+英文文章，10,000+中文文章，9,700+ AI回答笔记。过去一个月约70,000次页面浏览量（Cloudflare Analytics）。

```
lzwjava@lzw-mac jekyll-ai-blog % ls README.md
README.md
```

**与标准Jekyll博客的不同之处：**

- **AI驱动翻译**——基于LLM的翻译管道通过GitHub Actions自动将每篇文章扩展为多种语言。
- **Google Cloud Text-to-Speech**——自动生成文章的音频版本，提升可访问性。
- **XeLaTeX PDF/EPUB生成**——从Markdown源生成高质量可打印PDF和电子书导出。
- **GitHub Actions CI/CD**——自动化构建、测试、翻译和部署工作流。
- **8,000+ AI回答笔记**——基于日常LLM辅助研究构建的知识库，可在博客上搜索。
- **MathJax、夜间模式、RSS、双语内容**——通过自定义CSS和主题增强的标准功能。

**规模：**

| 指标 | 数量 |
|--------|-------|
| 英文文章 | 10,264 |
| 中文文章 | 10,259 |
| AI回答笔记 | 9,794 |
| Python脚本 | 323 |
| ML脚本 | 191 |
| 页面浏览量（过去一个月） | ~70,000 |

![jekyll-ai-blog——拥有10K+文章、翻译、TTS和PDF管道的AI驱动博客](/assets/images/ai-portfolio/blog.png)

![Cloudflare Web Analytics——38.9K访问量、45.2K页面浏览量、930ms加载时间、82%良好LCP](/assets/images/ai-portfolio/cloudflare-analytics.png)

GitHub: [lzwjava/jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog)

---

## 🌳 Tree_Of_Thought——与一名高中生合作进行思维树推理

[Tree_Of_Thought](https://github.com/Cerynitius/Tree_Of_Thought)是一个朋友的工程——一个外部思维树推理系统，用于解决需要物理知识的难题。它不依赖模型在单个不透明完成中的隐藏思维链，而是将推理转化为一个显式、可检查、可控的树，具有实时状态、评分、剪枝和确定性工具支持。

该系统结合了用于长时间推理会话的FastAPI服务、用于检查和剪枝分支的浏览器UI、节点级状态机和树调度器、用于精确符号计算的SymPy支持的技能层，以及用于规划、建模、审查和评估的多模型路由。

**我的贡献（1个PR）：** 添加了一个兼容OpenAI的请求器和`python-dotenv`配置，使系统能够连接到任何兼容OpenAI的端点（本地或云端）。

**背景：** 我指导一名构建了这个系统的高中生。在一次会议中，他向我介绍了完整的架构——推理树、基于FSM的审查、路由局部增量优化。我把他介绍给AI博士研究员，并帮助他思考研究方向。他现在正在探索使用LLM解决物理问题，使用Codex（GPT-5.4）等工具，并构建多智能体协作编码系统。

![思维树——终端树浏览器，具有节点检查、前沿管理和分支剪枝功能](/assets/images/ai-portfolio/tree-of-thought.jpg)

GitHub: [Cerynitius/Tree_Of_Thought](https://github.com/Cerynitius/Tree_Of_Thought)

---

## 🤖 iclaw——终端AI代理（REPL）

[iclaw](https://github.com/lzwjava/iclaw)是一个终端AI代理，可以自主编码、搜索和运行命令——适用于个人机器和受限的企业机器。一个最小的openclaw实现，构建为纯Python CLI，无需浏览器扩展或IDE插件，由GitHub Copilot提供支持。

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
  /search              网络搜索（用法：/search <查询>）
  /provider_search     选择网络搜索提供商
  /proxy               设置HTTP/HTTPS代理（用法：/proxy [url|off]）
  /ca_bundle           设置HTTPS的CA包（用法：/ca_bundle [path|off]）
  /log                 设置日志详细级别（用法：/log [verbose|info]）
  /copy                将上一条Copilot响应复制到剪贴板
  /read                将文件内容打印到终端（用法：/read <路径>）
  /clear               清除对话历史
  /compact             使用LLM压缩对话历史
  /export              将完整对话历史导出为JSON文件
  /status              显示当前设置
  /help                显示可用命令
  /exit                退出REPL。
```

**关键特性：**

- 在终端中与GitHub Copilot或OpenRouter进行**多轮对话**。
- **多个模型提供商**：GitHub Copilot（OAuth设备流）和OpenRouter（API密钥）。
- **原生工具调用**：模型自动调用网络搜索、执行shell命令和编辑文件——无需人工介入。
- **多个搜索提供商**：DuckDuckGo、Startpage、Bing和Tavily。
- **企业友好**：无需IDE插件或浏览器扩展。在带有代理和CA包支持的企业防火墙后也能工作。
- **默认模型**：GPT-5.2。

![iclaw——具有原生工具调用功能的终端AI代理REPL](/assets/images/ai-portfolio/iclaw.jpg)

![iclaw——显示自主编码和shell命令的执行日志](/assets/images/ai-portfolio/iclaw-log.png)

GitHub: [lzwjava/iclaw](https://github.com/lzwjava/iclaw)

---

## ⚙️ zz——数据集处理与训练工具

[zz](https://github.com/lzwjava/zz)是一个用于ML训练管道的工具包——数据集下载、分词、提取和推理工具。在RunPod H200、DigitalOcean H100和家庭RTX 4070上的GPT-2 124M训练运行期间使用。也托管在[Hugging Face](https://huggingface.co/lzwjava/zz)上。

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

- **FineWeb下载**——规划并下载分片以达到令牌预算（100亿、1000亿+令牌），可中断恢复并支持进度跟踪。
- **hf-mirror.com支持**——当HuggingFace被屏蔽时，提供用于中国访问的wget脚本。
- **Parquet提取**——通过pyarrow iter_batches进行内存安全迭代。
- **分词**——将原始文本转换为训练就绪格式。
- **训练分析**——根据训练日志计算时长、指标评估。
- **DeepSeek推理**——用于DeepSeek-V2-Lite的LLM推理脚本。

![zz在Hugging Face上——数据集处理与训练工具，22个提交，3位贡献者](/assets/images/ai-portfolio/zz-huggingface.png)

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
