---
audio: false
generated: true
image: false
lang: en
layout: post
title: Runpod hourly to monthly cost
translated: false
type: note
---

**Question:** If a Runpod instance costs **$0.24 per hour**, how much does it cost per week and per month?

**Answer:**

Assuming the instance runs **24 hours a day**:

| Time Period      | Calculation |        Cost |
| ---------------- | ----------- | ----------: |
| 1 hour           | $0.24 × 1   |   **$0.24** |
| 1 day (24 hours) | $0.24 × 24  |   **$5.76** |
| 1 week (7 days)  | $5.76 × 7   |  **$40.32** |
| 30-day month     | $5.76 × 30  | **$172.80** |
| 31-day month     | $5.76 × 31  | **$178.56** |

### If you don't run it continuously

* **8 hours/day:** $0.24 × 8 × 30 = **$57.60/month**
* **12 hours/day:** $0.24 × 12 × 30 = **$86.40/month**
* **16 hours/day:** $0.24 × 16 × 30 = **$115.20/month**

For Runpod, remember that:

* **Compute charges** stop when the pod is stopped.
* **Storage (volume) charges** usually continue even when the pod is stopped, so your total monthly bill may be slightly higher than the compute cost alone if you keep persistent storage attached.