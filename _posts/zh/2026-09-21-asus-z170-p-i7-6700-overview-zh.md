---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 华硕 Z170-P i7-6700 概述
translated: true
type: note
---

问题：**ASUS Z170-P + Intel Core i7-6700 组合简介**

回答：这是一套 **2015 年左右的 Intel Skylake 桌面平台**：ASUS Z170-P 主板 + Intel Core i7-6700，搭配原装 Intel 散热器。在其所属世代中，这是一套相当扎实的主流/高端配置。

### 硬件概览

| 部件                | 规格                                                         |
| ------------------- | ------------------------------------------------------------- |
| **CPU**             | Intel Core i7-6700                                            |
| **架构**            | Skylake，14 nm                                                |
| **核心/线程**       | 4C / 8T                                                       |
| **基础/睿频**       | 3.4 / 4.0 GHz                                                 |
| **缓存**            | 8 MB                                                          |
| **TDP**             | 65 W                                                          |
| **插座**            | LGA1151                                                       |
| **核显**            | Intel HD Graphics 530                                         |
| **主板**            | ASUS Z170-P                                                   |
| **内存**            | DDR4                                                          |
| **存储**            | 4× SATA 6 Gb/s + 1× M.2                                       |
| **扩展**            | PCIe 3.0，包括 x16 GPU 插槽                                   |
| **后置 I/O**        | USB 3.0、USB-C、USB 2.0、HDMI、DVI-D、千兆以太网、音频        |

Intel 将 i7-6700 标注为 **4 核 / 8 线程，基础频率 3.4 GHz，睿频最高 4.0 GHz**，TDP 65 W，搭载 HD Graphics 530。（[Intel][1]）

Z170-P 采用 **LGA1151** 插座，支持第 6 代 Core 处理器。它配备四根 DDR4 DIMM 插槽、一个支持 2242/2260/2280 设备的 M.2 插槽以及四个 SATA 6 Gb/s 接口。（[ASUS 下载中心][2]）

### 如今的意义

有趣的是，**这颗 CPU 对于基础的桌面/服务器工作依然完全可用**，但平台已经老旧：

```text
i7-6700
  ├── 4 个物理核心
  ├── 8 个线程
  ├── 3.4 GHz 基础频率
  └── 4.0 GHz 睿频
        │
        ▼
    ASUS Z170-P
        │
   ┌────┴─────┐
   ▼          ▼
 DDR4       PCIe 3.0
   │          │
 内存       GPU / 网卡
        │
        ▼
     M.2 / SATA
```

对于 **廉价的二手机器**，这套组合仍然可以胜任以下用途：

* Linux 家庭实验室 / 小型服务器
* NAS
* 路由器/防火墙
* 轻量级 Docker 工作负载
* 老游戏
* 日常桌面使用
* 开发机
* 以 GPU 为主的工作负载（CPU 不是瓶颈）

然而，对于现代 CPU 密集型工作负载，**4C/8T 是主要限制**。此外，i7-6700 已正式停止服务，Intel 将其服务更新结束日期列为 2022 年 9 月 30 日。（[Intel][1]）

一个有用的细节：**i7-6700 并非 6700K**。6700 的倍频被锁定，因此如果你期望通过这套配置进行典型的 Z170 超频，那就不符合预期了。

如果你正在查看 **二手清单**，请告诉我 **要价**，我可以告诉你这套组合在 2026 年是否划算，包括应该搭配什么样的 RAM/GPU/SSD。

参考：

* [Intel Core i7-6700 规格](https://www.intel.com/content/www/us/en/products/sku/88196/intel-core-i76700-processor-8m-cache-up-to-4-00-ghz/specifications.html?utm_source=chatgpt.com)
* [ASUS Z170-P 手册/规格](https://dlcdnets.asus.com/pub/ASUS/mb/LGA1151/Z170-P/E12045_Z170-P_UM_V3_WEB.pdf?utm_source=chatgpt.com)

[1]: https://www.intel.com/content/www/us/en/products/sku/88196/intel-core-i76700-processor-8m-cache-up-to-4-00-ghz/specifications.html?utm_source=chatgpt.com "Intel® Core™ i7-6700 处理器"
[2]: https://dlcdnets.asus.com/pub/ASUS/mb/LGA1151/Z170-P/E12045_Z170-P_UM_V3_WEB.pdf?utm_source=chatgpt.com "Z170-P 规格摘要"