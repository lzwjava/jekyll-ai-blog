---
audio: false
generated: true
image: false
lang: en
layout: post
title: ECS Stop Instance Save Mode Accuracy
translated: false
type: note
---

Question: Is this an accurate description of Aliyun (Alibaba Cloud) ECS "Stop Instance with Save Mode" (停机不收费 / 节省停机模式) billing behavior?

Answer:

Mostly accurate, but with two corrections worth flagging. Let me verify the current behavior.Your description matches Aliyun's official docs well. Here's the verification point by point.

**Point 1 — what stops being billed: accurate.** In 节省停机模式 (Economical Mode / formerly 停机不收费), compute resources (vCPU and memory), fixed public IP, and image License fees stop being charged. Your inclusion of "固定公网IP 的固定带宽模式" is correct — the fixed-bandwidth charge on the fixed public IP also pauses, since instance spec, fixed public bandwidth, and image license fees are all suspended.

**Point 2 — what still bills: accurate.** System disk and data disk, elastic public IP (EIP), and snapshots continue to be billed. Your list (系统盘、数据盘、EIP 固定带宽) is right. One thing your description omits: private IP is also retained (not billed as a separate line, but the disks are the real cost driver).

**Point 3 — restart stock risk: accurate.** Because compute resources are reclaimed, restarting may fail due to insufficient inventory or account arrears; you can retry later or switch to a different instance type. Your phrasing matches.

**Point 4 — IP change behavior: accurate, with one important nuance.** Because the fixed public IP is reclaimed, the fixed public IP may change after restart, but Economical Mode does not cause the private IP to change. And your last sentence is the key correct insight: if you need the public IP to stay constant, convert the fixed public IP to an EIP before enabling Economical Mode, because ECS does not release the EIP when entering this mode — so a pre-bound EIP survives the stop/start unchanged.

**The one caveat worth adding** (not wrong in your text, just unstated): this mode only applies to **pay-as-you-go (按量付费) and spot instances on VPC networks** — billing method must be pay-as-you-go (including spot instances); only VPC instances are supported, classic network is not. It also excludes local-disk families (d-series, i-series) and persistent-memory families (re6p, etc.). And entering it requires console/API/CLI — an in-OS shutdown/poweroff/halt will not trigger Economical Mode.

CLI to trigger it:

```bash
aliyun ecs StopInstance \
  --RegionId cn-hangzhou \
  --InstanceId <​INSTANCE_ID> \
  --StoppedMode StopCharging \
  --ForceStop false
```

Verdict: your 4-point summary is accurate. The only refinements are (a) private IP is retained, (b) scope is pay-as-you-go + VPC + non-local-disk only, and (c) EIP-before-stop is the clean way to keep a stable public IP.

References:

- [节省停机模式（原停机不收费）](https://help.aliyun.com/zh/ecs/user-guide/economical-mode)
- [停机不收费 - 产品概览](https://help.aliyun.com/zh/ecs/product-overview/economical-mode)
- [什么是按量付费计费方式](https://help.aliyun.com/zh/ecs/pay-as-you-go-1)
