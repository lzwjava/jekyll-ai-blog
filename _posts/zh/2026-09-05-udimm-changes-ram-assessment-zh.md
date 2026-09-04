---
audio: false
generated: true
image: false
lang: zh
layout: post
title: UDIMM变化的内存评估
translated: true
type: note
---

## 问题：如果卖家说这是UDIMM，那评估结果会改变吗？

**答案：是的——会有很大变化。** 如果确实是 **UDIMM**，那么 `2Rx4` 并**不**自动意味着是RDIMM。

对于三星DDR3L：

* **PC3L** = DDR3L，通常为1.35V
* **2Rx4** = 2个rank，×4 DRAM组织结构
* **UDIMM** = 无缓冲DIMM
* **RDIMM** 通常会在模块规格中带有 `R`，例如 `PC3L-12800R`

因此像这样的标识：

```text
Samsung 8GB 2Rx4 PC3L
DDR3L
UDIMM
ECC? ← 重要
```

完全可能是合法的 **DDR3L ECC UDIMM**。

### 但有一点我需要核实

请向卖家索要 **印在贴纸上的三星具体型号**，例如：

```text
M391B1G73BH0-YK0
M378B1G73DB0-YK0
...
```

型号能准确告诉我们它是：

```text
UDIMM / RDIMM
ECC / 非ECC
DDR3 / DDR3L
1333 / 1600 MHz
```

**¥160买2×8GB只有当你的主板支持该确切类型时才合理。** 对于普通DDR3L非ECC UDIMM，我认为¥160略高；对于ECC UDIMM，兼容性则是主要问题。

如果你上传 **内存条贴纸的照片**，我可以在你购买前解码出具体型号。
