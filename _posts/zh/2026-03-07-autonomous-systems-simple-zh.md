---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 自主系统简单解释
translated: true
type: note
---

**问题：** 网络中的 Autonomous System (AS) 是什么？

**答案：**

## 定义

Autonomous System (AS) 是一个由一个或多个网络运营商代表单一行政实体或域控制的相互连接的 Internet Protocol (IP) 路由前缀集合，该集合向 Internet 呈现一个共同且明确定义的路由策略。

简单来说：Internet 是一个网络的网络，而 autonomous systems 就是构成 Internet 的大网络。每个连接到 Internet 的计算机或设备都连接到一个 AS。

---

## 工作原理 — 类比

将 AS 想象成一个城镇的邮局。邮件从一个邮局传递到另一个邮局，直到到达正确的城镇，然后该城镇的邮局会在镇内递送邮件。同样，数据包通过从一个 AS 跳到另一个 AS 穿越 Internet，直到到达包含目标 IP 地址的 AS。

---

## Autonomous System Number (ASN)

每个 AS 都被分配一个唯一的标识符，称为 Autonomous System Number (ASN)。网络运营商需要 ASN 来控制其网络内的路由，并与其他 ISP 交换路由信息。

ASN 有两种格式：
- **2-byte ASN** 是一个 16 位数字，提供 65,536 个 ASN。**4-byte ASN** 是一个 32 位数字，提供超过 40 亿个 ASN。
- 截至 2025 年，全球大约有 **120,000 allocated ASNs**。

---

## Autonomous Systems 的类型

Autonomous Systems 有三种不同的类型：

- **Multi-homed AS**：连接到两个或更多 AS，即使一条连接失败，也能保持 Internet 连接。
- **Stub AS**：仅连接到一个其他 AS，尽管它可能有自己的私有连接，这些连接对 Internet 的其余部分不可见。
- **Transit AS**：充当两个或更多其他 AS 之间的链接，允许数据即使来自无关网络也通过它传递。

---

## BGP 的作用

AS 内部的网络使用内部网关协议 (IGPs) 通信路由信息。相比之下，autonomous systems 之间的通信依赖单一外部网关协议 — **Border Gateway Protocol (BGP)** — 这使得在 autonomous systems 之间共享路由信息并高效路由数据包成为可能。

---

## 内部视图与外部视图

将 AS 与其他网络组区别开来的特点是，它必须向外部 autonomous systems 呈现一个单一、连贯的路由计划，无论 AS 内部的通信如何进行。

---

## 真实世界示例

ISP 可能是运营 autonomous systems 的最常见实体示例。每个 ISP 通常都有自己的 ASN。另一个示例包括云服务提供商，如 Amazon Web Services (AWS)、Microsoft Azure 和 Google Cloud Platform (GCP)。

---

## 为什么 AS 重要

AS 促进全球路由的稳定性、网络故障隔离以及大型网络的简化管理，最终有助于提升网络性能并提供一致的用户体验。

---

**参考资料：**

- [Cloudflare — What is an Autonomous System?](https://www.cloudflare.com/learning/network-layer/what-is-an-autonomous-system/)
- [Wikipedia — Autonomous System (Internet)](https://en.wikipedia.org/wiki/Autonomous_system_(Internet))
- [TechTarget — What are Autonomous Systems?](https://www.techtarget.com/searchnetworking/definition/autonomous-system)
- [ARIN — Autonomous System Numbers](https://www.arin.net/resources/guide/asn/)
- [ControlD — What is an Autonomous System?](https://controld.com/blog/what-is-an-autonomous-system/)
