---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 损坏的CMP 170HX不值2500
translated: true
type: note
---

**问题：** **一块坏的 CMP 170HX 8GB（VBIOS 损坏，驱动无法安装）值 2500 元人民币吗？**

**回答：**

简短回答：**不，我不会花 2500 元买它，除非你能自己测试恢复。**
在 2500 元（约 350 美元）的价格下，只有当卖家允许退货，或者你拥有 SPI 编程器 + 相关经验时，才值得考虑。

CMP 170HX 的市场比较特殊，因为这块卡本质上是一个缩水的 GA100/A100 级加速器。它拥有 4480 个 CUDA 核心和 HBM2e 显存；社区的努力通过软件解锁了一些隐藏功能，使得能正常工作的卡变得有价值。([GitHub][1])

但具体到这块卡：

> "能认卡，驱动打不上，刷了vbios"

这是一个**高风险状态**。

## 价格分析

正常工作且规格为 8GB 的 CMP 170HX 的成交价大致为：

* 历史上矿卡约 200-500 美元 ([eBay][2])
* 解锁热潮后更高；部分标价/成交价要高得多 ([eBay][3])

对于一块**正常工作的**卡来说，2500 元（约 350 美元）可能是合理的价格。

但一块“VBIOS 损坏”的卡应该有很大的折扣。

我的定价参考：

| 状态                          | 合理价格 |
| ----------------------------- | -------: |
| 完全正常工作 + 驱动 + CUDA 测试 | 2500-4000 元 |
| 驱动失败但 nvflash 可恢复     | 1200-1800 元 |
| VBIOS 未知，无法测试          | 500-1000 元 |
| 已损坏/无 PCIe 识别           | 仅作零件 |

对于这块卡，我最多出价**1000-1500 元**。

---

## 为什么有风险？

VBIOS 错误可能意味着：

### 最佳情况

GPU 完好：

```
PCIe 被识别
      |
      v
错误的 ROM
      |
      v
刷入正确的 ROM
      |
      v
正常工作
```

成本：几乎为零。

### 最坏情况

```
错误的 ROM
      |
      v
SPI 闪存损坏
      |
      v
nvflash 无法访问
      |
      v
拆卸散热器
      |
      v
CH341A 编程器
      |
      v
手动 SPI 恢复
```

时间成本：数小时。

---

## 购买前，请向卖家索要以下信息：

1. GPU 检测信息：

```bash
lspci -nn | grep NVIDIA
```

需要看到：

```
10de:20c2
```

这是 8GB CMP 170HX 的 ID。([GitHub][1])

2. `nvidia-smi` 输出：

不良信息：

```
No devices were found
```

或：

```
GPU has fallen off the bus
```

3. nvflash 测试：

```bash
nvflash --list
```

如果 nvflash 能识别到卡 → 情况好很多。

4. 确切的 VBIOS 版本：

```bash
nvflash --version
```

---

考虑到你的背景（你使用 Linux/CUDA 并且之前刷过 GPU），**这是一个修复赌博，而不是 GPU 购买**。

我的个人阈值：

* **≤1000 元：** 作为项目购入
* **1500 元：** 可以考虑
* **2500 元：** 仅当卖家能证明 nvflash 可恢复时才买
* **3000+ 元：** 不如买一块正常工作的卡

在 2500 元的价格下，你几乎是在支付正常卡的钱，却要承担修复风险。我会选择放弃或者狠狠砍价。

[1]: https://github.com/Consensus-Protocol/cmp170hx/blob/main/docs/hardware/overview.md?utm_source=chatgpt.com "cmp170hx/docs/hardware/overview.md at main · Consensus-Protocol/cmp170hx · GitHub"
[2]: https://www.ebay.com/itm/278187573402?utm_source=chatgpt.com "NVIDIA CMP 170HX 8GB MINING GPU TESTED WORKING 100% | eBay"
[3]: https://www.ebay.com/itm/307075365403?utm_source=chatgpt.com "NVIDIA CMP 170HX 8GB Mining Card GPU 164mh/S Exclusive PCI-Express 4.0 X4 | eBay"