---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 大语言模型中的多令牌预测
translated: true
type: note
---

问题：在LLM中，**MTP**是什么意思？

回答：在现代LLM推理中，**MTP通常指*多Token预测（Multi-Token Prediction）***。

与仅预测下一个token的常规自回归模型不同：

```text
x1 x2 x3 x4 → 预测 x5
```

MTP训练模型**同时预测多个未来token**：

```text
x1 x2 x3 x4 → 预测 x5, x6, x7, ...
```

### 为什么重要

其主要用途是**推测式解码 / 加速推理**。

常规解码器的工作方式为：

```text
前向传播()
  → token 101

前向传播(token 101)
  → token 102

前向传播(token 102)
  → token 103
```

每个token都需要一次代价高昂的前向传播。

采用MTP后：

```text
                 ┌→ token 101
前向传播() ───────┼→ token 102
                 ├→ token 103
                 └→ token 104
```

额外的预测头可以提出多个token，然后由主模型进行验证。

因此，潜在效果为：

```text
常规方式：
1次前向传播 → 1个被接受的token

MTP：
1次主前向传播 → 多个被提出的token
                ↓
          验证这些token
                ↓
      接受2–4个token
```

这可以显著提升**每秒token数（tokens/sec）**，尤其适用于连续token相对可预测的任务，例如代码生成。

### 示例：DeepSeek

这一点与**DeepSeek的MTP架构**密切相关。DeepSeek将MTP描述为在训练过程中预测多个未来token，同时这些额外的预测模块也可在推理阶段用于推测式解码。

概念上可以理解为：

```text
                 隐藏状态
                      │
             ┌────────┴────────┐
             ↓                 ↓
        常规预测头         MTP模块1
             ↓                 ↓
           t+1               t+2
                               │
                         MTP模块2
                               ↓
                              t+3
```

需要强调的重要区别是：

**MTP ≠ 简单地独立生成多个token。**

这些预测经过训练，对应于**同一序列中的未来位置**，并且该架构可以利用它们来提高解码效率。

如果你正在研究**DeepSeek-V3/R1或特定的推理引擎（如vLLM）**，MTP在KV缓存和推测式解码方面还有一些额外的实现细节。我可以进一步讲解实际的前向传播过程和tensor形状。