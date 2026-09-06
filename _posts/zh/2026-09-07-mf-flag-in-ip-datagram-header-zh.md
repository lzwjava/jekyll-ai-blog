---
audio: false
generated: true
image: false
lang: zh
layout: post
title: IP数据报头中的MF标志
translated: true
type: note
---

问题：IP数据报头部中的“MF”是什么意思？

答案：

**MF** 代表 **More Fragments**（更多分片）。

它是 IPv4 头部 **标志字段** 中的 1 位标志。标志字段总共 3 位：

| 位 | 名称 | 含义 |
|----|------|------|
| 0 | 保留 | 始终为 0 |
| 1 | DF | 不分片 |
| 2 | **MF** | **更多分片** |

**MF 的作用：**

- **MF = 1** → 后面还有更多分片。接收方应继续等待后续分片以重组原始数据报。
- **MF = 0** → 这是 **最后一个（或唯一一个）分片**。接收方在收到所有之前的分片后，即认为数据报完整。

**示例场景：**

如果一个大型 IP 数据报被分成 3 个分片：
- 分片 1 → MF = 1（还有更多）
- 分片 2 → MF = 1（还有更多）
- 分片 3 → MF = 0（最后一个）

接收方结合 MF 标志和 **分片偏移** 字段，正确重组原始数据。

参考资料：
- [RFC 791 – Internet Protocol](https://www.rfc-editor.org/rfc/rfc791)
- [IP Fragmentation – Wikipedia](https://en.wikipedia.org/wiki/IP_fragmentation)