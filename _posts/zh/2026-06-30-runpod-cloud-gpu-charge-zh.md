---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Runpod云GPU收费
translated: true
type: note
---

问题：2026年6月29日有一笔20美元的扣款，商户是RUNPOD.IO MOORESTOWN US，请问这是哪家公司？

回答：

这笔费用来自 **Runpod**，一家为AI工作负载提供云GPU服务的供应商。总部位于美国新泽西州穆尔斯敦，成立于2022年，是一个以开发者优先的市场平台——这与您账单上显示的"MOORESTOWN US"描述相符。

与您的技术栈相关，他们的服务包括：

- **Pods** —— 专用于开发/训练/微调的GPU实例，完全控制容器、驱动和运行环境。30秒内启动，按秒计费，无出站流量费用。
- **Serverless** —— 自动伸缩的推理端点，可缩至零实例，FlashBoot实现低于200毫秒的冷启动。
- **Clusters** —— 多节点分布式训练（800–3200 Gbps互连）。

定价参考：GPU起步价$0.24/小时，按需配置平均约$1.33/小时，提供39种GPU类型（4090、L40S、A100、H100、B200）。社区云（对等提供商，便宜约20–30%）与安全云（企业级可用性）两种模式。他们获得了由Summit Partners领投的1亿美元融资，并在2026年突破了100万开发者用户。

这20美元的费用几乎可以肯定是**充值**——Runpod采用预付费余额模式，20美元是默认的最小自动/手动充值金额。如果您没有主动发起，请检查账户账单中的自动充值设置；如果是您自己充的，那这就是您预付费的计算余额。鉴于您在使用AMD MI300X和RTX 4070运行训练任务，这笔钱很可能是您（或自动充值）为Runpod实例补充资金，用于NVIDIA方面的实验。

如果您完全不认识这笔扣款，建议：登录runpod.io → 账单 → 查看交易记录并关闭自动充值，然后如果怀疑账户被盗，请轮换所有API密钥。

参考来源：

- [Runpod GPU定价与评测 — gpus.io](https://gpus.io/en/providers/runpod)
- [Runpod云GPU实例](https://www.runpod.io/product/cloud-gpus)
- [Runpod达到100万开发者用户](https://www.runpod.io/blog/one-million-developers)