---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 推理系统实验套件
translated: true
type: note
---

## 摘要

我构建了一套完整的实验套件（1326行），通过类似 nanoGPT 训练的实验循环来教授推理系统。以下是创建的内容：

### 创建的文件

```
experiments/
├── _00_utils.py                # 194 行 — 计时器、GPU 内存、调度器补丁
├── 01_input_length.py          # 133 行 — 改变提示长度（4→2048 token）
├── 02_generation_length.py     # 125 行 — 改变生成长度（8→512 token）
├── 03_batch_scaling.py         # 117 行 — 改变批大小（1→16）
├── 04_scheduler_watch.py       # 141 行 — ⭐ 实时观察连续批处理
├── 05_kv_cache_pressure.py     # 141 行 — KV 缓存耗尽与抢占
├── 06_config_sweep.py          # 245 行 — 扫描 gpu_mem、max_seqs、max_len
├── 07_mixed_length_batch.py    # 162 行 — ⭐ 混合长度批处理演示
├── README.md                   # 文档与学习指南
└── run_all.sh                  # 所有实验的编排脚本
```

另外修复了 `nanovllm/engine/llm_engine.py` 中的 atexit 双重释放问题。

### 你能学到什么

| 实验 | 关键见解 |
| --- | --- |
| **01** 输入长度 | Prefill 是计算密集型，Decode 是内存密集型。随着上下文变长，Decode 变慢，因为注意力需要读取整个 KV 缓存。 |
| **02** 生成长度 | 随着生成过程中 KV 缓存的增长，Decode 延迟增加。总时间与 max_tokens 成线性关系。 |
| **03** 批大小扩展 | 批处理提高了吞吐量，但增加了延迟。这催生了**连续批处理**。 |
| **04** 调度器观察 ⭐ | 你可以**观察**连续批处理：10 个序列同时启动，短序列先完成并提前离开，批处理动态缩小。 |
| **05** KV 缓存压力 | 当块耗尽时，序列被抢占（暂停并重启）。代价高昂！ |
| **06** 配置扫描 | `gpu_memory_utilization`、`max_num_seqs`、`max_model_len` 相互作用决定 KV 缓存容量。 |
| **07** 混合长度 ⭐ | 6 个请求长度差异巨大。短问答在故事仅生成 10 个 token 时就已完成。在静态批处理中，短请求需要等待——而在连续批处理中则不需要。 |

### 核心发现

实验 4 的轨迹完美展示了这一点：

```
Step 1:  PRE-FILL 10 seqs (760 tokens) — 全部同时到达
Step 2:  DECODE 10 seqs 并行
Step 4:  FINISHED seq[6] (短回答, 4 tokens) — 离开批次
Step 5:  剩余 9 个 seqs
Step 7:  FINISHED seq[4] (长上下文, 8 tokens) — 离开
...
Step 64: FINISHED seq[7] (文章, 64 tokens) — 最后一个完成
```

**这就是 vLLM 存在的原因。** 静态批处理会把每个序列都填充到最长长度。PagedAttention + 连续批处理让每个序列能够独立推进。

### 如何运行

```bash
cd /mnt/data/nano-vllm
bash experiments/run_all.sh           # 运行全部 7 个实验
# 或单独运行：
python3 experiments/04_scheduler_watch.py   # ⭐ 从这里开始
python3 experiments/07_mixed_length_batch.py # ⭐ 然后运行这个
```
