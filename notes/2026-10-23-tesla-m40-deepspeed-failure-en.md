---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tesla M40 DeepSpeed Failure
translated: false
type: note
---

🎮 The GPUs — two "supercomputer-class" relics

 Both boxes have exactly one PCIe GPU, both NVIDIA Tesla M40:

 - .34: Tesla M40 (12 GB), driver 580.178.04, "CUDA 13.0"
 - .137: Tesla M40 24 GB, driver 550.163.01, "CUDA 12.4"

 The Tesla M40 is a 2015 Maxwell-architecture datacenter card (GM200, compute capability
 5.2, ~6.8 TFLOPS FP32, no FP16/tensor cores).

 ❌ DeepSpeed: empirically tested — No (and it wedged the driver)

 I installed and tested on .34 with two software generations (total download struggle:
 pypi.org/download.pytorch.org are throttled to 13 KB/s on this CN network, so I routed via
 the Aliyun mirror at 28 MB/s):

 1. Modern stack — PyPI torch 2.14.1+cu130 + DeepSpeed 0.16: torch.cuda.is_available()
    hangs — CUDA ≥12/13 dropped Maxwell entirely.
 2. Legacy stack — torch 1.13.1+cu117 (last CUDA gen supporting Maxwell): CUDA init also
    hangs.
 3. Root cause (syslog): both probes wedged nvidia_uvm in the kernel — stack traces in
    /var/log/syslog show uvm_api_register_gpu → uvm_ioctl →
    thread_context_non_interrupt_add. nvidia-smi itself now hangs too. The driver's UVM
    can't register this GPU, and the hang is in an unkillable D-state.

 ⚠️ Action needed on .34: 3 stuck processes (PIDs 88864 nvidia-smi, 88959, 89100 python)
 are in D-state — kill -9 cannot remove them. Reboot .34 to clear the wedged GPU driver.
 .137 was spared the test (same GPU arch → same verdict).

 ### So, can you train with DeepSpeed? No — not practically:

 - Software wall: DeepSpeed needs a CUDA-capable torch; no modern torch runs on Maxwell,
   and the OS-installed driver here can't even init CUDA compute.
 - Hardware wall even if you downgraded everything (old driver + 2021-era stack): 1
   GPU/node, 12/24 GB VRAM, 4-core i5, 8–11 GB RAM, 1 GbE uplink, and per-GPU compute ≈
   1/12th of a single RTX 4090. DeepSpeed multi-node over 1 GbE would be pointless.

 ### Real options:

 1. Don't use the M40s for training — they're display/legacy cards. Push training to
    anywhere with a modern GPU.
 2. If the hardware must be used: swap in a modern GPU (e.g., RTX 3090/4090) into one of
    these boxes — then DeepSpeed works fine ([.34 has 733 GB free and a 915 GB disk; 12 GB
    RAM would still be limiting for CPU-offload]).
 3. Do GPU inference (not training) with a legacy cu110/cu117 build + old driver — even
    that still needs the driver downgraded (e.g., 470/550 branch that doesn't wedge like
    580 does).

 Notes: I left two venvs on .34 (~/dsvenv ~2.5 GB with broken modern torch, ~/dslegacy with
 torch 1.13.1) plus a ~40 GB uv download cache — free to delete with rm -rf ~/dsvenv
 ~/dslegacy ~/.cache/uv ~/.local/share/uv. Want me to clean those up and/or check anything
 else on .137?
