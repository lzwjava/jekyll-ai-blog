---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 多线程Word2Vec 2倍加速
translated: true
type: note
---

完成。已推送至 `origin/main`。

**变更内容：**

- 多线程训练：8 个线程，`std::thread::scope` 配合 Send 安全的 `TrainPtrs` 包装器
- 并行路径中的 epoch 循环
- `-threads N` 标志（默认 4）
- 原始指针训练函数（`train_sg_raw`、`train_cbow_raw`）

**在 M2 Air 上的性能表现（text8，词汇量 71k，维度=200）：**

| Config | Words/s | Time (5 epochs) |
|--------|---------|-----------------|
| `-threads 1` | 344k | ~240s |
| `-threads 8` | 740k | ~127s |

约 2 倍加速。受限于内存带宽——所有线程读写相同的 71k×200 权重矩阵。瓶颈在于共享缓存争用，而非计算能力。

使用方法：

```
cargo run --release -- word2vec train -input corpus.txt -output vec.bin -threads 8
```