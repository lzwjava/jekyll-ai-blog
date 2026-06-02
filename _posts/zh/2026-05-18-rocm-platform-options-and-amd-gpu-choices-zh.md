---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ROCm平台选项与AMD GPU选择
translated: true
type: note
---

**问题：** 哪些平台提供 AMD GPU 产品以便运行 ROCm 的平台有哪些？

**答案：**

有多种选择——从 AMD 自家的开发者云，到主流云服务提供商，再到你自己的本地硬件。以下是详细说明：

---

## 1. AMD 开发者云（官方 / 提供免费套餐）

AMD 推出了 **AMD 开发者云**，这是一个完全托管、零配置的环境，可即时访问 AMD Instinct MI300X GPU。借助 GitHub 账户或电子邮件，开发者可在数秒内启动 Jupyter notebook 并开始构建。

这是开始使用 ROCm 最简单、最直接的方式。

---

## 2. 主流云服务提供商（超大规模云）

### Microsoft Azure
Azure 提供 **ND MI300X v5** 虚拟机，搭载 AMD Instinct MI300X GPU，ROCm 与 Azure 无缝集成，可无缝支持强大的 AI 和 HPC 工作负载。此虚拟机上的 AMD Instinct MI300X GPU 能够运行当今庞大的前沿模型——例如，DeepSeek-R1 的全部 671B 参数均可容纳在单台虚拟机中。

### Oracle Cloud Infrastructure (OCI)
OCI 是唯一提供 **裸金属实例**（无虚拟化开销）的主流云服务提供商，支持 AMD GPU。OCI 提供搭载 192 GB 内存的 AMD Instinct **MI300X** GPU，定价为每 GPU 小时 6 美元，极具竞争力。

OCI 是最早采用 AMD 开放式机架规模 AI 基础设施（配备 AMD Instinct **MI355X** GPU）的行业领导者之一，并宣布将提供搭载多达 131,072 个 MI355X GPU 的 zettascale AI 集群。

### AWS
AWS 支持基于 AMD EPYC 的实例，并且是 AMD 广泛云扩展的一部分。不过，对于 ROCm 工作负载，AMD Instinct GPU 专用实例主要通过 Azure 和 OCI 提供。

---

## 3. 专业 / 新兴云服务提供商

**DigitalOcean** 通过其 Gradient AI GPU Droplets 提供 AMD MI300X 和 MI325X GPU，按需定价为 MI300X（单 GPU）每 GPU 小时 1.99 美元。

其他提供商如 **RunPod**、**CoreWeave**、**Lambda Labs** 和 **Vultr** 也越来越多地以具有竞争力的价格提供 AMD Instinct GPU（MI300X、MI350X）及兼容 ROCm 的环境。

---

## 4. 本地 / 本地部署硬件

AMD 已推出 **ROCm 6.4.4** 的公开预览版，该版本在 Windows 和 Linux 上原生支持 **Radeon RX 9000（RDNA 4）** 和 **RX 7000（RDNA 3）** GPU，以及部分 **Ryzen AI 300 "Strix"** 和 **Ryzen AI MAX "Strix Halo"** APU。

Windows 和 Linux 上的 PyTorch 现已作为公开预览版提供，这意味着你可以在 Windows 环境中直接使用 AMD 硬件运行 AI 推理工作负载——无需变通方案，无需双系统启动。

---

## 总结表

| 平台 | AMD GPU | 类型 |
|---|---|---|
| AMD 开发者云 | MI300X | 云（免费套餐） |
| Microsoft Azure（ND MI300X v5） | MI300X | 云虚拟机 |
| Oracle Cloud（OCI） | MI300X、MI355X | 裸金属 / 虚拟机 |
| DigitalOcean Gradient | MI300X、MI325X | 云 GPU Droplets |
| RunPod / CoreWeave / Lambda | MI300X、MI350X | 专业云 |
| 你的个人电脑（Radeon RX 7000/9000） | RDNA 3/4 消费级 GPU | 本地 / 本地部署 |

---

## ROCm 软件栈说明

AMD 已通过 ROCm 6/7 跨越了可行性的门槛——原生 PyTorch wheels、ROCm 容器以及在 vLLM/SGLang 中的上游支持意味着，如果你标准化使用 ROCm 镜像，开源栈能够“第 0 天”即可运行。MI工作。MI300X（192 GB）和 MI350X（288 GB HBM3E）在每 GPU 内存方面达到或超过 NVIDIA，并且越来越被新兴云服务商采用。

**参考资料：**

- [AMD Developer Cloud & ROCm 7 Blog](https://www.amd.com/en/blogs/2025/enabling-the-future-of-ai-introducing-amd-rocm-7-and-the-amd-developer-cloud.html)
- [ROCm on Radeon for Windows and Linux](https://www.amd.com/en/blogs/2025/the-road-to-rocm-on-radeon-for-windows-and-linux.html)
- [Oracle Cloud AMD GPU Offerings](https://www.oracle.com/cloud/compute/gpu/)
- [AMD & Microsoft Azure Partnership](https://www.amd.com/en/blogs/2025/amd-powers-developers-at-build-2025.html)
- [DigitalOcean GPU Platform Comparison](https://www.digitalocean.com/resources/articles/best-cloud-gpu-platforms)
- [State of Cloud GPUs 2025 – dstack](https://dstack.ai/blog/state-of-cloud-gpu-2025/)
