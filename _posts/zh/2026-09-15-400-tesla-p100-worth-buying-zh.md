---
audio: false
generated: true
image: false
lang: zh
layout: post
title: '¥400 Tesla P100: 值得买吗'
translated: true
type: note
---

**应该买一块二手的 NVIDIA Tesla P100（约 ¥400）吗？**

**答：是的——如果它是 16GB PCIe 版本，而且你只是想把它当作一块便宜的 CUDA/LLM 实验卡。但我*不*建议把它当作正经的现代训练 GPU。**

在 ¥400（约 $55）的价格下，P100 变得很有吸引力。

### 为什么它其实是一块有趣的 ¥400 GPU

P100 16GB 拥有：

*   **16GB HBM2**
*   **732 GB/s 内存带宽**
*   **3584 个 CUDA 核心**
*   ~**9.3–10.6 TFLOPS FP32**
*   ~**18–21 TFLOPS FP16**
*   PCIe 3.0 x16
*   250W TDP
*   计算能力 **6.0**（[GPUPoet][1]）

最吸引人的特性实际上是 **16GB + 732 GB/s，只要 ¥400**。

对于像这样的实验：

```text
CUDA 内核
PyTorch
小型 LLM 推理
量化 7B/8B 模型
嵌入/重排序
vLLM 实验
分布式训练实验
CUDA 扩展开发
```

它是一个相当好玩的玩具。

一个 4-bit 的 ~7B/8B 模型理论上可以塞进 16GB，但上下文/KV 缓存和运行时开销会减少可用容量。（[GetDeploying][2]）

### 但对你来说有一个巨大的陷阱

**Pascal 对于现代 ML 来说太古老了。**

P100 **没有 Tensor Core**，也没有现代的 BF16/TF32/FP8 硬件。这与 V100/A100 及更新的 GPU 有巨大差异。（[GetDeploying][2]）

所以不要这么想：

```text
P100 16GB
    ↓
便宜的 16GB AI GPU
    ↓
优秀的本地训练
```

更准确的说法是：

```text
P100
 ├── 16GB HBM2       ← 优秀
 ├── 732 GB/s         ← 优秀
 ├── CUDA             ← 优秀
 ├── FP32             ← 还行
 ├── FP16 CUDA 核心    ← 还行
 └── Tensor Core      ← 根本没有
```

对于现代 Transformer 训练，缺乏 Tensor Core 使其吸引力大打折扣。

### ¥400 的计算

我目前看到的二手价格五花八门，但 P100 16GB 卡大约在 **$120–170**，有些卖家开价更高；一个追踪器显示二手 P100 起价约 $74。（[GPUPoet][1]）

所以 **¥400 足够便宜，我不太担心转售价值**。

我会这样分类：

| 用途                     |    ¥400 P100 |
| ----------------------- | -----------: |
| CUDA 实验               | 🟢 优秀 |
| 16GB 本地推理           |      🟢 好 |
| 7B/8B 4-bit LLM         |      🟢 好 |
| GPU 编程                | 🟢 优秀 |
| FP32 科学计算           |      🟢 好 |
| Stable Diffusion        |       🟡 一般 |
| 现代 LLM 推理           |      🟡 慢 |
| LLM 微调                |      🔴 差 |
| LLM 训练                | 🔴 很差 |
| BF16 工作负载           |        🔴 不支持 |
| FP8                     |        🔴 不支持 |
| 游戏                    |     🔴 别买 |

### 有一件事我要非常仔细地检查

确保它是：

```text
Tesla P100 16GB PCIe
```

**而不是**

```text
P100 12GB
P100 SXM2
```

SXM2 版本完全是另一种物理形态，不能随便塞进普通 PC。PCIe 16GB 版本才是你想要的。（[Exxact Corporation][3]）

另外记住这些是**被动散热的服务器卡**。NVIDIA 规格标称板卡功耗约 250W，所以你的机箱需要强劲的气流。（[HPE Support][4]）

### 我的结论

**在 ¥400 价位：如果你想要一个 GPU 试验场，那就买。**

鉴于你已经在做 CUDA/模型工作，我实际上认为它值得，具体原因是 **¥400 就能得到 16GB HBM2 + 732GB/s，这是获得另一块 CUDA 设备异常便宜的方式**。

但如果你的实际目标是：

> “我想在 ¥400–1000 范围内获得尽可能多的 AI 算力”

那么我会**根据当地价格，去淘一块二手的 P40 / V100 / 2080 Ti / 3060 12GB / 4060 Ti 16GB 的优惠**。

特别是，**如果你能找到一块 V100 16GB 只贵 ¥600–800 左右，我会毫不犹豫地选 V100 而不是 P100**。V100 增加了 Tensor Core，对于现代深度学习来说有用得多。

### [NVIDIA Tesla P100 16GB](https://studio-supplies.com/products/nvidia-331011867-01-216985?utm_campaign=openai_catalog&utm_content=product_card&utm_medium=feed&variant=51251263537459&utm_source=chatgpt.com)

*$121.22*

### [HPE Tesla P100 16GB](https://www.newegg.com/hpe-proliant-q0e21a-tesla-p100-16gb-graphics-card/p/2VV-002K-00007?item=9SIB1PGJAB1355&negg_topt=1015&utm_campaign=ais_openai_product_feed&utm_medium=ai_search&utm_source=chatgpt.com)

*$167.00*

### [NVIDIA Tesla V100 16GB](https://www.newegg.com/nvidia-tesla-v100-16gb-video-cards-workstation/p/2VV-000H-000P0?item=9SIC6VHKXB9874&negg_topt=1015&utm_campaign=ais_openai_product_feed&utm_medium=ai_search&utm_source=chatgpt.com)

*$799.19*

### [NVIDIA Tesla P40 24GB](https://www.newegg.com/p/2RC-00RS-000K5?item=9SIBT5SKT21966&negg_topt=1015&utm_campaign=ais_openai_product_feed&utm_medium=ai_search&utm_source=chatgpt.com)

*$397.99*

**如果你把具体的 P100 链接/照片/规格发给我，我可以告诉你那块 ¥400 的卡是值得买还是陷阱。**

参考：

*   [NVIDIA Tesla P100 规格](https://www.nvidia.com/?utm_source=chatgpt.com)
*   （[GPUPoet][1]）

[1]: https://gpupoet.com/gpu/learn/card/nvidia-tesla-p100?utm_source=chatgpt.com "NVIDIA Tesla P100 16GB Specs, Benchmarks & Pricing"
[2]: https://getdeploying.com/gpus/nvidia-p100?utm_source=chatgpt.com "P100 Cloud Pricing: Compare 6+ Providers (2026)"
[3]: https://www.exxactcorp.com/blog/HPC/taking-a-look-at-the-nvidia-tesla-p100-gpu-accelerator-for-pcie-servers?utm_source=chatgpt.com "NVIDIA Tesla P100 GPU Accelerator For PCIe Servers"
[4]: https://support.hpe.com/hpesc/public/docDisplay?docId=a00114012en_us&docLocale=en_US&page=NVIDIA_Tesla_P100_GPU_Blade.html&utm_source=chatgpt.com "NVIDIA Tesla P100 GPU Blade | XC50-LC Hardware ..."