---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 理解RunPod无服务器指标与定价
translated: true
type: note
---

问题：RunPod Serverless 指标的含义是什么？定价如何计算？

回答：

这些数字是您的 **RunPod Serverless endpoint** 的当前状态，而不是您的 API 使用情况。

```
vLLM v2.22.5

$0.00126/s
1 running worker
0 jobs in progress
1 job waiting in queue
```

含义：

| 指标                     | 含义                                                                       |
| ------------------------ | -------------------------------------------------------------------------- |
| **$0.00126/s**           | 您当前为活跃 worker 每秒支付的费用。                                       |
| **1 个运行中的 worker**  | 一个 GPU 容器处于活动状态并正在计费。                                      |
| **0 个进行中的任务**     | 当前没有推理请求正在执行。                                                  |
| **1 个在队列中等待的任务** | 一个请求正在等待，通常是因为 worker 仍在启动或忙碌中。                     |

### Serverless 定价工作原理

与按小时租用 Pod 不同，**Serverless 按 worker 运行时间收费**。

本质上：

```
Cost =
(worker_seconds × GPU price_per_second)
+ storage
+ egress (if applicable)
```

如果您的 endpoint 保持 **1 个 worker 处于热备状态**，即使空闲时您也需要持续付费。

例如：

```
$0.00126/s

每分钟：
0.00126 × 60
= $0.0756

每小时：
0.00126 × 3600
≈ $4.54

24 小时：
≈ $109/天
```

因此，**以该费率保持一个始终运行的 worker 是非常昂贵的**。

### 为什么会有正在运行但没有任务的 worker？

通常是因为您的 endpoint 设置了：

```
min_workers = 1
```

或

```
idle timeout
```

尚未过期。

Worker 保持运行，以便下一个请求几乎具有零冷启动延迟。

### 如果您想几乎不支付费用

配置：

```
min_workers = 0
```

然后：

```
无请求
    ↓
0 个运行中的 worker
    ↓
$0/s
```

缺点是下一个请求必须冷启动一个 GPU 容器，这可能需要 **10–60 秒以上**，具体取决于模型和镜像大小。

### 典型部署选择

| 使用场景        | 推荐配置                            |
| --------------- | ----------------------------------- |
| 个人 API        | `min_workers = 0`                   |
| 低流量          | `min_workers = 0`, autoscale up     |
| 生产环境 API    | `min_workers = 1–2`                 |
| 高流量          | 多个 worker 并启用 autoscaling      |

对于 vLLM 的实验，`min_workers = 0` 通常是最具成本效益的选择，因为您仅在 worker 实际运行时付费。

参考文档：

* RunPod Serverless 文档：[https://docs.runpod.io/serverless](https://docs.runpod.io/serverless)
* RunPod 定价：[https://www.runpod.io/pricing/serverless](https://www.runpod.io/pricing/serverless)
