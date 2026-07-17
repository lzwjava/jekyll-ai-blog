---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 逻辑处理器索引含义
translated: true
type: note
---

问题：“12 (AMD EPYC 7443 24核处理器)”是什么意思？

答：这是来自 `/proc/cpuinfo` 或 `lscpu -e` 的一行输出——`12` 是**逻辑处理器索引**（从0开始），而字符串是该逻辑CPU的 `model name` 字段。

```bash
# 自己查看
grep -A0 "^processor\|^model name" /proc/cpuinfo | head -30
# 或者更清晰
lscpu -e
```

关于 EPYC 7443 的上下文：

- **24个物理核心 / 48线程（SMT2）** — Zen 3架构，7nm工艺
- 基础频率2.85 GHz，加速频率4.0 GHz
- 128 MB L3缓存
- 8个CCD缩减为更少...实际上7443有4个CCD × 6个核心，每个CCD区域共享32MB L3缓存
- TDP 200W，PCIe 4.0，8通道DDR4-3200

因此，处理器索引 `12` 只是该插槽上的第13个逻辑CPU（线程）——开启SMT后，核心0–23映射到物理核心0–23，而24–47是它们的兄弟线程（或交错排列，取决于拓扑结构——查看 `lscpu -e` 的实际 `CORE` 列，了解哪个物理核心拥有线程12）。

如果要固定训练/推理工作负载，有用的命令：

```bash
lscpu -e=CPU,CORE,SOCKET,ONLINE
numactl --hardware   # 在固定线程前检查NUMA节点映射
```

对于与MI300X配合使用的主机端数据加载/预处理，7443是一颗不错的CPU——只需确保将数据加载器工作线程固定在GPU的PCIe根复合体所在的同一NUMA节点上的核心，以避免跨节点内存流量。
