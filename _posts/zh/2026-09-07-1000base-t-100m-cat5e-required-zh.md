---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 1000BASE-T 100米 Cat5e 要求
translated: true
type: note
---

**问题：** 1000BASE-T的最大有效传输距离是多少，它使用的是Cat 5还是Cat 5e UTP线缆？

**答案：**

**最大距离：100米（328英尺）**

当使用Cat 5e或更高级别的铜缆时，1000BASE-T的最大线缆长度为**100米（328英尺）**。该距离包括水平线缆走线*加上*两端跳线的长度。

---

**线缆类别——你猜对了，但实际正确答案是Cat 5e：**

你提到了Cat 5或Cat 5e——正确的最低要求是**Cat 5e**（而非普通Cat 5）。

- 虽然1000BASE-T*设计*用于Cat 5e线缆，但在理想条件下它*可能*能在高质量Cat 5线缆上工作。然而，Cat 5线缆无法提供千兆操作所需的性能余量，尤其是在较长距离或存在电磁干扰的环境中。为获得有保证的性能，**强烈建议使用Cat 5e或更高级别线缆**。

- 1000BASE-T通常使用的最低线缆是**Cat 5e**，与仅使用2对双绞线的100 Mbps以太网不同，**1000BASE-T需要使用双绞线线缆内的全部4对线**。

- 1000BASE-T也可以在Cat 6、Cat 6A、Cat 7、Cat 7A和Cat 8上运行——均遵循相同的100米限制。

---

**编码：** 4对双绞线中的每一对都使用**PAM-5**（5级脉冲幅度调制）承载250 Mbps，总计1 Gbps全双工。

---

**参考资料：**

- [1000BASE-T概述 – Ctools.org](https://ctools.org/detailed-overview-of-the-1000base-t-gigabit-ethernet-standard-on-copper-cabling/)
- [1000BASE-T布线 – Infinity Cable Products](https://infinity-cable-products.com/blogs/performance/how-many-cable-pairs-are-needed-for-1000base-t-transmission)
- [以太网标准 – Professor Messer](https://www.professormesser.com/professor-messer-archives/n10-007/ethernet-standards-3/)
