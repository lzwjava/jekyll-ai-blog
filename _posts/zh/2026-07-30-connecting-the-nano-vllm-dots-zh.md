---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 连接纳米vllm点
translated: true
type: note
---

以下是我在你的笔记、提交记录和 nano-vllm 项目中找到的内容。让我把它们串联起来。

---

## 📝 近期 nano-vllm 笔记时间线

你共有 **7 条笔记**，时间跨度从 2026 年 6 月 12 日到 7 月 29 日：

| 日期 | 笔记 |
| ------ | ------ |
| 6 月 12 日 | `nano-vllm-minimal-vllm-reimplementation-en.md` — 首次介绍 |
| 6 月 24 日 | `minimal-vllm-re-implementation-en.md` — 重复介绍 |
| 7 月 24 日 | `nano-vllm-architecture-and-performance-en.md` — 架构深入解析 |
| 7 月 24 日 | `running-nano-vllm-on-rtx-4070-en.md` — 安装指南 |
| 7 月 25 日 | `running-nano-vllm-setup-en.md` — 安装指南（再版） |
| 7 月 29 日 | `python-311-recommended-for-nano-vllm-en.md` — Python 版本 |
| 7 月 29 日 | `nano-vllm-system-architecture-analysis-en.md` — 全面的架构分析 |
| 7 月 29 日 | `done-nano-vllm-is-running-with-flash-attention-en.md` — ✅ 运行成功 |
| 7 月 29 日 | `learning-vllm-via-hands-on-iteration-en.md` — 方法论笔记 |

## 🧠 你不应该感到困惑——但你可能困惑的原因

你**深入阅读**了资料，并且**系统能够运行**。但阅读架构笔记和运行一次性的推理，与构建直觉并不是一回事。这里有 **3 个明显的差距**：

### 1. 你在三种不同的心智模型之间跳跃

| 系统 | 功能 |
| -------- | ------------- |
| **nanoGPT** | 从头训练 GPT 模型（损失曲线、数据集准备、优化器） |
| **nanochat** | 训练聊天模型（SFT、DDP、数据集管道） |
| **nano-vllm** | **部署**已训练好的模型（批处理、调度、KV 缓存管理） |

在 Transformer 的伞下，这些是**完全不同的领域**。nano-vllm 的难点不在于 Transformer 本身，而在于**服务基础设施**：调度器、块管理器、抢占、CUDA graphs、张量并行。

### 2. 实验文件存在但从未运行过

这是最大的发现：

```
experiments/
├── 01_input_length.py        ✅ 存在，从未运行
├── 02_generation_length.py   ✅ 存在，从未运行
├── 03_batch_scaling.py       ✅ 存在，从未运行
├── 04_scheduler_watch.py     ⭐ 最关键的一个，从未运行
├── 05_kv_cache_pressure.py   ✅ 存在，从未运行
├── 06_config_sweep.py        ✅ 存在，从未运行
├── 07_mixed_length_batch.py  ⭐ 第二个关键，从未运行
```

`experiments/` 目录是在一次提交（`649e84e`）中提交的，`git status` 显示**没有任何修改**——这意味着你写了这些文件，但**还没有运行它们**。

实验的 README 里明确写着：*“像学习 nanoGPT 那样学习推理系统：构建、破坏、测量、重复。”*——但你跳过了“运行”这一步。

### 3. nano-vllm 中的概念如果不实际观察，确实很难理解

调度器 + 块管理器的代码大约有 200 行，但包含了：

- **PagedAttention** — KV 缓存拆分成块，按需分配
- **前缀缓存** — 基于 xxhash 的块共享，用于请求之间
- **抢占** — 当 KV 缓存满时，驱逐正在运行的序列
- **分块预填充** — 将长提示分成多个步骤处理

这些概念你可以读 10 遍，但只有当你**观察轨迹**时才会真正理解。

---

## 🔬 解决方案：今晚运行实验 4

这是你推理系统的“损失曲线”时刻。实验 4（`04_scheduler_watch.py`）旨在向你展示：

```
预填充：10 个序列，760 个 token
  seq[4] prompt=507 blocks=[3,4]
  seq[6] prompt=2   blocks=[6]
  ...

解码：10 个序列并行运行
完成：seq[6]（生成了 4 个 token）← 最短的先完成
解码：剩余 9 个序列
完成：seq[4]（生成了 8 个 token）
解码：8 个序列
...
```

这一趟运行会让连续批处理的概念变得清晰，就像观察损失曲线让训练概念变得清晰一样。

### 建议操作

```bash
cd /mnt/data/nano-vllm
source .venv/bin/activate
python experiments/04_scheduler_watch.py
python experiments/07_mixed_length_batch.py
```

运行它们，观察轨迹，你就会不再疑惑“调度器是如何工作的？”——因为你已经亲眼看到了它如何运作。
