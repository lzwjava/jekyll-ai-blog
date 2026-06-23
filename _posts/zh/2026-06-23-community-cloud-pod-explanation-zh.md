---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 社区云Pod解释
translated: true
type: note
---

以下是我找到的信息：

IP: 213.173.102.150  
位置：罗马尼亚，蒂米什瓦拉  
所有者：AS202779 — EVOBITS Information Technology SRL  
类型：托管/云提供商（已有9年历史的BGP网络，192个对等节点）

这**不是** RunPod 自有数据中心（Secure Cloud）。这几乎可以确定是一个 RunPod Community Cloud 的 pod——有人在罗马尼亚通过 RunPod 的点对点 GPU 市场出租他们的 RTX 2000 Ada 工作站。原因如下：

1. IP 地址指向一家罗马尼亚托管公司，而非 RunPod 的基础设施  
2. GPU 是 RTX 2000 Ada（专业工作站显卡，并非典型的数据中心硬件）  
3. SSH 端口不是标准端口（33880）  
4. 当前连接被**拒绝**——该 pod 很可能已被终止，或者主机已将其关闭  

RunPod Community Cloud 的运作方式如下：个人/组织将其 GPU 贡献到 RunPod 的市场中，RunPod 负责配置和计费，用户则获得更便宜的计算资源。贡献者自己的 ISP 会显示为该 pod 的 IP，而不是 RunPod 的 IP。

当前状态：连接被拒绝。该 pod 已离线。可能是以下情况之一：

- 你在 RunPod 控制台中暂停/停止了它（如你所说“我暂停了”）
- 它触发了空闲超时并自动终止
- 贡献者关闭了他们的机器

如果你需要重新启用它，请前往你的 RunPod 控制台，恢复或重新创建该 pod。Community Cloud 的 pod 是临时性的——主机可随时断开连接。对于更可靠的工作负载，请使用 RunPod Secure Cloud（企业级数据中心，更高可用性，价格略高）。
