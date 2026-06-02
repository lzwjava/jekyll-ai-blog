---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 我的AI作品集——每日AI工作证据
translated: true
---

我不只是说说AI——我每天都在大规模使用它。这篇文章是我的AI成果视觉作品集：我构建的工具、消耗的token以及获得的认证。

---

## 🖥️ LLM训练与推理——我的硬件设备

2023年搭建了我的机器学习工作站，从此开始训练和学习。

**硬件经验：**

| GPU | 显存 | 经验时长 | 使用场景 |
|-----|------|----------|----------|
| NVIDIA RTX 4070 | 12 GB | 3年 | 家庭工作站 |
| NVIDIA H200 | 141 GB | 3个月 | RunPod / DigitalOcean |
| AMD MI300X | 192 GB HBM3 | 3个月 | AMD Developer Cloud |

**我训练过的模型：**
- **GPT-2 124M** 从零开始基于FineWeb数据集（nanoGPT）——在RTX 4070、H200和MI300X上运行。
- **GPT-2 760M** 从零开始在AMD MI300X（192 GB HBM3）上训练——探索nanochat、DeepSeek v4 MoE。
- 各种关于超参数调优、学习率计划和数据集预处理的实验。

**工作站：**

![我的机器学习学习站——2023年搭建，RTX 4070 12GB，用于日常训练和实验](/assets/images/ai-portfolio/learning-station.jpg)

**AMD Developer Cloud——MI300X 192GB HBM3：**

![AMD Dev Cloud——用于大规模模型训练的MI300X实例](/assets/images/ai-portfolio/amd-dev-cloud.png)

---

## 📊 LLM API使用量——数据一览

### OpenRouter——过去一年

消耗9.27亿token，花费192美元，14.2万次API请求，覆盖多个模型。

![OpenRouter活动面板——9.27亿token，192美元花费，一年内14.2万次请求](/assets/images/ai-portfolio/openrouter-activity.png)

![OpenRouter模型花费明细——Claude 4 Sonnet $44.40，Claude 3.5 Sonnet $9.67，Grok 3，Mistral，Kimi](/assets/images/ai-portfolio/openrouter-spend.png)

![OpenRouter按模型划分的Token使用量——MiniMax 2.4亿，Gemini 2.03亿，DeepSeek 1.1亿](/assets/images/ai-portfolio/openrouter-models.png)

### 通过SSSAICode调用Claude API——2026年4月

一个月内花费171.53美元。2,555次请求。1.15亿+ token。90.9%缓存命中率。

![SSSAICode Claude使用情况——Opus 4.6、Opus 4.7、Sonnet 4.6、Haiku 4.5](/assets/images/ai-portfolio/sssaicode-usage.png)

### 小米MIMO订阅——已使用5亿Token

Pro月付计划，包含380亿主配额+87.5亿补偿配额（约46亿免费额度）。目前已消耗5亿token。

![小米MIMO Pro计划——已消耗5亿token，约46亿免费额度剩余](/assets/images/ai-portfolio/xiaomi-mimo-usage.png)

### 汇总

| 平台 | Token | 周期 | 费用 |
|------|-------|------|------|
| OpenRouter | 9.27亿 | 过去一年 | $192 |
| SSSAICode (Claude) | 1.15亿+ | 2026年4月 | $171.53 |
| 小米MIMO | 5亿 | 当前计划 | 免费46亿额度 |
| 其他 (GitHub Copilot等) | 5亿 | 过去一年 | — |
| **总计** | **~20亿+** | **过去一年** | **—** |

---

## 🏢 企业AI应用——汇丰银行

在汇丰银行（通过TEKsystems），我在GitHub Copilot之上构建了一个自主AI代理层，用于自动化脚本编写、日志记录、文档编写和测试。

**我构建的内容：**
- **20个定制的AI代理** ——针对不同技术栈和工作流程的专用提示和上下文。
- **400个可复用的Copilot编写脚本** ——跨Java、Spring、Python、Angular和DevOps工具链的常见任务自动化。
- **1,100份Copilot编写的指南** ——通过LLM输出生成并验证的文档，包含缓存和验证机制。
- **约70个通过Copilot API自动生成的测试用例** ——涵盖Spring过滤器、Python unittest、JSON截断、提示工程和区域端点。

