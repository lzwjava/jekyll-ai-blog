---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD Developer Cloud GPU Droplet Guide
translated: false
type: note
---

Question: What is the AMD Developer Cloud GPU Droplet with ROCm 7.2 on Ubuntu 24.04, and what should I know about using it?

Answer:

## AMD Developer Cloud — GPU Droplet Overview

Your droplet (`7.2-gpu-mi300x1-192gb-devcloud-atl1`) is a **single AMD Instinct MI300X GPU instance** hosted in the **ATL1 (Atlanta)** region, powered by the AMD Developer Cloud. Here is everything you need to know:

---

### What It Is

The AMD Developer Cloud is accessible via `devcloud.amd.com` and relies on DigitalOcean for the cloud environment, ultimately deploying GPU Droplets. You can create either a single GPU AMD Instinct MI300X or an 8×GPU Instinct MI300X instance.

Your specific droplet spec:
- **GPU:** 1× AMD Instinct MI300X
- **VRAM:** 192 GB
- **OS:** Ubuntu 24.04 LTS
- **Software Stack:** ROCm 7.2
- **Region:** ATL1 (Atlanta)

---

### ROCm 7.2 — What's It Capable Of

ROCm 7 delivers breakthrough performance gains over its predecessor — training workloads see up to 3× average improvement over ROCm 6 benchmarks, and inference performance increases by an impressive 4.6× on average versus ROCm 6. These gains are powered by improvements in GPU utilization, support for lower precision data types, and optimized data movement.

AMD ROCm is an open software stack including drivers, development tools, and APIs that enable GPU programming from low-level kernel to end-user applications. ROCm is optimized for Generative AI and HPC applications, and it is easy to migrate existing code into ROCm software.

---

### First Steps After Droplet Is Ready

#### 1. Apply the Security Update (as warned in the dashboard)
SSH into your droplet and run:
```bash
sudo apt update && sudo apt upgrade -y
sudo reboot
```

#### 2. Connect via SSH
```bash
ssh root@<your-droplet-ip>
```

#### 3. Verify GPU is Detected
```bash
rocm-smi
```
This is the AMD equivalent of `nvidia-smi`. You'll see GPU utilization, memory usage, and temperature.

#### 4. Enter the Pre-Built Docker Container (if using a Quick Start image)
```bash
docker exec -it rocm /bin/bash
```

---

### Running a Model (e.g., with vLLM)

You can start a vLLM API server inside the container like this:
```bash
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-1.5B-Instruct \
  --host 0.0.0.0 \
  --port 8000 \
  --dtype float16 \
  > /tmp/vllm.log 2>&1 &
```
This model downloads freely from HuggingFace with no authentication, loads in seconds on the MI300X's 192 GB of VRAM, and supports the OpenAI chat format out of the box.

---

### Important: Billing Warning

Even when the droplet is powered off, you are still billed. To stop charges completely, you must **Destroy** the droplet from the dashboard, not just power it off.

Your current status shows **"Turning off / Active"** — this means it is still incurring charges until fully destroyed or you stop using it intentionally.

---

### Pricing Reference

The standard pricing is **$1.99 USD per hour** for the single MI300X instance, or **$15.92 per hour** for the 8× MI300X.

---

### Available Frameworks Out of the Box

Besides being able to deploy with ROCm out-of-the-box, there are also quick start packages offered for JAX, Megatron, PyTorch, SGLang, and vLLM.

---

### Free Credits

The AMD AI Developer Program provides members with $100 of free AMD Developer Cloud credits, which is enough for approximately 50 hours of usage to get started. Members who showcase useful applications and publicly share their projects may also apply for additional credits.

References:

- [How to Get Started on the AMD Developer Cloud](https://www.amd.com/en/developer/resources/technical-articles/2025/how-to-get-started-on-the-amd-developer-cloud-.html)
- [AMD Developer Cloud Tutorial: Host Your First LLM on AMD GPU](https://lablab.ai/ai-tutorials/amd-developer-cloud-host-llm-vllm)
- [Trying Out the AMD Developer Cloud — Phoronix Review](https://www.phoronix.com/review/amd-developer-cloud)
- [Accelerating AI with Open Software: AMD ROCm 7 is Here](https://www.amd.com/en/solutions/data-center/insights/accelerating-ai-with-open-software-amd-rocm-7-is-here.html)
- [OpenClaw on AMD Developer Cloud: Free Deployment with Qwen 3.5 and SGLang](https://www.amd.com/en/developer/resources/technical-articles/2026/openclaw-on-amd-developer-cloud-qwen-3-5-and-sglang.html)
