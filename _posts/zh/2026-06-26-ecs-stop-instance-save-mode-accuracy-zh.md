---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ECS停止实例保存模式准确性
translated: true
type: note
---

问题：这是对阿里云 ECS“停机不收费”（节省停机模式）计费行为的准确描述吗？

答案：

基本准确，但有两点值得修正。让我验证当前行为。你的描述与阿里云官方文档吻合得很好。以下是逐点验证。

**要点 1 — 停止计费的内容：准确。** 在节省停机模式（原停机不收费）下，计算资源（vCPU 和内存）、固定公网 IP 以及镜像 License 费用停止计费。你提到的“固定公网IP 的固定带宽模式”是正确的——固定公网 IP 的固定带宽费用也会暂停，因为实例规格、固定公网带宽和镜像 License 费用都会暂停。

**要点 2 — 仍然计费的内容：准确。** 系统盘和数据盘、弹性公网 IP（EIP）、快照继续计费。你列出的（系统盘、数据盘、EIP 固定带宽）是正确的。你的描述遗漏了一点：私网 IP 也会保留（不单独计费，但磁盘是真正的成本驱动因素）。

**要点 3 — 重启时的库存风险：准确。** 由于计算资源被回收，重启可能因库存不足或账户欠费而失败；你可以稍后重试或更换实例规格。你的表述一致。

**要点 4 — IP 变化行为：准确，但有一个重要细节。** 由于固定公网 IP 被回收，重启后固定公网 IP 可能会变化，但节省停机模式不会导致私网 IP 变化。你最后一句话是关键正确的洞察：如果需要公网 IP 保持不变，在启用节省停机模式前将固定公网 IP 转为 EIP，因为 ECS 进入此模式时不会释放 EIP——因此预先绑定的 EIP 在停止/启动后保持不变。

**值得补充的一点**（你的文本没有错，只是未提及）：此模式仅适用于 **按量付费和 VPC 网络下的抢占式实例**——计费方式必须是按量付费（包括抢占式实例）；仅支持 VPC 实例，经典网络不支持。同时排除本地盘实例族（d 系列、i 系列）和持久内存实例族（re6p 等）。另外，需要通过控制台/API/CLI 进入——在操作系统内关机/poweroff/halt 不会触发节省停机模式。

触发它的 CLI：

```bash
aliyun ecs StopInstance \
  --RegionId cn-hangzhou \
  --InstanceId <INSTANCE_ID> \
  --StoppedMode StopCharging \
  --ForceStop false
```

结论：你的 4 点总结是准确的。唯一需要完善的是：(a) 私网 IP 会保留，(b) 适用范围仅限于按量付费 + VPC + 非本地盘，(c) 停止前绑定 EIP 是保持公网 IP 稳定的干净方式。

参考文档：

- [节省停机模式（原停机不收费）](https://help.aliyun.com/zh/ecs/user-guide/economical-mode)
- [停机不收费 - 产品概览](https://help.aliyun.com/zh/ecs/product-overview/economical-mode)
- [什么是按量付费计费方式](https://help.aliyun.com/zh/ecs/pay-as-you-go-1)