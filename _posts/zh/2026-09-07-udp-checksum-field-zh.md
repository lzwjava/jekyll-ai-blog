---
audio: false
generated: true
image: false
lang: zh
layout: post
title: UDP校验和字段
translated: true
type: note
---

问题：UDP 使用哪个字段来确保数据正确性？

答案：

UDP 使用 **校验和（Checksum）** 字段来确保数据正确性。

- 这是 UDP 头部中一个 16 位的字段。
- 它覆盖 UDP 头部、UDP 数据（有效载荷）以及从 IP 头部衍生出的伪头部（源/目标 IP、协议、UDP 长度）。
- 发送方计算校验和并填入该字段；接收方重新计算并进行比较——如果不匹配，数据包将被丢弃。
- 在 IPv4 中，校验和是**可选的**（值为 `0x0000` 表示未计算）；在 IPv6 中，校验和是**强制的**。

UDP 头部结构参考如下：

| 字段 | 大小 |
| --- | --- |
| 源端口 | 16 位 |
| 目标端口 | 16 位 |
| 长度 | 16 位 |
| **校验和** | **16 位** |

> 注意：UDP 仅提供基本的错误*检测*（而非纠正）。如果数据包未通过校验和检查，它会被直接丢弃——UDP 不会重新传输。

参考链接：

- [RFC 768 – 用户数据报协议](https://www.rfc-editor.org/rfc/rfc768)
- [UDP – MDN Web 文档术语表](https://developer.mozilla.org/en-US/docs/Glossary/UDP)