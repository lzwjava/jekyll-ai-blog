---
audio: false
generated: true
image: false
lang: en
layout: post
title: Raising MAX_JOBS Risks OOM
translated: false
type: note
---

Question: What happens if you increase `MAX_JOBS` to 16 or 32 when compiling FlashAttention?

Answer: Increasing `MAX_JOBS` to 16 or 32 is the fastest way to speed up this build, but it comes with a major risk: **running out of system memory (RAM) and crashing the compilation.**

Here is a detailed breakdown of what will happen, how to check if your system can handle it, and how to safely optimize it.

---

## The Benefits vs. The Risks

### The Benefit: Massive Speedup

Your build is currently bottlenecked by the CPU processing those 2,525 objects. Moving from 8 to 16 or 32 concurrent jobs allows the compiler to utilize more CPU cores simultaneously. This can easily cut your 30–60 minute build time down to **10–20 minutes**.

### The Risk: The Compiler OOM (Out of Memory) Killer

Compiling AMD Composable Kernel (CK) templates is incredibly RAM-heavy.

* Each HIP compilation job can easily consume **4 GB to 8 GB of RAM**.
* If you set `MAX_JOBS=32`, the compiler could demand up to **128 GB to 256 GB of system RAM** at peak times.

If your host system does not have enough RAM, the Linux kernel's **OOM Killer** will step in and abruptly terminate the compilation process, giving you a vague `Internal compiler error` or `Killed` message.

---

## How to Determine Your Optimal `MAX_JOBS`

Before raising the limit, you need to check your system's hardware capacity. The log you provided actually shows someone starting to check this at the very end (`free -h && nproc`).

Run these two commands in your terminal:

```bash
nproc
free -h

```

### The "Golden Rule" for GPU Compilations

To safely set your jobs, use the following formula:

$$\text{MAX\_JOBS} = \min\left(\text{Total CPU Cores}, \frac{\text{Total RAM in GB}}{6}\right)$$

### Decision Matrix

| Total System RAM | Available CPU Cores | Recommended `MAX_JOBS` | Outcome |
| --- | --- | --- | --- |
| **Less than 64 GB** | Any | **Stick to 8** (or lower) | Safe, but slow. Preventing a crash is worth the wait. |
| **128 GB** | 16 or more | **Set to 16** | Highly recommended. Will roughly double your build speed safely. |
| **256 GB+** | 32 or more | **Set to 32** | Ultimate speed. Cut build time down to a fraction of the original. |

---

## How to Apply the Change Safely

If your hardware passes the RAM check, you can clean the failed/partial build and restart with the higher job count by running:

```bash
# 1. Clean the previous incomplete build artifacts
cd /tmp/flash-attention && rm -rf build/ dist/ *.egg-info

# 2. Activate environment and set the new job limit (e.g., 24 jobs as a safe middle-ground)
source /root/nanochat/.venv/bin/activate
export ROCM_PATH=/opt/rocm-7.2.0
export HIP_PATH=$ROCM_PATH
export PATH=$ROCM_PATH/bin:$PATH
export GPU_ARCHS="gfx942"
export MAX_JOBS=24

# 3. Rerun the installer
python setup.py install 2>&1 | tee /tmp/flash_attn_build3.log

```
