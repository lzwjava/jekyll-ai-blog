---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 了解ECT23和ECT24电容器
translated: true
type: note
---

现在画面清晰多了。以下是修正后的答案：

---

**问题：** Quadro 410 GPU 板上电容（820µF、2.5V）顶部的 ECT23 和 ECT24 是什么意思？

**答案：**

这些是 **NCC（日本贵弥功）** 生产的 **固态聚合物铝电解电容**。标记含义如下：

| 标记 | 含义 |
| --- | --- |
| **E** | 电压代码——NCC 系统中的“E”表示额定电压 **2.5V** |
| **CT** | **系列名称**——NCC 内部产品系列（类似 NCC 还使用的 PSE、PSA、PSC 等系列） |
| **23** | **电容代码**——在 NCC 的缩写格式中编码为 **820µF** |
| **24** | **第二行**——很可能是 **批次/日期代码** 或第二行标记（年份或批次） |

NCC 的固态聚合物电容系列（如 PSE、PSC 和 PSA）是超低 ESR、高纹波电流设计，额定电压 2.5V 至 16V，可在 105°C 下工作 15,000 至 20,000 小时。ECT 系列属于同一类导电聚合物铝固态电容。

**简单来说**，在 Quadro 410 板上：

- 该电容为 **820µF / 2.5V**，属于 **固态（非液态）聚合物电容**
- 它用于 **VRM（电压调节模块）** 中，位于 GPU 核心附近，用于平滑和稳定非常低的 GPU 核心电压（通常在 0.9–1.1V 范围内）
- **ECT** 只是 NCC 对该特定产品线的系列命名
- **23 / 24** 指代 NCC 编号系统中的批次/日期代码或电容编码

板上你看到的两个不同编号（ECT23 与 ECT24）仅表示同一 820µF / 2.5V 电容的 **不同生产批次或子型号**——在电气性能上是等效的。

**参考资料：**

- [Nippon Chemi-Con 产品目录（NCC 2020）](https://chemi-con.com/wp-content/uploads/2021/04/Nippon-Chemi-Con-Product-Catalogue.pdf)
- [NCC 分组图 – 铝电解电容](https://www.chemi-con.co.jp/en/products/aluminum/chart/)
