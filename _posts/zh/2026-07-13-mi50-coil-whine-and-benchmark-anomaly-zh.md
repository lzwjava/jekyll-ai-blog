---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MI50 线圈啸叫与基准测试异常
translated: true
type: note
---

问题：(1) 为什么 MI50 在 300W 电源上会啸叫，但在 400W 电源上不会？(2) 本地店铺有一块“Radeon Pro VII”（交叉刷写 MI50），鲁大师跑分 1617——值得入手吗？

回答：

**1. 300W vs 400W 时的线圈啸叫**

这实际上与电源的*额定功率*关系不大，而是与**给 8-pin 供电的 12V 轨上的瞬态电流裕量**有关。MI50 默认为 ~200-225W，但常见的“满血”BIOS/注册表修改会将其推至 300W。在此负载下：

- HBM2 + VRM 会抽取快速电流尖峰，一个性能较差的电源无法干净地提供这些电流 → 电源自身的电感和 MOSFET 开始更努力地切换以补偿 → 产生可闻的啸叫，并非损坏，只是电压调节超负荷工作产生的噪音。
- “400W 额定”电源本身并非每瓦特更好——它只是提供了更多的**电源轨裕量**，因此在 300W 功耗下，你不会接近其瞬态极限。
- 中文 MI50 论坛中确认的模式：通过限制 GPU 功率来降低瓦特数可以完全消除啸叫——相同的机制，方向相反（他们减少了瓦特数，而不是增加电源容量）。

如果你受限于 300W 电源的实际解决方法是：通过 `rocm-smi --setpoweroverdrive` 或 AMD MPT 工具将功率上限设定为 ~250W。或者直接使用电源原生的 8-pin 线缆（不要从一个接口并联分接，不要使用大4D转接线）——糟糕的线缆连接是导致此症状的另一大常见原因。

**2. 店铺的“Radeon Pro VII”——是否可信，1617 分是否真实？**

这块卡几乎可以肯定是刷写了 Radeon Pro VII（或 V420）vBIOS 的 MI50——这是解锁 miniDP 输出的标准修改，经证实，只有此 BIOS 才能启用 MI50 上的 miniDP 端口。这是合法的操作，本身并不算欺骗——MI50 与 Radeon Pro VII/V420 共享相同的 Vega 20 硅片和 PCB。

但是 **1617 作为鲁大师总分是一个巨大的危险信号**。一块健康的 MI50/Radeon Pro VII 在鲁大师上的得分约为 400,000（40万）分。1617 差了约 250 倍。有两种可能：

- **它真的是总分** → 显卡有故障：PCIe 连接降速（运行在 x1 而非 x16）、坏的 vBIOS 刷写导致降频运行、驱动程序未实际加载（Windows 显示通用“Microsoft 基本显示适配器”）、或内存降速/损坏。直接走人，或要求当面进行实时重测。
- **它实际上是核心频率（MHz），而不是跑分**——MI50 基础频率为 1625 MHz，因此 1617 几乎完全吻合。如果卖家/店铺将“时钟频率”误当作“跑分”，那么这块卡可能完全没问题。

不要猜测——要求他们当场运行：
```bash
# 付款前，在现场
rocm-smi --showclocks --showtemp --showmeminfo vram
lspci -vv | grep -A2 "LnkSta:"   # 确认 PCIe x16 Gen3/4，而非 x1/x4
```
或在 Windows 上，用 GPU-Z 查看核心频率 ~1625-1725MHz、16GB HBM2、PCIe x16。

还要根据已知的诈骗模式进行物理检查：MI50 的外部标签和 ECC 芯片可以证明其未进行过挖矿工作——经过挖矿“蹂躏”的显卡会被重新焊接并失去石墨烯导热垫（脆性，拆解时易裂开），因此需询问是否曾打开过。

满载运行 10 分钟后温度达到 90°C 大致是正常范围（MI50 原装散热条件下，节流/报警阈值约为结温 95-100°C）——本身不算危险信号，但如果你要运行持续的训练任务，请计划更好的散热。

**结论**：在他们当面展示带有实际频率的 rocm-smi/GPU-Z 读数以及刚跑完的鲁大师跑分之前，不要付款。如果 1617 确实是基准测试总分，那就是块废卡。

参考链接：
- [MI50本地部署DeepSeek交流（上） - 知乎](https://zhuanlan.zhihu.com/p/23351570033)
- [MI50 32G版vbios汇总及通用驱动安装办法 - CSDN](https://blog.csdn.net/dwd112358/article/details/153295770)
- [不到600元的苏妈专业卡对标4060 - CSDN](https://blog.csdn.net/minge89/article/details/148349350)
- [ATX3.0 psu's and coil whine - Overclockers UK](https://forums.overclockers.co.uk/threads/atx3-0-psus-and-coil-whine.18967019/)