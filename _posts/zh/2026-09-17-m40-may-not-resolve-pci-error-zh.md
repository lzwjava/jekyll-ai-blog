---
audio: false
generated: true
image: false
lang: zh
layout: post
title: M40可能无法解决PCI错误
translated: true
type: note
---

问题：**如果我将P100换成特斯拉M40，PCI资源错误会消失吗？**

答案：**可能性更大，但无法保证。** M40实际上是一款适合搭配微星PRO B760M-E主板的显卡，但有一个重要注意事项：**M40同样有较大的BAR需求**，因此主板仍需正确分配一个大的64位PCIe MMIO区域。

### P100 vs M40

|              |    Tesla P100 | Tesla M40 24GB |
| ------------ | ------------: | -------------: |
| 架构         |        Pascal |        Maxwell |
| 显存         | 12/16 GB HBM2 |    24 GB GDDR5 |
| PCIe         |      Gen3 x16 |       Gen3 x16 |
| 功耗         |         250 W |          250 W |
| 散热         |       被动式  |        被动式  |
| 主要问题     | 大PCI BAR     |  大PCI BAR     |

NVIDIA官方标注M40为PCIe 3.0 x16，功耗250W，被动散热，配备24GB显存。（[NVIDIA图片][1]）

需要注意的是，**M40并不自动意味着“较小的PCI资源需求”**。确实有M40系统因BAR1无法分配而失败的案例，包括一块M40 24GB在华硕Z97系统上的问题。（[NVIDIA开发者论坛][2]）

所以：

```text
A68HM-E + P100
       ↓
PCI资源错误
       ↓
旧版BIOS / PCI MMIO分配
```

换成：

```text
A68HM-E + M40
       ↓
可能可行
       ↓
但并非可靠方案
```

而：

```text
B760M-E + M40
       ↓
现代UEFI
       ↓
CPU PCIe 4.0 x16
       ↓
M40 PCIe 3.0 x16
       ↓
更优候选方案
```

B760M-E的主PCIe插槽直连CPU，支持PCIe 4.0 x16。（[微星][3]）

### M40的一大优势

如果你的目标是**便宜的CUDA显存**，那么M40 24GB值得考虑。

但如果你要在**P100和M40之间选择**，不要以为M40更新更好：

```text
M40 = Maxwell，2015年
P100 = Pascal，2016年
```

P100在架构上明显更新。NVIDIA数据中心驱动文档中，470分支仍然将M40和P100列在支持的Tesla系列中。（[NVIDIA文档][4]）

对于机器学习工作负载，**P100通常是更强大的计算架构**，特别是因为Pascal增加了Maxwell所缺乏的功能。

### 我会怎么做

如果你**已经拥有M40**：

```text
微星PRO B760M-E
        +
特斯拉M40 24GB
        +
英特尔i5-12400/13400
```

值得一试。

如果你**专门为了装入B760M-E而购买显卡**，**我不建议为了避开PCI资源错误而购买M40**。主板/固件是更关键的因素。

实际上，有一个有用的实验：

```text
当前A68HM-E
       │
       ├── P100 → PCI资源错误
       │
       └── M40 → 测试
```

如果**两者**都产生相同的错误，那么基本可以证明A68 BIOS/平台是问题所在。

然后：

```text
B760M-E
   │
   ├── P100
   └── M40
```

应该进行下一步测试。

### 对我之前回答的一个修正

我还想纠正一个重要问题：**我不会用P100的大BAR存在来证明B760M-E会失败或成功。** 实际的BAR分配取决于固件的PCI资源映射、CSM/UEFI配置、其他设备以及BIOS实现。有记录显示，即使较新的主板也存在Tesla BAR分配问题。（[NVIDIA开发者论坛][5]）

对于B760M-E，微星明确将**Above 4G Decoding**作为允许64位PCIe MMIO超过4GB地址空间的机制。（[微星][6]）

所以，如果你的首要目标是：

> **“我想用最便宜的主板稳定启动我的Tesla显卡。”**

我会认真考虑**B760M-E + M40**，但如果你已经拥有P100，我仍然更倾向于**B760M-E + P100**。

**并且请确保M40有适当的辅助供电和强劲的风流**——这是一款250W的被动散热数据中心显卡。（[NVIDIA图片][1]）

参考文献：

* [NVIDIA Tesla M40数据表](https://images.nvidia.com/content/tesla/pdf/78071_Tesla_M40_24GB_Print_Datasheet_LR.PDF?utm_source=chatgpt.com)
* [微星PRO B760M-E规格](https://www.msi.com/Motherboard/PRO-B760M-E/Specification?utm_source=chatgpt.com)
* [微星Above 4G Decoding解释](https://us.msi.com/faq/2726?utm_source=chatgpt.com)

[1]: https://images.nvidia.com/content/tesla/pdf/78071_Tesla_M40_24GB_Print_Datasheet_LR.PDF?utm_source=chatgpt.com "数据表：Quadro M6000"
[2]: https://forums.developer.nvidia.com/t/this-pci-i-o-region-assigned-to-your-nvidia-device-is-invalid-above-4g-decoding-already-enabled/121633?utm_source=chatgpt.com "分配给您的NVIDIA设备的这个PCI I/O区域无效（Above 4G decoding已启用） - 驱动程序 - Linux, Windows, MacOS - NVIDIA开发者论坛"
[3]: https://www.msi.com/Motherboard/PRO-B760M-E/Specification?utm_source=chatgpt.com "PRO B760M-E"
[4]: https://docs.nvidia.com/datacenter/tesla/tesla-release-notes-470-103-01/index.html?utm_source=chatgpt.com "版本470.103.01（Linux）/472.98（Windows） :: NVIDIA数据中心GPU驱动文档"
[5]: https://forums.developer.nvidia.com/t/tesla-p40-in-dell-percision-7910-rack/281034?utm_source=chatgpt.com "Dell Precision 7910机架中的Tesla P40 - CUDA编程与性能 - NVIDIA开发者论坛"
[6]: https://us.msi.com/faq/2726?utm_source=chatgpt.com "微星美国 | 微星美国"