---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: OSI模型各层数据单元术语
translated: true
type: note
---

问题：在 OSI Reference Model (OSI/RM) 中，各层实体之间传送的比特组称为？

答案：

正确答案是 **A. 数据单元** (Data Unit)。

**详细英文解释：**

在 OSI Reference Model 中，层与层之间的通信使用特定的术语：

- **Data Unit** (数据单元)：传递于**相邻层**实体之间（即从 N 层到 N-1 层，或反之）的比特块（数据 + 可能包含控制信息）的通用术语。
  → 这是针对该问题最广泛且正确的术语。

- **Protocol Data Unit (PDU)** (协议数据单元)：根据该层的规则（Protocol），在不同系统的**同层**对等实体之间进行**水平**交换时的数据单元特定名称。

- **Service Data Unit (SDU)** (服务数据单元)：N 层实体从上层（N+1 层）接收到的纯用户数据，在添加其自身的 Header/Trailer 之前。

OSI 术语中的关键区别：

| 方向 / 关系 | 使用术语 | 含义 |
|-------------------------------|-------------------------------|----------------------------------------------|
| **相邻层**之间 (N ↔ N-1) | **Data Unit** (数据单元) | 在堆栈上下传递的比特组的通用术语 |
| **对等实体**之间 (同层，不同系统) | **Protocol Data Unit (PDU)** | 根据层协议交换的数据单元 |
| 从上层到当前层 | **Service Data Unit (SDU)** | 通过 Service Interface 交付的用户数据 |

题目特别询问关于**各层的实体之间**（between entities of each layer）传递的比特组，这指的是一个系统内部相邻层之间的**垂直**通信——因此正确的通用术语是 **数据单元 (Data Unit)**。

为什么 **C. 服务原语 (Service Primitive)** 是错误的：
Service Primitives（Request, Indication, Response, Confirm）是服务边界（Service User 与 Service Provider 之间）的**抽象交互**，而不是实际传输的比特组。

为什么 **D. 服务访问点 (Service Access Point - SAP)** 是错误的：
SAP 是层与层之间的**逻辑接口点**（类似地址的标识符），而不是数据本身。

为什么 **B. 接口 (Interface)** 是错误的：
Interface 是边界或规则集，而不是被传递的数据块。

**总结 – 正确映射：**

- 在**层与层**（相邻）之间传递的比特组 → **数据单元**
- 在**对等协议实体**之间传递的比特组 → **PDU**
- 在 **Service User** 与 **Service Provider** 之间传递的比特组 → **SDU**（从上到下）或封装后的 PDU（从下到上）

因此本题的正确答案是 **A. 数据单元**。

参考资料：

- 无（标准 OSI Reference Model 术语）
