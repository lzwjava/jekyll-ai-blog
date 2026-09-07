---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SSL/TLS重放攻击保护方法
translated: true
type: note
---

问题：SSL/TLS 如何提供重放攻击保护？

回答：

SSL/TLS 通过多层机制防御重放攻击：

**1. 会话密钥与随机数（Nonces）**
每次 TLS 握手都会基于两个随机值（客户端随机数和服务器随机数，各 28–32 字节的加密安全随机数）生成全新会话。这些值被组合用于派生唯一的会话密钥，因此即使攻击者捕获了整个会话，在新连接中重放这些精确字节也会因密钥不同而失败。

**2. 序列号**
每个 TLS 记录都有一个隐式序列号（不在线路上发送，但包含在 MAC 计算中）。接收方维护自己的计数器，并拒绝任何乱序或序列号已出现过的记录。这直接消除了会话内的重放。

**3. MAC（消息认证码）**
每条记录都通过 MAC 进行认证，MAC 覆盖：
- 有效载荷
- 记录类型和版本
- **序列号**

重放旧记录会导致 MAC 不匹配（因为期望的序列号已变化），连接随即被断开。

**4. TLS 1.3 — 0-RTT 重放考量**
TLS 1.3 的 0-RTT（早期数据）功能是重放风险重新出现的唯一区域。由于早期数据在握手完成前使用预共享密钥加密，网络攻击者可以重放它。TLS 1.3 通过以下方式缓解：
- **一次性会话票据**——服务器可强制一张票据仅被接受一次
- **反重放缓存**——服务器端布隆过滤器/缓存，记录已见过的 nonce
- **应用层幂等性要求**——针对所有 0-RTT 数据

**5. 时间戳（部分实现中）**
某些部署在握手中包含时间戳；服务器拒绝时间戳超出可接受窗口的握手，进一步限制重放窗口。

**汇总表**

| 机制 | 保护对象 |
|---|---|
| 客户端/服务器随机数 | 跨会话重放 |
| 序列号 | 会话内记录重放 |
| 基于序列号的 MAC | 被篡改或重放的记录 |
| 会话票据过期 | 陈旧的会话恢复重放 |
| 0-RTT 反重放缓存 | 早期数据重放（TLS 1.3） |

参考：
- [RFC 8446 – TLS 1.3 规范](https://datatracker.ietf.org/doc/html/rfc8446)
- [RFC 5246 – TLS 1.2 规范](https://datatracker.ietf.org/doc/html/rfc5246)
- [OWASP – 传输层保护速查表](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html)
- [Cloudflare – 0-RTT 与重放攻击](https://blog.cloudflare.com/introducing-0-rtt/)