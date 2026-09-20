---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Z97-K R2.0 兼容CPU
translated: true
type: note
---

**问题：** 华硕 Z97-K R2.0 主板支持哪些 CPU？

**回答：**

华硕 Z97-K R2.0 采用 **LGA1150 插槽**，搭载 Intel Z97 芯片组，支持以下 CPU：**问题：** 华硕 Z97-K R2.0 支持哪些 CPU？

**回答：**

根据华硕官方 Z97-K CPU 支持列表，该主板通过 LGA1150 插槽支持以下处理器系列：

---

### 🟢 Intel Core（第 4 代 — Haswell）

- **Core i7：** i7-4765T、i7-4770、i7-4770K、i7-4770S、i7-4770T、i7-4771、i7-4785T、i7-4790、i7-4790K、i7-4790S、i7-4790T
- **Core i5：**（完整系列，同代）
- **Core i3：** i3-4130、i3-4130T、i3-4150 等

---

### 🟢 Intel Core（第 5 代 — Broadwell，需更新 BIOS）

- **Core i5-5675C**（3.1GHz，65W）— 需要 BIOS 2604 或更高版本，以及 VGA 驱动 10.18.14.4206 或更高版本
- **Core i7-5775C**（3.3GHz，65W）— 相同的 BIOS 要求

---

### 🟢 Intel Pentium（Haswell）

- G3220、G3220T、G3240、G3240T、G3250、G3258、G3260、G3420、G3430、G3450、G3460、G3460T、G3470

---

### 🟢 Intel Celeron（Haswell）

- G1820、G1820T、G1830、G1840、G1840T、G1850

---

### 🟡 Intel Xeon E3 V3（支持但有限制）

- Xeon E3-1220 V3、E3-1220L V3、E3-1231 V3 — 支持，但“安装到 8 系列芯片组上时部分功能可能无法使用”，因为 Xeon 处理器专为服务器平台设计

---

### 总结

| 类别 | 最佳选择 | 备注 |
|---|---|---|
| 顶级性能 | i7-4790K（4.0GHz） | Devil's Canyon，此主板最佳 |
| 最佳性价比 | i5-4460 / i5-4590 | 稳定的四核，二手价格实惠 |
| 入门级 | Pentium G3258 | 倍频解锁，可超频 |
| Broadwell 升级 | i7-5775C | 需要 BIOS 2604+，稀有且昂贵 |

---

**参考资料：**
- [华硕 Z97-K CPU 支持列表（官方）](https://www.asus.com/supportonly/z97k/helpdesk_cpu/)