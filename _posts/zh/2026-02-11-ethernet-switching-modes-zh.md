---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 以太网交换模式详解
translated: true
type: note
---

问题：Ethernet switches 的主要交换模式包括 Cut-through switching 以及以下哪一种？

A. 间接交换  
B. 检测控制交换  
C. 分段交换  
D. Store-and-forward switching  

答案：  

**正确答案是 D. Store-and-forward switching**

**解释：**

Ethernet switches 主要使用以下数据交换（转发）方式：

1. **Cut-through switching** (直接交换 / 直通交换)  
   - Switch 在读取到目标 MAC 地址后（通常在接收到前 6–14 字节后）立即开始转发帧。  
   - 转发速度最快，延迟最低。  
   - 缺点：可能会转发错误帧（没有进行完整的 CRC 校验）。

2. **Store-and-forward switching** (存储转发交换)  
   - Switch 接收**整个数据帧**，执行完整的 CRC 校验，丢弃错帧，然后转发有效帧。  
   - 可靠性最高，可以过滤错误帧。  
   - 缺点：延迟较高（必须等待整个帧接收完毕）。

3. **Fragment-free switching** (改进直接交换 / 无碎片交换)  
   - 一种折中方法：Switch 等待接收前 **64 字节**（以避免冲突碎片），然后开始转发。  
   - 平衡了速度和错误过滤（过滤了大多数冲突碎片，但不能过滤所有错误）。

**题目中的正确分类：**

Ethernet switches 最常见且最主要的两种交换模式是：

- **Direct switching** (Cut-through)  
- **Store-and-forward switching**

因此，答案应为 **D. Store-and-forward switching**。

**为什么选项 C 是错误的：**

- “分段交换” (Fragment switching) **不是** Ethernet switches 的标准主流交换模式。  
- “分段交换”这一术语有时会被误用或出现在翻译欠佳的题目中，但它并不对应任何标准的 Ethernet switch 转发方法。最相关的概念是 “Fragment-free”，但它通常被称为“改进直接交换”或“无碎片交换”，而不是“分段交换”。

**标准 Ethernet switch 交换模式总结（多数教材和认证考试）：**

- 直接交换（Cut-through）  
- 存储转发交换（Store-and-forward）  
- 改进直接交换 / 无碎片交换（Fragment-free）

题目询问与“直接交换”并列的模式，即 **存储转发交换** → **D**。

参考资料：  

- 无（基于 IEEE 802.3 标准、Cisco CCNA 资料以及通用网络工程教材的 Ethernet 交换知识）