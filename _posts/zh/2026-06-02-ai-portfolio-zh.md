---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 我的AI作品集——日常AI工作证明
translated: true
---

我不只是谈论人工智能——我每天都在大规模使用它。这篇文章是我的AI成果视觉作品集：我构建的工具、我消耗的令牌数以及我获得的认证。

---

## 🖥️ LLM训练与推理——我的硬件设置

2023年搭建了我的机器学习工作站，并从此持续训练和学习。

**硬件经验：**

| GPU | 显存 | 经验时长 | 使用平台 |
| ----- | ------ | ------------ | ------- |
| NVIDIA RTX 4070 | 12 GB | 3 年 | 个人工作站 |
| NVIDIA H200 | 141 GB | 3 个月 | RunPod / DigitalOcean |
| AMD MI300X | 192 GB HBM3 | 3 个月 | AMD开发者云 |

**我训练过的模型：**

- **GPT-2 124M** 从零开始在FineWeb数据集上训练（nanoGPT）——分别在RTX 4070、H200和MI300X上进行。
- **GPT-2 760M** 从零开始在AMD MI300X（192 GB HBM3）上训练——探索nanochat、DeepSeek v4 MoE。
- 各种关于超参数调优、学习率调度和数据预处理的实验。

**工作站：**

![我的机器学习学习站——2023年搭建，RTX 4070 12GB，用于日常训练和实验](/assets/images/ai-portfolio/learning-station.jpg)

**AMD开发者云——MI300X 192GB HBM3：**

![AMD开发者云——用于大规模模型训练的MI300X实例](/assets/images/ai-portfolio/amd-dev-cloud.png)

---

### 🏋️ 训练运行摘要

| # | 模型 | 框架 | 参数量 | 硬件 | 步骤数 | 状态 |
| --- | ------- | ----------- | -------- | ---------- | ------- | -------- |
| 1 | FineWeb 125M 运行1 | nanoGPT | 124M | RTX 4070 | 20K | 已完成 |
| 2 | FineWeb 125M 运行2 | nanoGPT | 124M | RTX 4070 | 6K | 已完成 |
| 3 | FineWeb 125M 运行3 | nanoGPT | 124M | RTX 4070 | 11K | 已完成 |
| 4 | OpenWebText 125M | nanoGPT | 124M | RTX 4070 | 6K | 已完成 |
| 5 | FineWeb 125M MI300X | nanoGPT | 124M | MI300X | 750 | 冒烟测试 |
| 6 | FineWeb 760M | nanoGPT | 760M | MI300X | 76K/445K | 提前停止 |
| 7 | fineweb-edu-d12 | nanochat | 286M | RTX 4070 | 10K | 基础预训练完成 |
| 8 | rtx4070-d12-chinchilla | nanochat | 286M | RTX 4070 | 87K | **完全完成** |
| 9 | code-sec-fineweb-d12 | nanochat | 286M | H200? | 50K | 已完成 |
| 10 | code-sec-sft | nanochat | ~140M | H200? | 8,985 | 已完成 |
| 11 | codeparrot-d12 | nanochat | 286M | RTX 4070 | ? | 仅有脚本 |
| 12 | Notes SFT (Qwen3-4B) | trl/peft | 4B | RTX 4070 | ? | 仅有脚本 |
| 13 | SPGISpeech (Whisper) | transformers | 可变 | ? | ? | 仅有脚本 |

## 🧠 增强版 nanoGPT——我的分支

复刻了 [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT) 并进行了扩展，增加了额外的数据集处理流程、规模化的训练配置以及用于学习的联机形状注释。45次提交，2025年11月至2026年4月。

**新增数据集处理流程：**

| 数据集 | 路径 | 描述 |
| --------- | ------ | ------------- |
| FineWeb-Edu | `data/fineweb/` | HuggingFace FineWeb-Edu（100亿+ token）。基于分片的加载、分块处理、增量训练/验证集划分。 |
| OpenWebText 10k | `data/openwebtext_10k/` | 快速10k子集用于快速迭代。 |
| 本地维基百科 | `data/wikipedia_local/` | 直接对本地纯文本转储进行分词（无需HuggingFace下载）。 |

