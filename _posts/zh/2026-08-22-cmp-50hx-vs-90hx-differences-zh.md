---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CMP 50HX与90HX差异
translated: true
type: note
---

**问题：** NVIDIA CMP 50HX和CMP 90HX显卡之间有什么区别？

**回答：**

这两款都是NVIDIA **CMP（加密货币挖矿处理器）** 显卡，专为加密货币挖矿设计（而非游戏）。以下是主要差异：

**架构与制程节点**
- CMP 50HX基于较旧的**图灵架构**（12纳米），采用**TU102 GPU**，其板卡设计与RTX 2080 Ti类似。
- CMP 90HX是四款中唯一使用较新的**安培架构**（三星8纳米）的显卡，基于**GA102-100 GPU**，与RTX 3080共享相同板卡（PG132）。

**性能（哈希率）**
- CMP 90HX的哈希率几乎是CMP 50HX的两倍。

**功耗**
- CMP 50HX的功耗比CMP 90HX低约28%。
- CMP 90HX的TDP高达320W，显著更高。

**显存**
- 两款显卡均配备**10GB显存**。

**摘要表：**

| 特性 | CMP 50HX | CMP 90HX |
|---|---|---|
| 架构 | 图灵（12纳米） | 安培（8纳米） |
| GPU | TU102 | GA102-100 |
| 显存 | 10GB | 10GB |
| TDP | ~250W | 320W |
| 哈希率 | 基准 | 约为50HX的2倍 |

简而言之，**90HX是性能更强的显卡**，具备更好的挖矿性能和更新的架构，但功耗显著更高。**50HX更节能**，但原始哈希率较低。

**参考资料：**
- [NVIDIA CMP加密货币挖矿GPU详解 – WCCFTech](https://wccftech.com/nvidias-cmp-crypto-mining-gpus-detailed-90hx-based-on-ampere-ga102-while-50hx-40hx-30hx-based-on-turing-gpus/)
- [NVIDIA CMP 90HX据称基于RTX 3080 – HotHardware](https://hothardware.com/news/nvidias-cmp-90hx-cryptocurrency-gpu-rumored-geforce-rtx-3080)
- [CMP 50HX vs CMP 90HX基准测试 – Technical.city](https://technical.city/en/video/CMP-50HX-vs-CMP-90HX)