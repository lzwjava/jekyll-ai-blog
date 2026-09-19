---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVIDIA NCCL Collective Communications Library
translated: false
type: note
---

Here's a comprehensive overview of this project:

## NVIDIA NCCL (NVIDIA Collective Communications Library)

**Location:** `https://github.com/NVIDIA/nccl` — this is the official NVIDIA NCCL repository at version **2.32.3-1**.

### What is NCCL?

**NCCL** (pronounced "Nickel") is a **stand-alone library of standard GPU communication routines** developed by NVIDIA. It implements highly optimized collective communication primitives for multi-GPU and multi-node deep learning workloads.

### Key Capabilities

**Collective Operations implemented:**
- **All-Reduce** – Sum/reduce data across all GPUs and broadcast result back
- **All-Gather** – Gather data from all GPUs to every GPU
- **Reduce** – Reduce data from all GPUs to a single GPU
- **Broadcast** – Broadcast data from one GPU to all others
- **Reduce-Scatter** – Reduce then scatter data chunks
- **Send/Receive** – Point-to-point communication patterns

### Communication Backends (Transports)

The `src/transport/` directory reveals multiple transport layers:
| Transport | Description |
|-----------|-------------|
| **P2P** | Direct GPU peer-to-peer (NVLink, PCIe) |
| **SHM** | Shared memory for intra-node communication |
| **Net IB** | InfiniBand Verbs for RDMA networking |
| **Net Socket** | TCP/IP sockets for networking |
| **Net EFA GDA** | AWS EFA with GPU Direct Async |
| **NVLS** | NVLink Switch (NVSwitch) |
| **NVLS UB** | NVLink Switch Unicast/Broadcast |
| **Multicast** | NVLink multicast |
| **RMA Socket** | RDMA over sockets |

### Key Source Components

| Directory/File | Purpose |
|---------------|---------|
| `src/device/` | GPU kernel code for collectives (CUDA kernels) |
| `src/transport/` | Communication transport layer implementations |
| `src/include/` | Public & internal header files |
| `src/graph/` | Communication graph/topology algorithms |
| `src/tuning/` | Auto-tuning for optimal algorithm selection |
| `src/init.cc` | Core initialization (~169K, largest source file) |
| `src/proxy.cc` | Proxy thread for async operations |
| `src/bootstrap.cc` | Bootstrap network setup |
| `src/collectives.cc` | Collective operation orchestration |
| `src/enqueue/` | Operation enqueue/dequeue mechanisms |
| `src/plugin/` | Plugin system for custom transports/tuners |
| `src/ras/` | Reliability, Availability, Serviceability |
| `src/rma/` | Remote Memory Access |

### Additional Components

- **`bindings/`** – Language bindings (`nccl4py` for Python, `ir` for intermediate representation)
- **`plugins/`** – Plugin implementations for env, net, profiler, tuner, RMA, GIN
- **`contrib/`** – Community contributions (checkpoint, M2N, UBX, Rust bindings, etc.)
- **`docs/`** – Documentation
- **`pkg/`** – Packaging scripts for Debian, RPM, tarball, and Python wheel

### Usage

NCCL is the **de facto standard** for multi-GPU communication in deep learning frameworks like:
- **PyTorch** (via `torch.distributed`)
- **TensorFlow** (via `tf.distribute`)
- **MPI** applications
- **JAX** and other ML frameworks

It's the backbone behind distributed training at scale across thousands of GPUs, enabling operations like gradient all-reduce during `DDP` (Distributed Data Parallel) training.
