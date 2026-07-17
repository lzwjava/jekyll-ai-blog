---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA L4 GPU 概述
translated: true
type: note
---

问题：NVIDIA L4 GPU 是什么？

答案：

NVIDIA L4 是一款基于 **Ada Lovelace 架构**（与 RTX 40 系列同代）的 **低功耗数据中心推理 GPU**，主要面向 **AI 推理、视频处理和云工作负载**，而非大规模训练。

![Image](https://images.openai.com/static-rsc-4/S-fImIhGt-Cjj46vXR4rYJRG0aAKn1-r0NFNh2s4yWggwSL1g_lmTA0RlUsX0kz5pYIZLNZChn2RCiXkElTUVvY31bagQYeHFw8_8lHXjk5gj843Q4V740zWy8tmUT2DjcP0Bi0LYuDmWGELY-ZTHwZdheS-N_G6MuUVdqlD8afXEUy5Jpb2QC1jJJ_zwKoC?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/rM0l1u72mZUroI8B0wXYrUZiVqY4VOfNKhl2cLt912oGpp9ZIgR8V8fzOAic6H7XBvekUZlQS5VQzDwPcj_dU1V5mQdvltJAnVX6cXQGoKOSH8io0XLRgVu851IfrcJ6PpCNqpQgtmo0ARikBme3pdqOk6Cu8vpWNJllSKwUEtY4QM2RNzEcZA5bT_m_cHv9?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/mGVGYaU-TvegiPaWqZpGm2LXatOAgiY-l1qDiExOY-cyLO44BRixm1Gw1W7ArRzx2z3qlqJ-CvB4DnVC_EdvzR4Pxjw_E3Ts_Jcjxc5f14op3EZ4C55gq7FNBkzaxFuVhHh7y4z8PxHMlbwqe1Jt3OYVH9m6emQ6HyK3aE5i0_4p8q0AbJ8pnGawRT-P4GdB?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/0BWMw_DjhLMJeOCf1mrrxmKDipJkzIQzY2ZWyZxDEDYwCn-SZLcnmra1Y9nQhcUCEmCyHyNUxLZMPSBlsrZKv0_Ze4mN6q1TL6oNrjAE-_e7s9H1dymgbKnYrBuzKSxRI_sy46PcymAc8HZQs6O1E5H8aH14vd6ti-nk7O8juHw-oWVcEpeal3ILPaGpBDcp?purpose=fullsize)

关键规格：

|                  | NVIDIA L4                   |
| ---------------- | --------------------------- |
| 架构             | Ada Lovelace                |
| GPU 芯片         | AD104                       |
| 显存             | **24GB GDDR6**              |
| 显存带宽         | ~300 GB/s                   |
| Tensor Core      | 第四代                      |
| CUDA Core        | 7,424                       |
| FP32             | ~30 TFLOPS                  |
| FP16 Tensor      | ~242 TFLOPS（含稀疏性）     |
| 功耗             | **72W**                     |
| 外形尺寸         | 被动式单槽 PCIe             |
| PCIe             | Gen4 x16                    |

### 定位

将 L4 理解为：

```
RTX 4070       -> 消费级 AI / 游戏
RTX 4090       -> 消费级高性能推理
L4             -> 云推理服务器
A10            -> 旧款数据中心推理
A100/H100      -> 训练 + 大规模推理
```

L4 本质上是 **RTX 4060/4070 级别 Ada GPU 的服务器版本**，针对以下场景优化：

* 低功耗
* 高密度
* 7×24 小时运行
* 每台服务器可部署多 GPU

---

### AI 推理能力

24GB 显存使其适用于：

* Llama 3 8B
* Qwen 7B/14B
* Mistral 7B
* 嵌入模型
* 重排序模型
* 图像生成（较小模型）

示例：

```
Qwen2.5-14B FP16
14B * 2 字节 ≈ 28GB
```

无法容纳。

但：

```
Qwen2.5-14B INT8
14B * 1 字节 ≈ 14GB
```

可轻松容纳。

配合 vLLM：

```bash
vllm serve Qwen/Qwen2.5-14B-Instruct \
    --quantization awq \
    --gpu-memory-utilization 0.9
```

L4 可服务大量并发用户。

---

### 与你的 RTX 4070 对比

|              | RTX 4070    | L4                 |
| ------------ | ----------- | ------------------ |
| 显存         | 12GB GDDR6X | **24GB GDDR6 ECC** |
| 架构         | Ada         | Ada                |
| 功耗         | 200W        | **72W**            |
| 散热         | 主动风扇    | 被动散热           |
| FP32         | ~29 TFLOPS  | ~30 TFLOPS         |
| AI 推理      | 良好        | 更适合服务器       |
| 训练         | 更好        | 有限               |

有意思的是：原始算力几乎相同。

L4 的优势在于：

```
RTX 4070：
  快速的桌面 GPU

L4：
  同代 GPU +
  2 倍显存 +
  ECC +
  低功耗 +
  数据中心驱动
```

---

### 与 MI50（你的 ROCm 实验）对比

|              | NVIDIA L4  | AMD MI50    |
| ------------ | ---------- | ----------- |
| 发布年份     | 2023       | 2018        |
| 显存         | 24GB GDDR6 | 16GB HBM2   |
| 显存带宽     | 300GB/s    | 1TB/s       |
| FP32         | 30 TFLOPS  | 13.4 TFLOPS |
| AI 生态系统  | CUDA       | ROCm        |
| 功耗         | 72W        | 300W        |

MI50 拥有惊人的显存带宽，但 L4 在现代 LLM 推理中胜出，因为 CUDA + TensorRT/vLLM 生态系统更强大。

---

### 价格视角

典型二手 / 云服务价值：

* L4 云租赁：通常约 **$0.40–1/小时**
* 二手 L4 显卡：约 **$1,000–2,000+ 美元**（视市场情况而定）

对于业余 LLM 项目，二手 RTX 3090（24GB 显存）通常更具性价比：

```
RTX 3090：
  24GB 显存
  ~350W
  二手价格便宜

L4：
  24GB 显存
  72W
  价格昂贵
```

对于数据中心：

```
100 台服务器 × L4
vs
100 台服务器 × RTX 3090

L4 胜出，因为电力 + 密度 + 可靠性。
```

对于你的使用场景（训练 GPT 风格模型、ROCm 实验、本地 LLM 基础设施），L4 的主要吸引力在于 **以极高效的封装提供 24GB 显存**，但二手 RTX 3090/4090 或 A6000 通常是更好的实验用 GPU。
