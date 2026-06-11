---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为何互连带宽很重要
translated: true
type: note
---

**问题：** 为什么互连如此重要？为什么Marvell擅长互连带宽？SK海力士也做带宽——NVLink会使用Marvell吗？

**回答：**

这里混淆了三件不同的事情，让我们从基本原理来梳理。你把**内存带宽**（SK海力士的层面）和**网络互连**（Marvell的层面）混为一谈，而NVLink介于两者之间。它们都在“传输比特”，但物理距离不同，每个距离上的物理特性决定了谁能参与其中。

## 1. 为什么互连是瓶颈——数学分析

训练大模型本质上是一个伪装成计算问题的通信问题。以数据并行训练为例：每一步，每个GPU都必须对梯度进行全规约。对于环形全规约，每个GPU发送/接收：

```python
# 每步每个GPU的通信量（环形全规约）
P = 70e9            # 参数数量（70B模型）
bytes_per_grad = 2  # bf16
N = 1024            # GPU数量

vol = 2 * (N - 1) / N * P * bytes_per_grad   # ≈ 每步每个GPU 280 GB！

# 在400 Gbps（50 GB/s）网络下：每步纯通信时间 = 280/50 = 5.6秒。
# 一块B200完成该步的计算时间远小于1秒。
# => GPU空闲等待网络。FLOPs是免费的，字节不是。
```

这就是为什么人们如此关注重叠（与反向传播并行的分段梯度全规约——你在nanoGPT的DDP中见过这一点），以及为什么前沿实验室在网络架构上的投入与GPU相当。随着集群从10k → 100k → 1百万加速器扩展，计算线性增长，但通信模式（MoE中的全对全、张量并行的全收集）扩展性更差。互连带宽、光网络集成和机架级异构计算现在与原始性能一样重要，决定着谁能赢得基础设施订单。

按距离划分的带宽层级：

| 层级 | 距离 | 技术 | 硅片制造商 |
|---|---|---|---|
| HBM | 毫米级（封装内） | 通过中介层的DRAM堆叠，~8 TB/s | **SK海力士**、三星、美光 |
| 纵向扩展（NVLink） | <1米–机架 | 铜缆SerDes、NVSwitch，~1.8 TB/s/GPU | **英伟达**（专有） |
| 横向扩展网络 | 3米–500米 | 800G/1.6T光收发器 | **Marvell**、博通（内部的DSP） |
| DCI | 公里–100公里 | 相干光模块（400ZR/800ZR） | **Marvell**（前Inphi）、思科/Acacia |

**关键物理事实：** 铜缆在距离面前失效。在112G/224G每通道速率下，无源铜缆只能延伸几米，之后信号完整性就会崩溃。超出机架范围，每条链路都是光链路——而每个光模块都需要一颗DSP芯片进行PAM4调制、均衡和时钟恢复。这个DSP市场基本上是Marvell/博通的双头垄断。在10万GPU集群中的每个1.6T收发器都包含它们的一颗芯片。数一数NVL72部署中的收发器数量，你就会明白为什么这是一个价值数十亿美元的年金业务。

## 2. 为什么特别提到Marvell

他们的护城河是**高速模拟混合信号设计**——半导体领域中最难、最不易商品化的技能：

- **224G SerDes**：通过单条电通道实现224 Gbps是残酷的模拟工程（均衡、FFE/DFE、抖动预算）。Marvell拥有超过25年的PHY经验，可以追溯到其硬盘驱动读通道时代——读通道本质上就是从嘈杂的模拟介质中恢复信号，这正是相同的核心能力。
- **Inphi（2021年100亿美元收购）**：带来了PAM4 DSP产品线和相干DSP。这是皇冠上的明珠。
- **Celestial AI**：Marvell于2025年12月以32.5亿美元收购了Celestial AI——其光子结构实现了行级相干内存和网络内集合处理，类似于英伟达通过其Mellanox InfiniBand传统在NVSwitch中提供的功能。网络内全规约（类似SHARP）正是针对上述通信瓶颈的AI原生解决方案。
- 他们自己的话：在高性能模拟、光DSP、硅光子和定制硅片领域处于领先地位。

