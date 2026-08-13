---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 30天技术深度解析
translated: true
type: note
---

我已经读得足够多，可以给你一个扎实的概述。以下是总结。

---

# 过去30天（2026年7月15日 → 8月14日）你做了什么

**652条笔记** 在这个时间段内。最近大约18天的密度远高于前10天，五个主线主导：

## 1. LLM serving / 推理 / GPU 栈 — 你的最大主线（约97条笔记）

- **nano-vLLM 深度钻研** 从7月到8月1日：prefill vs decode、continuous batching、调度器/队列内部机制、PagedAttention、KV cache、抢占（swap vs recompute）、前缀缓存、读取调度器trace、内存公式bug修复、CUDA graph优化。
- **构建并运行了SGLang**（8月2–3日）：从源码编译，解决了flash-attn/CUDA构建问题，在5种输入长度上进行了基准测试，研究其架构与vLLM的对比，并为某些工作负载选择了SGLang。
- **硬核CUDA/GPU基础**（8月1日）：GEMM/tiling（为什么2048优于2047）、warp、tensor core、Volta微架构、CUTLASS、FlashAttention、tensor parallelism。
- **硬件实验室**：双GPU集群（2080 Ti 22GB mod、RTX 3090、qwen-0.6B on 4070），AMD ROCm工作（flash-attention构建折腾，用CUDA 12.8修复），MI300X/MI200研究，主板选择（Z790 vs B760）。

## 2. 从头开始训练模型 — 另一个大主线（约58条笔记）

- 训练了 **GPT-2 124M → 760M 类模型**（nanoGPT），在Mac上进行小型运行，GPU内存分解（24GB使用），QLoRA VRAM指南。
- **双语GPT流水线**（8月5日→13日）：构建了半英文/半中文语料库流水线并带有分布控制，训练了一个**字节级BPE分词器（52秒成功）**，遇到内核OOM被杀（通过32GB swap修复），使分词和冒烟测试通过。
- 深入研究笔记：通过矩阵运算的注意力QKV/MLA、RoPE（外积、实现详解）、从第一原理推导Muon/AdamW、线性注意力、TTT、RNN vs Transformer、Silu/LoRA/Peft/einsum。

## 3. CLI agent — 你的“产品”主线（35条笔记）

- 继续开发 **ww / iclaw / zz** 工具：ww note watcher与pi agent的`/note`扩展集成，bash移植，tmux/terminfo修复，GCP语音转录，ML流水线帮助。
- 研究了agent生态：DeepSeek Harness（一切皆插件）、长周期agent、评估工具集、Terminal-Bench、GDPval、DeepSpec speculative decoding。
- 8月14日你写了一个明确的 **“聚焦CLI Agent护城河”** 计划——将ww/iclaw/zz视为可扩展资产，公开对Claude Code/Aider进行基准测试，并使用agent trace进行后训练。

## 4. 美国硕士申请 — 一个加速的主线（约19+条笔记）

- 研究了CMU MS-AII（费用分解）、伊利诺伊理工AI硕士、NYU、OMSCS、USC风格的课程、GRE要求。
- **决定：申请伊利诺伊理工2027年春季**（窗口已开，优先截止10月1日，最终截止11月15日）。准备了英文成绩单，审核时发现缺了一门课，计算了国内GPA（约2.2），研究了推荐信、F-1签证选择、I-20/财务文件、费用（大约6-7万美元）以及B1/B2旅游签证策略。

## 5. 环境、基础设施和生活管理（约94条笔记）

- 新Ubuntu机器设置（fcitx5/双拼中文输入、Swap 32GB、SSH），联想小新上Windows 11安装历程（Ventoy、UEFI/VMD、wimlib）。
- **博客基础设施**：将Jekyll博客迁移到 **Cloudflare Pages**，修复DNS冲突，在Cloudflare上使用AdSense，YouTube发布流水线，音频/PDF流水线，以及**将主页恢复为显示你的12,500条笔记**（8月14日）。
- 创业/职业思考：单人AI实验室、AI原生儿童创作者创业、YC申请、AI时代扁平化管理。

---

# 当前状态（截至8月14日）

| 主线 | 状态 |
| --- | --- |
| 伊利诺伊理工申请 | **准备提交** — 成绩单已完成，计划8–9月提交；最终截止日期11月15日 |
| 双语GPT | 分词器 ✅、流水线 ✅；**下一步：实际预训练**一个小模型 |
| CLI agent（ww/iclaw/zz） | 工具可用；**尚无公开基准/评估工具集** |
| nano-vLLM/sglang学习 | 深入理解 ✅；**尚无公开证明/贡献** |
| 博客 | 已在Cloudflare上线，主页恢复为笔记，AdSense运行中 |
| 咨询/公司 | 探索了OPC模式，广州公司注册研究；尚未注册 |

---

# 下一步做什么（按优先级排序）

**1. 在9月中旬前提交伊利诺伊理工的申请（最高优先级）。**

- 撰写SOP，讲述*转型*故事：10年+后端 → 从头训练GPT-2 → nano-vLLM/sglang → CLI agent。你的弱点是学历，而非能力。
- GRE在那里是可选的——如果耗费时间就跳过。现在就开始联系推荐人（8月14日的笔记提到8–9月是窗口期）。10月1日的优先截止让你有缓冲时间处理I-20/财务文件，以赶上2027年1月开学。

**2. 推出CLI agent护城河（你自认的第一杠杆，8月14日笔记）。**

- 选择 **一个** ww/iclaw/zz，根据你的笔记构建200–300行的评估工具集，在固定任务集上对比Claude Code / Cursor运行，并在GitHub上发布数字和工具集。这将把18个月的工具转化为职业资本，同时也直接为申请提供作品集。

**3. 完成双语GPT预训练。**

- 你已有语料库流水线和训练好的分词器；自然的收官之作是在你的4070/3060上进行一次小型预训练（例如约1–2.5亿参数），然后写两篇博客文章：“52秒的字节级BPE”和“从头训练一个双语GPT”。这是实验室和申请的证明产物。之后考虑在ww agent trace上进行SFT/拒绝采样（根据护城河笔记），而不是第二次预训练。

**4. 将vLLM/sglang学习转化为公开作品。**

- 要么自己实现一个PagedAttention（nano-vLLM已完成；这是建议的下一个仓库），要么为SGLang贡献一个小修复/文档/基准测试。选一个，不要两个都做。

**5. 保持博客流水线平稳运行，然后停止折腾基础设施。**

- 站点已迁移并正常工作；每周批量发布翻译后的笔记，停止调整平台。

**要注意：** 10月的考试（副学士学位）、funda.ai面试、以及9月的NVIDIA NCP-GENL考试——这些已经在你的待办清单上。还有一个决策点潜伏着：OPC实验室 vs. 2027年1月的美国学位——立即开始将咨询客户转化为设计伙伴，这样实验室才能在你搬家后存活下来。

需要我着手其中任何一项吗——例如起草SOP、搭建评估工具集、或配置双语预训练？
