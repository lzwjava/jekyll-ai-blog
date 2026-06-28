---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RunPod GPU的按秒计费
translated: true
type: note
---

问题：在RunPod上，单个B200 GPU的计费是按分钟还是小时？计算成本的最小单位是什么？

答案：

RunPod按秒计费，而非按分钟或小时。广告中标注的费率是每小时报价，但实际费用会根据Pod运行时间按秒累计。

对于单个B200 GPU的Pod，有几个关键细节：

- **Secure Cloud / Community Cloud Pods**：Pod运行时按秒计费。收费基于Pod处于运行状态的挂钟时间，而非计算利用率。即使空闲但仍在运行的Pod也会产生费用。
- **已停止的Pod**：GPU计费停止，但仍需为持久卷/存储付费（即使停止状态也按小时按比例收费——停止的Pod上的存储仍可能产生费用，因此如果不需要磁盘，请删除Pod）。
- **Serverless**：按实际执行时间（活跃worker）按秒计费，这是处理突发推理任务时更具成本效益的模式。
- **积分扣除粒度**：余额会持续扣除；若余额归零，Pod将停止/终止。

因此最小单位是**1秒**。对你的工作流实际影响：通过API/CLI启动、运行任务并拆除，而非让其闲置——B200在REPL迭代之间空转一小时就是真金白银。请编写脚本（使用`runpodctl`或GraphQL API）管理Pod生命周期，确保Pod仅在活跃工作时存在。

当前B200的小时费率请查看定价页面，因为GPU费率会变动，但计费粒度（按秒）是RunPod的稳定策略。

参考：

- [RunPod定价](https://www.runpod.io/pricing)
- [RunPod文档——计费](https://docs.runpod.io/references/billing-information)
