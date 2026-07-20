---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PCIe 3.0 转接线够用吗？
translated: true
type: note
---

**问题：这个 PCIe 3.0 x16 riser cable 在 MSI MAG B760M Mortar + RTX GPUs 上能用吗？**

**回答：可以工作，但如果价格差距不大，我会选择 PCIe 5.0 的 Fenvi riser。**

这个 NZXT 原装 PCIe 3.0 x16 riser cable 实际上质量不错。重要的一点是：

> PCIe 3.0 x16 bandwidth 对于许多 AI inference workloads 来说足够了，但对于 newer GPUs 来说并不理想。

---

## 带宽对比

```
PCIe 3.0 x16  ≈ 15.8 GB/s
PCIe 4.0 x16  ≈ 31.5 GB/s
PCIe 5.0 x16  ≈ 63 GB/s
```

你的 GPU：

```
RTX 4070:
PCIe 4.0 x16

RTX 3090:
PCIe 4.0 x16
```

使用这个 riser：

```
RTX 4070
    |
    |
PCIe 3.0 x16 riser
    |
    |
B760M PCIe slot

结果：
PCIe 3.0 x16
```

GPU 将会降级到 PCIe 3.0。

---

## 性能影响

### 游戏

有时明显：

```
RTX 4090:
PCIe 3.0 x16 损失很少

RTX 4060:
PCIe 3.0 x8 可能损失更多
```

对于 RTX 4070/3090：

影响很小。

---

### AI 推理

通常没问题：

例子：

```
Qwen / Llama inference

GPU VRAM:
24GB RTX3090

模型权重：
保留在 VRAM 中

PCIe traffic:
low
```

所以：

```
RTX3090 + PCIe3.0 x16
= OK
```

对于 agents / local LLM：

✅ 很好

---

### 多 GPU 模型拆分

例子：

```
RTX3090 24GB
+
RTX4070 12GB

Total VRAM:
36GB
```

这个 riser 并不是最大的问题。

瓶颈在于：

```
B760M:

GPU1:
PCIe4 x16

GPU2:
PCIe4 x4
```

即使 riser 是 PCIe5，第二个插槽仍然是 x4。

---

## 重要提示：PCIe 3.0 x16 与物理 x16

许多便宜的 riser 声称是：

```
PCIe 3.0 x16
```

但内部只连接了：

```
x4
```

对于 AI，请检查：

* 16 lanes connected
* shielded cable
* short length

这个基于 NZXT 的 riser 可能是正品，因为 NZXT risers 通常质量很高。

---

## 针对你的 B760M AI 工作站的排名

### 最佳

```
PCIe 5.0 x16 20cm Fenvi
★★★★★
```

原因：

* future proof
* RTX 50 series ready
* better signal margin

---

### 这款 NZXT PCIe 3.0 x16

```
★★★★☆
```

适用条件：

* 价格便宜很多
* 仅使用 RTX3090/4070
* inference workload

---

### 便宜的不知名 PCIe riser

```
★★☆☆☆
```

避免使用。

---

针对你的用例（local LLM、agents、vLLM、实验 2 GPUs）：

如果只贵 20-50 元，我会购买 **PCIe 5.0 Fenvi**。

Riser cable 不是你应该省钱的地方；一个差的 riser 会导致随机的 CUDA crashes、GPU disappearing 以及 BIOS PCIe negotiation problems。
