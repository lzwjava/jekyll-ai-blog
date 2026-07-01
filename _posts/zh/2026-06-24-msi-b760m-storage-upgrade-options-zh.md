---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MSI B760M存储升级选项
translated: true
type: note
---

**问题：** 对于所述工作站（MSI MAG B760M Mortar WiFi，当前配备1TB NVMe SSD + 2TB HDD），将存储升级到2TB以上的最佳方案是什么？

**回答：**

你当前的存储情况：

- **1TB Samsung 980**（PCIe 3.0 x4 NVMe，M.2插槽1）
- **2TB WD Blue HDD**（SATA）
- 总容量：约3TB（原始）

---

## MSI MAG B760M Mortar WiFi 有哪些可用插槽

这款mATX主板拥有：

| 插槽 | 类型 | 状态 |
| ------ | ------ | ------ |
| M.2_1 (Key-M) | PCIe 5.0 x4 / PCIe 4.0 x4，NVMe | 可能被Samsung 980占用 |
| M.2_2 (Key-M) | PCIe 4.0 x4，NVMe | **空闲** |
| M.2_3 (Key-M) | PCIe 4.0 x4 / SATA | **空闲** |
| SATA接口 | 6× SATA 6Gb/s | 1个被HDD使用，5个空闲 |

你有 **两个空闲M.2插槽** 和 **5个空闲SATA接口**。空间充足。

---

## 升级选项

### 选项1：添加另一块NVMe M.2 SSD（性能最优）

在M.2_2插入一块2TB或4TB Gen4 NVMe。

**推荐：**

| 型号 | 容量 | 速度 | 价格（CNY） |
| ------- | ---------- | ------- | ------------- |
| Samsung 990 Pro | 2TB | 7,450/6,900 MB/s | ~799 |
| WD Black SN850X | 2TB | 7,300/6,600 MB/s | ~749 |
| Crucial T500 | 2TB | 7,400/7,000 MB/s | ~599 |
| Crucial T500 | 4TB | 7,400/6,500 MB/s | ~999 |

对于ML/AI工作负载（数据集、检查点），**在M.2_2上添加4TB Gen4**是性价比最高的单一升级。

### 选项2：添加更多SATA HDD（适合大量冷数据存储）

你有5个空闲SATA接口，且Aigo机箱通常可容纳2–3块3.5英寸硬盘。你已经拥有SATA线。

| 型号 | 容量 | 价格（CNY） |
| ------- | ---------- | ------------- |
| WD Blue 4TB | 4TB | ~499 |
| Seagate Barracuda 4TB | 4TB | ~459 |
| WD Red Plus 4TB（NAS级） | 4TB | ~599 |

适用于存储训练数据集、模型权重、视频、备份。不适用于活跃的交换/缓存。

### 选项3：用更大的Gen4硬盘替换1TB Samsung 980

980是Gen3，而M.2_1支持Gen5/Gen4。将其更换为4TB Gen4可以让你在最好的插槽上使用最快的硬盘。然后将980作为副盘或出售。

---

## 针对你的使用场景的推荐路径

鉴于你运行ML训练（RTX 4070、数据集、检查点）：

1. **立即**：在M.2_2中添加 **Crucial T500 4TB PCIe 4.0**（约999 CNY）。速度足以在训练期间读取数据集，容量足够存放模型权重和检查点。
2. **后续**：在空闲SATA接口中添加一块 **4TB WD Blue HDD**（约499 CNY），用于冷归档存储——原始数据集、旧检查点、备份。

从约3TB升级到约11TB的总成本：低于1,500 CNY。M.2无需新线缆，且你已有SATA线。

---

## 需要检查的一件事

验证Aigo Yueguangbaohe Jing Mini机箱物理上是否能容纳第二块3.5英寸HDD——迷你机箱有时只有1–2个硬盘位。如果空间紧张，优先考虑M.2 SSD升级，因为它无需工具且不占用机箱空间。
