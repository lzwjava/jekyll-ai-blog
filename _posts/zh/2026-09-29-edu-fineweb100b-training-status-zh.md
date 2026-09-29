---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Edu Fineweb100B 训练状态
translated: true
type: note
---

以下是发现的内容——哪些配置/模型使用了 `edu_fineweb100B` 数据集及其实际状态：

## 指向 `edu_fineweb100B`（FineWeb-Edu 分片）的配置

| 配置 | 模型 | 参数量 | 目标训练量 | 实际训练量 | 状态 |
|---|---|---|---|---|---|
| `train_fineweb_gpt3.py` | GPT-2 124M (L12/H12/C768) | 124M | 19,073 迭代 ≈ 10B token | 15,180 迭代 ≈ **7.9B token** | ⚠️ 提前停止（验证损失 3.026） |
| `train_gpt2_200m.py` | GPT-2 ~219M (L18/H16/C896) | 219M | 8,000 迭代 ≈ 4.2B token | 2,500 迭代 ≈ **1.3B token** | ⚠️ 提前停止（验证损失 3.459） |
| `train_gpt2_200m_smoke.py` | 同上 219M | 219M | 25 迭代 | 烟雾测试 | ✅ 完成 |
| `train_fineweb_760m.py` | GPT-2 760M (L24/H24/C1536) | 760M | 445,000 迭代 ≈ 14.6B token | **从未运行** | ❌ 缺少 `out-fineweb-760m/` 目录 |

## 主要发现

1. **该数据集上完成度最佳的模型 = `out-fineweb-gpt3`**（124M，验证损失 3.026）。日志显示其在 RTX 4070（12 GB）上运行，约 11 秒/迭代，MFU 约 12.8%，在第 15,180 步（共 19,073 步）时中断（当时仍在改进——末尾损失为 2.75–3.1）。

2. **`train_fineweb_760m.py` 存在一个 bug**——其 `shard_dir` 指向 `/root/nanoGPT/data/fineweb/edu_fineweb100B`，该路径在本机上不存在。若要运行，需改为 `/mnt/data/nanoGPT/data/fineweb/edu_fineweb100B`。这个 760M 模型*计划过但从未启动*。

3. **另外两个 "fineweb" 配置并未使用该数据集：**
   - `train_fineweb.py`（→ `out-fineweb`）读取的是旧的 `data/fineweb/train.bin` 内存映射文件，而非分片。
   - `train_fineweb1_5b.py`（GPT-2 XL 1.5B）同样没有 `shard_dir`，因此会读取 `train.bin`——并且也从未运行过。

## 总结

`edu_fineweb100B`（140.7B token）数据集已被用于：
- **GPT-2 124M** → 约 7.9B token（不完整，距目标少约 8.6B）
- **GPT-2 219M** → 约 1.3B token（不完整，距目标少约 3B）

同时还**计划用于 GPT-2 760M**（14.6B token）但从未启动，且存在路径错误需要修复。

是否需要我恢复某个未完成的运行，或者修复并启动 760M 配置？