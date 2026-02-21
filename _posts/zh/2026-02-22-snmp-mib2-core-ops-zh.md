---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SNMP MIB-2 核心操作
translated: true
type: note
---

问题：SNMP 实体可以对 MIB-2 中的对象执行哪些操作？

答案：

正确答案是 **D: Get、Set、Trap**。

### 解释：
在简单网络管理协议（SNMP）中，SNMP 实体（通常是管理器或代理）与管理信息库版本 2（MIB-2）中定义的托管对象进行交互。SNMP 定义的与这些对象交互的基本操作包括：

1. **Get**：由 SNMP 管理器使用，从代理检索特定对象实例的值。
2. **Set**：由 SNMP 管理器使用，修改或设置代理上特定对象实例的值。
3. **Trap**：由 SNMP 代理异步发送给管理器的通知，用于报告重要事件或错误（例如链路中断、认证失败）。虽然严格来说，Trap 是由代理发起的 PDU（协议数据单元）类型，而不是像 Get/Set 那样“作用于”对象的操作，但在涉及 MIB 对象和通信流的 SNMP 操作背景下，它被视为主要操作之一。

**其他选项为何错误：**
* **GetNext**：这是 SNMP 的有效操作，用于检索 MIB 树中的下一个对象实例（对遍历表格至关重要）。但在标准考试题目中，通常将 **Get、Set 和 Trap** 作为核心功能集（读取、写入、通知）引用。
  * 选项 A 包含 Trap 和 GetNext，但缺少 **Get**（最基本的读取操作）。
  * 选项 C 包含 Trap 和 GetNext，但缺少 **Set**。
  * 选项 B 包含 Get、Set 和 GetNext，但缺少 **Trap**。

*注：严格来说，SNMPv1 定义了五种 PDU：GetRequest、GetNextRequest、SetRequest、GetResponse 和 Trap。SNMPv2c 增加了 GetBulkRequest 和 InformRequest。但根据题目提供的详细解释（"SNMP 实体可以对 MIB-2 中的对象执行的操作有：Get, Set, Trap"），该问题所属的课程或考试机构将主要操作归类为 Get、Set 和 Trap，可能将 GetNext 视为 Get 的变体，或专注于检索、修改和通知三大功能类别。*

根据题目来源材料明确说明的操作集为 **Get、Set、Trap**，选项 D 是正确答案。

参考：