**新增训练配置：**

| 配置 | 目标 | 备注 |
| -------- | -------- | ------- |
| `train_fineweb.py` | 125M 在FineWeb上 | 针对RTX 4070 12 GB优化（n_embd=384, dropout=0.1）。 |
| `train_fineweb1_5b.py` | 1.5B 在FineWeb上 | 适用于H200 80 GB。 |
| `train_fineweb_gpt3.py` | GPT-3风格 100亿 token | 基于分片的加载器，更宽的调度。 |
| `train_fineweb_760m.py` | 760M 在FineWeb上 | 适用于MI300X 192 GB HBM3。 |
| `train_gpt2_200m.py` | GPT-2 200M | 通用中型配置。 |
| `train_gpt2_200m_smoke.py` | 冒烟测试 | 快速200M完整性检查（约几分钟）。 |

**模型变更：**

- 在 `model.py` 的前向传播中增加了**联机张量形状注释**（CausalSelfAttention, MLP, GPT）——以具体的GPT-2 XL示例展示每一步的精确形状，例如 `# x: (B, T, C) 例如 (1, 5, 1600)`。有助于理解Transformer数据流。

![增强版 nanoGPT——45次提交，数据集处理流程，规模化训练配置，联机形状注释](/assets/images/ai-portfolio/nanogpt-fork.png)