此外，SerDes/光学专业知识也滋养了XPU业务：Marvell的光学专长是客户对其XPU设计感兴趣的驱动因素——如果定制加速器的芯片边缘带宽跟不上，它就毫无用处，因此超大规模客户从同一供应商处购买I/O和芯片设计。

## 3. SK海力士——完全不同的层面

SK海力士与Marvell完全没有竞争关系。HBM是**内存带宽**：使用TSV堆叠的DRAM芯片，位于CoWoS中介层上离计算芯片毫米之处，为张量核心提供数据。它解决了“我的矩阵乘法能否足够快地读取权重”的问题（算术强度/计算上限）。Marvell解决的是“GPU #4071能否从GPU #88213获取梯度”的问题。两者都是带宽，但一个是内存技术，另一个是网络/信号技术。SK海力士将HBM堆栈*卖给*英伟达和Marvell的XPU客户——它们互补，而非竞争。

## 4. NVLink使用Marvell吗？

**NVLink本身：不。** NVLink和NVSwitch是英伟达自己的专有SerDes、协议和交换芯片——内部设计，台积电代工。完全没有Marvell的内容。

**但关系在2026年3月发生了变化。** 英伟达向Marvell投资了20亿美元，并建立了以NVLink Fusion为中心的战略合作伙伴关系，这是一个机架级平台，允许第三方芯片直接接入英伟达的专有互连架构。分工如下：Marvell提供定制XPU和兼容NVLink Fusion的纵向扩展网络，而英伟达提供Vera CPU、ConnectX网卡、BlueField DPU、NVLink互连和Spectrum-X交换机。因此，Marvell设计的芯片现在可以*说*NVLink语言——例如，AWS已表示未来的Trainium 4将同时支持UALink和NVLink协议，而作为AWS主要的定制芯片合作伙伴，Marvell需要访问英伟达的技术来实现这一点。

战略解读很犀利：Marvell的定制XPU业务在2026财年实现了15亿美元收入，预计到2028财年将翻倍，目前有18个活跃的定制芯片项目，其中12个来自亚马逊、谷歌、微软和Meta——这些芯片的存在是为了*取代*英伟达GPU。通过将Marvell拉入NVLink Fusion，每个NVLink Fusion设置至少需要一个英伟达部件，因此Marvell的ASIC仍能为英伟达创造收入，而博通则领导着UALink（NVLink的开放替代方案），处于架构战的另一方。

**TL;DR：** SK海力士 = 进入芯片的带宽（HBM）。英伟达 = 机架内的带宽（NVLink）。Marvell = 机架之间和建筑之间的带宽（光DSP、SerDes、光子）——再加上，自2026年3月起，获得了将NVLink端口放置在其设计的定制芯片上的许可入口。

如果你想在代码中直观感受这一点，可以在多节点nanoGPT运行中设置`NCCL_DEBUG=INFO`，观察随着节点扩展，`AllReduce`与计算相比占用了多少挂钟时间——Marvell的整个论点就在这个比值中。

**参考文献：**

- [英伟达–Marvell NVLink Fusion新闻稿（marvell.com）](https://www.marvell.com/company/newsroom/nvidia-ai-ecosystem-expands-marvell-joins-forces-through-nvlink-fusion.html)
- [The Next Platform：英伟达与Marvell的20亿美元交易](https://www.nextplatform.com/connect/2026/03/31/the-2-billion-nvidia-deal-with-marvell-is-about-a-lot-more-than-nvlink-fusion/5213790)
- [TNW：NVLink Fusion作为生态系统锁定](https://thenextweb.com/news/nvidia-marvell-nvlink-fusion-ecosystem-lock-in)
- [TFN：NVLink Fusion生态系统分析](https://techfundingnews.com/nvidia-2-billion-marvell-nvlink-fusion-ai-ecosystem/)
