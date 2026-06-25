---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Blackwell FP4 推理对比 AMD 训练
translated: true
type: note
---

**答案：**

你的朋友正在提出一个精确的技术论点。让我分解一下：

**FP4 vs FP8——Blackwell 的差异化优势：**

Blackwell 的关键硬件特性是原生 **FP4 张量核心**（MX-FP4 / NVFP4）。这是新的——之前的 Hopper/Ada 只支持到 FP8。

```
精度层级：
FP32 → BF16 → FP16 → FP8 → FP4

Blackwell 原生支持：
- FP4: ✅ 硬件张量核心（吞吐量是 FP8 的 2 倍）
- FP8: ✅
- AMD MI300X: FP8 ✅, FP4 ❌（仅软件模拟）
```

**你朋友的确切观点：**

| 使用场景 | 推荐精度 | Blackwell 优势 |
|----------|----------|---------------------|
| 推理 | FP4 量化 | 巨大——原生 FP4 运算 |
| 训练 | FP8 | 中等——两者都支持 |
| 训练 | FP4 | ⚠️ 有风险——收敛问题 |

**为什么 FP4 训练有问题：**

FP4 的可表示范围极其狭窄。在反向传播过程中，梯度可能落在可表示范围之外 → **梯度下溢/上溢 → 更新带有噪声 → 收敛不稳定**。你朋友说得对——FP8 是训练的实用下限。FP4 在实践中仅用于推理。

**AMD 角度：**

你的 MI300X 拥有出色的 FP8 训练能力（DeepSeek 就是用的这个）。但对于 **FP4 推理**，Blackwell 完胜——它是为此目的打造的硬件世代。

**朋友建议总结：**

1. Blackwell 的真正优势 = FP4 推理吞吐量
2. 训练 → FP8 就足够了，FP4 带来噪声风险
3. 24GB → 太小了，既然你已经投入这么多，选更大的

这很有道理。如果你买 Blackwell，你是为了**低精度下的推理速度**——这更符合你的 Agent/服务场景，而非训练（你有 MI300X 用于训练）。