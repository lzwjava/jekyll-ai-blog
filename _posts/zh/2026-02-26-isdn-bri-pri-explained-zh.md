---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ISDN BRI 和 PRI 详解
translated: true
type: note
---

问题：根据 ITU，有两种 ISDN 用户-网络接口标准定义，它们是 Primary Rate Interface (PRI) 和什么其他接口？

答案：

ITU 定义的两种 ISDN 用户-网络接口标准是：

- **PRI** (Primary Rate Interface)
- **BRI** (Basic Rate Interface)

问题中缺失的术语是 **基本速率接口** (Basic Rate Interface) 或 **BRI**。

**解释：**

ISDN (Integrated Services Digital Network) 定义了两种主要的用户-网络接口类型：

1. **Basic Rate Interface (BRI)**
   - 也称为 2B+D
   - 提供 2 × 64 kbps B-channel（用于用户数据/语音） + 1 × 16 kbps D-channel（用于信令）
   - 总比特率：144 kbps (2B + D)
   - 主要用于住宅用户、小型办公室和单线应用

2. **Primary Rate Interface (PRI)**
   - 也称为 23B+D（在北美/日本）或 30B+D（在欧洲和其他大多数地区）
   - 提供 23 或 30 × 64 kbps B-channel + 1 × 64 kbps D-channel
   - 总比特率：1.544 Mbps（北美）或 2.048 Mbps（欧洲/国际）
   - 设计用于大型组织、PBX 系统和高容量接入

这两种接口（BRI 和 PRI）是 ITU-T I.400 系列推荐（特别是 I.430 用于 BRI，I.431 用于 PRI）中定义的基本用户-网络接入标准。

因此，填空正确答案是 **基本速率接口** 或 **BRI**。

参考文献：

- 无（基于 ITU-T ISDN 推荐的标准电信知识）
