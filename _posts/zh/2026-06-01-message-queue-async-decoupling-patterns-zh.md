---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 消息队列异步解耦模式
translated: true
type: note
---

**问题：** 在分布式系统中，消息队列的核心使用模式是什么——特别是任务生产者可以发送后不管，稍后再轮询状态/结果，从而上游调用方不会阻塞？

**回答：**

是的，完全正确。这就是其基本价值主张。让我详细说明这些模式。

## 核心模式：异步解耦

无队列（同步）：

```
生产者 → [等待...........] → 消费者完成 → 生产者获取结果
```

有队列（异步）：

```
生产者 → 入队(任务) → 立即获取 task_id → 离开
                                    ↓
                             消费者取出并处理
                                    ↓
                             结果存储在某个位置（数据库、Redis 等）

稍后：
生产者 → 轮询(task_id) → 获取结果
```

生产者**从不阻塞**等待消费者。

## 三种子模式

### 1. 发送后不管（无需结果）

```python
queue.publish("send_email", {"to": "user@x.com", "body": "..."})
# 完成，不关心结果
```

用于：通知、日志、分析事件、Webhooks。

### 2. 带状态轮询的异步

```python
task_id = queue.publish("video_transcode", {"file": "input.mp4"})
# 立即将 task_id 返回给最终用户

# 用户稍后轮询
GET /tasks/{task_id}/status
→ {"status": "processing", "progress": 42}
→ {"status": "done", "result_url": "s3://..."}
```

这就是 Celery + Redis 的做法。任务元数据以 task_id 为键存储在 Redis 中。

```python
# Celery 示例
result = transcode_video.delay("input.mp4")  # 立即返回 AsyncResult
task_id = result.id  # 存储此值

# 稍后
result = AsyncResult(task_id)
result.state   # PENDING / STARTED / SUCCESS / FAILURE
result.result  # 完成后的返回值
```

### 3. 回调 / Webhook（推模式而非轮询）

```python
queue.publish("ml_inference", {
    "input": data,
    "callback_url": "https://myservice/done"
})
# 消费者完成时调用 callback_url
```

完全避免轮询。用于支付处理器、Stripe Webhooks 等场景。

## 为何这对分布式系统很重要

队列同时解决了多个问题：

| 问题 | 队列如何解决 |
|---|---|
| 生产者因慢消费者而阻塞 | 解耦——生产者立即返回 |
| 消费者在任务执行中崩溃 | 消息保留在队列中（完成后确认） |
| 流量高峰 | 队列吸收突发流量，消费者按自身速率处理 |
| 多个消费者 | 自然负载均衡——谁空闲谁取下一个 |
| 重试逻辑 | 死信队列 + 失败时重新入队 |

## 确认机制（关键细节）

生产者可以安全"离开"的原因：

```
1. 消费者从队列拉取消息
2. 队列标记为"处理中"（暂不删除）
3. 消费者处理
4. 消费者发送 ACK → 队列删除消息
   或者
   消费者崩溃 → 队列超时 → 消息重新入队
```

这提供了**至少一次投递**，且生产者无需保持存活。

## 实际技术栈示例

```
生产者（API 处理器）
    │
    ▼
RabbitMQ / Kafka / SQS
    │
    ▼
工作池（Celery workers、Go routines 等）
    │
    ▼
结果后端（Redis / Postgres）
    │
    ▲
客户端通过 task_id 轮询
```

在你的银行 AI 工程场景中——这正是 LLM 推理任务、报告生成、批量评分流水线的工作方式。用户提交 → 获取 job_id → 轮询。LLM 调用（有时 30-60 秒）永远不会阻塞 HTTP 层。
