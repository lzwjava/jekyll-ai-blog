---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding RunPod Serverless Metrics and Pricing
translated: false
type: note
---

Question: What do the RunPod Serverless metrics mean, and how is pricing calculated?

Answer:

Those numbers are the current state of your **RunPod Serverless endpoint**, not your API usage.

```
vLLM v2.22.5

$0.00126/s
1 running worker
0 jobs in progress
1 job waiting in queue
```

Meaning:

| Metric                     | Meaning                                                                       |
| -------------------------- | ----------------------------------------------------------------------------- |
| **$0.00126/s**             | What you're currently paying **per second** for active workers.               |
| **1 running worker**       | One GPU container is alive and billing.                                       |
| **0 jobs in progress**     | No inference request is currently executing.                                  |
| **1 job waiting in queue** | One request is waiting, usually because the worker is still starting or busy. |

### How Serverless pricing works

Unlike renting a Pod by the hour, **Serverless charges for worker runtime**.

Essentially:

```
Cost =
(worker_seconds × GPU price_per_second)
+ storage
+ egress (if applicable)
```

If your endpoint keeps **1 worker warm**, you pay continuously even when idle.

For example:

```
$0.00126/s

Per minute:
0.00126 × 60
= $0.0756

Per hour:
0.00126 × 3600
≈ $4.54

24 hours:
≈ $109/day
```

So **one always-on worker at that rate is quite expensive**.

### Why is there a running worker with no jobs?

Usually because your endpoint has:

```
min_workers = 1
```

or

```
idle timeout
```

hasn't expired yet.

The worker stays alive so the next request has almost zero cold-start latency.

### If you want to pay almost nothing

Configure:

```
min_workers = 0
```

Then:

```
No requests
    ↓
0 running workers
    ↓
$0/s
```

The downside is the next request must cold-start a GPU container, which can take anywhere from **10–60+ seconds**, depending on the model and image size.

### Typical deployment choices

| Use case       | Recommended configuration         |
| -------------- | --------------------------------- |
| Personal API   | `min_workers = 0`                 |
| Low traffic    | `min_workers = 0`, autoscale up   |
| Production API | `min_workers = 1–2`               |
| High traffic   | Multiple workers with autoscaling |

For experimenting with vLLM, `min_workers = 0` is usually the most cost-effective option because you only pay while a worker is actually running.

References:

* RunPod Serverless documentation: [https://docs.runpod.io/serverless](https://docs.runpod.io/serverless)
* RunPod pricing: [https://www.runpod.io/pricing/serverless](https://www.runpod.io/pricing/serverless)