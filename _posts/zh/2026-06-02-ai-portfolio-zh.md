---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 我的AI作品集 — 每日AI工作的证据
translated: true
---

我不只是谈论 AI——我每天都在大规模使用它。这篇文章是我的 AI 工作视觉作品集：我构建的工具、消耗的 token，以及获得的认证。

---

## 🖥️ LLM 训练与推理——我的硬件配置

自 2023 年搭建机器学习工作站以来，我一直在进行训练和学习。

**硬件经验：**

| GPU | 显存 | 经验 | 使用场景 |
| ----- | ------ | ------------ | ------- |
| NVIDIA RTX 4070 | 12 GB | 3 年 | 家庭工作站 |
| NVIDIA H200 | 141 GB | 3 个月 | RunPod / DigitalOcean |
| AMD MI300X | 192 GB HBM3 | 3 个月 | AMD 开发者云 |

**我训练过的模型：**

- **GPT-2 124M** 在 FineWeb 数据集上从头训练（nanoGPT）——在 RTX 4070、H200 和 MI300X 上。
- **GPT-2 760M** 在 AMD MI300X（192 GB HBM3）上从头训练——探索 nanochat、DeepSeek v4 MoE。
- 超参数调优、学习率调度和数据集预处理的各种实验。

**工作站：**

![我的 ML 学习工作站——2023 年组装，RTX 4070 12GB，用于日常训练和实验](/assets/images/ai-portfolio/learning-station.jpg)

**AMD 开发者云——MI300X 192GB HBM3：**

![AMD 开发者云——用于大规模模型训练的 MI300X 实例](/assets/images/ai-portfolio/amd-dev-cloud.png)

---

### 🏋️ 训练运行总结

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
| 13 | SPGISpeech (Whisper) | transformers | 各不相同 | ? | ? | 仅脚本 |

## 🧠 增强版 nanoGPT——我的分支

Fork 了 [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT) 并扩展了额外的数据集管道、扩展训练配置和用于学习的内联形状注释。45 次提交，2025 年 11 月 – 2026 年 4 月。

**新增数据集管道：**

| 数据集 | 路径 | 描述 |
| --------- | ------ | ------------- |
| FineWeb-Edu | `data/fineweb/` | HuggingFace FineWeb-Edu（100 亿+ token）。基于分片的加载、分块处理、增量训练/验证集划分。 |
| OpenWebText 10k | `data/openwebtext_10k/` | 用于快速迭代的 10k 子集。 |
| Wikipedia Local | `data/wikipedia_local/` | 直接对本地纯文本转储进行分词（无需下载 HuggingFace）。 |

**新增训练配置：**

| 配置 | 目标 | 备注 |
| -------- | -------- | ------- |
| `train_fineweb.py` | 在 FineWeb 上训练 125M | 针对 RTX 4070 12 GB 调优（n_embd=384, dropout=0.1）。 |
| `train_fineweb1_5b.py` | 在 FineWeb 上训练 1.5B | 适用于 H200 80 GB。 |
| `train_fineweb_gpt3.py` | GPT-3 风格 100 亿 token | 基于分片的加载器，更宽的调度。 |
| `train_fineweb_760m.py` | 在 FineWeb 上训练 760M | 适用于 MI300X 192 GB HBM3。 |
| `train_gpt2_200m.py` | GPT-2 200M | 通用中型配置。 |
| `train_gpt2_200m_smoke.py` | 冒烟测试 | 快速 200M  sanity 检查（约几分钟）。 |

**模型修改：**

- **内联张量形状注释**遍布 `model.py` 的前向传播（CausalSelfAttention、MLP、GPT）——每一步都显示精确形状，并附带具体的 GPT-2 XL 示例，例如 `# x: (B, T, C) e.g. (1, 5, 1600)`。有助于理解 transformer 数据流。

![增强版 nanoGPT——45 次提交、数据集管道、扩展训练配置、内联形状注释](/assets/images/ai-portfolio/nanogpt-fork.png)

