---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Intel Xeon Gold 6248R 简介
translated: true
type: note
---

**问题：** 什么是英特尔至强金牌6248R处理器？

**回答：**

英特尔至强金牌6248R是一款值得深入了解的服务器级处理器。以下是详细介绍：

**概述**

这是一款64位、24核x86高性能服务器微处理器，于2020年初由英特尔推出，基于 **Cascade Lake** 微架构，采用 **14 nm** 工艺制造。

**关键规格**

| 规格 | 参数 |
| --- | --- |
| 核心数 / 线程数 | 24 / 48 |
| 基础频率 | 3.0 GHz |
| 睿频加速 | 4.0 GHz |
| L3缓存 | 35.75 MB |
| 热设计功耗 | 205 W |
| 插槽类型 | LGA 3647 |
| 内存 | DDR4-2933，6通道，最高支持1 TB |
| 内存带宽 | 141 GB/s |
| 发布价格 | 2,700美元 |

**架构亮点**

该芯片支持双路处理，配备2个AVX-512 FMA单元和两条超路径互联（UPI）链路。值得注意的是，6248R的L3缓存容量为35.75 MiB，高于默认规格——这一容量通常出现在26核的处理器上。

**其重要意义**

6248R代表了英特尔至强CPU的重大转变，通过提供更高时钟频率来直接应对AMD EPYC 7002“罗马”系列的竞争。英特尔凭借这款205 W TDP的型号，将产品策略从功耗优化转向了性能优化。

**目标应用场景**

它针对要求严苛的主流数据中心、云计算、网络及存储工作负载进行了优化，并支持最多4路扩展，适用于更广泛的工作负载范围。

**当前状态**

该处理器目前已停产，其服务更新终止日期已于2025年6月30日到期。

---

**参考资料：**

- [英特尔至强金牌6248R官方规格](https://www.intel.com/content/www/us/en/products/sku/199351/intel-xeon-gold-6248r-processor-35-75m-cache-3-00-ghz/specifications.html)
- [WikiChip – 至强金牌6248R](https://en.wikichip.org/wiki/intel/xeon_gold/6248r)
- [ServeTheHome – 基准测试与评测](https://www.servethehome.com/intel-xeon-gold-6248r-benchmarks-and-review/)
- [cpu-monkey – 规格与基准测试](https://www.cpu-monkey.com/en/cpu-intel_xeon_gold_6248r)
