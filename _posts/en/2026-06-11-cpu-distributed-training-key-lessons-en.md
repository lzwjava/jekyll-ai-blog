---
audio: false
generated: true
image: false
lang: en
layout: post
title: CPU Distributed Training Key Lessons
translated: false
type: note
---

## Key Lessons — Deep Dive

### 1. Gloo vs NCCL: Backend Differences

**What they are:**
- **NCCL** (NVIDIA Collective Communications Library) — GPU-to-GPU, uses NVLink/PCIe/InfiniBand. The default when CUDA is available.
- **Gloo** — CPU-to-CPU, uses TCP sockets. Works on any machine, no GPU required.

**API compatibility gap we hit:**

The `DistMuonAdamW` optimizer in nanochat uses async operations with futures:
```python
# NCCL: this works
work = dist.all_reduce(grad, async_op=True)
future = work.get_future()  # ✅ NCCL supports this
future.wait()

# Gloo: this crashes
work = dist.all_reduce(grad, async_op=True)
future = work.get_future()  # ❌ RuntimeError: Work::getFuture not implemented
```

Gloo's `Work` object doesn't implement `get_future()`. This is because NCCL uses CUDA streams for async overlap (true pipelining), while Gloo uses CPU threads — the abstraction doesn't map 1:1.

**Our fix — a compatibility wrapper:**
```python
class _AsyncWorkWrapper:
    def __init__(self, work):
        self._work = work
    def wait(self):
        self._work.wait()  # synchronous wait on the Work object

def _async_op(work):
    try:
        return work.get_future()  # NCCL path
    except RuntimeError:
        return _AsyncWorkWrapper(work)  # Gloo fallback
```

This preserves the 3-phase async pattern (launch reduces → compute updates → gather results) that `DistMuonAdamW` uses, even though Gloo can't truly overlap communication with computation.

**Other differences:**
- NCCL uses `device_id=device` in `init_process_group()` — Gloo doesn't
- NCCL auto-selects the best transport (NVLink > PCIe > TCP) — Gloo always uses TCP
- NCCL requires all tensors on CUDA — Gloo works with CPU tensors
- NCCL typically achieves 10-100 GB/s — Gloo is limited by network bandwidth (~1 Gbps over WiFi in our case)

---

### 2. torch.compile on CPU: First-Call Latency

**What happens:**
`torch.compile` uses `torch.inductor` to JIT-compile the model's forward pass into optimized C++/Triton code. On GPU, this generates CUDA kernels. On CPU, it generates C++ with vectorized intrinsics (AVX2/AVX-512).

**The cold-start problem:**
```
Step 0: dt=28,386ms  (28 seconds — includes compilation)
Step 1: dt=19,493ms  (still warming up)
Step 2: dt=17,756ms  (stabilizing)
Step 3: dt=17,408ms  (steady state)
Step 4: dt=17,412ms  (steady state)
Step 8: dt=15,681ms  (best)
```

The first call triggers:
1. **TorchDynamo tracing** — captures the Python bytecode into a graph
2. **Inductor lowering** — converts the graph to C++ kernel code
3. **C++ compilation** — compiles with gcc/clang (this is the slow part on CPU)
4. **Kernel caching** — subsequent calls reuse the compiled code

On GPU, Triton compiles CUDA kernels which is also slow (~10-30s), but GPU kernels have simpler compilation pipelines. CPU C++ compilation with AVX vectorization is more complex.

**Why it matters for DDP:** Both ranks must compile independently (each has its own process). If one rank finishes compiling before the other, it blocks at the first collective op until the slow rank catches up. This is why step 0 takes 28s — it's the max of both compilation times.

---

### 3. CPU DDP Throughput Scaling

**Measured results:**
```
Single process (1 rank):  ~45 tok/sec
2 ranks, single node:     ~89 tok/sec  (1.98x speedup)
2 ranks, 2 nodes:         ~134 tok/sec (2.98x speedup)
```

**Why near-perfect scaling for single-node:**
With 2 ranks on the same machine, each rank processes half the data. The gradient sync via Gloo is over loopback (localhost), which is essentially free (~10 GB/s). So you get 2x compute for negligible communication cost.

