---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Threadripper Pro主板指南
translated: true
type: note
---

问题：什么是 Threadripper Pro 主板？

回答：

AMD Ryzen Threadripper PRO 平台是 AMD 的**工作站/服务器级桌面平台**，定位介于普通 Ryzen 和 EPYC 之间。

**Threadripper Pro 主板**是专为以下 CPU 设计的主板：

* Threadripper PRO 3000 WX 系列
* Threadripper PRO 5000 WX 系列
* Threadripper PRO 7000 WX 系列

示例：

* ASUS Pro WS WRX80E-SAGE SE WIFI
* ASUS Pro WS WRX90E-SAGE SE
* Gigabyte WRX80 SU8-IPMI

![Image](https://images.openai.com/static-rsc-4/y1XJtejCAelzyjAMYQ4x7XJaf9NGt-l_YPEmoL0IY-HL2SfogWqKChOmZ1pkhRCaUw0g6fUm8rJkd3ZNzWcOV5DxuM4v3Dv5WsxIH9_MAoo-5idEdwh_qjKx4uzYt1l2qupWQbrYAUnNhVXkJI44MjO7fAcq5yQdilaV2CKehSzrdkfD-gbsRsJj5eUswzPo?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/vvVknn1dleu_xkBY8z34NjYaG6CpzNjeJSFH0VgiqmHAywQiqB1ixoDe-3-X-ni88pPe_AZmKlD0Wx6_x90WzEBTAmJLpqSR-k264qoRf5bt2LpBKDHJncB0VWt-vEyvAmIRlWjed2nodvMfPuvQi1STgCljU2YfsTnHCqsDjQDXnv1tyrNuKuny4ALrN4nu?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/kuxiKRdy2YfrZW0mETG49g7fGX6DTQVas8Acx9SFRykDTvP2SJg7R5oCMwmczJhkR83eNXjDDwn4EI8OqQHwXsIFfHMtueVH3A53xWtQhdgU25vCnya7hfpbNPho5rsc4ix5JbK3aEfWFEipuDxngrLFObfGa_wnDqN8ZQ7Euk935drD1Nd-QSwp8xqjG3z_?purpose=fullsize)

与普通 Ryzen 主板的主要区别：

| 特性         | Ryzen AM5 主板 | Threadripper Pro 主板 |
| ------------ | -------------- | --------------------- |
| CPU 插槽     | AM5            | sWRX8 / sTR5          |
| CPU 核心数   | 最多 16 核     | 最多 96 核            |
| 内存         | DDR5 UDIMM     | DDR4/DDR5 RDIMM ECC   |
| 内存通道     | 2              | 8                     |
| 最大内存     | 约 192GB       | 1TB+                  |
| PCIe 通道    | 约 28-32       | 128 条 PCIe 通道      |
| GPU 支持     | 1-3 块 GPU     | 可支持 4-8 块 GPU     |

示例：

Threadripper PRO 7995WX：

* 96 个 Zen 4 核心
* 192 线程
* 8 通道 DDR5 ECC RDIMM
* 128 条 PCIe 5.0 通道

适用于：

* AI 工作站
* 3D 渲染
* CAD
* 科学计算
* 多 GPU 配置

针对 AI 场景：

一台 Threadripper Pro 机器可以这样配置：

```
Threadripper PRO 7995WX
          |
          |
     WRX90 主板
          |
   +------+------+------+
   |      |      |      |
 RTX4090 RTX4090 RTX4090 RTX4090
```

由于拥有大量 PCIe 通道，你可以让多块 GPU 以全带宽运行。

对比你当前的配置：

```
i9-13900KF
MSI B760
RTX 4070
```

你拥有：

* 在 GPU 和存储共享后仅有 8 条 PCIe 通道可用
* 双通道内存
* 消费级平台

Threadripper Pro 完全是另一个级别。

对于 LLM 训练/推理：

* 1× RTX 4090 → 普通发烧友
* 2-4× RTX 3090/4090 → Threadripper Pro 开始有意义
* 4-8× GPU → Threadripper Pro / EPYC 的领域

缺点：

* 主板：通常 ¥5,000-10,000+
* CPU：¥10,000-50,000+
* 需要 ECC RDIMM 内存
* 功耗巨大

对于单人 AI 实验室（OPL），二手 Threadripper Pro 3955WX/3975WX + 便宜 RTX 3090 实际上可能很有趣，因为 PCIe 通道解决了多 GPU 瓶颈。
