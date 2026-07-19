---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 华硕TUF Z790主板概览
translated: true
type: note
---

**问题：华硕 TUF GAMING Z790-PLUS WIFI 主板简介**

华硕 TUF GAMING Z790-PLUS WIFI 是一款基于英特尔 **Z790 芯片组**的**高端消费级 ATX 主板**，主要面向**第 12/13/14 代英特尔酷睿处理器**（Alder Lake / Raptor Lake / Raptor Lake Refresh）。

![Image](https://images.openai.com/static-rsc-4/DFmrk__nwKEbgYNhfdILQU9zhIXgaQLlb1CdCm3cQY-KF_kNjHJt3gSb3IjTlElgRla4BRgfj2GIcLKwRlqIVGSlcgruK3McyD_I6C8tQY383BXsf8miIXEKA8SMaj-5SqDa1Y4TZPQuYJg61RiIuJR4LdFIUHF6pv9s2wdcXUNz6WaGTjSBeqDUb906ZPHX?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/5P6jSxAxYHdsqLUZLlep0vQUwF-Od5rxHNLX6ZjxWG2HJZAiV5fvV7xsIuMkeJqba8AzMK8uByf8GouTbxvzJceNnEI0zOz8sU19rQkmoFyWBU8mdsoQW1x07SmG7Ou7R-rabX784JpO5qnXYAxb2MOvJJRMMrTEQf7LZEUMNwlTrGNqDtmrr1_OiWk0fenb?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/roXiiHcBRiOEbz2JBusvS5IySBkYPXzwqo8PRAe3OPLTPqj0bvdhMUpvqqBGh_AlnoSW4R0VX-oJQGs9Jr_s2ylbIhjsj0Wj--iQZ34JFduGoiOdAzMttnVnCI_FiNaLNiKXJG8WSRB9NK7ZtJAEPPMinwFSpfhInBHB4RiPfoRchrzznKNz0g0TE6k3PuyM?purpose=fullsize)

## 主要规格

| 特性         | 详情                                |
| ------------ | ----------------------------------- |
| CPU 插槽     | LGA1700                             |
| CPU 支持     | 英特尔第 12/13/14 代 Core           |
| 芯片组       | 英特尔 Z790                         |
| 板型         | ATX                                 |
| 内存         | 4 × DDR5 DIMM                       |
| 内存容量     | 最高 192GB DDR5（使用 48GB 模块时） |
| PCIe 显卡插槽 | PCIe 5.0 x16                        |
| M.2 存储     | 多个 M.2 NVMe 插槽（PCIe 4.0）     |
| 网络         | 2.5Gb 以太网                        |
| 无线         | WiFi 6 + 蓝牙                       |
| VRM          | 带散热片的强劲供电设计              |
| BIOS         | UEFI，支持 CPU 升级                 |

---

## 为什么 Z790 重要

英特尔主板层级：

```
H610
  |
B660/B760
  |
Z690/Z790  <--- 面向发烧友
```

关键区别：

* **B760**：
  * 不支持 CPU 超频
  * PCIe 通道数较少
  * 价格更低

* **Z790**：
  * 支持 CPU 倍频超频
  * VRM 更强
  * 扩展性更好
  * 更适合 i7/i9

对于以下处理器：

* i5-13600K
* i7-13700K
* i9-13900K
* i9-14900K

Z790 是合理的搭配。

---

## VRM / 供电

"供电稳"部分意味着主板拥有更强的 VRM 设计。

例如：

```
电源 12V
 |
VRM
 |
CPU 电压 ~1V
 |
CPU 核心
```

一颗 13900K 可消耗：

* 普通游戏：约 100-150W
* 重负载全核：250W+

弱主板可能会出现降频。而 TUF Z790 能更好地支持这些处理器。

---

## 针对你的 RTX 3090 / 双显卡设想

这块主板很有意思，但请注意：

### PCIe 布局

通常：

```
CPU PCIe 通道：

显卡插槽 1：
PCIe 5.0 x16

芯片组：
PCIe x4 通道
 |
M.2
 |
其他 PCIe 插槽
```

第二块显卡通常运行在：

```
显卡1：PCIe 5.0 x16
显卡2：PCIe 4.0 x4
```

因为消费级英特尔 CPU 只有：

```
CPU：
16 条 PCIe 通道用于显卡
4 条 PCIe 通道用于 NVMe

总计：
20 条 PCIe 通道
```

不像服务器平台：

```
Threadripper：
64+ 条 PCIe 通道

EPYC：
128+ 条通道
```

所以对于：

* 单块 RTX 3090 ✅
* RTX 4090 + NVMe ✅
* RTX 3090 + 另一块显卡 ⚠️ 受限

---

## 与你现有的 MSI MAG B760M Mortar WiFi 对比

你之前的这块主板：

MSI MAG B760M Mortar WiFi

本身其实已经是一块非常出色的主板了。

区别：

|            | MSI B760M Mortar | 华硕 TUF Z790 |
| ---------- | ---------------- | ------------- |
| 尺寸       | mATX             | ATX           |
| DDR5       | 支持             | 支持          |
| CPU 超频   | 不支持           | 支持          |
| PCIe 通道  | 较少             | 更多          |
| 扩展性     | 中等             | 更好          |
| VRM        | 良好             | 更强          |
| 双显卡     | 受限             | 略好          |

针对你的使用场景：

* GPT 训练
* RTX 3090
* 本地 LLM 推理
* PyTorch

主板本身**并非性能瓶颈**。

主要限制在于：

1. 显存
2. PCIe 带宽
3. 电源供应
4. 散热

---

## 二手市场价值

一块二手的 TUF Z790-PLUS WIFI 是比较合理的选择，因为：

* DDR5 平台
* 支持 13900K/14900K
* ATX 提供更多空间
* 良好的转售价值

但我不会为了它而支付远超 B760 的溢价。

对于 AI 工作站：

```
B760 + RTX3090
        |
        |
        v
相同的模型训练速度

Z790 + RTX3090
```

计算工作由 GPU 完成。

---

针对你的情况（目前使用 i9-13900KF + RTX 4070，考虑升级 RTX 3090/双显卡），**升级到 Z790 的主要原因不是性能，而是物理扩展空间和 PCIe 布局**。如果你想要 2×3090，即使是 Z790 也不理想——这时你需要考虑 **Threadripper / 工作站平台**。
