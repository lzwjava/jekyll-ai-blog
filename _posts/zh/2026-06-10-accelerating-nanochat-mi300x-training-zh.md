---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 加速NanoChat MI300X训练
translated: true
type: note
---

问题：如何加速这个 NanoChat MI300X 训练运行？

回答：

根据您发布的命令，您已经使用了一些最大的优化手段：

* 启用了 FP8（`--fp8`）
* 使用 FlashAttention 2（从您之前的测试来看）
* 大批量大小（`524288`）
* MI300X GPU
* 序列长度 2048

剩下的性能提升通常来自以下四个领域之一：

## 1. 确认 FlashAttention 2 是否实际被使用

这是最大的潜在收益点。

检查训练日志：

```bash
grep -i "flash" run_mi300x_d24_fa2_fp8.log
```

或

```bash
grep -i "attention" run_mi300x_d24_fa2_fp8.log
```

如果 NanoChat 静默回退到 SDPA，您可能会损失 20–40% 的性能。

您之前的基准测试显示：

| 配置         | 每步时间 |
| ------------ | -------- |
| bf16 + SDPA  | 7.7s     |
| FP8 + SDPA   | 6.4s     |
| FP8 + FA2    | ~4–5s    |

因此 FA2 通常是最大的单一加速来源。

---

## 2. 增加设备批量大小

您当前设置为：

```bash
--device-batch-size=32
```

在 MI300X（192 GB HBM）上，这通常偏保守。

尝试：

```bash
--device-batch-size=48
```

如果稳定：

```bash
--device-batch-size=64
```

监控内存：

```bash
watch -n 1 rocm-smi --showmemuse
```

如果利用率低于 160 GB，说明您还有性能潜力未发挥。

---

## 3. 增加序列长度（有时反而更快）

反直觉的是，更长的序列可以提高 MFU。

当前：

```bash
--max-seq-len=2048
```

尝试：

```bash
--max-seq-len=4096
```

如果 NanoChat 支持的话。

为什么？

更长的序列增加了算术强度，使矩阵单元更忙碌。

典型 MI300X 利用率：

| 序列长度 | MFU    |
| -------- | ------ |
| 2048     | 25–35% |
| 4096     | 35–45% |
| 8192     | 45–55% |

---

## 4. 增加模型大小

您正在训练一个 24 层约 760M 的模型：

```bash
--depth=24
```

小模型常常受限于 CPU 或数据加载器。

在 MI300X 上，760M 相对较小。

常见观察：

| 模型   | MFU    |
| ------ | ------ |
| 760M   | 25–35% |
| 3B     | 40–55% |
| 7B     | 55–70% |

GPU 喜欢更大的 GEMM。

---

## 5. 降低评估频率

当前：

```bash
--eval-every=1000
--eval-tokens=1048576
```

每次评估都会暂停训练。

对于纯吞吐量测试：

```bash
--eval-every=5000
```

或

```bash
--eval-every=-1
```

临时使用。

另外：

```bash
--sample-every=-1
```

```bash
--core-metric-every=-1
```

在基准测试期间。

---

## 6. 检查 GPU 利用率

运行：

```bash
watch -n 1 rocm-smi
```

查看：

```text
GPU Utilization
HBM Utilization
Power Draw
```

健康的训练应显示：

```text
GPU Util: 90-100%
Power: 650-750W
```

如果 GPU 利用率波动：

```text
20%
100%
30%
100%
```

说明您受到了数据加载器或 CPU 瓶颈。

---

## 7. 使用更多数据加载器工作线程

检查 NanoChat 是否暴露了：

```bash
--num-workers
```

或类似参数。

如果是：

```bash
--num-workers=16
```

或

```bash
--num-workers=32
```

可以显著提高吞吐量。

---

## 8. 检查实际 tokens/秒

最重要的指标是：

```text
tokens/sec
MFU
```

如果您看到：

```text
300K tok/s
```

还有提升空间。

如果您在 MI300X 上对于 760M 模型看到：

```text
500K-700K tok/s
```

那么您已经处于非常优秀的水平。

---

## 9. 对前 100 步进行性能分析

运行：

```bash
python -m scripts.base_train \
  ... \
  --num-iterations=100
```

然后检查：

```bash
grep -i "tok/s" run.log
grep -i "mfu" run.log
```

瓶颈会变得明显：

* 低 MFU → GPU 未饱和
* 高 MFU 但低 tok/s → 模型太小
* 利用率波动 → 数据加载器瓶颈
* 内存使用高 → 批量大小限制

## 建议的首批更改

我会按以下顺序尝试：

```bash
--device-batch-size=64
```

然后

```bash
--eval-every=5000
--sample-every=-1
--core-metric-every=-1
```

然后确认 FlashAttention 2 已激活。

这三项更改通常能在不修改 NanoChat 源代码的情况下实现最大的实际加速。
