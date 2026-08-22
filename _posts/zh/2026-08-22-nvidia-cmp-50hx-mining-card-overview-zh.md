---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA CMP 50HX 矿卡概述
translated: true
type: note
---

**问题：** 什么是 NVIDIA CMP 50HX 显卡简介？  

**回答：**  

NVIDIA CMP 50HX 是一款专为矿工设计的专用 **加密货币挖矿处理器（CMP）** ，于 2021 年中发布，并非面向游戏玩家。  

**背景与目的**  

CMP 50HX 是 NVIDIA 加密货币挖矿处理器（CMP）系列的一部分，该系列旨在通过为矿工提供专用挖矿显卡，让更多 GeForce 产品流向游戏玩家手中。  

**GPU 架构**  

CMP 50HX 采用了 TU102 芯片的缩减版本，该芯片曾用于 GeForce RTX 2080 Ti 等热门 Turing 型号。它配备 3,584 个 CUDA 核心 —— 甚至比 RTX 2080 Ti 的 4,352 个核心更少 —— 这将峰值 FP32 性能降至约 11 TFLOPs。  

**关键规格**  

| 规格 | 数值 |
| --- | --- |
| CUDA 核心 | 3,584 |
| 显存 | 10 GB GDDR6 |
| 显存速度 | 14 Gbps |
| 显存位宽 | 320-bit |
| 基础 / 加速频率 | 1,350 / 1,545 MHz |
| TDP | 225 W |
| 供电接口 | 2× 8-pin |
| 接口 | PCIe 1.0 x4 |

该显卡的以太坊算力标称为 45 MH/s（在 Epoch 394 参考条件下）。  

**设计决策**  

作为面向加密货币挖矿的产品，CMP 50HX 没有显示输出接口。相反，I/O 挡板区域保持开放，以便排气通风。微星版本采用双滚珠轴承的鼓风式“AERO”散热器，专为长期连续运行而设计。  

**总结**  

CMP 50HX 是一款 Turing 时代的挖矿显卡 —— 功能专用，无显示输出，针对每瓦算力而非游戏或通用渲染任务进行了优化。  

---  

**参考资料：**  

- [MSI CMP 50HX 规格 – 微星官网](https://www.msi.com/Graphics-Card/MSI-NVIDIA-CMP-50HX-MINER/Specification)  
- [微星发布 CMP 50HX 矿卡 – VideoCardz](https://videocardz.com/newz/msi-launches-cmp-50hx-miner-with-3584-cuda-cores-and-10gb-gddr6-memory)  
- [微星列出首款 CMP 50HX – Tom's Hardware](https://www.tomshardware.com/news/msi-lists-first-nvidia-cmp-50hx-mining-gpu)
