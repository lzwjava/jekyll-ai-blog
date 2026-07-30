---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD RX 9060 XT：命名澄清
translated: true
type: note
---

**问题：** AMD RX 9600 XT 显卡是什么？

**回答：** 首先需要指出命名上的混淆——"RX 9600 XT"是发布前的泄露代号；AMD在2025年台北电脑展上正式将其命名为**RX 9060 XT**并上市。市面上没有任何零售显卡实际标注为"9600 XT"。（上述部分搜索结果——那些提到12GB GDDR7、750GB/s带宽或0.25GB GDDR5的信息——是垃圾/AI生成的垃圾页面，请忽略。）

RX 9060 XT（RDNA 4，Navi 44）的真实规格：

| 规格 | 参数 |
|---|---|
| 制程 | TSMC N4P（4nm） |
| 晶体管数 | 29.7B |
| 计算单元 | 32 |
| 基础 / 加速频率 | 2530 MHz / 3130 MHz |
| 显存 | 8GB 或 16GB GDDR6 |
| 目标市场 | 1080p/1440p游戏，对标RTX 5060 Ti |
| 建议零售价 | 299美元（8GB）/ 349美元（16GB） |

针对您的使用场景（本地推理/小型微调），**16GB版本是唯一值得考虑的**——8GB连玩具模型都无法运行。即使16GB版本，它仍然是一款游戏卡：没有等效的张量核心，RDNA4消费级显卡的ROCm支持仍在完善中（如果计划在上面运行PyTorch/vLLM，购买前务必检查ROCm兼容性矩阵——纯CUDA栈显然完全无法工作）。

鉴于您已经在使用MI300X进行实际训练工作，这张卡仅适合作为廉价的本地开发/推理机，而非训练节点。

**参考资料：**
- [AMD Radeon RX 9600 XT Launched (Navi 44) - Geeks3D](https://www.geeks3d.com/20250521/amd-radeon-rx-9060-xt-announced-navi-44/)
- [AMD RX 9060 XT leaked specs - Tom's Hardware](https://www.tomshardware.com/pc-components/gpus/amd-rx-9060-xt-leaked-specs-allege-speedy-3-3-ghz-gpu-clock)