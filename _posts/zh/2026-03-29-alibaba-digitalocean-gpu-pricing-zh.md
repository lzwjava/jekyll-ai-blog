---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 阿里云与 DigitalOcean GPU 价格对比
translated: true
type: note
---

问题：比较阿里巴巴云（Alibaba Cloud）的 GPU gn7i 与 DigitalOcean 的 GPU 价格

回答：Alibaba Cloud 的 **gn7i** 系列和 DigitalOcean 的 **GPU Droplets** 针对不同的市场需求。gn7i 是搭载 NVIDIA A10 GPU 的专业企业级实例，而 DigitalOcean 在收购 Paperspace 后提供了更广泛的高端和中端 GPU 选择。

### **价格对比 (On-Demand)**

| Provider | Instance/GPU Type | GPU Model | vCPU / RAM | Price (Hourly) |
| :--- | :--- | :--- | :--- | :--- |
| **Alibaba Cloud** | `ecs.gn7i-c8g1.2xlarge` | 1x NVIDIA A10 (24GB) | 8 vCPU / 30GB | **$0.78** |
| **Alibaba Cloud** | `ecs.gn7i-c32g1.8xlarge`| 1x NVIDIA A10 (24GB) | 32 vCPU / 188GB| **$0.99** |
| **DigitalOcean** | GPU Droplet | 1x NVIDIA RTX 4000 | 8 vCPU / 32GB | **$0.76** |
| **DigitalOcean** | GPU Droplet | 1x NVIDIA RTX 6000 | 8 vCPU / 64GB | **$1.57** |
| **DigitalOcean** | GPU Droplet | 1x NVIDIA H100 | 20 vCPU / 240GB| **$3.39** |

### **核心差异**

  * **Performance：** **NVIDIA A10** (Alibaba gn7i) 是一款专为 AI inference 和图形工作站设计的企业级显卡，性能介于 DigitalOcean 的 RTX 4000（低端）和 RTX 6000/H100（高端）之间。
  * **Billing Granularity：** Alibaba Cloud 的 Pay-As-You-Go 通常采用按小时计费，但为月度或年度 **Subscriptions** 提供显著折扣（高达 50% 以上）。DigitalOcean 已转向 **per-second billing**（最小 60 秒），对于短周期的 Batch jobs 更具成本效益。
  * **Availability：** Alibaba Cloud gn7i 实例针对亚太地区进行了深度优化。DigitalOcean 的 GPU Droplets 目前在特定的 Data Centers（如 NYC3, AMS3, 和 SFO3）提供，更适合西方市场。
  * **Egress 成本：** DigitalOcean 对于数据密集型任务通常更便宜，超额流量费用约为 **$0.01 per GB**，而 Alibaba Cloud 的国际数据传输费率可能显著更高（根据地区不同，约为 **$0.07 - $0.23 per GB**）。

References:

  - [Alibaba Cloud Elastic GPU Service Pricing](https://www.google.com/search?q=https://www.alibabacloud.com/en/campaign/elastic-gpu)
  - [DigitalOcean GPU Droplet Pricing](https://www.digitalocean.com/pricing/gpu-droplets)
  - [Cloud GPU Pricing Comparison 2026](https://getdeploying.com/gpus)