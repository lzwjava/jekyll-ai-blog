---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVLink双RTX 2080 Ti
translated: true
type: note
---

问题：能否在两块RTX 2080 Ti 22GB显卡上使用NVLink？

答案：

可以。**两块RTX 2080 Ti显卡可以使用NVLink**，包括改装后的**22GB显存版本**，因为NVLink的支持取决于**GPU型号和PCB**，而非显存大小。

NVIDIA GeForce RTX 2080 Ti支持**2路NVLink**。

![Image](https://images.openai.com/static-rsc-4/Q5AohIWLm3DzB5MGefwz2qYFyv8lVc8l1eJmw6xeHHbdvX-PZCXfdQoEECMDaODWuX6IVI7qEKNqklK8MflGb-hINGmipYHk6yTQzCmabRVU8lqGYqM6SUueiDiuH8PnfBUeGfOvNh94hPBAzS72Gm8tj46Dw_VqEE99o8KZLFmWheATy0Em52GXbMQEAFZa?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/PGLjHUqkvh4D5p_B2u5VARZN9c5imNj6MAoHMuSfbmmcVrCry_pvPEnE6hvlgGX-QF3xXwJkXIGJ9rilJocQXUhVL55d0zUa_F4fSONGJ6TGWPWfP9AW6fdOVjsDjOcQc1aV9VLAJzJ1FF-60mQL8Vl6YANKw72MXU0hZuRerdb6redFbCb5DZDDIyyxkrx7?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/IRydkpHsizmBbGphPm34Gw8r1Q2vCn47drvjGet7-7F8vwVRKkZqApoLyoMxGLdk9O_dsLqDIVonUHVnyEKzTx6P44MPmySExrjI8BZCCjy727HKA_Wc8fCogI3iWRnsiNJz-mnYFT31Q6_056ecnb-_S1XEpk3MjYnpjBTOXbxYXj7HHMuqhJNu-ie1EeiT?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/I7Vzt-CLMwJ-y2vvlJoD87jeMmZnwXj3cQkZ-gQv11iKyFVXbZrPvlmJAwUUaM2NVePfoBk12WmPRangFF_1TfUgghNR3D-5X-A-I9WjekX5oE6fpzQXR2nXSnnzDXsb0uUmZ3CZ454_RQPRtPMLJX7IP06Nivrie8-SBEa9ZXhUa9Pk1C18a2VEQCWHDem7?purpose=fullsize)

## 硬件设置

你需要：

```
RTX 2080 Ti #1
       ||
       ||  NVLink桥接器
       ||
RTX 2080 Ti #2
```

NVLink桥接器直接连接两块GPU。

规格：

* NVLink代际：Turing NVLink
* 带宽：约50 GB/s（双向）
* 最大GPU数：2（消费级RTX 2080 Ti）
* 仍需PCIe插槽

---

## 但：NVLink不会自动提供44GB显存

这一点非常重要。

很多人认为：

```
22GB + 22GB = 44GB显存
```

不对。对于普通CUDA应用来说：

```
GPU0：
  22GB显存

GPU1：
  22GB显存
```

它们仍然是独立的内存池。

示例：

```python
torch.cuda.device_count()

# 2

torch.cuda.get_device_properties(0).total_memory
# 22GB

torch.cuda.get_device_properties(1).total_memory
# 22GB
```

PyTorch看到的：

```
cuda:0 -> 22GB
cuda:1 -> 22GB
```

---

## 用于LLM推理

框架可以切分模型：

示例：

```
Llama 70B

第0-35层
   GPU0（22GB）

第36-70层
   GPU1（22GB）
```

工具：

* vLLM tensor parallel
* HuggingFace Accelerate
* DeepSpeed inference
* llama.cpp multi-GPU

示例：

```bash
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen3-30B \
    --tensor-parallel-size 2
```

模型被跨GPU分片。

---

## 用于训练

NVLink有帮助，因为GPU之间通信更快：

无NVLink：

```
GPU0
 |
 PCIe
 |
GPU1
```

有NVLink：

```
GPU0
 ||
 || 50GB/s
 ||
GPU1
```

适用于：

* DDP
* tensor parallel
* pipeline parallel

但RTX 2080 Ti不具备：

* NVLink内存池化
* 统一显存
* NVSwitch

---

## 与RTX 3090对比

两块RTX 2080 Ti 22GB：

```
显存：
22 + 22 = 44GB

算力：
2 × 13.4 TFLOPS FP32
≈ 26.8 TFLOPS
```

两块RTX 3090：

```
显存：
24 + 24 = 48GB

算力：
2 × 35.6 TFLOPS FP32
≈ 71 TFLOPS
```

3090还具备：

* Ampere Tensor Core
* BF16支持
* 更快的transformer内核

---

## 对于你的nanoGPT / vLLM实验

一对2080 Ti 22GB实际上挺有意思：

```
2 × RTX 2080 Ti 22GB

显存：
44GB

适合：
✓ QLoRA 7B/14B
✓ 30B-40B量化模型推理
✓ 分布式训练实验
✓ 学习tensor parallel
```

但是：

```
2 × RTX 3090 24GB
```

是家庭AI实验室的最佳选择，因为：

* 48GB显存
* 更快的内核
* BF16
* FlashAttention兼容性

2080 Ti 22GB主要在你以极低价格入手时才具有吸引力。对于学习**LLM系统工程**来说，两块GPU非常有价值，因为你可以用大型集群中相同的思路进行实验：tensor parallelism、pipeline parallelism、NCCL通信以及分布式训练。
