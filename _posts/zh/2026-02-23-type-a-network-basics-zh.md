---
audio: false
generated: true
image: false
lang: zh
layout: post
title: A型网络服务基础
translated: true
type: note
---

问题：根据用户要求和错误性质，网络服务分为三种类型。以下哪项描述了 Type A network service？

答案：

**Type A Network Service** 以具有 **acceptable residual error rates** 和 **acceptable failure notification rates** 为特征。

在网络服务分类的上下文中（通常与 OSI model 和 transport layer services 相关）：
- **Type A**：底层网络提供具有低错误率的可靠服务。因此，transport layer 不需要实现广泛的错误恢复机制。residual error rate 和 failure notification rate 都被认为对用户需求是可接受的。
- **Type B**：网络具有可接受的 residual error rate，但 failure notification rate 不可接受（例如，故障未正确通知）。
- **Type C**：网络具有不可接受的 residual error rate，需要 transport layer 处理大量的错误检测和恢复。

由于 Type A 代表底层服务最高质量，其中两个指标均满足用户要求，因此正确描述是它同时具有可接受的 residual error rates 和 failure notification rates。

**正确选项：** C

参考文献：

- [OSI Transport Layer Services Overview](https://www.geeksforgeeks.org/types-of-services-in-transport-layer/)
