---
audio: false
generated: true
image: false
lang: en
layout: post
title: How to List RTX 4070 on RunPod
translated: false
type: note
---

**Question:** How do I list my RTX 4070 GPU machine on RunPod so others can rent it?

**Answer:**

RunPod has a **Secure Cloud** (their own DCs) and **Community Cloud** (your hardware). You want the Community Cloud host program.

## Requirements

- Linux host (Ubuntu 20.04+ recommended)
- Static or stable public IP
- Docker installed
- NVIDIA drivers + `nvidia-container-toolkit`
- Ports open: `22`, `8888`, `2222`, `443`, and a range for pod forwarding

## Steps

### 1. Install RunPod host daemon

```bash
# Install dependencies
curl -fsSL https://get.docker.com | sh
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list \
  | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# Verify GPU visible to Docker
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
```

### 2. Sign up as a host on RunPod

Go to: <https://www.runpod.io/console/host/machines> → **"List a GPU"**

You'll need:

- RunPod account with billing/payout setup (Stripe)
- Your machine's public IP

### 3. Run the host agent

RunPod gives you a one-liner after registration — looks like:

```bash
sudo docker run -d \
  --name runpod-host \
  --restart always \
  --privileged \
  --network host \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e RUNPOD_API_KEY=<API_KEY> \
  runpod/host-agent:latest
```

### 4. Configure pricing

In the dashboard, set:

- **GPU price** ($/hr) — RTX 4070 community cloud goes ~$0.15–0.25/hr currently
- **Disk price**
- **Min/Max pod duration**

### 5. Firewall rules (ufw example)

```bash
sudo ufw allow 22/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8888/tcp
sudo ufw allow 2222/tcp
sudo ufw allow 40000:60000/tcp  # pod port forwarding range
```

## Caveats for Your Setup

| Issue | Detail |
|---|---|
| **Home ISP** | Most residential ISPs block inbound ports or use CGNAT — check if you have a real public IP with `curl ifconfig.me` and test inbound connectivity |
| **Dynamic IP** | Use a DDNS service or pay for static IP; RunPod needs stable routing |
| **Uptime expectation** | Renters expect availability — RunPod tracks your uptime score |
| **RTX 4070 12GB** | Competes well for inference workloads (Mistral 7B, SDXL, Whisper) but won't attract training jobs |
| **Bandwidth** | You pay egress on your home connection — high-bandwidth pods will eat your quota |

## Honest Assessment

For a **home machine on residential internet**, RunPod hosting is marginal:

- CGNAT / dynamic IP is the biggest blocker
- Revenue on a 4070 is low (~$2–5/day max if 100% utilized, rarely happens)
- Your workstation at `192.168.1.36` is more valuable to you for local dev + your own inference

If you want passive GPU income, **Vast.ai** is often easier to set up for community hosting and has lower friction than RunPod for home hosts.

```bash
# Check if you have a real public IP (not CGNAT)
curl ifconfig.me
# Then check if port 22 is reachable from outside:
# Use https://portchecker.co or ask someone to nc -zv <your_ip> 22
```

**References:**

- [RunPod Community Cloud Host Docs](https://docs.runpod.io/hosting/overview)
- [Vast.ai Host Setup](https://vast.ai/docs/hosting/setup)
