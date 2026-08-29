---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 诊断和修复损坏的GPU
translated: true
type: note
---

问：**从二手/闲鱼显卡学习NVIDIA GPU维修的最佳方法是什么？我应该直接买坏卡动手修吗？**

答：**是的。对你来说，我绝对推荐动手学习。** 但不要一开始就随意加热芯片。把每块坏GPU都当作一次**诊断实验**。

最快的路径是：

```text
便宜的报废GPU
      ↓
目视检查
      ↓
电阻测量
      ↓
理解电源轨
      ↓
受控上电
      ↓
电压测量
      ↓
找到故障元件
      ↓
更换元件
      ↓
测试
      ↓
记录学到的内容
```

一个良好的GPU维修流程本质上是**电子电路调试**，而不是“GPU魔法”。专业的诊断流程从电阻检查、目测、电源轨测量、受控上电开始，然后才是热风枪/示波器操作。（[YouTube][1]）

### 1. 购买合适的坏卡

不要从昂贵的4090/5090开始。

我会在闲鱼上购买**GTX 10系列 → RTX 20系列 → RTX 30系列**的坏卡。

特别留意：

* `不亮`
* `无显示`
* `核心供电短路`
* `12V短路`
* `维修过`
* `烧供电`
* `掉件`
* `显存报错`
* 明确标注为`坏卡`的显卡

避免卖家声称：

> “GPU核心可能坏了”

这类卡是不好的学习板，因为你很难证明到底是什么问题。

相比之下，一块MOSFET烧毁、电容缺失、电源轨短路、接口损坏的卡更有学习价值。

---

### 2. 你的首要目标不是“修复”

你的首要目标应该是：

> **面对一块死掉的GPU，我能否从电气角度解释它为什么不工作？**

例如：

```text
GPU无法上电
       ↓
12V输入？
       ↓
12V → VRM？
       ↓
3.3V辅助供电？
       ↓
1.8V？
       ↓
PEX？
       ↓
Vcore？
       ↓
显存供电轨？
       ↓
BIOS？
       ↓
GPU初始化？
```

这比学习“更换这个MOSFET”有价值得多。

Learn Electronics Repair 的优秀长篇GPU维修指南几乎完全遵循这个流程：目视检查 → 电阻 → 电压 → 实际电压诊断 → GPU初始化问题。（[YouTube][1]）

---

### 3. 深入学习VRM

这可能是你的**第一要务**。

典型的GPU核心VRM大致如下：

```text
12V
 │
 ├── 上管MOSFET
 │
 ├── 下管MOSFET
 │
 ▼
 电感
 │
 ├──── VCORE
 │
 └──── 电容
```

包含多个相位：

```text
             ┌─ MOSFET ─ MOSFET ─ 电感 ─┐
12V ─────────┼─ MOSFET ─ MOSFET ─ 电感 ─┼── VCORE
             ├─ MOSFET ─ MOSFET ─ 电感 ─┤
             └─ MOSFET ─ MOSFET ─ 电感 ─┘
```

然后学习：

* 上管/下管MOSFET
* 栅极
* 源极
* 漏极
* PWM控制器
* 栅极驱动器
* 电感
* 输出电容
* 使能信号
* Power Good
* 反馈
* 电流检测

一旦掌握了这个电路，GPU维修就不再那么神秘了。

---

### 4. 从第一天开始使用原理图+BoardView

这是你应该发挥工程背景的地方。

**原理图告诉你：**

```text
什么连接什么
```

**BoardView告诉你：**

```text
它在物理上的位置
```

这是一个针对现代GPU的极其强大的组合。（[RC4BD][2]）

例如：

```text
原理图：

PVDD_GPU
   ↓
PUxxx
   ↓
Qxxx
   ↓
FBxxx
   ↓
NVVDD
```

然后BoardView：

```text
FBxxx → PCB上的物理位置
```

现在你的万用表探头有了目标。

有专门的GPU boardview数据库/工具可用；例如，GPU Doctor 目前提供涵盖500多种GPU型号的NVIDIA/AMD boardview。（[GPU Doctor][3]）

---

### 5. 建立维修笔记

这将极大地加速你的学习。

对于每块GPU：

```text
GPU: RTX 2060
PCB: MS-Vxxx

症状：
无显示

初始电阻：

12V PCIe:       正常
3.3V:           正常
VCORE:          0.8 Ω
Vmem:           35 Ω
PEX:            18 Ω

上电后：

12V:            12.1V
3.3V:            3.3V
1.8V:            1.8V
Vmem:            1.35V
Vcore:           0V

诊断：
Vcore VRM未启动

下一步：
检查PWM EN
检查VCC
检查栅极信号
```

