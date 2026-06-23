---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 2000 Ada GPU 状态
translated: true
type: note
---

已连接。以下是 GPU 信息：

  GPU：NVIDIA RTX 2000 Ada Generation  
  VRAM：16 GB（16380 MiB）  
  驱动：580.159.04  |  CUDA：13.0  
  利用率：0%  |  温度：27°C  |  功耗：7W/70W  
  已用显存：2 MiB / 16380 MiB（空闲）  
  持久模式：开启  |  ECC：关闭  

这是一块工作站级的 Ada Lovelace GPU，配备 16 GB 显存——适合使用 LoRA/QLoRA 微调中小型模型、运行量化推理或进行轻量训练。RTX 2000 Ada 基于 AD107 芯片（与 RTX 4060 系列相同），但搭载专业驱动并通过 ISV 认证。目前处于空闲状态，无进程运行。

需要牢记的关键规格：
- 计算能力：8.9（Ada）
- 约 3,072 个 CUDA 核心
- 128 GB/s 内存带宽
- 适合：LoRA 微调 7B-13B 模型（QLoRA）、GGUF 推理、flash-attention 工作负载
- 不适合：大模型的完整微调、多 GPU 重型训练

需要我检查这台机器的其他信息吗（CPU、内存、磁盘、已安装的包）？