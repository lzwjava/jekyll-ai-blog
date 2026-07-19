---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为NVLink再买一块RTX 3090
translated: true
type: note
---

问题：如果使用 NVLink，应该购买什么 GPU 而不是添加 RTX 3060？

答案：

对于你的 **i9-13900KF + RTX 4070** 系统，NVLink 彻底改变了答案。

首先：**RTX 4070 不支持 NVLink。**

RTX 40 系列消费级显卡移除了 NVLink：

| GPU         | NVLink 支持 |
| ----------- | ----------- |
| RTX 3090    | ✅ 是        |
| RTX 3090 Ti | ❌ 否        |
| RTX 4090    | ❌ 否        |
| RTX 4080    | ❌ 否        |
| RTX 4070    | ❌ 否        |
| RTX 3060    | ❌ 否        |

因此你不能这样做：

```
RTX 4070 + RTX 3060 + NVLink
```

没有连接器。

---

## 如果你想用 NVLink，再买一块 RTX 3090

现实的二手 AI 配置是：

```
RTX 3090 24GB
+
RTX 3090 24GB
```

搭配 NVLink 桥接器。

![Image](https://images.openai.com/static-rsc-4/IkHwikN9QA4muNyeTGZrzJ2dtez6C-OduZHsv_Yr56HiozSZbiiu297DlmCPLjuu7pzpbR0gFc8bx9JTNFh9O0VjaAD5_3vyqrEY3Y_TEYCO8HQgLTONyqayb8Y2zTrZG1X0eCvlinHucc6R9rQV9nnVU4hKxrkSQd2tJosxevBnWwPem2RHLktVpH6GEiup?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/EZT8aeMW8dhwl8kl1T3f93MFe7rpBXkrmeMHv-OWFNgl-M_t3uE0NobapgIl-bVs_zWu1Fdc9s8vqI-JJP3jnYPq25P7LQ3bbeUmY7h7C56Zm3f-mq_THhjkhsEAlCkn-tX3YxA2yw8whtB1bnBWh0_tFH2V7lkBWw6MEMXlhtVFCYpLWdkvrgcsmVYHvSzk?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/GhDXkJnl1dIyCzfyRpBc9w2Zjm3uhZGGwrgzPm1z7EGrp1t4noVvDc287V7t4fSyWT5C9hzj2zmgU4B_BeJF4B9Be40jpfGW3ReMHiYmwI6VFATEDWq3lP68AzqW1TfMoNo-mR7YVt2fwhBVnIHhtlDzpIBBJIImpgmnM-6Chx5YWwe7iCBK50orWo6Ya8_q?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/I7Vzt-CLMwJ-y2vvlJoD87jeMmZnwXj3cQkZ-gQv11iKyFVXbZrPvlmJAwUUaM2NVePfoBk12WmPRangFF_1TfUgghNR3D-5X-A-I9WjekX5oE6fpzQXR2nXSnnzDXsb0uUmZ3CZ454_RQPRtPMLJX7IP06Nivrie8-SBEa9ZXhUa9Pk1C18a2VEQCWHDem7?purpose=fullsize)

你将得到：

```
GPU 0:
24GB GDDR6X

GPU 1:
24GB GDDR6X

总计:
48GB VRAM
```

NVLink 提供高带宽的 GPU 到 GPU 连接：

```
PCIe:
CPU
 |
PCIe x16
 |
GPU

GPU <-- PCIe --> GPU
```

对比：

```
NVLink:

GPU0 <=======> GPU1
     高带宽
```

这有助于：

* 模型并行推理
* 某些分布式训练
* tensor parallel 负载

---

## 但有一个重要注意事项

NVLink **不会神奇地合并 VRAM**。

这个：

```
2 x RTX 3090

24GB + 24GB
```

不会变成：

```
一个 CUDA 设备，拥有 48GB
```

CUDA 看到的是：

```python
torch.cuda.device_count()

2
```

你需要软件支持：

* DeepSpeed ZeRO
* Megatron-LM tensor parallel
* vLLM tensor parallel
* HuggingFace Accelerate

示例：

```bash
vllm serve Qwen2.5-32B \
 --tensor-parallel-size 2
```

那么：

```
GPU0:
层 0-?

GPU1:
层 ?-?
```

---

## 与 RTX 4070 + RTX 3060 对比

你当前的配置：

```
RTX 4070
12GB
+
RTX 3060
12GB

= 24GB 总计
```

便宜，但：

* 没有 NVLink
* 混合 GPU 代际
* 通信较慢

3090 配对：

```
RTX 3090
24GB
+
RTX 3090
24GB

= 48GB
```

对于 LLM 工作负载来说好得多。

---

## 电源需求

你当前的电源：

```
750W
```

不够。

3090：

```
RTX 3090:
350W

两块:
700W

CPU:
250W

系统:
100W
```

峰值：

```
~1000W
```

你需要：

```
1200W 电源
```

最低要求。

示例：

* Corsair HX1200
* Seasonic PRIME TX-1300
* Super Flower Leadex 1200W

---

## 主板要求

对于双 RTX 3090：

你需要：

```
PCIe 插槽间距：

GPU1
|
3 槽间隙
|
GPU2
```

大多数普通 ATX 主板空间太挤。

更好的选择：

* ASUS ProArt Z790-Creator WiFi
* Gigabyte Z790 AORUS Master
* MSI MEG Z790 ACE

这些主板间距更宽。

---

## 针对你的具体情况

鉴于你已经拥有 RTX 4070：

我**不会**购买 RTX 3060。

选择如下：

### 选项 A — 最便宜的 AI 扩展

```
RTX 4070
+
RTX 3090
```

优点：

* 总计 36GB VRAM
* CUDA
* 一张现代卡 + 一张大显存卡

缺点：

* 没有 NVLink
* 混合 GPU

这可能是最合适的方案。

---

### 选项 B — 认真的本地 LLM 工作站

卖掉 RTX 4070：

```
2 x RTX 3090 24GB
NVLink
```

你将得到：

```
48GB VRAM
```

可以运行：

* Llama 70B 量化版
* Qwen 72B 量化版
* 更大上下文的推理

---

### 选项 C — 保留 RTX 4070

说实话，对于你的工作负载（nanoGPT 训练、LoRA、代理开发），我会这样做：

```
当前:
RTX 4070 12GB

添加:
RTX 3090 24GB
```

总计：

```
36GB VRAM
```

使用：

* RTX 3090 → LLM 推理/训练
* RTX 4070 → 实验/显示

这比 RTX 3060 提供更多价值。

RTX 3090 二手市场存在，正是因为它仍然是获得 **24GB CUDA VRAM** 最便宜的方式之一。