然后：

```text
更换了：xxx MOSFET
结果：Vcore = 0.75V
GPU启动
```

在20-30块板子之后，你将拥有自己的**GPU故障数据库**。

这比观看100个维修视频有价值得多。

---

### 6. 不要立即购买示波器

我会按以下顺序：

```text
万用表
    ↓
可调电源
    ↓
热风枪 + 烙铁
    ↓
显微镜
    ↓
热成像仪
    ↓
示波器
```

前四样工具就能解决大量问题。

基本GPU维修设备通常包括万用表、热风枪、焊台和可调电源，显微镜/BGA设备稍后才有用。（[Cnblogs][4]）

你的工程背景可能会让你比普通初学者更快遇到万用表的极限。那时，示波器对以下场景会非常有用：

```text
PWM
栅极驱动
时钟
复位
PCIe信号
使能
电源时序
```

---

### 7. 系统性地处理短路

这大概是我会有意训练的第一项主要技能。

假设：

```text
12V → 对地短路
```

不要立即注入电源并碰运气。

追踪：

```text
12V
 │
 ├── VRM #1
 ├── VRM #2
 ├── VRM #3
 ├── 滤波
 ├── 保护
 └── 其他电路
```

然后隔离各部分。

对于VRM：

```text
12V
 ↓
MOSFET
 ↓
电感
 ↓
VCORE
```

如果VCORE短路：

```text
是GPU核心短路吗？
       还是
MOSFET？
       还是
电容？
       还是
其他负载？
```

这种区分才是真正的维修技能。

---

### 8. 不要一开始就学BGA植球

我建议**避免一开始就做GPU核心植球/核心更换/显存更换**。

这些看起来很诱人，因为看起来很酷：

```text
加热GPU
↓
取下GPU
↓
植球
↓
安装
↓
祈祷
```

但如果卡突然好了，你学到的很少。

相反：

```text
找到短路
→ 识别元件
→ 更换元件
→ 验证电源轨
→ 启动
```

这样你的理解才会不断积累。

之后：

```text
显存
↓
GDDR6
↓
GDDR6X
↓
GPU BGA
↓
核心更换
```

---

## 我个人会这样安排你的前10张卡

| 卡片   | 目标                                  |
| ------ | ------------------------------------- |
| 1–2    | 学习PCB布局 + 万用表                  |
| 3–4    | 寻找短路                              |
| 5–6    | 诊断VRM                              |
| 7      | BIOS / SPI                            |
| 8      | 显存供电 / 显存                       |
| 9      | 无显示时序                            |
| 10     | 不看教程独立诊断                      |

而且**不要在意是否成功修复了全部10张**。

如果第3张卡永久报废，但你能够解释：

> “这个MOSFET失效，导致PVDD短路，进而阻止了VRM启动。”

这已经是成功的学习经验了。

---

## 一个重要原则

不要让实验变成：

```text
坏GPU
↓
加热所有东西
↓
更换MOSFET
↓
更换显存
↓
重新植球GPU
↓
仍然不工作
```

而应该是：

```text
观察
    ↓
假设
    ↓
测量
    ↓
更新假设
    ↓
维修
    ↓
测量
```

本质上就是**科学方法 + 电路分析**。

鉴于你已经熟悉计算机、GPU、Linux、CUDA/ROCm和硬件，我认为这个爱好特别适合你：你不是从零开始学电子，而是将**调试直觉应用到物理电路**。

