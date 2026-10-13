---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 当前仓库算法：快速排序和Word2Vec
translated: true
type: note
---

以下是仓库中目前所有的算法/实现：

## 1. Quicksort — Lomuto 分区方案（3 种语言）

三种语言中的算法完全相同，用于对 10,000 个整数进行跨语言基准测试：

| 文件 | 说明 |
|---|---|
| `quicksort.py` | 递归，pivot = 最后一个元素，`i`/`j` 交换扫描；使用 `time.perf_counter()` 计时 |
| `Quicksort.java` | 相同的 Lomuto 分区；使用种子 `Random(42)`，用 `System.nanoTime()` 计时 |
| Rust 版本 | README 中提到（“通过 TUI 项目的主二进制文件”）——但实际已不在 `src/` 中；README 在这点上已经过时 |

特点：最后一个元素作为 pivot（无随机化 → 在已排序输入上最坏情况 O(n²)），原地排序，平均 O(n log n)，递归深度最坏情况 O(n)。

## 2. Word2Vec — `src/word2vec.rs`（约 39 KB，最大的一个）

是对 Mikolov 原始 `word2vec.c` 的忠实 Rust 移植，零外部依赖：

- **Skip-gram with negative sampling**（`train_sg`）— context → center word
- **CBOW with negative sampling**（`train_cbow`）— averaged context → center word
- **Negative sampling table**：unigram distribution 的 **0.75** 次幂，表大小 1e8
- **Subsampling of frequent words**：`ran = (sqrt(f/t) + 1) * (t/f)` — Mikolov 的高频词丢弃技巧
- **Sigmoid lookup table** 近似（预计算的 `exp_table`），而不是每一步都调用 `exp()`
- **Dynamic window reduction**：`b = next_random % window`（每个样本随机缩小 context window）
- **Linear learning-rate decay**：基于总训练词数线性衰减
- **LCG PRNG**：与原版 C 一致：`next_random * 25214903917 + 11`
- **Vocabulary building**：使用 `min_count` 词频剪枝
- **Multi-threaded training**：通过 raw pointers（`UnsafeCell` wrapper）实现——有意复刻原版 pthreads 的“benign data races”设计
- 输出为 text 或 binary 格式（`word\0<float32 × dim>`）

## 3. 其余都是 I/O，不是算法

- `gcloud.rs` — 读取/解析 gcloud config 与 credentials 文件，并调用 `gcloud config/auth list`
- `uno.rs` — 串口 open/listen/status
- `main.rs` — sysinfo 采样（CPU 百分比、内存、磁盘），格式化为 ratatui tables

**总结：** 该项目实际上有两个算法部分——**quicksort（Lomuto）**作为语言基准测试，以及一个相当完整的**word2vec（Skip-gram/CBOW + negative sampling + subsampling）**训练实现。如果你愿意，我可以补充缺失的 Rust quicksort benchmark（例如 `cargo run -- bench`），让三路对比真正跑起来。