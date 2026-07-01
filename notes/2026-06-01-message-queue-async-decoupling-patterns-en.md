---
audio: false
generated: true
image: false
lang: en
layout: post
title: Message Queue Async Decoupling Patterns
translated: false
type: note
---

**Question:** In distributed systems, what is the core usage pattern of a message queue — specifically that task producers can fire-and-forget, then poll for status/result later, so upstream callers don't block?

**Answer:**

Yes, exactly. That's the fundamental value proposition. Let me be precise about the patterns.

## The Core Pattern: Async Decoupling

Without a queue (synchronous):

```
Producer → [waits...........] → Consumer completes → Producer gets result
```

With a queue (async):

```
Producer → enqueue(task) → gets task_id immediately → goes away
                                    ↓
                             Consumer picks up, processes
                                    ↓
                             Result stored somewhere (DB, Redis, etc.)

Later:
Producer → poll(task_id) → gets result
```

The producer is **never blocked** waiting for the consumer.

## Three Sub-Patterns

### 1. Fire and Forget (no result needed)

```python
queue.publish("send_email", {"to": "user@x.com", "body": "..."})
# done, don't care about result
```

Used for: notifications, logging, analytics events, webhooks.

### 2. Async with Status Polling

```python
task_id = queue.publish("video_transcode", {"file": "input.mp4"})
# return task_id to end user immediately

# user polls later
GET /tasks/{task_id}/status
→ {"status": "processing", "progress": 42}
→ {"status": "done", "result_url": "s3://..."}
```

This is what Celery + Redis does. The task metadata lives in Redis keyed by task_id.

```python
# Celery example
result = transcode_video.delay("input.mp4")  # returns AsyncResult immediately
task_id = result.id  # store this

# later
result = AsyncResult(task_id)
result.state   # PENDING / STARTED / SUCCESS / FAILURE
result.result  # the return value once done
```

### 3. Callback / Webhook (push instead of poll)

```python
queue.publish("ml_inference", {
    "input": data,
    "callback_url": "https://myservice/done"
})
# consumer calls callback_url when finished
```

Avoids polling altogether. Used in payment processors, Stripe webhooks, etc.

## Why This Matters for Distributed Systems

The queue solves several things simultaneously:

| Problem | How queue solves it |
| --- | --- |
| Producer blocks on slow consumer | Decoupled — producer returns immediately |
| Consumer dies mid-task | Message stays in queue (ack-on-complete) |
| Traffic spike | Queue absorbs burst, consumer processes at its rate |
| Multiple consumers | Natural load balancing — whoever's free picks next |
| Retry logic | Dead letter queue + requeue on failure |

## The Ack Mechanism (critical detail)

The reason the producer can "go away" safely:

```
1. Consumer pulls message from queue
2. Queue marks it "in-flight" (not deleted yet)
3. Consumer processes
4. Consumer sends ACK → queue deletes message
   OR
   Consumer crashes → queue timeout → message requeued
```

This gives you **at-least-once delivery** without the producer needing to stay alive.

## Real Stack Example

```
Producer (API handler)
    │
    ▼
RabbitMQ / Kafka / SQS
    │
    ▼
Worker pool (Celery workers, Go routines, etc.)
    │
    ▼
Result backend (Redis / Postgres)
    │
    ▲
Client polls via task_id
```

In your bank AI engineering context — this is exactly how LLM inference jobs, report generation, batch scoring pipelines work. User submits → gets job_id → polls. The LLM call (sometimes 30-60s) never blocks the HTTP layer.
