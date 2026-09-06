---
audio: false
generated: true
image: false
lang: en
layout: post
title: PoE Repeaters Explained Simply
translated: false
type: note
---

Question: What is a "PoE 中继器" (PoE Repeater), and what does PoE stand for?

Answer:

**PoE** stands for **Power over Ethernet** — a technology that allows a single Ethernet cable to carry **both data and electrical power** simultaneously, eliminating the need for a separate power adapter.

---

**PoE Repeater (PoE 中继器)**

A **PoE Repeater** is a device that does two things at once:
1. **Extends the network signal** beyond the standard 100-meter Ethernet limit
2. **Passes through (or regenerates) the PoE power** so the end device still receives power after the extension

---

**Why It's Useful**

Standard Ethernet (without PoE repeater) is limited to **100 meters per cable run**. If you need to power a device like an IP camera or access point that's farther away, a PoE repeater lets you:

```
[PoE Switch] ──100m──> [PoE Repeater] ──100m──> [IP Camera / AP]
     ↑                        ↑
  sends power          regenerates both
  + data               signal AND power
```

---

**Common Devices Powered by PoE**

| Device | Why PoE Matters |
|---|---|
| IP Cameras (监控摄像头) | No wall outlet needed at camera location |
| Wi-Fi Access Points (AP) | Flexible ceiling/wall placement |
| VoIP Phones | Single cable for voice + power |
| Smart door locks / intercoms | Easy installation anywhere |

---

**PoE Standards**

| Standard | Max Power | Common Use |
|---|---|---|
| PoE (802.3af) | 15.4W | IP phones, basic cameras |
| PoE+ (802.3at) | 30W | PTZ cameras, APs |
| PoE++ (802.3bt) | 60–90W | High-power APs, TVs |

---

**Key Benefit**: Run one cable to a remote location and power + connect a device — no electrician needed.

References:
- [Power over Ethernet – Wikipedia](https://en.wikipedia.org/wiki/Power_over_Ethernet)
- [What is PoE? – Cisco](https://www.cisco.com/c/en/us/solutions/enterprise-networks/what-is-poe.html)
- [PoE Repeater Explained – FS.com](https://community.fs.com/article/poe-extender-vs-poe-repeater-vs-poe-injector.html)
