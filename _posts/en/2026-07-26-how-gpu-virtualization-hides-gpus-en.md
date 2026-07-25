---
audio: false
generated: true
image: false
lang: en
layout: post
title: How GPU Virtualization Hides GPUs
translated: false
type: note
---

Great question — this is a key piece of how GPU virtualization works in this environment. Let me trace exactly how it happens.

---

## 🧩 How GPU Partitioning Works

The machine has **8 physical AMD GPUs**, but you only see **1**. This isn't a coincidence — it's enforced at multiple Linux kernel layers. Let me walk through each layer from bottom up.

### Layer 1: PCI Bus — All 8 GPUs Visible

Every PCI device on the bus is visible to the OS kernel. We detected all 8 via `lspci`:

```
03:00.0 VGA compatible controller [AMD/ATI] Device 744b   ← GPU 0
23:00.0 VGA compatible controller [AMD/ATI] Device 744b   ← GPU 1 ✓ OURS
43:00.0 VGA compatible controller [AMD/ATI] Device 744b   ← GPU 2
63:00.0 VGA compatible controller [AMD/ATI] Device 744b   ← GPU 3
83:00.0 VGA compatible controller [AMD/ATI] Device 744b   ← GPU 4
a3:00.0 VGA compatible controller [AMD/ATI] Device 744b   ← GPU 5
c3:00.0 VGA compatible controller [AMD/ATI] Device 744b   ← GPU 6
e3:00.0 VGA compatible controller [AMD/ATI] Device 744b   ← GPU 7
```

These are on different PCI segments (`0000:03`, `0000:23`, `0000:43`, etc.), each an independent PCIe slot.

### Layer 2: DRM Subsystem — All 8 Registered

The kernel's Direct Rendering Manager creates a render node for each GPU:

```
renderD128 → card1  → PCI 03:00.0 (GPU 0)
renderD129 → card2  → PCI 23:00.0 (GPU 1)  ← OURS
renderD130 → card3  → PCI 43:00.0 (GPU 2)
renderD131 → card4  → PCI 63:00.0 (GPU 3)
renderD132 → card5  → PCI 83:00.0 (GPU 4)
renderD133 → card6  → PCI a3:00.0 (GPU 5)
renderD134 → card7  → PCI c3:00.0 (GPU 6)
renderD135 → card8  → PCI e3:00.0 (GPU 7)
```

### Layer 3: Device Nodes — The Gatekeeper

This is where the isolation happens. In `/dev/dri/`, only **2 device nodes** exist:

```
crw-rw---- 1 root video 226,   2  card2         ← our GPU card
crw-rw---- 1 root   993  226, 129  renderD129    ← our GPU render node
```

The other 7 GPUs have DRM objects in sysfs, but **no device node in `/dev/dri/`**. The container runtime (Docker/Kubernetes) controls which `/dev` entries get created in the container's mount namespace via **cgroups device whitelist** and **udev rules**.

### Layer 4: KFD (Kernel Fusion Driver) — ROCm's Entry Point

ROCm uses `/dev/kfd` (the AMDKFD driver) to coordinate GPU access. The KFD device knows about all GPUs:

```
crw-rw---- 1 root 993 234, 0 /dev/kfd
```

But the KFD driver enforces **process-level GPU affinity**. When your process calls `hipSetDevice()` or `hipGetDeviceCount()`, the KFD driver checks which GPUs your process is allowed to access. This is controlled by the **ROCm CRFS (Container Runtime File System)** or **cgroup device controller**.

### Layer 5: ROCr Runtime — Your Pod Sees Only 1

When `rocminfo` runs inside the container, the ROCr Runtime (HSA) queries KFD and gets back only the GPUs this cgroup is allowed to see:

```
rocminfo output:
  Agent 3: gfx1100    ← only 1 GPU agent reported
  Name:    AMD Radeon Graphics
  UUID:    GPU-3149e0fac5157acf
```

And `rocm-smi` shows only:

