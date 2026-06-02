---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 用于路由的 ATM VPI/VCI 详解
translated: true
type: note
---

问题：在 ATM cell header format 中，VPI/VCI 字段用于

A. Error control
B. Flow control
C. Routing
D. Cell selection

您的答案：D
正确答案：C

答案：

正确答案是 **C. Routing** (路由选择)。

### 详细解释：

在 ATM (Asynchronous Transfer Mode) 信元头部（5 字节头部）中，主要字段及其主要功能是：

- **GFC** (Generic Flow Control) → 用于 **flow control**（主要在 UNI 接口，4 位，仅本地有效）
- **VPI** (Virtual Path Identifier) + **VCI** (Virtual Channel Identifier) → 用于 **routing** / 路径选择
  这两个字段共同标识虚拟连接（VPC 或 VCC），是 ATM 网络中转发信元的最重要字段（类似于 IP 网络中的 IP destination address）。
- **PT** (Payload Type) → 表示 payload 类型（user data / management data）
- **CLP** (Cell Loss Priority) → 用于 **congestion control** / 信元丢弃优先级
- **HEC** (Header Error Control) → 用于 **error detection** 和头部中的单比特 **error correction**

因此，正确的映射是：

- Error control → **HEC**
- Flow control → **GFC**
- Routing / 路径选择 → **VPI/VCI**
- Congestion / 信元丢弃优先级 → **CLP**

因此，VPI/VCI 字段显然用于 **routing selection** (路由选择)，而不是“cell selection”（信元选择）。

“Cell selection”不是 ATM 头部中任何字段的标准功能。

**您的错误**：您选择了 D（信元选择），但正确选择是 C（路由选择）。

参考文献：

- ITU-T Recommendation I.361 - B-ISDN ATM Layer Specification
- ATM Forum specifications (historical reference)
