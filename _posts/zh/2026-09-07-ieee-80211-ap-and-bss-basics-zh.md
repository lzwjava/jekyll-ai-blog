---
audio: false
generated: true
image: false
lang: zh
layout: post
title: IEEE 802.11 接入点和基本服务集基础
translated: true
type: note
---

问题：什么是IEEE 802.11，其中的**AP**和**BSS**是什么意思？

答案：

![Image](https://images.openai.com/static-rsc-4/KcIG_5yF_R-LD25uBILzsHTVW43IiTtMr1PEEfEmusAltZirbSxGF0ssAZ3CHzEQ1YDCIQv4evt6e6iDu2ZbfeG-vEzSYVC6qlwUfeNs-MzIf5kBl75VzZy-2VAqRCIMzRyjhVsd_TQiZPYGndpYz4t3RFSwqVmFkewc4g08o285ukzlLHl7XMN6o6mWBNYv?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/-Oz1bUvPSyg4jLrGlOMye4zjvflr2-y956_drl1s7RJfanWOM53cdQlp-GoS_F7uSaEGMPQr3sB3ZmmD7fBnI1U50vl4V-WTlR-qVDFexkFQzG3pQmtLEd9AkTTQaN0rvCbIkyPC7bu5xr085D91nWQndeE_vf4tJfIC7tzgrhE0VLpDzZyMJ634GFOam2PQ?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Z1orJ7tqK_urZ7vm_5713Qq_p3hiJ3diAjFJQJr1eYDycL8Tlp0cw17J9oZBhCM-kuanDnojpUkpEHf3asmaOlncpJR6CYIl-UYd6oRwSCg29BHbxLXTs3JwgaNgKOof2WSqp-67pOBMyKcUQRPTbKj70UutsLNQ0m_P4BiF5Sr-4Vxs3PU-PJBceJK6DsiE?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/tDB7KP1-eug-yIqCMIDkZqmifbTVqg7vah90dvA9fAAStmi5Dw_Xi3SwT0IgXrDkVSSTBAmIVaZ--sgvprTmkvyyPcxHdEM9STlhqbpFHnlVCUfotjQ0mcV40M8-ofhq_TfNzlFWLUovwDFENcgKSmgowSRi5yXRwOxLDEV7vjgiP_DNcvrpAJXyjuARiJId?purpose=fullsize)

### 1. 什么是802.11？

**IEEE 802.11 是定义 Wi-Fi 的标准系列。**

可以把它看作无线设备在 **MAC + PHY 层** 通信的规范：

```text
Application
    │
TCP / UDP
    │
IP
    │
802.11 MAC        ← Wi-Fi 协议
    │
802.11 PHY        ← 无线电：2.4 / 5 / 6 GHz，调制，编码
    │
   RF
```

以太网主要是 **IEEE 802.3**。

Wi-Fi 主要是 **IEEE 802.11**。

不同代际对应不同的修订版本：

```text
802.11b  → 2.4 GHz
802.11a  → 5 GHz
802.11g  → 2.4 GHz
802.11n  → Wi-Fi 4
802.11ac → Wi-Fi 5
802.11ax → Wi-Fi 6 / 6E
802.11be → Wi-Fi 7
```

重要的是，**802.11 不仅仅是“无线电频率”**。它还定义了以下内容：

* MAC 地址
* Wi-Fi 帧
* 关联/认证
* AP 行为
* 信道接入
* 重传
* 信标帧
* 加密/安全机制
* PHY 调制/编码

---

# 2. 什么是 STA？

在讨论 AP 和 BSS 之前，还有一个重要术语：

**STA = 站点（Station）**

STA 基本上就是参与 802.11 网络的 Wi-Fi 设备。

例如：

```text
             Wi-Fi
               │
       ┌───────┴───────┐
       │               │
    笔记本电脑         手机
      STA              STA
```

你笔记本电脑的 Wi-Fi 网卡就是一个 **STA**。

你手机的 Wi-Fi 网卡是另一个 **STA**。

AP 在概念上也包含一个无线站接口，但在通常的 802.11 术语中，我们将 AP 与普通的客户端 STA 区分开来。

---

# 3. 什么是 AP？

**AP = 接入点（Access Point）**

AP 是提供无线网络接入的设备。

例如：

```text
                 互联网
                    │
                 路由器
                    │
              ┌─────┴─────┐
              │     AP    │
              └─────┬─────┘
                    │
          ~~~~~~~~~ Wi-Fi ~~~~~~~~~
             │          │
          笔记本电脑    手机
           STA          STA
```

一个家用 Wi-Fi 路由器通常同时承担多个角色：

```text
┌───────────────────────────────┐
│ 家用路由器                    │
│                               │
│  AP                           │
│  DHCP 服务器                  │
│  NAT                          │
│  以太网交换机                 │
│  防火墙                       │
│  路由器                       │
└───────────────────────────────┘
```

但 **802.11 中的 AP 特指 Wi-Fi 侧的职责**。

---

# 4. 什么是 BSS？

这是关键概念。

**BSS = 基本服务集（Basic Service Set）**

BSS 本质上是一个 **802.11 无线网络单元**，在基础设施模式下以 AP 为中心。

例如：

```text
                    BSS
        ┌─────────────────────────┐
        │                         │
        │       AP                │
        │        ●                │
        │      / | \              │
        │     /  |  \             │
        │    ●   ●   ●            │
        │   STA STA STA            │
        │                         │
        └─────────────────────────┘
```

所以：

```text
BSS
 ├── AP
 ├── STA
 ├── STA
 └── STA
```

AP 及其关联的站点构成一个 **BSS**。

AP 有一个特殊的标识符，称为 **BSSID**：

```text
BSSID = 标识 BSS 的 MAC 地址
```

通常 BSSID 就是 AP 无线接口的 MAC 地址。

---

# 5. SSID 与 BSSID

这个区别非常重要。

假设你的路由器广播：

```text
SSID = MyWiFi
```

你的笔记本电脑可能会看到：

```text
SSID       BSSID               Channel
------------------------------------------------
MyWiFi     AA:BB:CC:11:22:33   36
```

**SSID** 是面向用户的网络名称。

**BSSID** 标识特定的 BSS。

可以这样理解：

```text
SSID
  │
  │ "MyWiFi"
  │
  ├──────── BSS #1
  │          BSSID = AA:BB:CC:11:22:33
  │
  └──────── BSS #2
             BSSID = AA:BB:CC:44:55:66
```

当你有多个 AP 时，这一点就变得很重要。

---

# 6. 多个 AP → ESS

假设一家公司有三个 AP：

```text
              SSID = CompanyWiFi

        AP1              AP2              AP3
         ●                ●                ●
       / | \            / | \            / | \
      STA STA          STA STA          STA STA
```

每个 AP 通常创建自己的 **BSS**：

```text
BSS1                BSS2                BSS3
 ┌─────┐              ┌─────┐              ┌─────┐
 │ AP1 │              │ AP2 │              │ AP3 │
 │ STAs│              │ STAs│              │ STAs│
 └─────┘              └─────┘              └─────┘
```

但它们都可以广播相同的 SSID：

```text
             SSID = CompanyWiFi

BSS1              BSS2              BSS3
 AP1                AP2                AP3
```

这些 BSS 共同构成一个：

**ESS = 扩展服务集（Extended Service Set）**

```text
                 ESS
 ┌──────────────────────────────────────────┐
 │                                          │
 │   BSS1       BSS2        BSS3            │
 │    AP1        AP2         AP3            │
 │     ●          ●           ●             │
 │                                          │
 └──────────────────────────────────────────┘
```

这就是大型 Wi-Fi 网络的工作原理。

你在建筑物中走动：

```text
        AP1                 AP2                 AP3
         ●                   ●                   ●
       )))))               )))))               )))))
          \                  |                  /
           \                 |                 /
            ─────── 以太网 / LAN ───────────
```

你的笔记本电脑可以移动：

```text
STA
 │
 ├── 关联到 AP1
 │
 │       走动 →
 │
 ├── 漫游到 AP2
 │
 │       走动 →
 │
 └── 漫游到 AP3
```

**SSID 可以保持为 `CompanyWiFi`**，而 STA 会切换它所关联的 **BSSID/AP**。

---

# 7. 层级结构

最容易理解的心智模型是：

```text
802.11
 │
 └── ESS
      │
      ├── BSS
      │    ├── AP
      │    ├── STA
      │    ├── STA
      │    └── STA
      │
      ├── BSS
      │    ├── AP
      │    └── STAs
      │
      └── BSS
           ├── AP
           └── STAs
```

以及：

```text
SSID  → 逻辑/面向用户的网络名称
BSSID → 特定 BSS/AP 的标识
BSS   → 一个 Wi-Fi 单元
ESS   → 互连的 BSS 集合
STA   → Wi-Fi 客户端/设备
AP    → 提供无线接入点的设备
```

### 最有用的区分

如果你在数据包层面调试 Wi-Fi，请记住：

```text
                 "什么网络？"
                      │
                     SSID
                      │
                 "哪个 AP？"
                      │
                    BSSID
                      │
                 "哪个客户端？"
                      │
                  STA MAC
```

而一个 802.11 数据包通常包含多个地址，让你能够确定 **谁在发送、谁在接收、涉及哪个 AP/BSS、以及帧如何被转发**。

这自然引出了 802.11 中最有趣的部分：**3 地址/4 地址帧格式，Beacon → Probe → Authentication → Association → Data**，它使 AP 和 BSS 的概念在数据包层面变得具体。接下来我可以使用实际的 802.11 帧示例来讲解。
