---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DMIT LAX 眼球方案详解
translated: true
type: note
---

## DMIT LAX.AN5.EB.TINY — 详细解析

### 名称的含义是什么？

DMIT 的产品命名遵循标准结构：**地点 + 硬件平台 + 网络线路 + 套餐规模**。因此 `LAX.AN5.EB.TINY` 表示：
- **LAX** = 洛杉矶数据中心
- **AN5** = AMD EPYC 9005 (AN5) 硬件平台
- **EB** = Eyeball 网络路由
- **TINY** = 入门级套餐规模

---

### LAX.AN5.EB.TINY 的规格

LAX.AN5.EB.TINY 套餐包括：
- **vCPU：** 1 虚拟核心
- **RAM：** 2.0 GB
- **存储：** 20 GB SSD
- **路由配置：** Eyeball (EB)
- **IPv4：** 1 个 IPv4 地址
- **IPv6：** 1 个 IPv6 /64 地址
- **DDoS 防护：** 标准防护
- **流量：** 双向 **1500 GB** @ 2 Gbps
- **超出配额后：** 不限速但降至 @ 4 Mbps
- **价格：** 每月 $12.98

---

### 什么是 "Eyeball" (EB) 网络？

LAX.AN5.EB 路由配置包含 Tier 1 线路以及通过 CMIN2 或类似中国 ISP 的尽力优化中国路由。

具体来说：洛杉矶 Eyeball 系列使用 CMIN2 路由 —— 中国电信和中国联通通过 CN2 高级线路出境，中国移动使用 CMIN2，所有三家运营商均通过 CMIN2 回程。IPv6 也双向使用 CMIN2。

---

### 价格

标准月付价格为 **每月 $12.98**。但是，目前有一个值得注意的优惠码：

使用优惠码 `LAX-EB-LAUNCH-NON-MONTHLY-RECURRING-20OFF`，在按季或按年付款时，可获得 **永久性 20% 循环折扣**，适用于 LAX Eyeball 系列。这不是一次性折扣 —— 每个计费周期都会生效，并且适用于 TINY 及以上套餐。

因此，使用该优惠码按季/按年付款后，有效价格降至约 **每月 ~$10.38**。

---

### 为什么有些列表显示 1000GB 而不是 1500GB？

这是 **EB (Eyeball)** 系列和 **Pro (Premium)** 系列在 TINY 级别的一个关键区别：

**LAX.AN5.Pro.TINY** (Premium/CN2 GIA 路由) 仅提供 **1000 GB** 双向流量，端口为 1 Gbps，价格为 $12.98/月；而 EB.TINY 以相同价格提供 **1500 GB** 双向流量，端口为 2 Gbps。

在相同价格下，EB 套餐提供的流量配额显著高于 Pro 套餐 —— 如果您不是特别需要 CN2 GIA 路由，EB 套餐更值得考虑。

简而言之，您看到的 **1000GB** 数据属于 **Pro (CN2 GIA) TINY** 套餐，而不是 EB TINY。两者的路由不同：
- **Pro** = CN2 GIA (对中国电信质量更高，但带宽配额较少，端口 1 Gbps)
- **EB** = CMIN2 Eyeball (带宽配额更大，1500GB，端口 2 Gbps，路由质量稍逊于高级路由)

---

### 超出流量配额后会发生什么？

当您超出带宽分配后，DMIT 不会直接切断您的服务，而是会限制您的速度。对于 LAX.EB.TINY (和 Pro.TINY)，超出配额后的限速为 **4 Mbps** —— 您的服务保持在线，只是速度变慢。这比意外的超额费用或突然的服务中断更具可预测性。

---

### 总结表格

| 特性 | LAX.AN5.EB.TINY | LAX.AN5.Pro.TINY |
|---|---|---|
| 流量 | **1500 GB** (双向) | **1000 GB** (双向) |
| 端口速度 | 2 Gbps | 1 Gbps |
| 价格 | $12.98/月 | $12.98/月 |
| 路由 | CMIN2 Eyeball | CN2 GIA Premium |
| 超出配额后 | 限速至 4 Mbps | 限速至 4 Mbps |
| 库存情况 | 有货 | 经常缺货 |

参考链接：

- [DMIT 定价页面](https://www.dmit.io/pages/pricing)
- [DMIT 购物车 (实时规格)](https://www.dmit.io/cart.php)
- [DMIT 云实例页面](https://www.dmit.io/pages/cloud-instance)
- [AN5 平台升级详情 (GitHub)](https://github.com/yygr61/dmit-an5-premium-plans)
- [DMIT 2026 优惠码 (GitHub)](https://github.com/jjleyw3/DMIT)
