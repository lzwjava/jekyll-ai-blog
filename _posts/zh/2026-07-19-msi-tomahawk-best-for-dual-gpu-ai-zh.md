---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 微星战斧最佳双GPU AI主板
translated: true
type: note
---

问题：MSI MAG Z790 Tomahawk WiFi DDR5 和 ASUS TUF Gaming Z790-PLUS WiFi 哪款主板更适合用于搭载 i9-13900KF + RTX 4070 + RTX 3060 双 GPU 的 AI 主机？

答案：MSI Tomahawk。以下是从实际依据出发的理由，而非凭感觉。

**电气布局基本相同**——这一点对你的配置至关重要，且两者持平：

```
MSI Tomahawk:  PCIe5 x16 (CPU) + PCIe4 x16插槽@x4 (芯片组) + PCIe3 x1
ASUS TUF Plus: PCIe5 x16 (CPU) + PCIe4 x16插槽@x4 (芯片组) + PCIe4 x4
```

根据 MSI 官方规格表确认：2 个 PCI-E x16 插槽支持 x16/x4 模式，PCI_E1 来自 CPU 的 Gen5 最高 x16，PCI_E3 来自芯片组的 Gen4 最高 x4。两块主板都将你的第二张显卡（3060）连接到芯片组的 x4 电气通道。对于 CUDA 推理/训练——只要不是每一步都做张量并行 all-reduce——x4 Gen4（约 8GB/s）不会成为你的瓶颈；真正的瓶颈在于模型加载时间和 DDP 中 PCIe 受限的梯度同步，而 DDP 在 x4 下只会变慢，不会崩溃。

**MSI 真正胜出的地方：**

- 价格 $209 vs $268——ASUS 贵了 $60，却采用相同的 PCIe 拓扑结构
- 根据多数评测，其 VRM/供电设计在 13900KF 持续负载下表现更优（这对你很关键，因为训练时你会让两块 GPU 和 CPU 长时间满载 100%，而非突发的游戏负载）
- 4 个 M.2 插槽，全部为 Gen4 x4，其中一个来自 CPU——如果你需要在本地暂存数据集或检查点，这很有用

**ASUS 胜出的地方：** 基本没有决定性优势。TUF Plus 是不错的主板，但多花 $60 换来的只是略有不同的品牌和 BIOS 体验，对你的使用场景来说不值。

**真正的瓶颈不在主板，而在于你的设想。** 你反复提到“总共 24GB 显存”，仿佛它是一张 RTX 3090。但事实并非如此。没有 NVLink，且异构计算（4070 Ada 架构 vs 3060 Ampere 架构），你无法在这两张卡之间高效地实现张量并行。实际可行的用法：

```python
# 实际可行的做法：两个独立进程，而非拆分一个模型
CUDA_VISIBLE_DEVICES=0 python train.py --model 7B-int4   # 在 4070 上运行
CUDA_VISIBLE_DEVICES=1 python inference_server.py --model llama-8b-gptq  # 在 3060 上运行
```

如果你确实想不顾非对称性而进行跨 GPU 模型拆分，`accelerate` / `transformers` 中的 `device_map="auto"` 可以处理，但要预期到 x4 链路及 Ada/Ampere 架构不匹配带来的明显性能下降。不要指望买一张 3060 就能当廉价版 24GB 显存卡——它应该作为第二张独立工作卡使用。

原文档中关于机箱/电源的条目可以直接跳过——那些数字没问题，无论选择哪块主板，850W 金牌电源 + ATX 风道机箱都是正确的选择。

参考来源：

- [MSI MAG Z790 Tomahawk WiFi 规格讨论帖](https://forum-en.msi.com/index.php?threads/mag-z790-tomahawk-wifi-pci_e1-5-0x16-and-1st-m2-4-0x4-gpu-alteration-or-not.396659/)
- [MSI MAG Z790 Tomahawk WiFi @ B&H](https://www.bhphotovideo.com/c/product/1731165-REG/msi_mag_z790_tomahawk_wifi.html)
