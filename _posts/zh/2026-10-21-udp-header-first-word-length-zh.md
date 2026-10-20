---
audio: false
generated: true
image: false
lang: zh
layout: post
title: UDP报头第一个字长度
translated: true
type: note
---

答案：

## UDP 首部结构

UDP（用户数据报协议）首部总长 **固定为 8 字节（64 位）**，包含四个 16 位字段：

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |  ← 首字 (First Word)
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|            Length             |           Checksum            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                     Data (variable)                          ...
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

| 字段 | 大小 | 描述 |
|---|---|---|
| **Source Port** | 16 位（2 字节） | 发送方端口 |
| **Destination Port** | 16 位（2 字节） | 接收方端口 |
| **Length** | 16 位（2 字节） | UDP 段总长度（首部 + 数据）；最小值为 8 |
| **Checksum** | 16 位（2 字节） | 错误检测（IPv4 中可选，IPv6 中强制） |

---

## 首字长度 (First Word Length)

> 在中国网络术语中，**“字”（word）= 16 位 = 2 字节**，在 UDP 上下文中。

- **首字（First Word）** = 第一个 16 位单元 = **Source Port** 字段
- **首字长度 = 16 位（2 字节）**

整个第一行 32 位（Source Port + Destination Port）= **4 字节 = 1 个“双字”**

完整的 **UDP 首部长度 = 8 字节（固定）** — 与 IP/TCP 不同，UDP **没有可变长的选项** 也没有单独的“首部长度”字段。

---

## 与 TCP 的主要区别

| 特性 | UDP | TCP |
|---|---|---|
| 首部大小 | 固定 8 字节 | 可变 20–60 字节 |
| 首部长度字段 | ❌ 无 | ✅ 有（4 位，以 32 位字为单位） |
| 连接 | 无连接 | 面向连接 |
| 可靠性 | ❌ 否 | ✅ 是 |

---

参考资料：
- [RFC 768 – User Datagram Protocol](https://www.rfc-editor.org/rfc/rfc768)
- [UDP – Wikipedia](https://en.wikipedia.org/wiki/UDP)
- [TCP/IP Guide – UDP](http://www.tcpipguide.com/free/t_UDPMessageFormat.htm)