---
audio: false
generated: true
image: false
lang: zh
layout: post
title: TCP传输层作业
translated: true
type: note
---

问题：TCP协议属于哪一层——网络层还是传输层？

答案：TCP（传输控制协议）属于OSI模型中的**传输层**（第4层）。

以下是一个快速区分表，帮助澄清两者的区别：

| 层 | OSI模型 | 协议 |
| ------- | ----------- | ----------- |
| 第3层 | 网络层 | IP、ICMP、ARP |
| 第4层 | 传输层 | **TCP**、UDP |

**为什么是传输层？**

- TCP负责不同主机上进程之间的**端到端通信**，而非网络间的路由。
- 它提供**可靠性**（确认、重传）、**流量控制**、**拥塞控制**以及**有序传输**——这些都是传输层的职责。
- **网络层**（第3层）处理逻辑寻址和数据包路由（这是IP的工作）。TCP运行在IP**之上**。

一个常用的助记符来描述两者协同工作：**IP**将数据包送到正确的*机器*，**TCP**在该机器上将数据可靠地送到正确的*进程*。

参考资料：

- [TCP - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Glossary/TCP)
- [OSI模型 - Cloudflare](https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/)
