---
audio: false
generated: true
image: false
lang: en
layout: post
title: Per-Second Billing for RunPod GPUs
translated: false
type: note
---

Question: On RunPod, for a single B200 GPU, is billing based on minutes or hours? What's the minimum unit used to calculate cost?

Answer:

RunPod bills per-second, not per-minute or per-hour. The advertised rate is quoted per-hour, but the actual charge accrues by the second for the time your pod is running.

A few specifics that matter for a B200 single-GPU pod:

- **Secure Cloud / Community Cloud pods**: per-second billing while the pod is running. You're charged for the wall-clock time the pod exists in a running state, not for compute utilization. An idle-but-running pod still bills.
- **Stopped pods**: GPU billing stops, but you still pay for the persistent volume/storage (charged per-hour, prorated, even when stopped — and storage on stopped pods can still be billed, so delete the pod if you don't need the disk).
- **Serverless**: billed per-second of actual execution (active workers), which is the more cost-efficient mode for bursty inference.
- **Credit deduction granularity**: balance is deducted continuously; if your balance hits zero, the pod gets stopped/terminated.

So the minimum unit is **1 second**. Practical implication for your workflow: spin up, run the job, and tear down via the API/CLI rather than leaving it parked — a B200 idling for an hour between REPL iterations is real money. Script the lifecycle (`runpodctl` or the GraphQL API) so the pod only exists during active work.

Verify the current B200 hourly rate on the pricing page since GPU rates shift, but the billing granularity (per-second) is stable RunPod policy.

References:

- [RunPod Pricing](https://www.runpod.io/pricing)
- [RunPod Docs — Billing](https://docs.runpod.io/references/billing-information)