GitHub: [lzwjava/nanoGPT](https://github.com/lzwjava/nanoGPT)

---

## ⚙️ MoE与LLM推理——刚刚开始学习

在训练了密集的GPT-2模型之后，我想看看LLM的架构和系统层面：**混合专家模型（MoE）** 和**推理引擎**。老实说，我在这方面才刚刚起步。我读了一些代码，运行了一些东西，并跟着做了——但我无法从头编写任何这些内容，我仍然认为自己在很大程度上还是个初学者。

**我开始了解的内容：**

- **MoE架构**——路由 + 分发 + 专家计算 + 合并 + 负载均衡的高层图景。我粗略浏览了DeepSeek-MoE（细粒度 + 共享专家）、MegaBlocks（无丢弃的块稀疏分发）、Tutel（all-to-all专家并行）和Mixtral（8×7B, top-2）作为参考实现——主要是通过AI代理带我阅读代码。
- **前向传播**——路由（`router_logits` → `topk(softmax(...))`）、每个专家的计算，以及如何让 `tokens → experts → tokens` 在跨GPU时变得快速。我能理解这个流程，但自己还无法权衡其中的利弊。
- **KV缓存分页、预填充/解码调度、连续批处理、CUDA图、前缀缓存、张量并行**——我知道这些名字和大致的想法，但服务栈很深，我只触及了皮毛。

**我的学习方式——使用代理进行探索：**

1. **阅读代码**——我使用编码代理（例如Hermes Agent）帮助我在 mini-sglang 中端到端地追踪MoE：`router (LinearReplicated) → MoELayer → FusedMoe (top-k路由 → 块对齐分发 → 2个融合GEMM → sum-reduce) → Triton分组GEMM内核`。当代理带我过一遍时我能理解；但我自己还无法复现。
2. **运行并基准测试**——让 nano-vLLM 在我的 RTX 4070 上使用flash-attention运行 Qwen3-0.6B：**506 tok/s 预填充**，解码约4–30 tok/s，在笔记本基准测试中约1434 tok/s。我把这些视为数据点，而不是任何东西的证明。
3. **从源码编译**——从源码构建了 **SGLang**（`pip install -e "python"`，修复了一个 torch/torchaudio CUDA 不匹配问题至 2.11.0+cu130，编译了它的3个 PyO3 Rust扩展），并让 Qwen2.5-0.5B 服务器在 `localhost:30010` 上提供补全服务。还让 nano-vLLM 使用预编译的 `flash-attn==2.8.3` wheels 运行。能让东西构建起来是一回事；深入理解它们则是另一回事。

**我目前学到的（仍然很浅显）：**

| 概念 | 我理解的内容 |
| --------- | -------------------------------- |
| **分页KV缓存** | 固定的256 token块、空闲列表、内容哈希前缀缓存、写时复制共享——仅高层概念 |
| **调度器** | 长提示的分块预填充、解码步进、KV缓存满时的抢占——大致了解 |
| **CUDA图** | 捕获解码批次（`[1,2,4,…512]`）以减少CPU内核启动开销——动机理解了，细节不详 |
| **MoE分发** | `moe_align_block_size` 排序 + 填充每个专家的token块以实现高效的Triton分组GEMM——跟着代码走过一次 |
| **张量并行** | 行并行层的 `all_reduce`、LM头的 `gather`、`LinearReplicated`共享路由器——现在能理解这些名字了 |
| **融合MoE内核** | 门/上投影融合为一个GEMM，SwiGLU激活拆分，路由权重仅应用一次——读过，记忆不完整 |

**我的处理方法**——老实说，我的很多“阅读”都是代理阅读代码然后向我解释。循环大致是这样：

```text
阅读20% → 修改30% → 弄坏东西30% → 提交20%
```

我接触这个才几周时间。我懂的刚好能跟上关于MoE推理的对话——但还不足以自己构建或改进这类系统。

---

## 📝 SEC-EDGAR-GPT——在SEC文件上从零训练的GPT-2（124M）

在 **15.5亿 tokens** 的SEC EDGAR金融文件（10-K、10-Q、及其他公司披露文件）上从零训练了一个 **1.24亿参数的GPT-2**——在单个 **RTX 4070**（12 GB显存）上训练了约8小时，验证损失收敛至2.28。

该模型能生成令人信服的SEC标准文本——风险因素、管理层讨论与分析、业务描述——并通过 RunPod 上的 FastAPI 服务器部署用于交互式聊天。

整个项目——模型训练、论文、聊天机器人和网站——在 **3天内使用 Hermes Agent** 构建完成，展示了AI代理如何让LLM研究变得触手可及。

该项目在一家全球银行内部共享，获得了 **200多次内部浏览**。一位首席工程师留言称其为 *“不错”*。此外，受一位朋友关于循环Transformer工作的启发，该项目让我思考是否应该将金融令牌与自然语言令牌区别对待，以提高生成准确性。

![SEC-EDGAR-GPT 聊天机器人](/assets/images/sec-edgar-gpt/chatbot_web.png)

**代码：** [github.com/lzwjava/sec-edgar-gpt](https://github.com/lzwjava/sec-edgar-gpt) · **论文：** [sec-edgar-gpt.pdf](https://github.com/lzwjava/sec-edgar-gpt/raw/main/sec-edgar-gpt.pdf) · **模型：** [Hugging Face](https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf) · **聊天：** [sec-edgar-gpt.lzwjava.workers.dev](https://sec-edgar-gpt.lzwjava.workers.dev/)

---

## 📊 LLM API 使用情况——数据

### OpenRouter——过去一年

消耗22.8亿 tokens，花费$239，155K次API请求，覆盖多个模型。

![OpenRouter 活动仪表板——过去一年 22.8亿 tokens，$239 花费，155K 请求](/assets/images/ai-portfolio/openrouter-activity.png)

### DeepSeek——过去一年

过去一年通过 DeepSeek 平台消耗了6.29亿 tokens。

### 通过 SSSAICode 使用的 Claude API——2026年4月

一个月 $171.53。2,555 次请求。1.15亿+ tokens。90.9% 缓存命中率。

![SSSAICode 的 Claude 使用情况——Opus 4.6, Opus 4.7, Sonnet 4.6, Haiku 4.5](/assets/images/ai-portfolio/sssaicode-usage.png)

### 小米 MIMO 订阅——已使用 12.5亿 Tokens

Pro 月套餐，包含 380亿 主配额 + 87.5亿 补偿配额（约46亿免费额度）。2026年5月至6月期间**消耗12.5亿 tokens**。

![小米 MIMO Pro 套餐——已消耗 12.5亿 tokens，剩余约34亿免费额度](/assets/images/ai-portfolio/xiaomi-mimo-usage.png)

#### 每月 Token 使用明细

| 月份 | 模型 | 总 Tokens | 输入（缓存命中） | 输入（缓存未命中） | 输出 | 请求数 |
| ------- | ------- | -------------: | -------------------: | --------------------: | -------: | ---------: |
| 2026-06 | mimo-v2.5 | 285,179 | 36,416 | 143,556 | 105,207 | 78 |
| 2026-06 | mimo-v2.5-pro | 734,873,374 | 710,036,672 | 21,617,131 | 3,219,571 | 10,704 |
| 2026-05 | mimo-v2.5 | 91,203 | 5,312 | 52,908 | 32,983 | 27 |
| 2026-05 | mimo-v2.5-pro | 508,851,211 | 488,291,136 | 17,725,731 | 2,834,344 | 8,649 |
| 2026-05 | mimo-v2-pro | 3,571,328 | 3,021,568 | 539,357 | 10,403 | 167 |

**月度总计：** 2026年5月：**5.125亿 tokens**（8,843次请求）· 2026年6月：**7.352亿 tokens**（10,782次请求）

> mimo-v2.5-pro 占主导地位（约占总量的96%）。mimo-v2.5-pro 上的缓存命中率约为96.7%，保持成本效益。6月份的token量较5月份增长43.5%。

### 总结

| 平台 | Tokens | 时间段 | 费用 |
| ---------- | -------- | -------- | ------ |
| OpenRouter | 22.8亿 | 过去一年 | $239 |
| DeepSeek | 6.29亿 | 过去一年 | — |
| SSSAICode (Claude) | 1.15亿+ | 2026年4月 | $171.53 |
| 小米 MIMO | 12.5亿 | 2026年5–6月 | 免费46亿额度 |
| 其他（GitHub Copilot等） | 7.26亿 | 过去一年 | — |
| **总计** | **约50亿** | **过去一年** | **—** |

---

## 🏢 企业AI应用——在英国环球银行

在一家英国环球银行（通过一家全球IT外包公司），我在编码助手之上构建了一个自主AI代理层，用于自动化脚本编写、日志记录、文档编写和测试。

**我构建的内容：**

- **20个定制化的AI代理**——为不同的技术栈和工作流程提供专用提示和上下文。
- **400个由编码助手编写的可复用脚本**——跨Java、Spring、Python、Angular和DevOps工具的常见任务自动化。
- **1,800份由编码助手编写的指南**——在人类提示下由AI生成的文档。
- **通过编码助手API自动生成了约70个测试用例**——涵盖Spring Filters、Python unittest、JSON截断、提示工程和区域端点。

**成果：**

- 在整个企业中，按高级请求衡量，编码助手使用量排名**前6%**。
- 因高知名度的 AIPlayer 项目获得**贡献奖**。
- 加入该银行内部AI社区。

![AIPlayer 贡献奖](/assets/images/ai-portfolio/aiplayer.jpg)

---

## 🎤 AI讲座——从神经网络到Agent

向一家英国环球银行的 **80名参与者** 进行了一场技术讲座——包括高级顾问、专家、副总监、软件工程师和承包商。

**讲座：** *“从神经网络到Agent”*——从最简单的神经网络（`y = wx`）出发，途经MNIST、Transformers、GPT、nanoGPT，一直到构建个人AI Agent的旅程。

**我涵盖的内容：**

- 神经网络基本原理——前向传播、反向传播、梯度下降
- Transformer架构——Q/K/V注意力、多头注意力、位置编码
- GPT内部机制——分词、嵌入、训练、生成
- nanoGPT——在H200/RTX 4070上从零训练GPT-2
- LLM Agent——Claude Code、OpenClaw、Hermes、工具调用、Agent循环
- 真实数据——消耗10亿 tokens，H200每小时$3.44，钱的真正去向
- 我的路径——从阅读Q/K/V文章到从零训练模型，历时3年

**反馈：**

- 一位初级工程师说：*“你就是我想成为的人”*——这场讲座让他看到了AI的无限可能
- 高级工程师们欣赏这种从基本原理出发的方法——没有炒作，只有数学和代码
- 后续多次关于训练、Agent和职业方向的对话

**幻灯片：** 使用 Claude Code 和 Marp 构建，基于我的公开AI回答笔记。

幻灯片 (Marp)：[PDF](/assets/marp/neural_networks_to_agents_public.pdf)

---

## 🛠️ ww——跨平台CLI工具包

[ww](https://github.com/lzwjava/ww) 是我的旗舰CLI工具包——255+次提交，10+个命令组，跨平台（macOS + Linux）。涵盖带有AI提交消息的git工作流、笔记管理、图像/PDF处理、网页搜索、GitHub Copilot聊天、系统工具和LLM驱动的辅助工具。

```
lzwjava@lzw-mac ww % uv run ww --help
用法：ww <组> [命令] [选项]

操作：
  ww action [workflow.yml]  触发 GitHub Actions 工作流

AMD Dev Cloud：
  ww amd-dev-cloud snapshots    列出快照
  ww amd-dev-cloud start-train  创建用于训练的 GPU droplet
  ww amd-dev-cloud end-train    快照并销毁 GPU droplet

Copilot：
  ww copilot auth           通过 GitHub OAuth 进行身份验证
  ww copilot chat           与 Copilot 模型聊天

Git：
  ww git gpa            对所有仓库执行 Git pull --all
  ww git squash <n>     压缩最近 n 次提交
  ww git amend-push     修改最近提交并强制推送

LLM：
  ww llm compare <prompt>   比较多个 LLM 回复
  ww llm query <question>   查询本地 RAG 文档

笔记：
  ww note              剪贴板到笔记（快速捕获）
  ww note process      清空笔记队列
  ww note watch        自动处理守护进程

截图：
  ww screenshot              捕获并创建笔记
  ww screenshot interact-note  交互式截图笔记

255+次提交。10+个命令组。跨平台（macOS + Linux）。
```

![ww —— GitHub 上的跨平台 CLI 工具包](/assets/images/ai-portfolio/ww1.png)

GitHub: [lzwjava/ww](https://github.com/lzwjava/ww)

---

## 📝 jekyll-ai-blog——AI驱动博客平台

[jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog) 是 [lzwjava.github.io](https://lzwjava.github.io) 的源代码——一个通过AI自动化增强的Jekyll博客。10,000+ 英文帖子，10,000+ 中文帖子，9,700+ AI回答笔记。过去一个月约70,000次页面浏览（Cloudflare分析）。

```
lzwjava@lzw-mac jekyll-ai-blog % ls README.md
README.md
```

**它与标准Jekyll博客的不同之处：**

- **AI驱动翻译**——基于LLM的翻译流程，通过GitHub Actions自动将每篇帖子扩展到多种语言。
- **Google Cloud Text-to-Speech**——自动生成帖子的音频版本，提高可访问性。
- **XeLaTeX PDF/EPUB生成**——从Markdown源生成高质量的打印版PDF和电子书导出。
- **GitHub Actions CI/CD**——自动化构建、测试、翻译和部署工作流。
- **8,000+ AI回答笔记**——基于日常LLM辅助研究构建的知识库，可在博客上搜索。
- **MathJax、夜间模式、RSS、双语内容**——通过自定义CSS和主题增强的标准功能。

**规模：**

| 指标 | 数量 |
| -------- | ------- |
| 英文帖子 | 10,264 |
| 中文帖子 | 10,259 |
| AI回答笔记 | 9,794 |
| Python脚本 | 323 |
| 机器学习脚本 | 191 |
| 页面浏览量（过去一月） | ~70,000 |

![jekyll-ai-blog —— 拥有10K+帖子、翻译、TTS和PDF管道的AI驱动博客](/assets/images/ai-portfolio/blog.png)

![Cloudflare Web Analytics —— 38.9K次访问，45.2K次页面浏览，930ms加载时间，82%良好LCP](/assets/images/ai-portfolio/cloudflare-analytics.png)

GitHub: [lzwjava/jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog)

---

## 🎬 FluxReel——AMD黑客马拉松短视频工作室

[FluxReel](https://github.com/lzwjava/flux-reel) 将一个一行主题转变成 **15秒的垂直短视频**（1080×1920, 9:16, 30 fps）——核心图像生成在 **AMD Radeon GPU (ROCm)** 上运行。为2026年7月AMD AI DevMaster黑客马拉松**赛道1——多模态内容创作工具**而构建。

**工作原理：**

1. **脚本**——LLM根据主题起草一篇300–500字的markdown文章，然后场景规划器精确生成5个场景，包含 `title` / `subtitle` / `image_prompt`（双语，根据主题自动检测）。
2. **图像**——并行生成5个场景图像：通过AMD GPU使用diffusers（FLUX.1-schnell / dev / 2-dev）、stable-diffusion.cpp（FLUX.1-schnell Q4_0 GGUF，低显存）或OpenRouter。
3. **合成**——PIL构建每个1080×1920的幻灯片，包含标题/副标题栏，字体自动缩小以适应，支持CJK换行。
4. **组装**——ffmpeg将每个幻灯片编码为3秒H.264片段，无需重新编码即可连接，并混合背景音乐。

**主要特点：**

- **主题到视频只需几分钟**：从提示到精美的MP4的完整流程，在AMD本地完成。
- **双语字幕**——使用Noto Sans CJK字体和基于字符的换行自动检测英文/中文。
- **多种图像后端**——`local`（ROCm + diffusers FLUX）、`sdcpp`（GGUF 4位，低显存）、`openrouter`（云回退）、`auto`（优先本地，失败后回退到云）。
- **Web UI + REST API**——FastAPI服务器，带有任务队列、进度轮询、视频预览和下载。
- **可选的YouTube上传**——通过LLM自动生成标题/描述/标签。
- **远程AMD GPU管理**——rc-tunnel，通过 `hf-mirror.com`（对中国友好）下载FLUX模型，GPU / ROCm / 磁盘信息。

**演示输出帧（1080×1920, 9:16）：**

![FluxReel 演示帧2 —— 在AMD GPU上生成的15秒垂直短视频](https://raw.githubusercontent.com/lzwjava/flux-reel/main/submission/demo_frame_2.jpg)

**🏆 AMD AI DevMaster 黑客马拉松——完成奖**（0121 李智维）：

![AMD AI DevMaster 黑客马拉松完成奖 —— FluxReel](/assets/images/ai-portfolio/fluxreel-award.png)

GitHub: [lzwjava/flux-reel](https://github.com/lzwjava/flux-reel)

---

## 🤖 iclaw——终端AI Agent（REPL）

[iclaw](https://github.com/lzwjava/iclaw) 是一个终端AI Agent，可以自主编码、搜索和运行命令——适用于个人机器和受严格管控的企业机器。一个最小化的 openclaw 实现，构建为纯 Python CLI，无需浏览器扩展或IDE插件，由 GitHub Copilot 提供支持。

```
lzwjava@lzw-mac iclaw % iclaw

  ██  █████  ██       █████  ██   ██
  ██ ██      ██      ██   ██ ██   ██
  ██ ██      ██      ███████ ██ █ ██
  ██ ██      ██      ██   ██ ██████
  ██  █████  ███████ ██   ██  ███ ██

可用命令：
  /provider_model      选择并验证模型提供商
  /model               从您的提供商选择特定模型
  /search              网页搜索（用法：/search <查询>）
  /provider_search     选择网页搜索提供商
  /proxy               设置 HTTP/HTTPS 代理（用法：/proxy [url|off]）
  /ca_bundle           为 HTTPS 设置 CA 包（用法：/ca_bundle [path|off]）
  /log                 设置日志详细程度（用法：/log [verbose|info]）
  /copy                复制上次 Copilot 回复到剪贴板
  /read                打印文件内容到终端（用法：/read <路径>）
  /clear               清除对话历史
  /compact             使用 LLM 压缩对话历史
  /export              导出完整对话历史到 JSON 文件
  /status              显示当前设置
  /help                显示可用命令
  /exit                退出 REPL。
```

**主要特点：**

- **多轮对话**，在终端中使用 GitHub Copilot 或 OpenRouter。
- **多个模型提供商**：GitHub Copilot（OAuth设备流）和 OpenRouter（API密钥）。
- **原生工具调用**：模型自主调用网页搜索、执行Shell命令和编辑文件——无需人工干预。
- **多个搜索提供商**：DuckDuckGo、Startpage、Bing 和 Tavily。
- **对企业友好**：无需IDE插件或浏览器扩展。支持代理和CA包，可在企业防火墙后工作。
- **默认模型**：GPT-5.2。

![iclaw —— 具有原生工具调用功能的终端AI Agent REPL](/assets/images/ai-portfolio/iclaw.jpg)

![iclaw —— 显示自主编码和Shell命令的执行日志](/assets/images/ai-portfolio/iclaw-log.png)

GitHub: [lzwjava/iclaw](https://github.com/lzwjava/iclaw)

---

## ⚙️ zz——数据集处理与训练工具

[zz](https://github.com/lzwjava/zz) 是一个用于机器学习训练管道的工具包——包括数据集下载、分词、提取和推理工具。在 RunPod H200、DigitalOcean H100 和家用 RTX 4070 上的 GPT-2 124M 训练运行期间使用。也托管在 [Hugging Face](https://huggingface.co/lzwjava/zz) 上。

```
lzwjava@lzw-mac zz % tree -L 1
scripts/
  download/     # 数据集下载脚本（FineWeb, Wikimedia, HF mirrors）
  extract/      # 数据提取、分词和重命名
  analysis/     # 训练持续时间和指标评估
  deepseek/     # LLM 推理脚本（DeepSeek-V2-Lite）
logs/           # 训练日志和输出
datasets/       # 下载的数据集存储
```

**主要功能：**

- **FineWeb 下载**——规划并下载分片以达到 token 预算（100亿、1000亿+ tokens），支持断点续传并带有进度跟踪。
- **hf-mirror.com 支持**——当 HuggingFace 被屏蔽时，提供中国访问的 wget 脚本。
- **Parquet 提取**——通过 pyarrow 的 `iter_batches` 实现内存安全迭代。
- **分词**——将原始文本转换为训练就绪格式。
- **训练分析**——从训练日志计算持续时间和指标评估。
- **DeepSeek 推理**——用于 DeepSeek-V2-Lite 的 LLM 推理脚本。

![zz 在 Hugging Face 上 —— 数据集处理 & 训练工具，22 次提交，3 位贡献者](/assets/images/ai-portfolio/zz-huggingface.png)

GitHub: [lzwjava/zz](https://github.com/lzwjava/zz) · Hugging Face: [lzwjava/zz](https://huggingface.co/lzwjava/zz)

---

## 🎓 证书

### 机器学习专项课程——DeepLearning.AI 与斯坦福大学

完成于2023年11月。三门课程：监督式机器学习、高级学习算法、无监督学习、推荐系统、强化学习。

![Coursera 机器学习专项课程证书 —— 李智维，2023年11月](/assets/images/ai-portfolio/coursera-ml-1.png)

### 深度学习专项课程——DeepLearning.AI

完成于2023年12月。五门课程：神经网络、超参数调优、结构化机器学习项目、卷积神经网络、序列模型。

![Coursera 深度学习专项课程证书 —— 李智维，2023年12月](/assets/images/ai-portfolio/coursera-dl-1.png)

---

- GitHub: [https://github.com/lzwjava](https://github.com/lzwjava)
- 博客: [https://lzwjava.github.io](https://lzwjava.github.io)

---

AI翻译提示：British Universal Bank（英国环球银行）。
