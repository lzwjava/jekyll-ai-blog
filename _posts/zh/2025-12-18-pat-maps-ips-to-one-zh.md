---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: PAT 将多个 IP 映射到一个 IP
translated: true
type: note
---

问题：哪种类型的 NAT 将多个私有 IP 映射到一个公共 IP？
A) 静态 NAT
B) 动态 NAT
C) PAT (过载)
D) 一对一 NAT

答案：

正确答案是 **C) PAT (过载)**。

### 解释：
网络地址转换 (NAT) 允许私有 IP 地址使用公共 IP 地址与外部网络通信。不同类型如下：

- **静态 NAT**：提供一对一映射，其中单个私有 IP 始终翻译为相同的单个公共 IP。它不允许多个私有 IP 共享一个公共 IP。

- **动态 NAT**：使用公共 IP 池来动态映射私有 IP（也是一对一，但公共 IP 可以改变）。多个私有 IP 需要池中的多个公共 IP；它不会使单个公共 IP 过载。

- **PAT（端口地址转换），也称为 NAT 过载**：通过使用不同的端口号来区分会话，将**多个私有 IP 映射到一个公共 IP**。这是家庭路由器和企业中最常见的 NAT 形式，用于节约公共 IPv4 地址。

- **一对一 NAT**：指具有固定或可变一对一映射的静态或动态 NAT（等同于 A 或 B）；它不会在多个私有 IP 之间共享单个公共 IP。

PAT 专门设计用于多对一转换，因此 **C** 是正确的选择。
