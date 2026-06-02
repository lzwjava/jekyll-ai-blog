---
audio: false
generated: true
image: false
lang: en
layout: post
title: DigitalOcean GPU Droplet Creation Explained
translated: false
type: note
---

Question: What does the DigitalOcean GPU Droplet creation UI with AMD MI300X and ROCm options mean, and how does each section work?

Answer:

This is the **DigitalOcean GPU Droplet creation interface**, specifically for provisioning cloud-based GPU virtual machines powered by AMD hardware. Here is a full breakdown of every section shown:

---

## 1. What is a GPU Droplet?

DigitalOcean GPU Droplets are virtualized servers with high-performance AMD GPUs, available in both single-GPU and multi-GPU configurations. These instances include local NVMe storage and AI/ML-ready images, allowing users to launch compute environments with pre-installed drivers and frameworks in a few clicks.

---

## 2. GPU Plan — MI300X Options

You are choosing between two hardware configurations, both using the **AMD Instinct MI300X** GPU:

### MI300X x8 (8-GPU Plan)
- 8 GPUs, 1.5 TB total VRAM, 160 vCPU, 1920 GB RAM
- Boot disk: 2 TB NVMe | Scratch disk: 40 TB NVMe
- **$1.99/GPU/hr** (= ~$15.92/hr total for all 8 GPUs)

### MI300X x1 (Single GPU Plan)
- 1 GPU, 192 GB VRAM, 20 vCPU, 240 GB RAM
- Boot disk: 720 GB NVMe | Scratch disk: 5 TB NVMe
- **$1.99/GPU/hr**

The AMD Instinct MI300X's large memory capacity allows it to hold models with hundreds of billions of parameters entirely in memory, reducing the need for model splitting across multiple GPUs.

The MI300X is based on next-generation AMD CDNA 3 architecture, delivering high-level efficiency and performance for the most demanding AI and HPC applications, and was especially optimized for the training and inference of LLM technologies.

---

## 3. Choose an Image

This section lets you pick the operating system and software stack pre-installed on your Droplet.

### Bare OS
- **ROCm Software** — A clean OS with AMD's ROCm driver stack installed. You install any AI tools yourself manually. Best for users who want full control over their environment.

### Quick Start Packages
These are pre-configured Docker-based environments with ready-to-use JupyterLab notebooks, accessible via SSH or browser. Each package bundles ROCm with a specific AI framework:

| Package | Version | Purpose |
|---|---|---|
| **vLLM** | 0.17.1 + ROCm 7.2.0 | Optimized LLM inference and serving |
| **SGLang** | 0.5.9 + ROCm 7.0.0 | LLM inference and serving |
| **PyTorch** | 2.6.0 + ROCm 7.0.0 | General deep learning / model training |
| **Megatron-LM** | 0.10.0 + ROCm 7.0 | Large-scale distributed LLM training |
| **JAX** | 0.4.35 + ROCm 6.4.2 | Large-scale ML training (Google's framework) |
| **ROCm-enabled GPT-OSS** | 120B + ROCm 7 | Run OpenAI's open-weight 120B reasoning model |

ROCm is comparable to NVIDIA's CUDA, including drivers, development tools, and APIs that enable GPU programming from low-level kernel to end-user applications for AMD development. There is a robust ecosystem of ROCm packages growing as AMD GPUs become more prevalent for development, especially around Large Language Models.

---

## 4. SSH Key Authentication

You **must** add an SSH key to create a GPU Droplet. This is a security requirement — GPU Droplets do not support password-based login. An SSH key pair (public + private) allows you to securely connect to your Droplet via terminal after it is provisioned.

If you don't have one, DigitalOcean walks you through generating one.

---

## 5. Pricing Summary

Accessing these GPU Droplets offers competitive pricing at $1.99/GPU per hour, a simple setup process, and enterprise-grade SLAs. While other cloud providers require multiple steps and deep technical knowledge to configure security, storage, and network requirements, DigitalOcean's GPU Droplets can be set up with just a few clicks.

Billing is per-second with a minimum 5-minute round-up. Powered-off Droplets still accrue charges since resources remain reserved, so always destroy droplets when not in use.

---

## When to Choose What

| Use Case | Recommended Option |
|---|---|
| Serve a large LLM via API | vLLM Quick Start |
| Fine-tune or train a model | PyTorch or Megatron |
| Run the GPT-OSS 120B model | ROCm-enabled GPT-OSS |
| Custom setup, full control | Bare OS + ROCm |
| Research / experimentation | JAX or SGLang |

References:

- [Introducing AMD Instinct MI300X GPU Droplets – DigitalOcean Blog](https://www.digitalocean.com/blog/now-available-amd-instinct-mi300x-gpus)
- [Next Generation AI Development with the AMD MI300X – DigitalOcean Community](https://www.digitalocean.com/community/tutorials/amd-gpu-droplets-mi300x)
- [DigitalOcean GPU Droplets Product Page](https://www.digitalocean.com/products/gradient/gpu-droplets)
- [DigitalOcean and AMD Collaborate – Press Release](https://investors.digitalocean.com/news/news-details/2025/DigitalOcean-and-AMD-Collaborate-to-Advance-AI-Using-Cloud-Based-GPUs/default.aspx)
