---
audio: false
generated: true
image: false
lang: en
layout: post
title: Multi-Node CPU Training Status
translated: false
type: note
---

Here's a comprehensive summary of what we've accomplished and the current state:

---

## Multi-Node CPU Distributed Training Setup — Status Report

### What We Discovered

**Machine Inventory:**

```
192.168.1.36 (lzw@) — MASTER
  CPU:  i9-13900KF, 24 cores/32 threads
  RAM:  62 GB
  GPU:  RTX 4070 12GB (CUDA)
  Torch: 2.9.1+cu128

192.168.1.47 (xiaoxin@xx) — WORKER
  CPU:  i5-12450H, 8 cores/12 threads
  RAM:  16 GB
  GPU:  Intel UHD (integrated, NO CUDA)
  Torch: 2.9.1+cpu (just installed)
```

**Key Architecture Insight:** Nanochat does NOT use PyTorch's DDP wrapper. Instead, it has a custom `DistMuonAdamW` optimizer that handles gradient synchronization directly using `dist.all_reduce` / `dist.reduce_scatter_tensor` / `dist.all_gather_into_tensor` — a ZeRO-2 style approach.

### Code Patches Applied (3 files)

**1. `nanochat/common.py` — compute_init()**
Added Gloo backend support for CPU DDP:

```python
elif is_ddp_requested and device_type == "cpu":
    device = torch.device("cpu")
    dist.init_process_group(backend="gloo")
    dist.barrier()
```

**2. `nanochat/flash_attention.py` — _resolve_impl()**
Added `NANOCHAT_FORCE_SDPA=1` env var override. Flash Attention is CUDA-only; CPU training must use PyTorch SDPA fallback.

**3. `nanochat/optim.py` — DistMuonAdamW**
Added `_AsyncWorkWrapper` + `_async_op()` helper because Gloo doesn't support `Work.get_future()` (NCCL does). All 5 `.get_future()` calls wrapped:

```python
class _AsyncWorkWrapper:
    def __init__(self, work):
        self._work = work
    def wait(self):
        self._work.wait()

def _async_op(work):
    try:
        return work.get_future()
    except RuntimeError:
        return _AsyncWorkWrapper(work)
```

**4. `nanochat/dataset.py`**
Added `NANOCHAT_DATA_DIR` env var override so both machines can use a shared subset of data shards.

### What Works

**Single-process CPU training on 1.36:** ✅

```
step 00001 | loss: 10.397800 | tok/sec: 45
```

**Single-node 2-process CPU DDP on 1.36 (Gloo):** ✅

```
step 00001 | loss: 10.397759 | tok/sec: 89  (2x speedup!)
```

Gloo connected, gradient sync working, checkpointing works.

### What's Still Needed

**1. Data parity:** Both machines need the same parquet files. Currently:

- 1.36: 201 shards (18GB) in `~/.cache/nanochat/base_data_climbmix/`
- 1.47: 4 shards (352MB) in `~/.cache/nanochat/base_data_climbmix/`
- Created `base_data_small/` symlink dir on 1.36 with 4 shards
- Need to run both with `NANOCHAT_DATA_DIR=~/.cache/nanochat/base_data_small`

**2. Port 29500 access:** The master (1.36) needs port 29500 reachable from 1.47. Verified network connectivity works (SSH port 22 reachable).

**3. Final multi-node test not yet run.** All patches are synced to both machines.

### How to Run Multi-Node

**On 1.36 (master) — terminal 1:**

```bash
cd /mnt/data/nanochat && source .venv/bin/activate
export NANOCHAT_BASE_DIR=~/.cache/nanochat
export NANOCHAT_DATA_DIR=~/.cache/nanochat/base_data_small
export NANOCHAT_FORCE_SDPA=1
export OMP_NUM_THREADS=8
torchrun --nnodes=2 --nproc_per_node=1 --node_rank=0 \
    --master_addr=192.168.1.36 --master_port=29500 \
    -m scripts.base_train -- \
    --device-type cpu --depth 4 --max-seq-len 512 \
    --device-batch-size 2 --total-batch-size 2048 \
    --num-iterations 20 --eval-every 10 --tracker none --run dist-cpu-2node
```

**On 1.47 (worker) — terminal 2:**

```bash
cd ~/projects/nanochat && source .venv/bin/activate
export NANOCHAT_BASE_DIR=~/.cache/nanochat
export NANOCHAT_FORCE_SDPA=1
export OMP_NUM_THREADS=4
torchrun --nnodes=2 --nproc_per_node=1 --node_rank=1 \
    --master_addr=192.168.1.36 --master_port=29500 \
    -m scripts.base_train -- \
    --device-type cpu --depth 4 --max-seq-len 512 \
    --device-batch-size 2 --total-batch-size 2048 \
    --num-iterations 20 --eval-every 10 --tracker none --run dist-cpu-2node
```

**Launch scripts also saved:**

- `/mnt/data/nanochat/run_dist_cpu_master.sh` on 1.36
- `~/projects/nanochat/run_dist_cpu_worker.sh` on 1.47

### Key Learning Points

1. **Backend choice:** NCCL (GPU-to-GPU, high bandwidth) vs Gloo (CPU-to-CPU, works over TCP network)
2. **No DDP wrapper needed:** Nanochat uses custom optimizer-level gradient sync (ZeRO-2 style)
3. **Async ops:** NCCL supports `get_future()` for async communication; Gloo requires synchronous fallback
4. **Flash Attention is CUDA-only:** Must force SDPA fallback for CPU training
5. **torchrun `--` separator:** Script args with `--run` conflict with torchrun's `--run-path`; use `--` to separate
6. **Batch size math:** `total_batch_size` must be divisible by `device_batch_size × seq_len × world_size`