**Why sub-linear scaling for multi-node:**
With 2 nodes over WiFi, the gradient sync goes over the network:
- Model has ~37M parameters × 4 bytes (float32) = ~148 MB of gradients
- WiFi bandwidth: ~50-100 Mbps effective = ~6-12 MB/s
- Transfer time: ~12-25 seconds per step

But each step takes ~16-17 seconds total. This means the communication is overlapping with computation (the 3-phase async pattern in `DistMuonAdamW`), but there's still some serialization overhead. The 134 tok/sec vs theoretical 90×2=180 tok/sec shows the network bottleneck.

**The scaling formula:**
```
Speedup = N / (1 + α(N-1))
where α = communication_time / computation_time
```
For our case: α ≈ 0.15 (15% of time is communication), giving speedup ≈ 1.75x for 2 nodes.

---

### 4. bf16 Auto-Detection Bug

**The bug:**
```python
def _detect_compute_dtype():
    if torch.cuda.is_available():  # ← checks SYSTEM capability, not training device
        capability = torch.cuda.get_device_capability()
        if capability >= (8, 0):
            return torch.bfloat16, "auto-detected: CUDA SM 89"
    return torch.float32, "auto-detected: no CUDA (CPU/MPS)"
```

On 1.36, `torch.cuda.is_available()` returns `True` (RTX 4070 is installed), even when `--device-type=cpu` is passed. So the compute dtype is set to `bfloat16`.

**Why bf16 on CPU is terrible:**
- CPU doesn't have native bf16 hardware (no AMX/VNNI for bf16 in most CPUs)
- PyTorch emulates bf16 on CPU by casting to float32, computing, then casting back
- This means every matmul does: bf16→fp32→matmul→fp32→bf16 — 2x the memory bandwidth
- The i9-13900KF has AVX-512 for fp32 but no bf16 acceleration
- Result: training hangs or runs at ~0 tok/sec (effectively deadlocked in the emulation layer)

**The fix:**
```bash
export NANOCHAT_DTYPE=float32  # Force fp32, bypass CUDA auto-detection
```

This is a general pitfall when running CPU training on a machine that has a GPU installed. The auto-detection logic assumes "if CUDA is available, use CUDA-optimized dtypes" — but that's wrong when you explicitly request CPU training.

**Broader lesson:** Always check what `COMPUTE_DTYPE` is actually set to when debugging CPU training issues. The banner prints it:
```
COMPUTE_DTYPE: torch.bfloat16 (auto-detected: CUDA SM 89 (bf16 supported))
```
If you see bf16 but you're on CPU, that's your problem.

---

### 5. IPv4/IPv6 Mismatch in Gloo

**The error:**
```
RuntimeError: ss1.ss_family == ss2.ss_family. 10 vs 2
```
(`10` = AF_INET6, `2` = AF_INET)

**Root cause:** Both machines have Tailscale VPN interfaces with IPv6 addresses. When Gloo auto-selects an interface, the master picks the Tailscale interface (IPv6) while the worker picks the WiFi interface (IPv4). They can't communicate because they're using different address families.

**The fix:**
```bash
export GLOO_SOCKET_IFNAME=enp4s0  # Force specific interface on master
export GLOO_SOCKET_IFNAME=wlp3s0  # Force specific interface on worker
```

This pins Gloo to the physical LAN interface on each machine, ensuring both use IPv4 over the same network.

**General rule:** When debugging Gloo connectivity, always check:
1. Both machines can reach each other on the specified interface
2. The firewall allows traffic on that interface (we added `ufw allow from 192.168.1.0/24`)
3. Both machines use the same address family (pin with `GLOO_SOCKET_IFNAME`)
4. `GLOO_IPV6=0` as an additional safety net

---

### 6. Data Parity in Distributed Training

**The problem:** The dataloader shards data by row group index:
```python
rg_idx = ddp_rank       # start at rank
while rg_idx < pf.num_row_groups:
    yield data[rg_idx]
    rg_idx += ddp_world_size  # stride by world_size
```

If one machine has 201 parquet files and another has 4, they read completely different data. The optimizer averages gradients from different datasets, which produces garbage.

**The fix:** Both machines must have identical parquet files. We used `NANOCHAT_DATA_DIR` to point both at a shared 4-shard subset.

**Broader lesson:** In distributed training, data consistency is as important as code consistency. Always verify:
- Same dataset files on all nodes
- Same tokenizer on all nodes
- Same number of shards/row groups
- Same train/val split logic
