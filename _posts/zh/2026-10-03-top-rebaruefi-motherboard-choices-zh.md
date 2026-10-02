---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 最佳 ReBarUEFI 主板选择
translated: true
type: note
---

问题：我应该选择**ReBarUEFI测试主板列表**中的哪一款主板？

回答：

是的，您指的是ReBarUEFI Wiki / Issue #11中的**“测试主板列表”**。它包含了用户实际测试过的主板、GPU、BAR大小以及是否需要UEFIPatch的信息。（[GitHub][1]）

针对您的目标（便宜的闲鱼主板 + RTX 3090/M40/P100实验 + 4G解码 + CSM控制），我会这样筛选该列表：

## 列表中的最佳选择

### 1. 华硕 Z170-P ⭐⭐⭐⭐⭐

来自列表：

```
ASUS Z170-P
GPU: RTX 3090
BAR: 32GB
UEFIPatch: Y
```

（[GitHub][2]）

原因：

* 二手市场价格便宜
* DDR4
* M.2接口
* 华硕BIOS易于操作
* 有很大概率找到“Above 4G Decoding”选项
* 适合您的i7-6700 / Xeon E3-1280 v5方案

这大概是我会优先购买的主板。

---

### 2. 华硕 Z170-A ⭐⭐⭐⭐⭐

来自列表：

```
ASUS Z170-A
GPU: RX 5700 XT / RTX 3080 / Arc A750
BAR: 8GB-16GB
UEFIPatch: Y
```

（[GitHub][2]）

与Z170-P类似，但规格稍高。

优势：

* 更好的供电模块
* 更多扩展接口
* 更多发烧友用户 → 更容易获取BIOS信息

---

### 3. 华硕 X99-DELUXE II ⭐⭐⭐⭐⭐（AI实验室选择）

来自列表：

```
ASUS X99 DELUXE II
GPU: RTX 3090
BAR: 24GB
UEFIPatch: Y
```

（[GitHub][2]）

对于您的AI GPU实验来说，这个其实非常有意思：

```
Xeon E5 v4
+
ECC DDR4
+
RTX 3090
+
Tesla卡
```

优势：

* 众多PCIe通道
* 四通道内存
* 更好的多GPU平台

---

### 4. 华南金牌 X99-QD4 ⭐⭐⭐⭐（廉价国货选项）

来自列表：

```
Huananzhi X99-QD4
RTX 3060
BAR:16GB
UEFIPatch:N
```

（[GitHub][1]）

有趣之处在于：

* 无需BIOS补丁
* 价格便宜
* 容易买到

但BIOS质量不如华硕级别。

---

## 即使出现也应避免的主板

针对您的需求：

* 需要DSDT补丁的Z97主板
* 除非非常便宜，否则避免老旧X79主板
* 随机的H61/B75主板

这些也能用，但您会花时间处理PCI资源问题。

---

我的推荐排序：

```
AI GPU实验室：
1. 华硕 X99-DELUXE II
2. 华硕 Z170-P
3. 华硕 Z170-A

廉价实验：
1. 华硕 Z170-P
2. 华南金牌 X99-QD4
3. 微星 Z170A Gaming M5
```

针对您之前P100/M40遇到的**PCI资源不足**问题，我尤其推荐**华硕 Z170-P / Z170-A**，因为它们的BIOS选项通常更清晰：

```
Advanced
 └── PCI Subsystem Settings
      ├── Above 4G Decoding  [Enabled]
      └── Re-Size BAR Support [Enabled]

Boot
 └── CSM
      └── Launch CSM [Disabled]
```

ReBarUEFI列表证实Z170-P、Z170-A和X99主板确实有成功的大BAR测试案例。（[GitHub][2]）

[1]: https://github.com/xCuri0/ReBarUEFI/wiki?utm_source=chatgpt.com "Home · xCuri0/ReBarUEFI Wiki · GitHub"
[2]: https://github.com/xCuri0/ReBarUEFI/issues/11?utm_source=chatgpt.com "List of working motherboards · Issue #11 · xCuri0/ReBarUEFI · GitHub"
