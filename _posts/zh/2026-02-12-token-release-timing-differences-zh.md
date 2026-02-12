---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 代币释放机制差异详解
translated: true
type: note
---

Question: 虽然 FDDI 和 IEEE 802.5 都使用 token passing protocol，但它们在帧传输后处理 token regeneration 的方式上有何关键区别？

Answer: 

正确答案是 **C. 在 FDDI 协议中，发送站在完成其帧的传输后可以立即发送一个新的 token，而在 IEEE 802.5 中，只有在帧的前导边缘返回到发送站后才发送新的 token。**

**Detailed explanation:**

FDDI 和 IEEE 802.5 都是 token ring 协议，但它们实现 **token release timing** 的方式不同，这显著影响了性能，特别是在高速环境下。

- **IEEE 802.5 (classic Token Ring)**  
  - 使用 **"delayed token release"** 或 **"token after frame return"** 策略。  
  - 发送站在接收到自己发送的帧返回之前（具体来说，是直到看到发送帧的头部返回到自身），会一直持有 token（不释放新的 token）。  
  - 只有在帧头返回后，该站才会释放一个新的 free token。  
  - 这确保了环路上一次只有一个帧在循环（single-token mode）。  
  - 这种保守的方法降低了帧冲突的风险，但限制了吞吐量，尤其是在大型环路或高速环境下。

- **FDDI (Fiber Distributed Data Interface)**  
  - 使用 **"immediate token release"** 或 **"early token release"**。  
  - 一旦发送站完成其帧的发送（即发送完帧尾的最后一位），它会 **立即** 生成并释放一个新的 free token。  
  - 它 **不** 等待帧在环路上绕行回来。  
  - 这允许环路上同时存在多个帧在循环（multiple-token operation），大大提高了效率和吞吐量——这对于 FDDI 的 100 Mbps 速度和可能的大型环路规模（最长 100 km，每环最多 500 个站点，双环则为 1000 个）尤为重要。  
  - FDDI 可以支持 **synchronous** 和 **asynchronous** 流量，并使用 timed token rotation protocol (TTRT) 来保证带宽和延迟。

**关键区别总结：**

| 特性 | IEEE 802.5 (Token Ring) | FDDI |
| :--- | :--- | :--- |
| Token release timing | 帧头返回发送者后 | 帧传输完成后立即执行 |
| 环路上是否允许同时存在多个帧？ | 否 (single token/frame) | 是 (可能存在多个 tokens/frames) |
| 最适用场景 | 低速 (4/16 Mbps)，较小规模环路 | 高速 (100 Mbps)，较大规模环路 |

**为什么其他选项是错误的：**

- **A**: 错误 — IEEE 802.5 **不** 立即释放 token。  
- **B**: 错误 — FDDI **不** 等待帧返回；只有 802.5 会这样做。  
- **D**: 错误 — FDDI 在仍在发送帧时 **不** 生成新 token；它是在发送完帧后 **立即** 释放。

**记忆技巧：**  
FDDI = Fast（快）→ "Finish frame → Free token immediately"  
802.5 = Slow & safe（慢速且安全）→ "Wait until frame comes back → then free token"

References:  

- None (standard comparison between IEEE 802.5 Token Ring and ANSI X3T9.5 / ISO 9314 FDDI specifications)