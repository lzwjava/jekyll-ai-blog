---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 华为VRP基础配置视图识别
translated: true
type: note
---

Question: Which command view in Huawei VRP is used for basic configuration tasks?

Answer: 

正确答案是 **B) System view**。

在 Huawei 的 Versatile Routing Platform (VRP) 中：

- **User view** (< >)：这是初始登录视图，主要用于 Monitoring、基础的 display 命令（例如 `display version`、`ping`）以及简单的操作任务。此处不允许进行配置更改。
- **System view** ([ ])：这是进行基础和全局配置任务的主要视图，例如创建 VLAN、设置系统参数、配置 AAA、管理用户以及进入其他特定视图（例如 Interface 或 Protocol 视图）。
- **Interface view**：用于配置特定接口的参数（例如 Ethernet 端口上的 IP address）。
- **Protocol view**：用于配置 Routing protocols（例如 OSPF 或 BGP 区域）。

基础配置任务（如 Hostname 更改、VLAN 创建或 Management IP 设置）是在通过 `system-view` 命令进入 System view 后执行的。

选项 D 是错误的。