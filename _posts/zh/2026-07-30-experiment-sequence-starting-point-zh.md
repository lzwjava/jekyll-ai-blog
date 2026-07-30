---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 实验序列起点
translated: true
type: note
---

## 首先运行哪个实验

实验按顺序设计——但根据项目说明，核心是**实验4**。以下是推荐顺序：

### 🥇 从 **实验4** 开始 —— *Scheduler Watch*

```bash
cd /mnt/data/nano-vllm
python3.12 experiments/04_scheduler_watch.py
```

这被描述为**"推理系统的'损失曲线时刻'"**——唯一最重要的实验。你可以实时观察连续批处理：10个请求同时开始，然后逐步完成并离开批次。这是 vLLM 核心洞察的可视化呈现。

### 之后，按以下顺序获得完整图景

| # | 实验 | 原因 |
| --- | ------ | ------ |
| **4** | `04_scheduler_watch.py` ⭐ | 亲眼观察连续批处理 |
| **1** | `01_input_length.py` | 理解预填充（计算密集型）与解码（内存密集型） |
| **2** | `02_generation_length.py` | 观察 KV 缓存增长并拖慢解码 |
| **3** | `03_batch_scaling.py` | 理解批处理为何有帮助但也带来问题 |
| **5** | `05_kv_cache_pressure.py` | 观察 KV 缓存耗尽时发生的情况（抢占） |
| **6** | `06_config_sweep.py` | 调优权衡参数 |
| **7** | `07_mixed_length_batch.py` ⭐ | 理解连续批处理为何比静态批处理快 10 倍 |

### 运行任意实验的命令

```bash
cd /mnt/data/nano-vllm
python3.12 experiments/04_scheduler_watch.py   # 从这里开始
python3.12 experiments/07_mixed_length_batch.py # 同样标记为星标
python3.12 experiments/01_input_length.py       # 然后理解基础
# ... 等等
```

> **重要提示：** 始终使用 `python3.12`（而不是 `python3`）。系统自带的 `python3` 是 3.14.3 版本，超出了 nano-vllm 的支持范围（`>=3.10,<3.13`）。