**成果：**
- 在企业级Copilot使用量中排名**前6%**（按高级请求数计算）。
- 因高知名度AIPlayer项目获得**贡献奖**。
- 加入汇丰内部AI社区。

![GitHub Copilot——超过1600万安装量，集成到VS Code的AI结对程序员](/assets/images/ai-portfolio/copilot.png)

![汇丰银行AIPlayer贡献奖](/assets/images/ai-portfolio/aiplayer.jpg)

---

## 🛠️ ww——跨平台CLI工具包

[ww](https://github.com/lzwjava/ww) 是我的旗舰CLI工具包——255+次提交，10+个命令组，跨平台（macOS + Linux）。涵盖带AI提交信息的Git工作流、笔记管理、图片/PDF处理、网络搜索、GitHub Copilot聊天、系统工具以及LLM辅助功能。

```
lzwjava@lzw-mac ww % uv run ww --help
用法: ww <组> [命令] [选项]

Action:
  ww action [workflow.yml]  触发GitHub Actions工作流

AMD Dev Cloud:
  ww amd-dev-cloud snapshots    列出快照
  ww amd-dev-cloud start-train  创建GPU实例用于训练
  ww amd-dev-cloud end-train    创建快照并销毁GPU实例

Copilot:
  ww copilot auth           通过GitHub OAuth进行身份验证
  ww copilot chat           与Copilot模型对话

Git:
  ww git gpa            对所有仓库执行git pull --all
  ww git squash <n>     压缩最近n次提交
  ww git amend-push     修改最近一次提交并强制推送

LLM:
  ww llm compare <prompt>   比较多个LLM响应
  ww llm query <question>   查询本地RAG文档

Note:
  ww note              剪贴板内容转笔记（快速捕获）
  ww note process      处理笔记队列
  ww note watch        自动处理守护进程

Screenshot:
  ww screenshot              捕获并创建笔记
  ww screenshot interact-note  交互式截图笔记

255+次提交。10+个命令组。跨平台（macOS + Linux）。
```

![ww——GitHub上的跨平台CLI工具包](/assets/images/ai-portfolio/ww1.png)

---

## 📝 jekyll-ai-blog——AI驱动博客平台

[jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog) 是[lzwjava.github.io](https://lzwjava.github.io)的源码——一个通过AI自动化增强的Jekyll博客。10,000+篇英文文章，10,000+篇中文文章，9,700+条AI回答笔记。过去一个月约70,000次页面浏览量（Cloudflare Analytics统计）。

```
lzwjava@lzw-mac jekyll-ai-blog % ls README.md
README.md
```

**它与标准Jekyll博客的不同之处：**

- **AI驱动翻译** ——基于LLM的翻译流水线，通过GitHub Actions自动将每篇文章扩展到多种语言。
- **Google Cloud Text-to-Speech** ——自动生成文章音频版本，提升无障碍性。
- **XeLaTeX PDF/EPUB生成** ——从Markdown源生成高质量打印版PDF和电子书导出。
- **GitHub Actions CI/CD** ——自动化的构建、测试、翻译和部署工作流。
- **8,000+条AI回答笔记** ——基于日常LLM辅助研究构建的知识库，可在博客上搜索。
- **MathJax、夜间模式、RSS、双语内容** ——通过自定义CSS和主题增强的标准功能。

**规模：**

| 指标 | 数量 |
|------|------|
| 英文文章 | 10,264 |
| 中文文章 | 10,259 |
| AI回答笔记 | 9,794 |
| Python脚本 | 323 |
| ML脚本 | 191 |
| 页面浏览量（过去一个月） | ~70,000 |

![jekyll-ai-blog——AI驱动博客，1万+文章，翻译、TTS和PDF流水线](/assets/images/ai-portfolio/blog.png)

---

## 🤖 其他AI项目

### iclaw——终端AI代理（REPL）

[iclaw](https://github.com/lzwjava/iclaw) 是一个终端AI代理，可以自主编码、搜索和运行命令——适用于个人电脑和受限制的企业环境。一个极简的openclaw实现，构建为纯Python CLI，无需浏览器扩展或IDE插件，由GitHub Copilot驱动。

```
lzwjava@lzw-mac iclaw % iclaw

  ██  █████  ██       █████  ██   ██
  ██ ██      ██      ██   ██ ██   ██
  ██ ██      ██      ███████ ██ █ ██
  ██ ██      ██      ██   ██ ██████
  ██  █████  ███████ ██   ██  ███ ██

可用命令：
  /provider_model      选择和验证模型提供商
  /model               从提供商中选择特定模型
  /search              网络搜索（用法：/search <查询词>）
  /provider_search     选择网络搜索提供商
  /proxy               设置HTTP/HTTPS代理（用法：/proxy [url|off]）
  /ca_bundle           设置HTTPS的CA bundle（用法：/ca_bundle [path|off]）
  /log                 设置日志详细程度（用法：/log [verbose|info]）
  /copy                将最后一条Copilot响应复制到剪贴板
  /read                将文件内容打印到终端（用法：/read <路径>）
  /clear               清除对话历史
  /compact             使用LLM压缩对话历史
  /export              将完整对话历史导出为JSON文件
  /status              显示当前设置
  /help                显示可用命令
  /exit                退出REPL。
```

**主要特性：**
- **多轮对话** ——在终端中与GitHub Copilot或OpenRouter进行对话。
- **多模型提供商**：GitHub Copilot（OAuth设备流）和OpenRouter（API密钥）。
- **原生工具调用**：模型自主调用网络搜索、执行Shell命令和编辑文件——无需人工介入。
- **多搜索提供商**：DuckDuckGo、Startpage、Bing和Tavily。
- **企业友好**：无需IDE插件或浏览器扩展。支持代理和CA bundle，可在企业防火墙后工作。
- **默认模型**：GPT-5.2。

![iclaw——具有原生工具调用功能的终端AI代理REPL](/assets/images/ai-portfolio/iclaw.jpg)

![iclaw——显示自主编码和Shell命令的执行日志](/assets/images/ai-portfolio/iclaw-log.png)

### zz——数据集处理与训练工具

[zz](https://github.com/lzwjava/zz) 是一个ML训练流水线工具包——包含数据集下载、分词、提取和推理工具。在RunPod H200、DigitalOcean H100和家庭RTX 4070上进行GPT-2 124M训练时使用。也托管在[Hugging Face](https://huggingface.co/lzwjava/zz)上。

```
lzwjava@lzw-mac zz % tree -L 1
scripts/
  download/      # 数据集下载脚本（FineWeb、Wikimedia、HF镜像）
  extract/       # 数据提取、分词和重命名
  analysis/      # 训练时长和指标评估
  deepseek/      # LLM推理脚本（DeepSeek-V2-Lite）
logs/            # 训练日志和输出
datasets/        # 下载的数据集存储
```

**主要功能：**
- **FineWeb下载** ——规划和下载分片以达到token预算（100亿、1000亿+ token），支持断点续传和进度追踪。
- **hf-mirror.com支持** ——当HuggingFace被屏蔽时，提供wget脚本用于中国访问。
- **Parquet提取** ——通过pyarrow iter_batches实现内存安全的迭代。
- **分词** ——将原始文本转换为训练就绪格式。
- **训练分析** ——从训练日志计算时长和指标评估。
- **DeepSeek推理** ——DeepSeek-V2-Lite的LLM推理脚本。

![zz在Hugging Face上——数据集处理与训练工具，22次提交，3位贡献者](/assets/images/ai-portfolio/zz-huggingface.png)

---

## 🎓 证书

### 机器学习专项课程——DeepLearning.AI & 斯坦福大学

2023年11月完成。三门课程：监督式机器学习、高级学习算法、无监督学习、推荐系统、强化学习。

![Coursera机器学习专项课程证书——李智维，2023年11月](/assets/images/ai-portfolio/coursera-ml-1.png)

### 深度学习专项课程——DeepLearning.AI

2023年12月完成。五门课程：神经网络、超参数调优、结构化机器学习项目、卷积神经网络、序列模型。

![Coursera深度学习专项课程证书——李智维，2023年12月](/assets/images/ai-portfolio/coursera-dl-1.png)

---

* GitHub: https://github.com/lzwjava
* 博客: https://lzwjava.github.io