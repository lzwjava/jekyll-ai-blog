---
audio: false
generated: true
image: false
lang: en
layout: post
title: Runpod Cloud GPU Charge
translated: false
type: note
---

Question: What company is RUNPOD.IO MOORESTOWN US, the merchant on a USD 20 charge dated 2026-06-29?

Answer:

That charge is from **Runpod**, a cloud GPU provider for AI workloads. Headquartered in Moorestown, NJ, founded in 2022, developer-first marketplace — which matches the "MOORESTOWN US" descriptor on your statement.

What they do, relevant to your stack:

- **Pods** — dedicated GPU instances for dev/training/fine-tuning, full control over container, drivers, environment. Spin up in under 30 seconds, billed by the second, no egress fees.
- **Serverless** — autoscaling inference endpoints, scale to zero, FlashBoot for sub-200ms cold starts.
- **Clusters** — multi-node distributed training (800–3200 Gbps interconnect).

Pricing context: pricing starts at $0.24/GPU-hour, averaging ~$1.33 across on-demand configs, with 39 GPU types (4090, L40S, A100, H100, B200). Community Cloud (peer providers, ~20–30% cheaper) vs Secure Cloud (enterprise uptime). They raised $100M led by Summit Partners and crossed one million developers in 2026.

The USD 20 charge is almost certainly a **credit top-up** — Runpod runs on a prepaid balance model, and $20 is the default minimum auto-load/manual top-up amount. If you didn't initiate it, check your account's auto-reload setting in billing; if you did, it's just your prepaid compute balance. Given you run training workloads on AMD MI300X and RTX 4070, this is likely you (or auto-reload) funding a Runpod pod for NVIDIA-side experiments.

If you don't recognize it at all, the move is: log into runpod.io → Billing → check transaction history and disable auto-reload, then rotate any API keys if you suspect account compromise.

References:

- [Runpod GPU Pricing & Review — gpus.io](https://gpus.io/en/providers/runpod)
- [Runpod Cloud GPU Instances](https://www.runpod.io/product/cloud-gpus)
- [One Million Developers on Runpod](https://www.runpod.io/blog/one-million-developers)
