---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 构建建议：使用Linux，而非MacBook
translated: true
type: note
---

Short answer: **你不需要在4070机器上构建——但MacBook Pro也不是一个好选择。** 理由如下：

## 构建实际需要什么

构建过程本身不会接触到GPU。所有繁重的步骤（DeepEP、MSCCL++、HPC-ops kernels、FlashInfer cubins）要么是**prebuilt wheel downloads**，要么是**nvcc cross-compilation**——nvcc可以在没有GPU的情况下编译CUDA kernels。它*确实*需要的是：

| 要求 | 详情 |
| --- | --- |
| **CPU架构** | 镜像是`linux/amd64`。构建必须生成x86_64镜像 |
| **磁盘** | 可用空间约40–60 GB（此镜像非常大，有多个阶段） |
| **内存** | 建议16 GB以上，用于并行BuildKit阶段 |
| **宿主机** | 装有Docker的Linux（或Docker Desktop / buildx） |

## 为什么MacBook Pro有问题

- **Apple Silicon MacBook Pro（M系列）** = `arm64`主机。构建`amd64`镜像需要通过`buildx --platform linux/amd64`进行QEMU模拟。这个Dockerfile会编译*大量*原生代码——在模拟下需要很多小时，经常超时或OOM，并且模拟下的CUDA/kernel构建很不稳定。强烈不建议。
- **Intel MacBook Pro** = `x86_64`，因此架构匹配。*理论上*可以通过Docker Desktop的Linux虚拟机工作，但仍然很慢，而且你需要一台配置很高的机器。不值得。

## 我建议的替代方案

**选项1（最简单）——拉取预构建镜像。** 该项目发布官方镜像；你完全不需要自己构建：

```bash
docker pull lmsysorg/sglang:latest
# 或者固定版本，例如 lmsysorg/sglang:v0.5.16
```

**选项2——在4070机器（或任何Linux x86_64机器）上构建。** 在你要运行的那台机器上构建是常见且可行的——只要确保它有上述的磁盘/内存。或者在任何Linux x86_64虚拟机（云实例、CI）上构建，然后：

```bash
docker push your-registry/sglang:runtime
# 在4070机器上：
docker pull your-registry/sglang:runtime
```

## 关于RTX 4070的一点

RTX 4070是Ada Lovelace架构（`sm_89`）。镜像中预构建的cubins覆盖了常见的数据中心架构，因此一些kernels（例如FlashInfer、DeepGEMM FP8）会在4070上首次启动时进行**JIT编译**。这正是`runtime`目标保留完整CUDA工具链（`nvcc`）的原因。有两个后果：

- 使用`runtime`目标（正如你计划的那样）——`framework`目标也可以，但更大。
- 首次启动时会较慢，因为JIT kernels需要编译；后续启动会复用缓存（`.cache/sglang`）。

**底线：** 在4070机器或其他Linux amd64机器上构建；除非万不得已，否则跳过MacBook；如果不需要自定义修改，考虑直接拉取`lmsysorg/sglang`。
