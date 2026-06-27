---
audio: false
generated: true
image: false
lang: en
layout: post
title: Alibaba Cloud Stopped Instance Cost
translated: false
type: note
---

I need to verify current Alibaba Cloud pricing for the resources still billed in economical stop mode (stop-and-save). Let me check.Question: For my stopped Alibaba Cloud ECS instance (Hong Kong, ecs.e-c1m1.large, 2 vCPU / 2 GiB, 5 Mbps BGP bandwidth, 经济停机/economical-stop mode), how much will it cost while stopped?

Answer:

In 节省停机 (economical-stop) mode, here is what stops and what keeps billing for your instance:

**Stops billing (released):**
- vCPU + memory (the `ecs.e-c1m1.large` instance spec)
- Image license
- Fixed public IP and its **fixed-bandwidth (5 Mbps) charge** — this is paused

**Still billing:**
- System disk (cloud disk)
- Any data disks
- EIP (elastic public IP) bandwidth, *if* you converted your fixed IP to an EIP — but you described a fixed BGP IP with fixed-bandwidth mode, so this is **paused, not charged**

So for your specific config, the only thing you keep paying for while stopped is **the cloud disk(s)**.

**Cost estimate — system disk only**

You didn't specify disk size/type, but the default for this instance type is typically a 40 GB ESSD (or cloud_efficiency). Hong Kong pay-as-you-go disk pricing (approximate):

| Disk type | Price | 40 GB / month |
|-----------|-------|---------------|
| ESSD PL0/PL1 | ~¥0.0014/GB/hr | ~¥40/month (~¥1.3/day) |
| cloud_efficiency | ~¥0.00021/GB/hr (~¥0.5/GB/month) | ~¥20/month (~¥0.7/day) |

So roughly **¥0.7–1.3/day (¥20–40/month)** depending on disk type, while stopped.

**To verify exactly:** check your disk type/size in the console (实例详情 → 云盘), then look at the live billing breakdown — the most reliable number is in **费用中心 → 账单详情**, filtered to this instance ID, since it produces an hourly line item per resource.

**Caveat on restart:** because compute is released, you may hit `OperationDenied.NoStock` on start (Hong Kong zone C can be tight), and your fixed public IP will change on next boot (private IP stays the same).

References:

- [什么是按量付费计费方式 — 阿里云](https://help.aliyun.com/zh/ecs/pay-as-you-go-1)
- [节省停机模式 — 阿里云](https://help.aliyun.com/zh/ecs/user-guide/economical-mode)
- [实例规格计费体系成本优化 — 阿里云](https://help.aliyun.com/zh/ecs/instance-types)
