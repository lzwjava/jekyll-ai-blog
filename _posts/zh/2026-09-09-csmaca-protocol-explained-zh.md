---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CSMA/CA协议详解
translated: true
type: note
---

问题：什么是CSMA/CA协议？

答案：

**CSMA/CA（载波侦听多路访问/冲突避免）**是一种网络协议，用于管理设备如何共享通信介质——主要应用于**无线网络（Wi-Fi / IEEE 802.11）**。

---

### 工作原理

与有线网络能在冲突发生后检测到冲突（CSMA/CD）不同，无线设备**无法同时发送和监听**，因此CSMA/CA试图**在冲突发生之前就避免它**。

**逐步过程：**

1. **载波侦听** — 发送前，设备先监听信道是否空闲或忙碌。
2. **若忙碌则等待** — 如果信道忙碌，设备等待直至空闲。
3. **随机退避** — 信道空闲后，设备再等待一个额外的随机时间段（退避计时器），以减少两个设备同时发送的概率。
4. **发送** — 如果退避后信道仍然空闲，设备便发送数据。
5. **确认（ACK）** — 接收方发回ACK以确认成功接收。若未收到ACK，发送方认为发生了冲突并重新发送。

---

### 可选：RTS/CTS机制

为了解决**隐藏节点问题**（两个发送方无法听到对方，但都能到达同一个接收方），CSMA/CA可选使用以下机制：

- **RTS（请求发送）** — 发送方表示准备发送的意图
- **CTS（允许发送）** — 接收方授予发送权限

这会预留信道，并使附近其他节点静默。

---

### CSMA/CA 与 CSMA/CD 对比

| 特性 | CSMA/CA | CSMA/CD |
|---|---|---|
| 用于 | 无线（Wi-Fi） | 有线（以太网） |
| 策略 | 避免冲突 | 检测冲突 |
| 需要ACK | 是 | 否 |
| 效率 | 较低 | 较高 |

---

参考来源：
- [CSMA/CA – 维基百科](https://en.wikipedia.org/wiki/Carrier-sense_multiple_access_with_collision_avoidance)
- [IEEE 802.11 MAC层 – 详解](https://www.ieee802.org/11/)
- [无线局域网中的碰撞避免 – Cisco](https://www.cisco.com/c/en/us/support/docs/wireless-mobility/wireless-lan-wlan/69583-cat-wlan.html)