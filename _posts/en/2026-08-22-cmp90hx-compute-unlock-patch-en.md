---
audio: false
generated: true
image: false
lang: en
layout: post
title: CMP90HX Compute Unlock Patch
translated: false
type: note
---

**Question:** What does "compute unlock" mean in this repo, and what is the state before and after applying it?

**Answer:**

The **CMP90HX** is NVIDIA's **Crypto Mining Processor** — a GPU variant intentionally crippled for mining only, with its general compute performance (CUDA/tensor compute) artificially restricted at the driver/firmware level. The "compute unlock" is a patch that removes that restriction.

---

**Before the unlock:**

The CMP90HX has nine SM issue-rate limiters applied by NVIDIA's Resource Manager (RM) — covering `DP`, `FFMA`, `FMLA16`, `FMLA32`, `IMLA0`–`IMLA4`. These throttle the GPU's shader/compute throughput, preventing it from being used effectively for CUDA workloads, AI inference, or general GPU computing. The card is only useful for cryptocurrency mining in this state.

---

**What the patch does:**

The project patches NVIDIA Open Kernel Modules driver `580.159.03` to write and read back only the compute-related selectors during a specific validated initialization window, using a temporary "bootstrap" `nvidia.ko`. It does this via a PCIe **bus reset** cycle on each card — unloading the stock driver, loading the patched bootstrap driver to apply the unlock, then reloading the original unmodified driver.

Importantly, it only addresses the compute restriction — it does not modify VRAM capacity, FBPA, LMR, ECC, VBIOS, OTP, or PCIe link speed, and does not port CMP170HX features.

---

**After the unlock:**

The nine SM issue-rate fields are set to their unrestricted values, making the CMP90HX behave like a full compute-capable Ampere GPU (it shares silicon with the GA100/A100 class). After the service completes and the original NVIDIA driver is reloaded, all target cards come back online as normal, and GPU workloads (miners, CUDA programs, containers) can then be started.

**The unlock is not permanent in flash** — it must be re-applied on every cold boot or reboot, which is why a `systemd` service (`cmp90hx-persistent.service`) is installed to run automatically at startup before `multi-user.target`.

---

**References:**
- [bendy2/cmp90hx — GitHub](https://github.com/bendy2/cmp90hx)