![Image](https://images.openai.com/static-rsc-4/-8ve_1Mtsf4-iXxohmG_lFElZwTdFdE-qDKcadcLASp4fmtfTQHU1FfMhCigJgPJCfSN4nzPfwL8lqpusB0jAvGaecldd5CbgsG_wOqs_dCPqLFIghdN--1E4dxt1yw_XqBLaW8F5UTOek6EurG0d3D0EWM0WXHZu4hBVzA-Ba5NZTfZzfizHGITotJezRKA?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/nLMC9ujWUn4v1U7p_o3S4e2q3G59SBokeHJNlwDQCzfhrbva7eMRL_bFN1hXz1KL0OJ5bm5f0JmrJ6srcj5Hirn8p8Z3GkJdu2iggbRVHBPo7JL1xwTP-Ha627A4bL3FTDq-RsSyQuJhHVuRRL_bH3II7huLuOae259eLmybQdQOjtfEfmD9YoseH7euFLHk?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/F1rlULV95gBsDlLu1hEmprAqibWSZdMLeaFUx-RZt7cr-BP9X0LAC9XVNsOI4Q7Oz7JdqkJ8dT1FVZSNbuXbFb3OBccZwyb7VilOZQNRiDB979hFPQsfVuOXyU007eVFZ34zmSGfqNsXpYx17tsYck9r9oqCURsrAZvwYM1U-9fPYtwWUgtMFn0UcfVEMPg2?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/GgA0r3eNMt4UoxAtttbz4uxVRMObc6ZYp90AGgUwK4dDGKGVCWA4lN3mfHxszo2Zoc7Z9zpt27_xr2zh5IIDK7qiOQjXR010yqfSDmZL6gPpFU9rnmbayJ4DE4DS4vVcSNxf7hi9rdqditYIpv0bgwDati6IquLOmr-XzCzYZbUBXwXqz29lUrDLM-gdFlz2?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/NZ6nx18tb9sDyP22U5_yyBmBjQ_8UCiR1rXcTBrZClmvZkgggJZyk7wH1akIjau5RkMbnv4iA8XoAKb6pFUHQisSuG9sMptZhYjzf2VuLhXJa0BPCjyFLK0E8ngUcWJ3tV4PSayyMYpHtIgXxiKxZWCUA0qh5dfBDam2Ghd0J5qi3wdNUWf30U2ULVhW5hiG?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/NgsjMF_001ZP-aefXFTxz-mPDdLh6U1E4ZMI_NXrw0Ez3WwKXuRjw8m9fUpBnmoQsp3ENmCbFKZ8Hvd0CUVCsoegcNZZNRWySttQ_77pW89_Iz_w6zjq-EG158d0sBKesWM_mKArdy7AptG60kiYLQbfHEcIoP-MWEtic_Rr6q2HjKP0zmRBi1hUTLzwSs_9?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/9SV7SwNUO8yXQZOj4lCoX_cM1EsWesIlcSB3VH7gc1YxTJWxtYcr3snxYB6LN1xnLkSgqiz6e_FyBwUavPZobOF_17CnIpGZI_9_UEs1rDHIrr-ZLjk8FDlWuqOXR2leyV4O4ApkYAdC-XfFVMcEr28Iw1SB4s3cV6GLLaFzG0By0n7Nc8MtovnZIfD6oWrk?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/TE2ZdqwuxyvIvSFtBoYdLvpDa3bPexLFwtJGSUbprfyz-0gWLJSDBMt9dMulvu7Q5UbxD56oOExY8PWjrTAcDL31biIzhDn1sPDUQbIV8Bnh4X4Mwnrz9WoZEoS0FOwouHZ5Ew3k9BbKGo_Hhq2YmfQdT2-TE6wpZdQSiyX19i4O7eXC4b0aKjo_blWtv9S-?purpose=fullsize)

### 最佳入门资源

* [Learn Electronics Repair — GPU维修指南](https://www.youtube.com/watch?v=SmVdl8kew_4&utm_source=chatgpt.com) — 可能是最好的单篇长视频入门点；它明确地讲解了电阻和电压诊断。（[YouTube][1]）
* [GPU维修Wiki / 社区资源](https://www.reddit.com/r/GPURepair/?utm_source=chatgpt.com) — 当你开始发布实际测量数据和症状时非常有用。
* [GPU Doctor BoardView](https://gpudoctor.com/boardview?utm_source=chatgpt.com) — 有助于学习将原理图参考映射到物理PCB位置。（[GPU Doctor][3]）

**所以是的：去买闲鱼上坏的GPU，直接动手吧——但要让每张卡都成为一个受控的调试实验，而不是热风枪实验。**

[1]: https://www.youtube.com/watch?v=SmVdl8kew_4&utm_source=chatgpt.com "GPU维修指南。如何修复GPU/显卡不被检测到。AMD Radeon或Nvidia - YouTube"
[2]: https://rc4bd.com/motherboard-schematic-and-boardview-guide/?utm_source=chatgpt.com "维修技术员用的主板原理图和板图指南"
[3]: https://gpudoctor.com/boardview?utm_source=chatgpt.com "BoardView查看器——交互式GPU PCB浏览器 | GPU Doctor | GPU维修专家"
[4]: https://www.cnblogs.com/maojun1998/p/16474059.html?utm_source=chatgpt.com "GPU维修资源列表（原理图、板图、教程、工具等） - maojun1998 - 博客园"
