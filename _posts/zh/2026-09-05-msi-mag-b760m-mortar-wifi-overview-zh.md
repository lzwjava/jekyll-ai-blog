---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MSI MAG B760M MORTAR WIFI 概述
translated: true
type: note
---

![Image](https://images.openai.com/static-rsc-4/i_SjU_1AhCST0vxGq5qFs_w89wnke-MeO5dVy_A_nwqBf2Xo_u0IO77LBldyySUEg9Alcx6y6rKp5lkBWidaiFsTWjcSekQj9Nurj-0ss_9320QAjsp1nKyYrspKdI6BWrlmR5kZF_hvmhHzy5j-EL1MYUMTbsaSb1cgQn71fXpP-OImgz5TbAdMhvuewVTx?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/ezsGDKN_q-RXa6QxJaQ5kPmRjTQi84jSJCIolkYHTPkUrOnWnGpCuv52EjHvL9fJTxy1VbKVJBNuWAZghKk4kDRWYjeVEOR4ar2fwOWX7HF02mc0g81AunOU98av9JcMBQi_U8RwODlMih2KKvv0gDTTOgd5Eqaap1GAMzc3IUnuH16pg444kXh1EuQv902M?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/ljaCxS9Qh3OUuCZig4mGcQM_fQWKj_-_5jn0ZKuYLWCmdvi_u7UU0py0zcmBCDTNYSjaTzI73qvyLz7ddTWMtcxYVnYC9g-xHB98kh2WZKTaDTFZt_J66vRpcVGq_ITMulV4RX6KJzqmguCATnHxNhtr6kEVXiKJlNjnmhm7EhEyxUdM-e9Z6KrVRSYIgRoi?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/AFHdVs1dhsjsSEHjuA9ezNdqmWYBoYCTFs4SE68Q2U4HUBf6gEA_SURHeJdIZMMy2aNbX73GNnEj1kpKjRGEDfzC3XoMs-B_3VddzkemdSV1-zyXrD72-CW37T2__oMFTgsHFT7MfKngDWhdSmviFox5wAKKdo6O5W3wmhgd70MHwevF96tCMKc4XBruCJF1?purpose=fullsize)

**MSI MAG B760M MORTAR WIFI** 是一款相当高端的 **mATX Intel LGA1700 主板**。对你来说它特别有吸引力，因为相比廉价的 H610/B660 主板，它为 **GPU 测试 / 多 PCIe 设备 / 硬件实验** 提供了更好的平台。

[MSI 官方规格](https://www.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI/Specification?utm_source=chatgpt.com)

### 核心规格

| 部件            | 规格                                  |
| --------------- | ------------------------------------- |
| 板型            | **mATX，243.84 × 243.84 mm**          |
| 芯片组          | **Intel B760**                        |
| CPU 插槽        | **LGA1700**                           |
| CPU             | 第12/13/14代 Intel                    |
| 内存            | **4× DDR5**，最高 256 GB              |
| GPU 插槽 1      | **来自 CPU 的 PCIe 5.0 x16**          |
| GPU 插槽 2      | **来自芯片组的 PCIe 4.0 x4**          |
| 小型插槽        | PCIe 3.0 x1                           |
| M.2             | **2× PCIe 4.0 x4**                    |
| SATA            | **4× SATA 6 Gb/s**                    |
| 有线网络        | **2.5 GbE**                           |
| 无线网络        | **Wi-Fi 6E + 蓝牙 5.3**               |
| USB             | 最高 **USB 3.2 Gen 2x2 20 Gb/s**      |
| VRM             | **12+1+1** 供电设计                    |
| PCB             | **6 层，2 oz 铜**                      |

MSI 官方列出了 4 个 DDR5 DIMM 插槽、最高 256 GB 内存以及 PCIe x16/x4 扩展配置。（[MSI USA][1]）

---

## 1. 对你 GPU 实验重要的部分

这可能是一个最有趣的特点：

```text
CPU
 │
 ├── PCIe 5.0 x16 ─────────── GPU #1
 │
 └── DMI
      │
      └── B760 芯片组
           ├── PCIe 4.0 x4 ─── GPU #2
           ├── PCIe 3.0 x1
           ├── M.2 #2
           ├── SATA
           ├── USB
           └── LAN/WiFi
```

主插槽是 **PCIe 5.0 x16**，而第二个全长插槽是 **PCIe 4.0 x4**。（[MSI USA][1]）

因此你可以物理安装类似这样的配置：

```text
RTX 4070
    ↓
PCIe 5.0 x16 插槽

GT 730 / Quadro / 测试 GPU
    ↓
PCIe 4.0 x4 插槽
```

这使得它作为 **GPU 维修/测试平台** 非常有用。

但有一个重要区别：

**第二个插槽物理上是 x16，但电气上只有 x4。**

这对于测试 GPU 是否枚举、驱动测试、显示输出、诊断等来说完全合理。但它不等同于拥有两个连接到 CPU 的 x16 插槽。

---

## 2. CPU 支持

它采用 **LGA1700**，因此以下 CPU：

```text
i3-12100
i5-12400
i5-12600K
i5-13400
i5-13600K / KF
i7-13700K / KF
i9-13900K / KF
i5-14600K
i7-14700K
i9-14900K
```

都在其兼容范围内。

MSI 当前的规格也列出了对第 14 代的支持，尽管该产品最初是在第 12/13 代时推出的。（[MSI USA][1]）

对于 GPU 测试平台，我实际上更推荐类似：

**i5-12400 / i5-13400**

而不是把钱花在 i9 上。

你不需要一个 300 W 的 CPU 仅仅用来测试 GPU 是否能工作。

---

## 3. DDR5

有 **四个 DIMM 插槽**：

```text
A1   A2   B1   B2
│    │    │    │
└────┴────┴────┴── DDR5
```

官方标称最大容量为 **256 GB**。

它支持 DDR5 最高约 **7200+ MT/s（通过超频/XMP）**，而标准 JEDEC 速度要低一些。（[MSI USA][1]）

对于实用型工作站：

```text
2 × 32 GB DDR5
= 64 GB
```

已经非常好了。

对于你的 AI 工作：

```text
2 × 32 GB
或
2 × 48 GB
```

会比追求 7200 MT/s 更有用。

---

## 4. 存储

包括：

```text
M.2 #1 ── PCIe 4.0 x4 ── CPU
M.2 #2 ── PCIe 4.0 x4 ── B760
```

以及：

```text
4 × SATA 6 Gb/s
```

因此你可以拥有：

```text
NVMe SSD #1
NVMe SSD #2
SATA SSD/HDD × 4
```

MSI 还提供了 M.2 Shield Frozr 散热片。（[MSI Storage][2]）

对于你的模型训练机器，两个 NVMe 驱动器很方便：

```text
SSD #1 → 系统 / 代码 / 环境
SSD #2 → 数据集 / 检查点
```

---

## 5. 对于 B760 主板来说，网络配置出奇地好

你得到：

**Realtek 2.5 GbE**

以及：

**Intel Wi-Fi 6E + 蓝牙 5.3**。（[MSI USA][1]）

对于你的工作负载，如果你有以下配置，2.5 GbE 实际上非常有用：

```text
GPU 工作站
      │
  2.5 GbE
      │
NAS / 服务器
```

而不是依赖 1 GbE。

---

## 6. 后置 I/O

后置面板大致提供：

```text
USB 2.0
DisplayPort
USB 10 Gb/s
2.5G 以太网
Wi-Fi 天线
音频
HDMI 2.1
USB-C 20 Gb/s
S/PDIF
```

HDMI/DP 输出来自 **CPU 的集成显卡**，因此像 i5-12400F 这样的 `F` 版本 CPU 无法使用这些主板视频输出。（[MSI USA][1]）

在搭建测试平台时值得记住这一点。

例如：

```text
i5-12400     → 主板 HDMI/DP 正常工作
i5-12400F    → 主板 HDMI/DP 无画面
```

---

# VRM / 供电

这是 MORTAR 比廉价 B760 主板好得多的原因之一。

MSI 指定了 **12+1+1** 供电设计、双 8-pin CPU 电源接口、大型散热片以及 6 层 2 oz 铜 PCB。（[MSI][3]）

物理结构大致为：

```text
             CPU
              │
        ┌─────┴─────┐
        │   VRM     │
        │ 12+1+1    │
        └───────────┘
              │
          DDR5 DIMMs

PCIe GPU ────────────────
```

对于 i5/i7 级别的 CPU 来说，它绰绰有余。

然而，对于 13900K/14900K 这样的 CPU，**CPU 本身** 才是散热/功耗的难题——而不是这块主板能否启动它。

---

# 为什么 MORTAR 对你很有吸引力

我大致评分如下：

| 方面               | 评分    |
| ------------------ | ------: |
| GPU 测试           |  ⭐⭐⭐⭐⭐ |
| AI 工作站          |  ⭐⭐⭐⭐½ |
| CPU 性能平台       |  ⭐⭐⭐⭐⭐ |
| 扩展性             |   ⭐⭐⭐⭐ |
| 网络               |  ⭐⭐⭐⭐⭐ |
| 存储               |   ⭐⭐⭐⭐ |
| 性价比             |    ⭐⭐⭐ |
| mATX 紧凑性        |  ⭐⭐⭐⭐⭐ |

关键组合是：

```text
mATX
+
PCIe 5.0 x16
+
PCIe 4.0 x4
+
4× DDR5
+
2× NVMe
+
2.5GbE
+
Wi-Fi 6E
+
强劲 VRM
```

这是一块 **非常优秀的小板**。

---

# 但关于你的 ¥1,299 价格

这需要谨慎对待。

现在的 **MAG B760M MORTAR WIFI** 已经是较老的 LGA1700 代产品了。MSI 当前的官方网站仍然列出它，但更新的 **MORTAR WIFI II** 也存在。（[MSI][3]）

目前中国市场上的报价显示较新的 **B760M MORTAR WIFI II** 大约在 **¥1,199–1,299**，而原版 MORTAR WIFI 根据卖家不同也可能出现在这个价格附近。（[MSI Store][4]）

因此：

**今天来看，¥1,299 购买原版 MORTAR WIFI DDR5 并不特别划算。**

我需要区分：

```text
原版 B760M MORTAR WIFI
        ↓
    好板子
        ↓
   ¥1,299 = 偏贵


B760M MORTAR WIFI II
        ↓
新版本 / 3× M.2
        ↓
~¥1,199–1,299
        ↓
更有吸引力
```

例如，WIFI II 有 **3 个 M.2 插槽**，而原版只有 2 个。（[MSI][5]）

### 针对你的特定用途

如果你购买这块主板主要是为了 **GPU 维修/测试平台**，我实际上会寻找 **二手/拆机版 MORTAR，价格约 ¥500–800**，而不是花 ¥1,299。

在 ¥1,299 这个价位，我会首先与更新的 B760/B860/AM5 主板进行比较。

[MSI MAG B760M MORTAR WIFI 官方页面](https://www.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI?utm_source=chatgpt.com)

我还可以为你画出 **在这块主板上搭建双 GPU 维修/测试平台时，应该使用哪个 PCIe 插槽、M.2 插槽、内存插槽、CPU 电源接口、F_PANEL 以及风扇接口**。

[1]: https://us.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI/Specification?utm_source=chatgpt.com "MAG B760M MORTAR WIFI"
[2]: https://storage-asset.msi.com/datasheet/mb/cn/MAG-B760M-MORTAR-WIFI.pdf?utm_source=chatgpt.com "主板
MAG B760M MORTAR WIFI
U N I T E  A S  O N E
FEA"
[3]: https://www.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI?utm_source=chatgpt.com "MAG B760M MORTAR WIFI"
[4]: https://store.msi.cn/?utm_source=chatgpt.com "微星商城msi-微星笔记本电脑、主板、显卡，官网直营商城，正品有保障"
[5]: https://www.msi.cn/Motherboard/MAG-B760M-MORTAR-WIFI-II?utm_source=chatgpt.com "MAG B760M MORTAR WIFI II"
