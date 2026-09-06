---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PoE中继器简单解释
translated: true
type: note
---

**问题：什么是"PoE 中继器"？PoE 代表什么？**

**答案：**

**PoE** 代表 **Power over Ethernet**（以太网供电）——一种允许单根以太网电缆同时传输**数据和电力**的技术，无需单独电源适配器。

---

**PoE 中继器**

**PoE 中继器**是一种同时完成两件事的设备：
1. 将网络信号扩展到标准 100 米以太网限制之外
2. 传递（或再生）PoE 电力，使终端设备在扩展后仍能获得供电

---

**为什么它有用**

标准以太网（无 PoE 中继器）每段线缆限制为 **100 米**。如果需要为更远的 IP 摄像头或接入点等设备供电，PoE 中继器可让您实现：

```
[PoE 交换机] ──100m──> [PoE 中继器] ──100m──> [IP 摄像头 / 接入点]
     ↑                        ↑
  发送电力             再生信号和电力
  和数据
```

---

**常见 PoE 供电设备**

| 设备 | PoE 的优势 |
|---|---|
| IP 摄像头（监控摄像头） | 摄像头位置无需墙壁插座 |
| Wi-Fi 接入点（AP） | 灵活的吊顶或墙面安装 |
| VoIP 电话 | 单根线缆同时传输语音和电力 |
| 智能门锁 / 对讲机 | 可轻松安装在任何位置 |

---

**PoE 标准**

| 标准 | 最大功率 | 常见用途 |
|---|---|---|
| PoE (802.3af) | 15.4W | IP 电话、基础摄像头 |
| PoE+ (802.3at) | 30W | PTZ 摄像头、接入点 |
| PoE++ (802.3bt) | 60–90W | 高功率接入点、电视 |

---

**主要优势**：只需一根线缆即可连接到远程位置，为设备供电并联网——无需电工。

参考资料：
- [Power over Ethernet – 维基百科](https://en.wikipedia.org/wiki/Power_over_Ethernet)
- [什么是 PoE？ – Cisco](https://www.cisco.com/c/en/us/solutions/enterprise-networks/what-is-poe.html)
- [PoE 中继器详解 – FS.com](https://community.fs.com/article/poe-extender-vs-poe-repeater-vs-poe-injector.html)