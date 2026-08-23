---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CMP 170HX 解锁租赁状态
translated: true
type: note
---

**问题：** 目前是否有人在RunPod上出租解锁后的CMP 170HX（64GB）显卡？

**答案：**

这是一个非常新的话题——CMP 170HX解锁功能仅在几周前才广为人知。以下是真实情况：

**CMP 170HX解锁的实际含义：**

CMP 170HX是英伟达CMP系列中的旗舰型号，采用GA100（安培）架构芯片——与A100相同的核心。一款名为“CMPUnlocker”的软件工具恢复了之前被锁定的内存，使其内存容量提升高达8倍——从仅8GB提升至惊人的64GB。

**能否将其上架RunPod？目前基本不行：**

目前没有证据表明有人在RunPod的社区云上成功运行解锁后的170HX显卡。实际原因如下：

- 让显卡显示更大的内存容量，与证明该内存在持续负载下稳定可靠是两回事。独立测试人员指出，在解锁容量的边缘区域存在不一致行为，且具体表现因显卡使用的内存颗粒和芯片体质差异而不同。由于缺乏ECC纠错，原本在真正A100上能被捕捉并纠正的内存错误，在此处可能会静默地破坏数据。

- PCIe Gen 2 x4接口限制了神经网络权重的加载速度，但加载完成后实际计算速度很快。这种带宽瓶颈对于运行大型工作负载的租户来说是一个实际问题。

- 64GB下的稳定性无法保证——原始研究论文仅确保40GB在压力下可靠运行。部分用户报告64GB可用，另一些用户则反馈不稳定。该显卡也不支持FP8/FP4格式，因此尽管拥有大显存，速度仍不及RTX 5090。

- RunPod的社区云会对主机进行审核——一张经过非官方固件破解的矿卡很难通过其准入检查。

**人们实际在哪里试验：**

二手市场上170HX的挂牌量有所增加，一些卖家将解锁后的显卡宣传为本地AI推理的低成本选择，并指出其约1.5 TB/s的内存带宽对内存密集型工作负载具有真正吸引力。目前的使用场景主要是**个人/本地推理**，而非云端出租。

**Vast.ai** 可能是一个更现实的平台，因为它是一个真正开放的市场，允许个人主机自行设置挂牌——但即便如此，租户仍可能因稳定性风险而拒绝使用。

**归根结底：** 解锁是真实且令人兴奋的，但它太新、太不稳定、也未经过充分验证，目前尚不适合平台出租。在考虑将其用于云托管之前，给社区几个月时间，看看能否稳定实现64GB解锁。

**参考资料：**

- [Tom's Hardware — CMP 170HX VRAM解锁](https://www.tomshardware.com/pc-components/gpus/nvidia-crypto-mining-gpus-hacked-to-restore-locked-away-vram-in-order-to-feed-ai-boom-software-mod-unlocks-64gb-of-vram-on-usd250-cmp-170hx)
- [WCCFTech — CMP 170HX价格暴涨](https://wccftech.com/nvidia-cmp-170hx-8-10-gb-prices-explode-over-1000-usd-as-tool-unlocks-hidden-64-80gb-vram/)
- [PBX Science — 解锁CMP 170HX](https://pbxscience.com/unlocking-the-cmp-170hx-how-far-the-community-has-actually-gotten-toward-an-a100-on-the-cheap/)
- [Bytwork — CMP 170HX解锁指南](https://bytwork.com/en/articles/cmp-170hx-unlock)
