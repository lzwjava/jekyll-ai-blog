---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 2080 Ti 22GB显存模组评测
translated: true
type: note
---

问题：RTX 2080 Ti 22GB显存改装卡怎么样？它是一款好的AI GPU吗？

回答：

这实际上是一个非常有趣的“AI穷人的GPU破解方案”。这个想法是可行的，但存在重要的权衡。

NVIDIA GeForce RTX 2080 Ti官方拥有**11GB GDDR6显存**，但TU102 GPU系列在硬件上具备超越此限制的能力。改装者已经演示了通过添加更高密度的显存芯片并修改BIOS配置，使2080 Ti显卡显示**22GB显存**。（[Tom's Hardware][1]）

架构：

```
RTX 2080 Ti
----------------
GPU: TU102
CUDA核心: 4352
张量核心: 544
显存: 11GB -> 22GB改装
内存: GDDR6
带宽: ~616 GB/s
FP16张量: ~113 TFLOPS（稀疏更低）
PCIe 3.0
```

22GB版本：

```
RTX 2080 Ti 22GB
----------------
相同GPU计算能力
相同内存带宽
容量翻倍
```

含义：

* ✅ 可以加载更大的模型
* ✅ 可以运行11GB无法运行的LLM推理
* ✅ 适合实验
* ❌ 不会使速度翻倍

对于AI工作负载，显存通常是瓶颈。

示例：

RTX 4070：

```
12GB显存
Ada架构
更快的计算
```

RTX 2080 Ti 22GB：

```
22GB显存
较旧的Turing架构
较慢的计算
```

对于LLM推理：

```
Qwen 14B FP16

RTX 4070:
OOM（显存溢出）

2080 Ti 22GB:
可以运行
```

因此2080 Ti因为能容纳模型而胜出。

---

与RTX 3090对比：

|                  | 2080 Ti 22GB    | RTX 3090  |
| ---------------- | --------------- | --------- |
| 显存             | 22GB            | 24GB      |
| 架构             | Turing          | Ampere    |
| CUDA核心         | 4352            | 10496     |
| 张量核心         | 第一代           | 第三代    |
| 内存带宽         | 616GB/s         | 936GB/s   |
| 训练速度         | 约3090的50-60%   | 100%      |
| 价格             | 便宜            | 昂贵      |

对于**LLM推理**，差距较小。

对于**训练**，3090彻底碾压它。

---

有趣的部分是价格。

一年前，一块22GB改装的2080 Ti售价2500元人民币还算合理。如今要看情况。仍然有商家在制造这些显卡，尤其是在中国。（[Reddit][2]）

对于个人AI实验室：

优点：

```
2080 Ti 22GB
+
便宜的AM4/X79机器
+
Linux
+
vLLM / llama.cpp
```

你可以获得：

* 20B-30B量化模型
* LoRA实验
* 嵌入模型
* 小型视觉模型

缺点：

* 完整预训练
* 大批量训练
* 重度CUDA研究

---

对于你这类用途（本地AI实验），我的排名如下：

```
RTX 3090 24GB
    |
    | 最佳平衡
    v

RTX 2080 Ti 22GB
    |
    | 性价比之王（每元显存）
    v

Tesla P40 24GB
    |
    | 便宜但老旧

MI50 16GB
```

考虑到你已经有RTX 4070 + MI50的实验，一块2080 Ti 22GB实际上是一个有趣的“显存扩展卡”。它填补了空白：

```
4070:
快速但仅12GB

2080 Ti 22GB:
慢但显存足够
```

对于OPL（单人实验室）配置，两块异构GPU往往比一块昂贵GPU更有价值：

```
RTX 4070
  - 快速推理
  - 现代CUDA

2080 Ti 22GB
  - 大模型加载
  - LoRA实验

MI50
  - ROCm探索
```

主要风险不在于概念，而在于**卖家质量**。显存重做需要BGA焊接、BIOS测试、热验证。仅当提供了GPU-Z、压力测试和长时间CUDA工作负载截图时再购买。（[Tom's Hardware][1]）

对于AI黑客来说，这张卡基本上相当于购买二手服务器CPU的GPU版本：外观丑陋、效率低下，但每元性能极强。

[1]: https://www.tomshardware.com/news/nvidia-geforce-rtx-2080-ti-22gb-mod?utm_source=chatgpt.com "Nvidia's RTX 2080 Ti Can Be Modded to Support 22GB of GDDR6 Memory | Tom's Hardware"
[2]: https://www.reddit.com/r/LocalLLaMA/comments/1ap8h8q/anyone_tried_a_rtx_2080_ti_22gb/?utm_source=chatgpt.com "Anyone Tried a RTX 2080 Ti 22GB?"