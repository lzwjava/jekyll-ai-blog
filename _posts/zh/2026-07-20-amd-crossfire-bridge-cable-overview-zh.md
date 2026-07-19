---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD CrossFire桥接电缆概述
translated: true
type: note
---

问题：这是什么AMD CrossFire线缆？

答案：

这是一根 **AMD CrossFire 桥接线缆**（也称为 **CrossFire 互连线缆**）。它是一种小型物理连接，用于连接 **两块 AMD Radeon GPU** 以实现多 GPU 渲染。

![Image](https://images.openai.com/static-rsc-4/CRHxU-qGC5CAZoHeTkh9Ek-j_JxfL7qAcL8q2-DfciNdZ1EDtUpYnPcmH9CQQi0p3HHI7E4lXb4pxmqiSRx8kTD2U_wIwEimRpokdBJB-jfSVJTv7u4R-SFOoMcwf0NWEZxdgnsnF5kHXGJvUNQyiGqxc-_xe45bDYkITV6PjhQHETMasK2MJmnOYOG7Mqml?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/MKx8xLOhmd1GpEML-r8jxszVvjg8jkpzyoytbC01sVQ6s16I8kQCBMmiE24hg7IXWgpQ1x80ODmd0wmqz0mD-JlI0M0_mcfKFCTJmf7yZ62SUpgb743qSgz3c_nHtEQ4T5ZoDymdqhvfq9ucM71_NiPKtOPLwvYba_d5hD1fJ86FhFAON3FtQroZGW2GrIy6?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/lbNKDIlqlxVRpWHS92a2D1yHhVpTu-prtSxxdC-G3A9guzzO1BRUu6xB4X2NFBRPYfurfIgVdARdk6_Kz5l9__b6GfaHwaXs6P-L69Mfa8P44EevsC7iaQoAgmgIth86d2MixRE33o33OW5Q-uHwIxClQCljnCuNdzakeUh11fDCApMF-DILcJfCTJpXMfot?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/bXiOq6NqfjTLPSE79SL7wafx3RakUKbqflxxR2k_GhVUOkRkYV_VepkMMRrgz18X8aooCZU7rIgWzeIyyEYAsvVEUcUEF1-U4HM6WQrtFERW9kIFEbrcnGFfqWAiva1Y3yJyCkFwwA2wfRkWbm7Hn-11J6tBT1JmpwPphLJb2lM5vFsM6vt5i-OO9st9CeP1?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/s0UVSTkGWsKnGzElWwCWaFDMoOWAX5shyV0SOP12nfpN5zcZs_j-5SMuqKuZRRZhrd4vLjdr5yQRkReaGBJqq18PJDeC-qN3wWu_oY5XaMWygOzAeCC20sCu_PX6KnrXTg2pC3cELylMhMuzFJkgW9piRyVL1kYR-jRRbshF1VlPd_8elr3Or6JZ5JNvLP-I?purpose=fullsize)

### 功能

老款 AMD Radeon 显卡在 GPU 顶部边缘有一个小型连接器：

```
GPU 1  ===== CrossFire Bridge =====  GPU 2
```

该线缆允许两块 GPU 直接交换部分渲染数据。

典型用途：

* 游戏多 GPU（CrossFire）
* 老旧专业工作负载
* 部分 OpenCL 工作负载

### 重要提示：现在基本已过时

现代 AMD GPU 通常 **不使用 CrossFire 桥接器**。

示例：

| GPU                      | 是否使用 CrossFire 桥接器？       |
| ------------------------ | ---------------------------------- |
| Radeon HD 7000 系列      | 是                                |
| Radeon R9 280/290        | 通常有（部分仅使用 PCIe）         |
| Radeon RX 400/500        | 大多无桥接，通过 PCIe 使用 XDMA   |
| Radeon RX 5000/6000/7000 | 不支持 CrossFire                  |

AMD 在 Vulkan/DX12 时代左右放弃了游戏领域的 CrossFire，因为现代 API 允许应用程序自行管理多 GPU。

### 与 NVIDIA SLI/NVLink 对比

|                | AMD CrossFire       | NVIDIA SLI          |
| -------------- | ------------------- | ------------------- |
| 桥接器         | CrossFire 线缆      | SLI 桥接器          |
| 用途           | 多 GPU 渲染         | 多 GPU 渲染         |
| 现代支持       | 几乎已消亡          | 几乎已消亡          |
| AI 训练        | 否                  | 否                  |
| 显存池化       | 否                  | 否                  |

对于 AI/LLM 工作：

```
2 × RTX 3090
```

在大多数情况下，**不**使用 SLI/NVLink 进行 PyTorch 训练。

通常使用：

```python
torch.distributed
DistributedDataParallel (DDP)
NCCL
```

GPU 通过 PCIe/NVLink 自动通信。

### 针对您的 GPU 实验

鉴于您对 RTX 3090 / Tesla / MI 系列 / 多 GPU 训练的兴趣：

这根线缆如今基本上已是 **收藏品**。除非您正在修复一台老旧的 AMD 游戏机，否则它几乎毫无价值。

类似如下的双 AMD GPU 配置：

```
R9 290 + R9 290
HD 7970 + HD 7970
```

可以使用它，但现代 AI 工作站会忽略它。