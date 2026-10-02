---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ASUS Z170-P i3-6100 套装介绍
translated: true
type: note
---

问题：介绍这款华硕 Z170-P + i3-6100 主板套装。

答案：

华硕 Z170-P 是 Skylake 时代（2015–2016）的一款中端 Intel Z170 芯片组主板。该套装包含一颗 Intel Core i3-6100 CPU。

![Image](https://images.openai.com/static-rsc-4/iplQ9I4jlH7ekXSf8-dpMWsjazySl_d-WO8fjh7DthAeuuYYSQ88D8zFkJ9HsZ6rr-ll5hPsmIvBtOWWldPDGJy_NvEcmNXO2n0z5HMoQ6H5Yn4b6aAe4lbvKrQQQkOzt9aAseU6GWHjN1wdlhwVWqaD4V139ygTeGXrQw8ugX4Q1m7hcBeDbBO2ytVoz2Tq?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/dwS6bprg4lsBQb3iiVU41YhEwbR3BGn5l7Eyi2WGP3sNc1y7HY7sMXfxsF2ECG8YNvUPQjyXEvB8zPjshDSsCV3TY5DuqME0VpHqIuDFcKhMi-L-p1tn1jCg1tmTePidAMengO1xWRScNBdp35y-Qu67b-m9O9xsyO8CHvpVUNyh4rZCWN4qcO_Op7GfszJp?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/3aymNS2M6gxCn0p_opGKTidq3j8XsO3u7ObHdgC0WGEtHbBq7-SEtRP_jQ5v_BYxkeSlP15naT02mA1uvoLQt-8nRNOxWc_v392h_b_wooZBZsHQxLo7nt2Gkmq_6BgA-pTcRk8WCRPxtsPjYNq-dR5bd1Od2qrE2-1IXC0JsGHhMOyizL47MdBbB6-tGOWJ?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/lNnIOdqzs-5UPbZTr9pw_MaeW9GOpAaYCEnHGWBcdZGF_iEwdG9RI_QjlRyDpK0Bjx9ApdjPqJpnjguRcDEfwr7WkYVSqJykohU1UzK3uUHX-NbNB6ZCNYUIN0uB-hDI-zb1nnbuMRiuPZK37VF8umBwYTFKRqMTsdVLDBh9hsfCaddRipj3ZvUtuklwuvLM?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Of0CX7AgcZ0H1bBZci6gTf6Mc_cE3u4l5b3yRZyN1km-ZXhhMXyYQ1UUrX7DYi9tP3QCXX3TKlOROVeP70ghd12lP9kn4L_NB-e5Y-bD7L5BPn9h4XrAJViWOwLw67eRuJWR23x335ZWIB1bPjbWLNoBZ--NWnXN6QNmFXLv5bVpUBPAWnpffKw8pcXduSro?purpose=fullsize)

### 1. 主板：华硕 Z170-P

主要规格：

* **CPU 插槽：** LGA 1151
* **芯片组：** Intel Z170
* **CPU 支持：**

  * 官方支持第 6 代 Intel Core（Skylake）
  * 部分第 7 代 Kaby Lake CPU 需更新 BIOS 后支持
* **内存：**

  * 4 × DDR4 DIMM 插槽
  * 通常最高支持 64GB DDR4
  * 支持 XMP 内存超频
* **扩展插槽：**

  * 1 × PCIe 3.0 x16（显卡插槽）
  * 其他 PCIe 插槽用于扩展卡
* **存储：**

  * M.2 插槽（支持 PCIe 3.0 x4 NVMe）
  * SATA 6Gb/s 接口
* **显示输出：**

  * HDMI
  * DVI
  * VGA
    （仅在使用 Intel 核显时有用）
* **网络：**

  * 千兆以太网
* **USB：**

  * 支持 USB 3.0

Z170 芯片组实际上比 H110/B150 定位更高，因为它支持：

* 搭配带 K 的解锁 CPU 进行 CPU 超频
* 内存超频
* 更多 PCIe 通道

Z170-P 本身是 Z170 中的入门级主板，不像华硕 Z170 Pro Gaming 那种发烧友主板，但它仍然是一个扎实的平台。

---

### 2. CPU：Intel Core i3-6100

规格：

| 项目 | 规格 |
| ------------ | --------------------- |
| 架构 | Skylake |
| 核心 | 2 |
| 线程 | 4 |
| 基础频率 | 3.7 GHz |
| TDP | 51W |
| 核显 | Intel HD Graphics 530 |
| 插槽 | LGA1151 |

如今性能表现：

* 办公 / 浏览网页：可以
* Linux 服务器：可以
* NAS / 软路由：可以
* 轻度编程：可以
* 较老的游戏：可以
* 现代 AI 工作负载：不适用

CPU 是整套的短板。主板可以支持强得多的 CPU：

可升级选项：

* i5-6500 / i5-6600
* i7-6700
* i7-7700（需更新 BIOS）
* i7-6700K / i7-7700K（超频取决于主板 BIOS）

---

### 3. 用于 GPU 实验 / AI 实验室

由于你经常关注老显卡，这个平台很有意思：

优点：

✅ PCIe 3.0 x16
✅ DDR4 平台
✅ M.2 NVMe
✅ 替换零件便宜
✅ 支持较老的 NVIDIA 显卡

但限制：

* CPU 只有 16 条 PCIe 通道
* 没有 PCIe 4.0/5.0
* 官方不支持 Resizable BAR（ReBarUEFI 有时有帮助）
* i3-6100 作为 GPU 计算的主机 CPU 较弱

对于这些显卡：

* GTX 1060/1070/1080 → 没问题
* RTX 3060 → 没问题
* RTX 3090 → 能用，但 CPU 会是瓶颈
* Tesla P100/M40 → 可能可以，但可能遇到 BIOS/PCI 资源问题

---

### 4. 二手市场价值（中国二手市场）

2026 年大致价格：

* 华硕 Z170-P 主板：约 150–250 元
* i3-6100 CPU：约 50–100 元

套装合理价格：

* **200–300 元：** 划算
* **300–400 元：** 如果成色好且测试过可接受
* **>400 元：** 不划算

对于显卡维修/测试平台来说，这个平台其实比便宜的 H110 更有用，因为 Z170 提供更多 BIOS 选项和 PCIe 灵活性。

与你之前问的 MSI Z170A SLI PLUS 相比，华硕 Z170-P 是一块更入门的板子：

* Z170-P：基础款 Z170，供电相数更少，扩展功能更少
* Z170A SLI PLUS：VRM 更好，PCIe 插槽更多，更适合多显卡实验

对于**显卡维修工作台 + 老款 Tesla/Pascal 显卡测试**，如果价格差距不大，我更倾向于选择 Z170A SLI PLUS。如果只是要一台便宜的日常测试机，这款华硕套装也完全可以。
