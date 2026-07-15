---
audio: false
generated: true
image: false
lang: zh
layout: post
title: EATX主板指南
translated: true
type: note
---

## 问题：什么是EATX主板？

**EATX（扩展ATX）** 是一种**比标准PC主板尺寸更大的板型**。它是标准ATX尺寸的扩展版，专为需要**更多PCIe插槽、更多内存插槽、更强供电或更高扩展能力**的系统设计。

![Image](https://images.openai.com/static-rsc-4/Qea2CXiQ9yClfkczPZbsw61MJI6HBF5wa9yElTyRnaiHlC_032VEObFcT3PGKLIMf3Sl67NX_hp7g7H1e5n-uwRlV0_nye58ZG_0XkQBk2h_5gcvHFJqZ6qkxcu2noJRhD-pDlfQ2LxWIfRsgSUBPgG_dLoUdiD8qUwJk1BYWNkXTTMdCbUDw4pMqmuBXdT3?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/RauGj7lNjPyc-ts7GbL3zV9rgrbtvAPvBlQmw2Laic0DCRaUNEF94GHvv-sPWilqRhfkW60XHSbqYExTs-03aTabnImLk8kOZoL1Zn4HrIXj3jlSl3fWqy7T3v2JEJmewvRqx8gwtbizAtMSGdWxNUHuwJkNOfSIBwiGyB4Tkny9jxr2kB-alPgz0LdV1ZEK?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/S8tKyk-5-JFLwTti8Qwm9jJFcqc3qQh3TW5BwSrsVBEcxBE_NU1wmYRNyrIbUXMeBs40Jyz-Vaj69wqmKPDyKgnRDeXHWaaWvfcvr7nz41D9mVo1Agcu__MbHefYA3NRoFUZQ8Hf_Iyd7Da229GW4cSk4uZT3dug-j7UaxXAHtYfOCP-MV86KEals0tbcobT?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/QtnFaAmuvms4v5oFt4-T-MFvABuCCZy4uqkgr4J_PQqHpeKKRqbagvRmE-B-cDXIFLQSu7XLrUNYyQtyYhCz-_Ws1peqDP7Hdgl4JYPK75wIMUrhw-Su9amcDEc71fBExLS2jSXrMSVxDKI2DtC9fLJYqu8-6pTlBHFriL1T8g2WREeYaLGmOjLrQ9aILUOh?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/LOgYafmdb_8xjicb2nQuAGN_gXeTE3wjUoA2w7nNEKuLJTLEZsE41LcajHZ1o_qgj79s05PzyYBI6cuNxAuu7l1s-_k8RCB6tevMWTXVgrlAlvk5az5yVg_Hud-UapmI1t7ayEt2IBptUvONemSATcslUj11UhviiuOJQI8j36MQuTNNLbZo7-MolR_GZxUW?purpose=fullsize)

### 尺寸对比

| 板型         |            尺寸（约） | 典型用途                 |
| ------------ | ---------------------: | ------------------------ |
| Mini-ITX     |              170 × 170 mm | 小型PC                   |
| Micro-ATX    |              244 × 244 mm | 入门/主流配置            |
| ATX          |              305 × 244 mm | 常规台式机               |
| **EATX**     | **305 × 330 mm**（按型号变化） | 工作站 / HEDT / 服务器   |
| SSI-EEB      |              305 × 330 mm | 服务器级别               |

主要区别通常在于**宽度**（前后纵深）。EATX通常比ATX更宽。

---

## 为什么使用EATX？

### 1. 更多PCIe插槽

常规ATX主板：

```
[ CPU ]

PCIe x16
PCIe x1
PCIe x1
PCIe x16
```

EATX工作站主板：

```
[ CPU ]

PCIe x16
PCIe x16
PCIe x16
PCIe x16
PCIe x16
```

适用于：

* 多GPU
* AI训练平台
* 视频渲染
* 存储控制器
* 网卡

示例：

* 4 × RTX 4090
* 4 × RTX 3090
* 多块 MI50 / Radeon Instinct 显卡

---

### 2. 更多内存

桌面级ATX：

```
DIMM DIMM DIMM DIMM
```

EATX工作站：

```
DIMM DIMM DIMM DIMM
DIMM DIMM DIMM DIMM
```

尤其适用于：

* Threadripper Pro
* Intel Xeon W
* AMD EPYC 工作站主板

示例：

* 8通道 DDR5 内存
* 1TB+ 内存容量

---

### 3. 更大的CPU平台

EATX常见于：

### AMD Threadripper Pro

示例：
ASUS Pro WS WRX80E-SAGE SE WIFI

特性：

* sWRX8 插槽
* 8通道 DDR4 ECC
* 7个 PCIe 4.0 x16 插槽
* 新型号主板支持 Threadripper Pro 7000 系列对应产品

---

### AMD EPYC 工作站

EPYC平台通常采用：

* SP3/SP5 插槽
* EEB/EATX 尺寸
* 超大内存容量

示例：

```
EPYC CPU
   |
   +-- 8通道内存
   |
   +-- 128条PCIe通道
   |
   +-- 多块GPU
```

---

## EATX 与常规游戏主板对比

示例：

### MSI X870E（ATX）

适用于：

* Ryzen 9000
* RTX 4070/4090
* 游戏
* 单GPU AI实验

通常配置：

```
CPU
 |
GPU
 |
GPU（可选）
```

---

### Threadripper Pro EATX

专为以下配置设计：

```
CPU
 |
GPU GPU GPU GPU
 |
NVMe NVMe NVMe
 |
1TB 内存
```

更像一台迷你服务器。

---

## 针对AI工作负载

当您从以下配置升级时，EATX变得值得考虑：

```
RTX 4070 12GB
      |
      |
单GPU
```

升级至：

```
Threadripper Pro
+
4 × RTX 3090 24GB

= 96GB VRAM
```

或：

```
EPYC
+
8 × GPU

= 强大的训练节点
```

主板本身不会提升速度。其优势在于**I/O容量**：

* 更多PCIe通道
* 更多GPU
* 更多内存通道
* 更多存储

---

对于您当前的实验（RTX 4070 + MI50 + 可能的多GPU），常规**ATX X870/B550/X570**主板通常足够。只有在搭建**4-8 GPU本地AI工作站**时，EATX才真正发挥价值。