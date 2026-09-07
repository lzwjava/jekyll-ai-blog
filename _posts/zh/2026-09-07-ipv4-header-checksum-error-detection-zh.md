---
audio: false
generated: true
image: false
lang: zh
layout: post
title: IPv4头部校验和错误检测
translated: true
type: note
---

问题：IPv4 如何进行错误检查，以及使用哪个特定字段？

答案：

IPv4 使用 **Header Checksum**（头部校验和）进行错误检测——但它只保护 **头部**，而不保护负载/数据。

---

## 校验和字段

| 字段 | 大小 | 头部中的位置 |
|---|---|---|
| 头部校验和 | 16 位（2 字节） | 字节 10–11 |

---

## 工作原理

**发送端（计算）：**
1. 将校验和字段设置为 `0x0000`
2. 将整个 IPv4 头部拆分为 **16 位字**
3. 使用 **二进制反码加法** 求和所有 16 位字
4. 对结果取 **二进制反码** → 即为校验和
5. 将其填入校验和字段

**接收端（验证）：**
1. 将接收到的头部拆分为 16 位字（包括校验和字段）
2. 求和所有字
3. 如果结果为 `0xFFFF` → 头部 **有效**；否则 → **损坏**，数据包被丢弃

---

## 关键点

- ✅ 保护对象：**仅头部字段**（TTL、源 IP、目的 IP、标志等）
- ❌ 不保护：**负载/数据**（这由 TCP/UDP 校验和或上层协议负责）
- ♻️ **在每一跳路由器上重新计算**——因为每一跳 TTL 都会递减，从而改变头部
- IPv6 **完全移除了** 头部校验和，转而依赖第 4 层校验和

---

## 覆盖的头部字段

20 字节（最小）头部中的所有字段都会被检查：

```
Version | IHL | DSCP/ECN | Total Length
Identification | Flags | Fragment Offset
TTL | Protocol | [校验和字段本身，设置为 0]
Source IP Address
Destination IP Address
Options（如果有）
```

---

参考：
- [RFC 791 – Internet Protocol](https://datatracker.ietf.org/doc/html/rfc791)
- [IPv4 Header – Wikipedia](https://en.wikipedia.org/wiki/IPv4#Header)
- [IPv4 Checksum Explained – GeeksforGeeks](https://www.geeksforgeeks.org/error-detection-in-computer-networks/)