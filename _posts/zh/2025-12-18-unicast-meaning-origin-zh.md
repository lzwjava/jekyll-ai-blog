---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 单播的含义与起源解释
translated: true
type: note
---

问题：网络中的“unicast”是不是指“unique cast”？这个词的最初含义是什么？

答案：

是的，网络中的“unicast”实际上是指“unique cast”（独一无二的发送）或发送给单个独一无二的接收者。它指的是**一对一通信**，即数据包从一个发送方发送到且只发送到一个由唯一的网络地址（如IP地址）标识的特定接收方。

### 字面和最初含义
“unicast”是一个复合词，由以下部分组成：
- **Uni-**: 拉丁语前缀，意为“一”或“单一”（如“unique”、“universe”或“uniform”）。
- **Cast**: 源自“broadcast”，而“broadcast”则源于广播电视，意为“散布”或“广泛地投掷”（源自古英语中与播种相关的词根）。

在计算机网络中，“-cast”后缀是类比广播术语而采用的：
- **Broadcast**: 发送给所有接收者（一对所有）。
- **Multicast**: 发送给多个特定接收者（一对多）。
- **Unicast**: 发送给一个特定接收者（一对一）。

“unicast”一词是在20世纪70年代至80年代，在分组交换网络背景下创造的，特别是随着ARPANET和早期IP网络等协议的发展而出现。它与已有的“broadcast”和“multicast”（在大约同时间引入IP规范）形成对比。“unicast”在网络出现之前没有使用过；它是一个技术新词，用于描述点对点传输。

Unicast是当今最常见的网络流量形式，用于日常活动，例如浏览网站、发送电子邮件或向单个用户流媒体视频。

参考文献：  

- [Unicast - Wikipedia](https://en.wikipedia.org/wiki/Unicast)
- [Unicast, Broadcast, and Multicast - University of Aberdeen](https://erg.abdn.ac.uk/users/gorry/course/intro-pages/uni-b-mcast.html)
- [Difference between Unicast, Broadcast and Multicast - GeeksforGeeks](https://www.geeksforgeeks.org/difference-between-unicast-broadcast-and-multicast-in-computer-network/)