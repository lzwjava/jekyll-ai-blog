---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 华硕H170主板概览
translated: true
type: note
---

问题：**ASUS H170 主板简介**

答案：

![Image](https://images.openai.com/static-rsc-4/HGvWQGRzHHPZcD5asqbaX4UnE_dOvzOfJoD1PD2tqOqUmnf5dp8QD5bSNOfdshFqGKew7t1CWN1t3RJmvHBTUW2tKxFvn6Uc4qBMoUZwXN60vpPi1P9W0mvmX8RZBFoh_k9_FsM_HgFH4DXw_1ga2oKu_3QAi0SxGHmSLLvneh88ldxA-8cLAmta1qVyJnKb?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/N7ibr4zFWwHtQJQV5GL7cBdhnqbHMH79p-VrjsF1t3CVK5ri5PKU_nRxPJjFuLQFOd6kkn4sV1xRTRzO__TtQ5jUaXyuNa_dzMHX8TOkA955STCKGg6S3_MCPsFzG5IjxDD-Gb6LLyr7GGn5_UGOE2Ftv3KCvYT2ZtyQ1RIFNPe2pptjhdZPi5jNIecy8VzD?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/bRKF1Kxyif3PdTAVqdQqntK7OFcR5IhqiTS231-p4KEyAp8ul7ktq7HRR9ZiTuFolJnKxXmxlzwamh5VdGXR20FoUys3OEXGMDVQcZg6LG4cKk0vN-36WfdZ9rXgaJxRqF6GWpsDqmxoeml-YhCXeccvKoho7MPjNSYhN8rFzDAl4Wv3a6O4QM0sKm0Lj9iw?purpose=fullsize)

**ASUS H170 系列**是英特尔 **100 系列主板平台**，大约在 **2015–2016 年**发布，主要面向第 6 代 Skylake CPU。

### 核心规格

| 特性               | ASUS H170                     |
| ------------------- | ----------------------------- |
| CPU 插槽           | **LGA1151**                   |
| CPU 代际           | Intel 第 6 代 Core (Skylake)  |
| 芯片组             | Intel H170                    |
| 内存               | DDR4，通常为 2133 MHz         |
| 内存通道           | 双通道                         |
| CPU 超频           | ❌ 不支持                      |
| 内存超频           | 一般不支持 ❌                  |
| PCIe x16           | 通常为 1 × x16                |
| M.2                | 取决于具体 ASUS 型号           |
| SATA               | 最多 6 × SATA 6 Gb/s          |
| USB                | USB 3.x + USB 2.0             |
| 集成显卡           | 输出接口取决于主板              |
| 板型               | ATX / mATX 取决于型号         |

### CPU 兼容性

有趣的是，H170 使用 **LGA1151** 插槽，因此通常可以搭配以下 CPU：

```text
Celeron G39xx
Pentium G44xx/G45xx
Core i3-6100 / 6300
Core i5-6400 / 6500 / 6600
Core i7-6700
```

部分 ASUS H170 主板在更新 BIOS 后也可支持 **第 7 代 Kaby Lake** CPU，例如：

```text
i7-7700
i5-7500
i3-7100
```

但在确认支持第 7 代之前，应检查**具体的 ASUS 型号 + BIOS 版本**。

### H170 vs B150 vs Z170

三种常见的 100 系列芯片组大致对比如下：

```text
                    H170       B150       Z170
------------------------------------------------
CPU 超频             否          否          是
PCIe CPU 通道数        16         16         16
芯片组 PCIe 通道数     16          8          20
SATA                  6          6          6
M.2                  取决于      取决于      取决于
定位                 中端        入门        发烧友
```

对于你当前的 **GPU 测试/维修工作台**，H170 实际上是一个相当实用的廉价平台。

你不需要一块昂贵的现代主板来测试 GPU：

```text
H170 + 廉价 Skylake CPU
       │
       ├── PCIe x16
       │      │
       │      └── 待测 GPU
       │
       ├── PSU
       ├── RAM
       └── 显示器
```

关键在于拥有一个**已知良好的 PCIe x16 插槽、PSU、CPU 和 RAM**。这可以为你提供一个受控环境，用于区分：

```text
GPU 问题
   vs
主板 PCIe 问题
   vs
电源问题
   vs
CPU/BIOS 问题
```

如果你指的是**某款具体的 ASUS H170 主板**，请发送主板型号标签的照片给我。我可以识别出具体型号，并详细讲解其 **PCIe 插槽、电源接口、前置面板插针、M.2/SATA、BIOS 以及 GPU 测试要点**。

我还可以将一块 H170 主板映射成一个**实用的 GPU 诊断工作台**，并展示如何使用万用表进行测量。
