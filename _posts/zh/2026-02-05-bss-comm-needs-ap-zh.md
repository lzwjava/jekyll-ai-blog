---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: BSS 通信需要接入点
translated: true
type: note
---

**Question:**
If a mobile device within a BSS wants to communicate with devices outside this BSS, it must go through the ______ within this BSS.

A. AP
B. APS
C. SAP
D. Hub

**Answer:** A
**Your answer:** A

---

## Detailed Explanation:

When a mobile device within a BSS (Basic Service Set) needs to communicate with devices outside its BSS, it must go through the **AP (Access Point)** within that BSS.

### Key Concepts:

**BSS (Basic Service Set):**
- wireless local area network (WLAN) 中的基本单元
- 由一个或多个 mobile devices 和一个 AP 组成
- 形成一个单一的无线覆盖区域

**Communication within BSS:**
- mobile devices 可以通过无线信道直接相互通信
- 在某些配置中，BSS 内部通信无需通过 AP

**Communication outside BSS:**
- mobile devices **必须** 使用 AP 作为中介
- AP 充当连接外部网络的 bridge/gateway
- 数据流向：Mobile Device → AP → External Network → Destination Device

**Role of the AP:**
- 作为一个关键的 relay point
- 实现无线 BSS 与有线/外部网络之间的连接
- 管理其 BSS 内设备的 authentication、association 和 routing

In summary，AP 作为 gateway，允许 BSS 内的无线设备访问资源并与本地无线网络之外的设备进行通信。
