---
audio: false
generated: true
image: false
lang: zh
layout: post
title: IP工作在网络层
translated: true
type: note
---

问题：鉴于互联网协议（IP）是一种无连接、不可靠的数据包传输协议，负责路由和转发数据，它工作在OSI模型的哪一层？

答案：IP工作在OSI模型的**网络层**（第3层）。

原因如下：

- **无连接**——IP在发送数据前不建立专用连接。每个数据包独立路由。
- **不可靠**——IP不保证交付、顺序或纠错。这一责任由更高层（例如传输层的TCP）承担。
- **路由与转发**——这些是网络层的核心任务。路由器利用IP地址为每个数据包在互联网络间确定最佳路径。

**OSI层映射（供参考）：**

| 层 | 名称 | 示例 |
| ------- | ------ | --------- |
| 7 | 应用层 | HTTP, FTP, DNS |
| 6 | 表示层 | TLS, JPEG |
| 5 | 会话层 | NetBIOS |
| 4 | 传输层 | TCP, UDP |
| **3** | **网络层** | **IP, ICMP, OSPF** |
| 2 | 数据链路层 | 以太网, Wi-Fi |
| 1 | 物理层 | 电缆, 无线电 |

因此，空白处应填写：**网络（Network）层**

参考文献：

- [OSI模型 – 维基百科](https://en.wikipedia.org/wiki/OSI_model)
- [互联网协议 – 维基百科](https://en.wikipedia.org/wiki/Internet_Protocol)
