---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ATM 信元固定长度详解
translated: true
type: note
---

问题：What is the fixed length of an ATM cell?

答案：

正确答案是 **C. 53 bytes**。

**详细解释**：
在 ATM (Asynchronous Transfer Mode) 网络中，数据传输的基本单位称为 **cell** (信元)。这个 cell 具有 **fixed length** 为 **exactly 53 bytes**，由以下部分组成：

- **Header**：5 bytes
- **Payload** (information field / 用户信息域)：48 bytes

总计：5 + 48 = **53 bytes**

ATM 设计中故意选择这种固定且相对较小的 cell 大小，以：
- 最小化排队延迟（对实时语音和视频流量尤为重要）
- 实现高效的统计复用
- 简化硬件交换实现

常见错误选项及其原因：
- **A. 8 bytes**：太小——ATM 中未使用
- **B. 16 bytes**：有时与其他协议的 header 大小混淆，但对 ATM cell 不正确
- **D. 64 bytes**：接近 53-byte 大小，但不准确（有些人错误地记为“大约 64 bytes”）

因此唯一正确答案是 **C. 53 bytes**。

参考资料：

- 无（标准 ATM 协议定义，在网络教科书和 ITU-T I.150 / I.361 推荐标准中广泛记载）
