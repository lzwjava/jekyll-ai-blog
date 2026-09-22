---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Suqiao RTX 5090 96GB 翻盖改装版
translated: true
type: note
---

问题：**速桥是如何把RTX 5090变成96GB显卡的？具体改了什么？**

答案：

关键在于：**他们并不是神奇地“解锁”了64GB隐藏显存。** 更可能的方法是**定制PCB + 不同的GDDR7显存颗粒布局 + 固件/VBIOS修改**。

### 1. 从GB202 GPU开始讲起

RTX 5090采用的是NVIDIA的**GB202** GPU。

有趣的是，**英伟达RTX PRO 6000 Blackwell同样使用GB202，并且官方配置就是96GB GDDR7显存**。所以从GPU架构本身来说，并非完全不具备96GB寻址能力。（[Tom's Hardware][1]）

概念上：

```text
RTX 5090
             ┌───────────────┐
             │     GB202     │
             │     GPU       │
             └───────┬───────┘
                     │
          32 GB GDDR7
          16 × 2 GB 颗粒
```

原版5090采用了**512-bit显存位宽**和32GB GDDR7显存。

---

### 2. 关键可能是“三明治（clamshell）”显存排列

这就是有意思的硬件魔改思路了。

不在每个显存通道位置上只放一颗显存颗粒，而是**在同一通道对应的两个电气连接位置，分别位于PCB正反两面各焊一颗显存颗粒**。

概念上类似：

```text
             PCB 正面
       ┌──────────────────────┐
       │ GDDR7 GDDR7 GDDR7 ... │
       │        GB202          │
       │ GDDR7 GDDR7 GDDR7 ... │
       └──────────────────────┘
             PCB 背面
       ┌──────────────────────┐
       │ GDDR7 GDDR7 GDDR7 ... │
       │ GDDR7 GDDR7 GDDR7 ... │
       └──────────────────────┘
```

这就是**三明治（clamshell）显存排列**。

RTX PRO 6000强有力地证明了，NVIDIA的GB202平台可以适配这种高密度显存配置。关于速桥显卡的报道中，也明确指出**定制PCB和clamshell排列**是最可能的实现方式。（[The Silicon Report][2]）

所以物理上的改动大致是：

```text
原版5090：

GPU ── 16 × 2GB GDDR7
       = 32GB


速桥版：

GPU ── 32 × 3GB GDDR7
       = 96GB
```

**最关键的细节是显存颗粒的密度。**

如果他们真的做到了96GB，那么需要的是**单颗3GB的GDDR7显存颗粒，共32颗**，或者等效的其他高密度方案。

---

### 3. 这正是Alibaba上规格参数可疑的原因

据报道，该商品页面上的标注大致是：

```text
GDDR6X
14 Gbps
96GB
```

这些数字放在一起就很不合理。

GDDR6X一般速率远高于14 Gbps，而且已知的单颗16Gb（2GB）的GDDR6X颗粒，即使采用clamshell排列，也很难凑出96GB的配置。（[The Silicon Ledger][3]）

对于真正96GB的Blackwell实现来说， **采用单颗3GB的GDDR7颗粒组成96GB，在工程上要合理得多。**

所以我目前倾向于认为Alibaba上的规格参数是：

> **产品本身可能是真的，但公开的规格表在技术上并不可信。**

到目前为止，还没有可靠独立的拆解或跑分证据，能确认速桥到底出货的是什么东西。（[NeoTeo][4]）

---

### 4. PCB才是最难的部分

你不能简单地把5090上的32GB显存焊下来，然后往原装PCB上焊更多显存颗粒。

你需要一块为这种显存拓扑专门设计的PCB。

想想看：

```text
                 ┌──────────────┐
                 │    GB202     │
                 └──────┬───────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
     memory          memory          memory
     channel 0       channel 1       channel 2
        │               │               │
     ┌──┴──┐         ┌──┴──┐         ┌──┴──┐
     │     │         │     │         │     │
    front back      front back      front back
```

这时你就需要解决：

* 高速GDDR7布线
* 额外显存颗粒的供电
* 信号完整性
* 终端电阻
* 显存训练
* 散热设计
* GPU与显存之间的拓扑
* VBIOS显存配置

这就是为什么这更像是**ODM级别的工程制造**，而远不是普通的“显卡硬改”。

据报道，速桥有显卡、主板和服务器的制造经验，这使得定制PCB方案的可行性很高。（[Tom's Hardware][1]）

---

### 5. 还需要固件/VBIOS的支持

这部分最容易被低估。

GPU需要知道：

```text
显存类型       = GDDR7
显存颗粒       = ...
单颗容量       = ...
总容量         = 96GB
通道拓扑       = ...
时序           = ...
训练           = ...
```

所以，即使你真把96GB显存颗粒物理焊上去了：

```text
GPU
 ↓
“他妈的另外那些显存呢？”
```

它也不会神奇地就识别成96GB。

你需要对应的**VBIOS / 显存配置 / 初始化固件**。

此前国内有人在RTX 4090上修改出48GB显存，就证明了增加显存除了更换硬件颗粒，还涉及到固件的修改。（[Jagat Review][5]）

---

## 更有趣的问题：为什么能做到这么便宜？

这就是对AI来说最刺激的部分了。

NVIDIA已经量产了一款概念上极为接近的产品：

```text
                 GB202
                   │
        ┌──────────┴──────────┐
        │                     │
   RTX 5090              RTX PRO 6000
   32GB                  96GB
   消费级                 工作站级
```

GPU核心本身，在概念上并不一定是昂贵或限制性的部分。

5090和PRO 6000之间巨大的价差，还包括：

- 产品市场细分
- ECC / RAS功能
- 工作站认证
- 驱动程序
- 质保
- 企业级技术支持
- 显卡板卡设计
- 显存
- NVIDIA产品定位

所以，深圳的ODM厂商完全可以基于**GB202平台**，去打造一块便宜得多的显卡，专门优化用于：

```text
大语言模型推理
      ↓
96GB显存
      ↓
单张显卡
      ↓
无需NVLink
      ↓
更大模型放进单一地址空间
```

对于本地推理来说，这是**非常有吸引力**的配置。

---

## 但有一大区别非常重要

**96GB容量 ≠ 96GB性能。**

对于大语言模型推理，大致是：

```text
模型权重
    ↓
显存容量       → “模型放不放得下？”
    ↓
显存带宽       → “解码能跑多快？”
```

如果是一张96GB的显卡，但GDDR7显存跑在较低的频率上，那么它的性能表现可能会和32GB的5090截然不同。

所以，入手前我想看到这些数据：

```bash
nvidia-smi

nvidia-smi --query-gpu=name,memory.total,memory.bus_width,\
memory.clock,clocks.current.memory,power.draw \
--format=csv

nvidia-smi -q
```

以及特别是：

```text
显存 = 96GB?
显存类型 = GDDR7?
位宽 = 512-bit?
显存频率?
实际带宽?
ECC？
PCIe?
CUDA计算能力?
驱动识别?
```

然后再实测大模型的性能：

```bash
vllm serve <模型名称> \
  --tensor-parallel-size 1
```

并测量：

```text
prefill tokens/s
decode tokens/s
显存占用
功耗
温度
长时间运行的稳定性
```

### 我目前的工程判断

我会把速桥的可能设计画成这样：

```text
                    ┌──────────────────┐
                    │      GB202       │
                    │  RTX 5090级别    │
                    └────────┬─────────┘
                             │
                       512-bit总线
                             │
              ┌──────────────┴──────────────┐
              │                             │
       PCB 正面                      PCB 背面
       ┌──────────────┐              ┌──────────────┐
       │  GDDR7      │              │  GDDR7      │
       │  GDDR7      │              │  GDDR7      │
       │  ...        │              │  ...        │
       └──────────────┘              └──────────────┘
              │                             │
              └──────────────┬──────────────┘
                             │
                           96GB
                             │
                       定制VBIOS
```

**这是目前看起来最合理的架构。** 但就目前能看到的报道来说，速桥的具体实现**还没有经过独立验证**，而且Alibaba上自相矛盾的显存规格参数，确实是一个危险信号。（[NeoTeo][4]）

参考链接：

* [Tom's Hardware — 96GB RTX 5090分析](https://www.tomshardware.com/pc-components/gpus/china-modified-nvidia-rtx-5090-with-massive-96gb-of-memory-appears-on-alibaba-for-less-than-usd4-000-3x-more-vram-at-65-percent-the-cost-of-the-original?utm_source=chatgpt.com)
* [The Silicon Report — 对定制PCB/clamshell方案的技术分析](https://www.thesiliconreport.com/articles/blackwell-unleashed-shenzhen-odm-re-engineering-yields-96gb-modified-rtx-5090?utm_source=chatgpt.com)
* [NeoTeo — 规格不一致及验证状况](https://www.neoteo.com/en/alibaba-lists-a-claimed-96gb-geforce-rtx-5090-but-the-hardware-is-unverified?utm_source=chatgpt.com)
* [Igor'sLAB — 技术可行性与注意事项](https://www.igorslab.de/zh/rtx-5090-96gb-vram-alibaba-modification-unconfirmed-zh-cn/?utm_source=chatgpt.com)

我还可以根据RTX PRO 6000/GB202的数据手册，去反推**96GB显存的具体拓扑**，搞清楚速桥到底需要多少颗GDDR7颗粒、多少条总线连接、几层PCB、以及多少个显存通道。

[1]: https://www.tomshardware.com/pc-components/gpus/china-modified-nvidia-rtx-5090-with-massive-96gb-of-memory-appears-on-alibaba-for-less-than-usd4-000-3x-more-vram-at-65-percent-the-cost-of-the-original?utm_source=chatgpt.com “China-modified Nvidia RTX 5090 with massive 96GB of memory appears on Alibaba for less than $4,000 - 3x more VRAM at 65% the cost of the original”
[2]: https://www.thesiliconreport.com/articles/blackwell-unleashed-shenzhen-odm-re-engineering-yields-96gb-modified-rtx-5090?utm_source=chatgpt.com “Blackwell Unleashed: Shenzhen ODM Re-Engineering Yields 96GB Modified RTX 5090 | The Silicon Report”
[3]: https://thesiliconledger.com/industry/chinese-manufacturer-offers-modified-rtx-5090-with-96gb-vram-on-alibaba-for-under-4000?utm_source=chatgpt.com “Chinese Manufacturer Offers Modified RTX 5090 with 96GB VRAM on Alibaba for Under $4,000”
[4]: https://www.neoteo.com/en/alibaba-lists-a-claimed-96gb-geforce-rtx-5090-but-the-hardware-is-unverified?utm_source=chatgpt.com “Alibaba lists a claimed 96GB RTX 5090, but the specs do not add up | NeoTeo”
[5]: https://www.jagatreview.com/2026/09/rtx-5090-dimodifikasi-jadi-96gb/?utm_source=chatgpt.com “RTX 5090 Dimodifikasi Jadi 96GB, Harganya Sekitar Rp68 Jutaan • Jagat Review”