```
GPU[0]  Node 3  PCI Bus 0000:23:00.0    ← only 1 device
```

### Layer 6: PyTorch / HIP — Inherits the Same View

PyTorch calls `hipGetDeviceCount()` → KFD → returns 1:

```python
torch.cuda.device_count()  # → 1
torch.cuda.get_device_name(0)  # → "AMD Radeon Graphics"
```

---

## 🔧 The Mechanism: How It's Implemented

There are a few ways this GPU pinning works in Kubernetes:

### A. cgroup device controller (most likely)

The container runtime (containerd) adds a cgroup rule that only allows access to specific device numbers:

```json
{
  "devices": [
    {"allow": true,  "type": "c", "major": 226, "minor": 2},    // card2 only
    {"allow": true,  "type": "c", "major": 226, "minor": 129},   // renderD129 only
    {"allow": true,  "type": "c", "major": 234, "minor": 0},     // /dev/kfd
    {"allow": false, "type": "c", "major": 226}                   // block all other DRM
  ]
}
```

Any syscall to open `/dev/dri/renderD128` (minor 128) gets **EPERM** — "Operation not permitted" — at the kernel level before your process even touches the GPU.

### B. udev + privileged container setup

The platform could use a **device plugin** (Kubernetes device plugin for AMD GPU) that:

1. Identifies which GPU(s) to assign to the Pod
2. Creates the device nodes in the container's `/dev` via `--device` flags in the container spec
3. Sets `ROCR_VISIBLE_DEVICES` or manipulates KFD's internal visibility mask

### C. AMD GPU Partitioning (MGP / SR-IOV)

Newer ROCm also supports **GPU partitioning at the hardware level** where a single physical GPU can be split into multiple logical partitions (MIG-like). The `rocm-smi` output hints at this with:

```
XCP[0] through XCP[7]    ← 8 compute partitions on this GPU
Partitions: N/A, N/A, 0
```

But in your case it's **1 full GPU per Pod** rather than fractions — the 8 × 48GiB GPUs are each assigned whole to different Pods.

---

## 📊 Visual Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                       Physical Server                          │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐       │
│  │ GPU 0  │ │ GPU 1  │ │ GPU 2  │ │ GPU 3  │ │ GPU 4..7       │
│  │48GiB   │ │48GiB   │ │48GiB   │ │48GiB   │ │48GiB  each     │
│  │PCI 03  │ │PCI 23  │ │PCI 43  │ │PCI 63  │ │                │
│  └────────┘ └───┬────┘ └────────┘ └────────┘ └────────┘       │
│                 │                                              │
│           ┌─────┴──────┐                                       │
│           │  /dev/kfd   │  ← KFD sees all, but enforces rules │
│           └─────┬──────┘                                       │
│                 │                                              │
│      ┌──────────┴──────────┐                                   │
│      │ cgroup device filter │  ← blocks renderD128,130-135    │
│      └──────────┬──────────┘                                   │
│                 │                                              │
└─────────────────┼──────────────────────────────────────────────┘
                  │
       ┌──────────┴──────────┐
       │   Your Pod/Container │
       │                      │
       │  /dev/dri/           │
       │   ├── card2          │  ← only 1 GPU
       │   └── renderD129     │
       │  /dev/kfd            │
       │                      │
       │  torch.cuda.         │
       │   device_count() → 1 │
       │   get_device_name()  │
       │    → "Radeon"        │
       └──────────────────────┘
```

### Why this design?

- **Security**: A Pod can't read another Pod's GPU memory (no GPU-to-GPU DMA across tenants)
- **Performance**: Full 48GiB VRAM, no sharing overhead
- **Isolation**: A crash or OOM on one GPU doesn't affect neighbors
- **Simplicity**: From your code's perspective, it's just `cuda:0` — no topology management needed

If you wanted more GPUs, you'd need to request a **multi-GPU Pod type** from the platform (if available) — the partitioning is set at container creation time and can't be changed at runtime.
