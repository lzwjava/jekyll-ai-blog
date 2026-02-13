---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 异步与同步效率比较
translated: true
type: note
---

Question: 对于传输速率相同的数据链路，当使用 Asynchronous protocol 或 Synchronous protocol 控制海量数据传输时，传输效率之比（Asynchronous protocol / Synchronous protocol）是多少？

A. 接近 80%  
B. 接近 1  
C. 接近 50%  
D. 等于 1  

Answer: 

**A**

**Explanation:**

在串行数据通信中：

- **Asynchronous protocol**（通常指 UART 风格的异步串行通信）：  
  每个字符/字节都独立成帧，包含 **1 个起始位 + 8 个数据位 + 1 个停止位**（最常见的 8N1 格式）。  
  → 每个字节的总位数 = 10 bits  
  → 效率 = 8 / 10 = **80%**

- **Synchronous protocol**（例如 HDLC、SDLC、同步串行协议或现代高速同步链路）：  
  通常以块/帧的形式传输数据，仅包含少量的帧同步、标志、报头、CRC/checksum 等开销。  
  当传输**海量数据**时，分摊到每个字节的开销变得非常小（通常小于 1–5%）。  
  → 效率通常**非常接近 100%**（在实际的大块传输中通常大于 95%）

因此，对于**大批量/海量数据传输**，效率比为：

Asynchronous 效率 / Synchronous 效率 ≈ 80% / ~100% ≈ **80%**

所以正确答案是 **A. 接近 80%**。

**为什么不选择其他选项？**

- **B. 接近 1** → 只有当两种协议的开销相似时才成立，但在海量数据情况下并非如此。
- **C. 接近 50%** → 这过于悲观；即使是 Asynchronous UART 也有 80% 的效率，而不是 50%。
- **D. 等于 1** → 由于 Asynchronous 模式中存在固定的起始位/停止位开销，这显然是错误的。

**记忆技巧**（如解释中所述）：  
“异步低效八成满，同步高效更划算”  
→ Asynchronous 效率约为 80%，Synchronous 效率更高，更具性价比。

References:  

- 无（标准数据通信理论）