GitHub: [lzwjava/nanoGPT](https://github.com/lzwjava/nanoGPT)

---

## ⚙️ MoE 与 LLM 推理——阅读代码、运行代码、编译代码

在训练完密集的 GPT-2 模型后，我转向了 LLM 的架构和系统层面：**混合专家（Mixture-of-Experts，MoE）**和**高吞吐推理引擎**。我的学习方法简单且动手实践：**阅读代码、运行代码、破坏代码、从源码编译**——而不仅仅是阅读相关资料。

**我一直在学习的内容：**

- **MoE 架构**——将"多个 FFN"转化为路由 + 分发 + 专家计算 + 合并 + 负载均衡 + 分布式通信的心智模型。我研究 DeepSeek-MoE（细粒度 + 共享专家）、MegaBlocks（dropless 块稀疏分发）、Tutel（all-to-all 专家并行）和 Mixtral（8×7B，top-2）作为参考实现。
- **前向传播**——路由（`router_logits` → `topk(softmax(...))`）、逐专家计算，以及如何跨 GPU 加速 `tokens → experts → tokens`。
- **KV 缓存分页、prefill/decode 调度、连续批处理、CUDA graphs、前缀缓存、张量并行**——将模型变成生产引擎的完整服务栈。

**我的学习方法——阅读代码 / 运行调试 / 编译循环：**

1. **阅读代码**——在 mini-sglang 中端到端追踪 MoE：`router (LinearReplicated) → MoELayer → FusedMoe (top-k routing → block-aligned dispatch → 2 fused GEMMs → sum-reduce) → Triton grouped-GEMM kernel`。`fused_moe_kernel` 按专家分发排序、填充的 token 块，并在两个 SwiGLU GEMM 之间切换 `mul_routed_weight` 标志。
2. **运行调试与基准测试**——nano-vLLM 在我的 RTX 4070 上运行 Qwen3-0.6B，使用 flash-attention：**506 tok/s prefill**，decode 约 4–30 tok/s，在笔记本电脑基准测试中约 1434 tok/s，与 vLLM 本身相当或更优。
3. **从源码编译**——从源码构建了 **SGLang**（`pip install -e "python"`，修复了 torch/torchaudio CUDA 不匹配问题到 2.11.0+cu130，编译了 3 个 PyO3 Rust 扩展），并在 `localhost:30010` 上运行了一个 Qwen2.5-0.5B 服务器提供补全服务。还使用 `flash-attn==2.8.3` 预构建 wheel 让 nano-vLLM 运行起来。

**我具备基础知识的系统：**

| 概念 | 我通过阅读代码学到的东西 |
| --------- | -------------------------------- |
| **Paged KV cache** | 固定的 256-token 块、空闲列表、content-hash 前缀缓存、copy-on-write 共享 |
| **调度器** | 长提示的分块 prefill、decode 步进、KV cache 满时的抢占 |
| **CUDA graphs** | 捕获 decode 批次（`[1,2,4,…512]`）以减少 CPU 内核启动开销 |
| **MoE 分发** | `moe_align_block_size` 按专家对 token 块进行排序和填充，以实现高效的 Triton grouped-GEMM |
| **张量并行** | 行并行层的 `all_reduce`、LM head 的 `gather`、`LinearReplicated` 共享路由器 |
| **Fused MoE kernel** | gate/up 融合为一个 GEMM，SwiGLU 激活拆分，路由权重恰好应用一次 |

**我遵循的学习路径**——根据笔记，这是适用于大型系统的有效循环，也是我处理每个仓库的方式：

```text
read 20% → modify 30% → break things 30% → submit 20%
```

---

## 📝 SEC-EDGAR-GPT——在 SEC 文件上从头训练的 GPT-2（124M）

在 **15.5 亿 token** 的 SEC EDGAR 财务文件（10-K、10-Q 和其他公司披露文件）上从头训练了一个 **124M 参数 GPT-2**——在单张 **RTX 4070**（12 GB 显存）上训练约 **8 小时**，验证损失收敛到 2.28。

该模型能生成令人信服的 SEC 样板文本——风险因素、MD&A 部分、业务描述——并通过 RunPod 上的 FastAPI 服务器部署用于交互式聊天。

整个项目——模型训练、论文、聊天机器人和网站——在 **3 天内使用 Hermes Agent** 构建完成，展示了 AI 代理如何让 LLM 研究变得人人可及。

该项目在一家全球银行内部共享，获得 **200+ 次内部浏览**。一位首席工程师留下评论称其 *"nice"*。此外，受一位朋友关于循环 transformer 工作的启发，这个项目让我开始思考如何将金融 token 与自然语言 token 区别对待，以提高生成准确性。

![SEC-EDGAR-GPT 聊天机器人](/assets/images/sec-edgar-gpt/chatbot_web.png)

**代码：** [github.com/lzwjava/sec-edgar-gpt](https://github.com/lzwjava/sec-edgar-gpt) · **论文：** [sec-edgar-gpt.pdf](https://github.com/lzwjava/sec-edgar-gpt/raw/main/sec-edgar-gpt.pdf) · **模型：** [Hugging Face](https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf) · **聊天：** [sec-edgar-gpt.lzwjava.workers.dev](https://sec-edgar-gpt.lzwjava.workers.dev/)

---

## 📊 LLM API 使用量——数据

### OpenRouter——过去一年

消耗 11.5 亿 token，消费 $239，跨多个模型的 15.5 万次 API 请求。

![OpenRouter 活动仪表板——1 年内 11.5 亿 token、$239 消费、15.5 万次请求](/assets/images/ai-portfolio/openrouter-activity.png)

![OpenRouter 模型消费明细——Claude 4 Sonnet $44.40、Claude 3.5 Sonnet $9.67、Grok 3、Mistral、Kimi](/assets/images/ai-portfolio/openrouter-spend.png)

![OpenRouter 按模型的 token 使用量——MiniMax 2.4 亿、Gemini 2.03 亿、DeepSeek 1.1 亿](/assets/images/ai-portfolio/openrouter-models.png)

### 通过 SSSAICode 的 Claude API——2026 年 4 月

一个月 $171.53。2,555 次请求。1.15 亿+ token。90.9% 缓存命中率。

![SSSAICode Claude 使用量——Opus 4.6、Opus 4.7、Sonnet 4.6、Haiku 4.5](/assets/images/ai-portfolio/sssaicode-usage.png)

### 小米 MIMO 订阅——使用 12.5 亿 token

Pro 月付计划，38B 主配额 + 8.75B 补偿配额（约 4.6B 免费额度）。**2026 年 5 月至 6 月消耗 12.5 亿 token**。

![小米 MIMO Pro 计划——消耗 12.5 亿 token，剩余约 34 亿免费额度](/assets/images/ai-portfolio/xiaomi-mimo-usage.png)

#### 每月 token 使用明细

| 月份 | 模型 | 总 token | 输入（缓存命中） | 输入（缓存未命中） | 输出 | 请求数 |
| ------- | ------- | -------------: | -------------------: | --------------------: | -------: | ---------: |
| 2026-06 | mimo-v2.5 | 285,179 | 36,416 | 143,556 | 105,207 | 78 |
| 2026-06 | mimo-v2.5-pro | 734,873,374 | 710,036,672 | 21,617,131 | 3,219,571 | 10,704 |
| 2026-05 | mimo-v2.5 | 91,203 | 5,312 | 52,908 | 32,983 | 27 |
| 2026-05 | mimo-v2.5-pro | 508,851,211 | 488,291,136 | 17,725,731 | 2,834,344 | 8,649 |
| 2026-05 | mimo-v2-pro | 3,571,328 | 3,021,568 | 539,357 | 10,403 | 167 |

**月度总计：** 2026 年 5 月：**5.125 亿 token**（8,843 次请求） · 2026 年 6 月：**7.352 亿 token**（10,782 次请求）

> mimo-v2.5-pro 占使用量的主导地位（约占总量的 96%）。mimo-v2.5-pro 上约 96.7% 的缓存命中率保持了成本效率。6 月的 token 量较 5 月增长 43.5%。

### 汇总

| 平台 | token | 周期 | 成本 |
| ---------- | -------- | -------- | ------ |
| OpenRouter | 11.5 亿 | 过去一年 | $239 |
| SSSAICode (Claude) | 1.15 亿+ | 2026 年 4 月 | $171.53 |
| 小米 MIMO | 12.5 亿 | 2026 年 5 月–6 月 | 免费 4.6B 额度 |
| 其他（GitHub Copilot 等） | 5 亿 | 过去一年 | — |
| **总计** | **~30 亿+** | **过去一年** | **—** |

---

## 🏢 企业级 AI 使用——在英国环球银行

在一家英国环球银行（通过一家全球 IT 外包公司），我在编码助手之上构建了一个自主 AI 代理层，用于自动化脚本编写、日志记录、文档编写和测试。

**我构建的内容：**

- **20 个定制化 AI 代理**——针对不同的技术栈和工作流程提供专用提示词和上下文。
- **400 个可复用的编码助手编写脚本**——涵盖 Java、Spring、Python、Angular 和 DevOps 工具链的常见任务自动化。
- **1,800 份编码助手编写的指南**——在人工提示下由 AI 生成的文档。
- **通过编码助手 API 自动生成约 70 个测试用例**——涵盖 Spring Filters、Python unittest、JSON 截断、提示词工程和区域端点。

**成果：**

- 在整个企业的编码助手使用量中排名 **前 6%**（按 premium 请求衡量）。
- 因高知名度的 AIPlayer 项目获得 **贡献奖**。
- 加入了该银行的内部 AI 社区。

![AIPlayer 贡献奖](/assets/images/ai-portfolio/aiplayer.jpg)

---

## 🎤 AI 演讲——从神经网络到代理

在英国环球银行向 **80 名参与者** 做了一场技术演讲——包括高级顾问、专家、副总监、软件工程师和承包商。

**演讲：** *"从神经网络到代理"* —— 从最简单的神经网络（`y = wx`）出发，经过 MNIST、Transformers、GPT、nanoGPT，到构建个人 AI 代理的旅程。

**我涵盖的内容：**

- 从第一性原理理解神经网络——前向传播、反向传播、梯度下降
- Transformer 架构——Q/K/V 注意力、多头注意力、位置编码
- GPT 内部机制——分词、嵌入、训练、生成
- nanoGPT——在 H200/RTX 4070 上从头训练 GPT-2
- LLM 代理——Claude Code、OpenClaw、Hermes、工具调用、代理循环
- 真实数据——消耗 10 亿 token、H200 每小时 $3.44、钱真正花在哪里
- 我的路径——从阅读 Q/K/V 到从头训练模型的 3 年

**反馈：**

- 一位初级工程师说：*"你就是我想成为的人"* —— 这场演讲打开了他对 AI 可能性的认知
- 高级工程师赞赏第一性原理的方法——没有炒作，只有数学和代码
- 多次关于训练、代理和职业方向的后续对话

**幻灯片：** 使用 Claude Code 和 Marp 构建，源于我的公开 AI 回答笔记。

幻灯片（Marp）：[PDF](/assets/marp/neural_networks_to_agents_public.pdf)

---

## 🛠️ ww——跨平台 CLI 工具包

[ww](https://github.com/lzwjava/ww) 是我的旗舰 CLI 工具包——255+ 次提交、10+ 个命令组、跨平台（macOS + Linux）。涵盖带 AI 提交消息的 git 工作流、笔记管理、图像/PDF 处理、网页搜索、GitHub Copilot 聊天、系统实用程序和 LLM 驱动的辅助工具。

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

[jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog) 是 [lzwjava.github.io](https://lzwjava.github.io) 的源代码——一个使用 AI 自动化增强的 Jekyll 博客。10,000+ 英文文章、10,000+ 中文文章、9,700+ AI 回答笔记。过去一个月约 70,000 次页面浏览量（Cloudflare Analytics）。

```
lzwjava@lzw-mac jekyll-ai-blog % ls README.md
README.md
```

**它与标准 Jekyll 博客的不同之处：**

- **AI 驱动翻译**——基于 LLM 的翻译管道通过 GitHub Actions 自动将每篇文章扩展到多种语言。
- **Google Cloud Text-to-Speech**——自动生成文章的音频版本，用于无障碍访问。
- **XeLaTeX PDF/EPUB 生成**——从 Markdown 源文件生成高质量打印级 PDF 和电子书导出。
- **GitHub Actions CI/CD**——自动化的构建、测试、翻译和部署工作流。
- **8,000+ AI 回答笔记**——从日常 LLM 辅助研究构建的知识库，可在博客上搜索。
- **MathJax、夜间模式、RSS、双语内容**——通过自定义 CSS 和主题增强的标准功能。

**规模：**

| 指标 | 数量 |
| -------- | ------- |
| 英文文章 | 10,264 |
| 中文文章 | 10,259 |
| AI 回答笔记 | 9,794 |
| Python 脚本 | 323 |
| ML 脚本 | 191 |
| 页面浏览量（过去一个月） | ~70,000 |

![jekyll-ai-blog——AI 驱动的博客，拥有 10K+ 文章、翻译、TTS 和 PDF 管道](/assets/images/ai-portfolio/blog.png)

![Cloudflare Web Analytics——38.9K 访问量、45.2K 页面浏览量、930ms 加载时间、82% 良好 LCP](/assets/images/ai-portfolio/cloudflare-analytics.png)

GitHub: [lzwjava/jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog)

---

## 🎬 FluxReel——AMD 黑客松短视频工作室

[FluxReel](https://github.com/lzwjava/flux-reel) 将一行主题转化为 **15 秒竖屏短视频**（1080×1920，9:16，30 fps）——核心图像生成在 **AMD Radeon GPU（ROCm）** 上运行。为 AMD AI DevMaster 黑客松 2026-07 的 **赛道 1——多模态内容创作工具** 而构建。

**工作原理：**

1. **脚本**——LLM 根据主题起草一篇 300–500 字的 markdown 文章，然后场景规划器生成恰好 5 个场景，包含 `title` / `subtitle` / `image_prompt`（双语，从主题自动检测）。
2. **图像**——并行生成 5 张场景图像：通过 diffusers 使用 AMD GPU（FLUX.1-schnell / dev / 2-dev）、stable-diffusion.cpp（FLUX.1-schnell Q4_0 GGUF，低显存）或 OpenRouter。
3. **合成**——PIL 构建每个 1080×1920 幻灯片，包含标题/字幕栏，字体自动缩小以适应，支持 CJK 感知换行。
4. **组装**——ffmpeg 将每个幻灯片编码为 3 秒 H.264 片段，无需重新编码即可拼接，并混入背景音乐。

**关键特性：**

- **主题 → 视频只需几分钟**：从提示到精美 MP4 的完整管道，全程本地 AMD 运行。
- **双语字幕**——使用 Noto Sans CJK 字体和基于字符的换行自动检测英文/中文。
- **多个图像后端**——`local`（ROCm + diffusers FLUX）、`sdcpp`（GGUF 4-bit，低显存）、`openrouter`（云端回退）、`auto`（本地优先，回退到云端）。
- **Web UI + REST API**——FastAPI 服务器，带任务队列、进度轮询、视频预览和下载。
- **可选 YouTube 上传**——通过 LLM 自动生成标题/描述/标签。
- **远程 AMD GPU 管理**——rc-tunnel、通过 `hf-mirror.com` 下载 FLUX 模型（对中国友好）、GPU / ROCm / 磁盘信息。

**演示输出帧（1080×1920，9:16）：**

![FluxReel 演示帧 2——在 AMD GPU 上生成的 15 秒竖屏短视频](https://raw.githubusercontent.com/lzwjava/flux-reel/main/submission/demo_frame_2.jpg)

GitHub: [lzwjava/flux-reel](https://github.com/lzwjava/flux-reel)

---

## 🤖 iclaw——终端 AI 代理（REPL）

[iclaw](https://github.com/lzwjava/iclaw) 是一个终端 AI 代理，可以自主编写代码、搜索和执行命令——适用于个人机器和受限的企业环境。一个极简的 openclaw 实现，作为纯 Python CLI 构建，无需浏览器扩展或 IDE 插件，由 GitHub Copilot 驱动。

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

**关键特性：**

- 在终端中与 GitHub Copilot 或 OpenRouter 进行**多轮对话**。
- **多模型提供商**：GitHub Copilot（OAuth device flow）和 OpenRouter（API key）。
- **原生工具调用**：模型自主调用网页搜索、执行 shell 命令和编辑文件——无需人工介入。
- **多个搜索提供商**：DuckDuckGo、Startpage、Bing 和 Tavily。
- **企业友好**：无需 IDE 插件或浏览器扩展。支持代理和 CA bundle，可在企业防火墙后运行。
- **默认模型**：GPT-5.2。

![iclaw——具有原生工具调用的终端 AI 代理 REPL](/assets/images/ai-portfolio/iclaw.jpg)

![iclaw——显示自主编码和 shell 命令的执行日志](/assets/images/ai-portfolio/iclaw-log.png)

GitHub: [lzwjava/iclaw](https://github.com/lzwjava/iclaw)

---

## ⚙️ zz——数据集处理与训练工具

[zz](https://github.com/lzwjava/zz) 是用于 ML 训练管道的工具包——数据集下载、分词、提取和推理工具。在 RunPod H200、DigitalOcean H100 和家庭 RTX 4070 上进行 GPT-2 124M 训练运行期间使用。也托管在 [Hugging Face](https://huggingface.co/lzwjava/zz) 上。

```
lzwjava@lzw-mac zz % tree -L 1
scripts/
  download/     # Dataset download scripts (FineWeb, Wikimedia, HF mirrors)
  extract/      # Data extraction, tokenization, and renaming
  analysis/     # Training duration and metric evaluation
  deepseek/     # LLM inference scripts (DeepSeek-V2-Lite)
logs/           # Training logs and outputs
datasets/       # Downloaded dataset storage
```

**核心功能：**

- **FineWeb 下载**——规划并下载分片以达到 token 预算（100 亿、1000 亿+ token），可断点续传并带有进度跟踪。
- **hf-mirror.com 支持**——当 HuggingFace 被屏蔽时，提供 wget 脚本供中国访问。
- **Parquet 提取**——通过 pyarrow iter_batches 进行内存安全迭代。
- **分词**——将原始文本转换为训练就绪格式。
- **训练分析**——训练时长计算、从训练日志中评估指标。
- **DeepSeek 推理**——用于 DeepSeek-V2-Lite 的 LLM 推理脚本。

![zz on Hugging Face——数据集处理与训练工具，22 次提交，3 位贡献者](/assets/images/ai-portfolio/zz-huggingface.png)

GitHub: [lzwjava/zz](https://github.com/lzwjava/zz) · Hugging Face: [lzwjava/zz](https://huggingface.co/lzwjava/zz)

---

## 🎓 证书

### 机器学习专项课程——DeepLearning.AI 与斯坦福大学

2023 年 11 月完成。三门课程：监督式机器学习、高级学习算法、无监督学习、推荐系统、强化学习。

![Coursera 机器学习专项课程证书——李智维，2023 年 11 月](/assets/images/ai-portfolio/coursera-ml-1.png)

### 深度学习专项课程——DeepLearning.AI

2023 年 12 月完成。五门课程：神经网络、超参数调优、结构化机器学习项目、CNN、序列模型。

![Coursera 深度学习专项课程证书——李智维，2023 年 12 月](/assets/images/ai-portfolio/coursera-dl-1.png)

---

- GitHub: [https://github.com/lzwjava](https://github.com/lzwjava)
- 博客: [https://lzwjava.github.io](https://lzwjava.github.io)