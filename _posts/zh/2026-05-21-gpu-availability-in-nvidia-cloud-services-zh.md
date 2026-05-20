---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA 云服务中的 GPU 可用性
translated: true
type: note
---

Question: 如果 AMD 有开发者云，是否存在类似的 NVIDIA 云，并且其 GPU 可用性是否更高？

Answer:

是的，NVIDIA 提供类似于 AMD 开发者云的云服务。主要的 NVIDIA 云服务包括 **NVIDIA DGX Cloud**、**NVIDIA GPU Cloud (NGC)**，以及通过主流云提供商（如 **AWS、Azure 和 Google Cloud**）提供的 GPU 访问，这些提供商提供 NVIDIA GPU（A100、H100 等）用于 AI 和 HPC 工作负载。

关于 **GPU 可用性**：

* **NVIDIA GPU** 在云服务中通常更广泛可用，因为 NVIDIA 在 AI 和 HPC 领域拥有更大的市场份额。这意味着你通常能找到更多实例类型、区域和并发可用性。
* **AMD GPU** 的存在感正在增长，但在云服务中仍较少。AMD 的 MI 系列（如 MI300X）目前仅限于特定云（如 AMD 开发者云）或本地部署。
* 可用性还取决于**区域、订阅类型和需求**。热门 NVIDIA GPU（A100/H100）在高需求时段可能会遇到排队情况。

因此，如果你的优先级是**更容易获取和更多选择**，NVIDIA 云解决方案通常提供更高的可用性和灵活性。AMD 云则更为细分，但对于特定的 MI300X 工作负载仍然不错。

参考来源：

* [NVIDIA GPU Cloud (NGC)](https://www.nvidia.com/en-us/gpu-cloud/)
* [AWS EC2 GPU 实例](https://aws.amazon.com/ec2/instance-types/gpu/)
* [AMD 开发者云](https://developer.amd.com/amd-developer-cloud/)