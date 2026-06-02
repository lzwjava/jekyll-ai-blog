---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 计算中瞬态的含义
translated: true
type: note
---

**问题：** “ephemeral”是什么意思？

**回答：**

暂时的 / 短暂的 / 只存在片刻，随后消失。

在计算机科学语境中会经常见到它：

- **Ephemeral storage**（临时存储）—— 容器或虚拟机停止时随之消失的磁盘（例如 Docker 的可写层、EC2 实例存储）
- **Ephemeral port**（临时端口）—— 操作系统为出站 TCP 连接分配的临时端口（范围 49152–65535）
- **Ephemeral environment**（临时环境）—— 为每个 PR 临时部署、合并后销毁的测试环境
- **Ephemeral key**（临时密钥）—— 使用一次即丢弃的加密密钥（Diffie-Hellman 临时密钥 = TLS 中的 DHE/ECDHE）

反义词：**persistent**（持久化）/ **durable**（耐用）
