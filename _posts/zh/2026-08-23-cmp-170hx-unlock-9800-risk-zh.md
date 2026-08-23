---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CMP 170HX 解锁：¥9800风险？
translated: true
type: note
---

**问题：** 在闲鱼上花9800元人民币购买NVIDIA CMP 170HX（8GB版本，可通过cmpunlocker解锁至64GB）划算吗？

---

**回答：**

这是个当前的热门话题。以下是完整情况：

**cmpunlocker的作用**

该工具能恢复固件/OTP配置中受限的完整SM计算吞吐量，并解锁被限制的HBM2e显存寻址能力。具体到8GB版本，可将8GB的170HX解锁至64GB。

**价格暴涨背景**

在该工具走红后，此前售价约100-200美元的显卡，全球范围内现已飙升至1000美元以上。9800元人民币约合1350美元，处于当前市场价格**高位**，但鉴于炒作热度，并不算离谱。

**关键注意事项——这部分很重要**

据报道，8GB型号可达到64GB，而其他型号仅能在更低容量下保持稳定。显存稳定性与带宽也因HBM芯片体质而异。有报告称，使用海力士显存的8GB显卡在扩展至64GB时可能更稳定。

并非所有人都能成功解锁完整显存堆栈，因为CMP 170HX基于原版A100安培GPU的低等级芯片，大多数HBM2e堆栈因使用了有缺陷或次品显存芯片而被禁用。

简单来说：**64GB并非百分之百保证。** 许多显卡稳定在32GB或更低。

**硬件背景**

NVIDIA使用了A100生产过程中被淘汰的GA100芯片。这些残次品没有报废，而是被禁用了部分CUDA和Tensor核心，并将显存削减至8或10GB。所以你买到的是一块有缺陷的芯片，*可能*会发挥其全部潜力。

**运行解锁工具的要求**

你需要Linux（x86-64架构）、root权限、已安装nvidia-open 610.43.0x驱动、与运行内核匹配的内核头文件、禁用安全启动，以及Python 3。不支持Windows。

**结论**

| 因素 | 评估 |
|---|---|
| 价格（9800元） | 考虑到风险，略高 |
| 64GB解锁保证 | ❌ 无法保证——看运气 |
| 计算性能 | ✅ GA100架构，带宽出色 |
| 仅限Linux | ⚠️ 不支持Windows |
| 使用场景 | AI推理、运行大语言模型，非游戏用途 |

**仅在以下情况推荐：** 你愿意赌一把显存解锁能完美成功，你使用Linux，并且需要一种低成本方式实验大型AI模型。如果你需要保证64GB，这不适合你。如果运气好拿到体质好的芯片，性价比极高。建议将价格谈到7000-8000元以对冲风险。

---

**参考链接：**
- [cmpunlocker GitHub](https://github.com/amoghmunikote/cmpunlocker)
- [CMP 170HX因解锁工具曝光价格飙升至1000美元以上](https://www.digitalcitizen.life/nvidia-cmp-170hx-prices-surge-past-1000-after-tool-unlocks-up-to-80-gb-of-vram/)
- [WCCFTech：价格从100美元暴涨至1000美元以上](https://wccftech.com/nvidia-cmp-170hx-8-10-gb-prices-explode-over-1000-usd-as-tool-unlocks-hidden-64-80gb-vram/)
- [Bytwork：A100级基准测试与背景信息](https://bytwork.com/en/hw/videocards/cmp-170hx)