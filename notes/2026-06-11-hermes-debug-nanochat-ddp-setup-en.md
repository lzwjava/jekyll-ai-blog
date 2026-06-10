---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Hermes Debug: Nanochat DDP Setup"
translated: false
type: note
---

**Question:** Summarize this Hermes agent log — what were the key steps, and how did the agent fix each problem while setting up multi-node CPU DDP training for nanochat?

**Answer:**

## Goal

Run nanochat `base_train` across two machines over LAN using PyTorch distributed with the **Gloo** backend (CPU-only DDP): master = workstation (i9-13900KF, 24 cores), worker = laptop (i5-12450H, 8 cores). Stock nanochat assumes CUDA + NCCL, so several layers needed patching.

## Key steps

**1. Environment setup on the worker (slowest part, mostly waiting)**

- Installed `torch==2.9.1+cpu` from the PyTorch index, then the rest of the deps. Two gotchas:
  - LAN node's network to PyPI was slow → moved pip to `nohup ... &` background jobs, killed duplicate pip processes, polled the log.
  - `--index-url https://download.pytorch.org/whl/cpu` doesn't host `datasets`/`pyarrow` etc. → had to split into two installs (torch from PyTorch index, the rest from PyPI).

**2. Patch #1 — `common.py` `compute_init()`: backend selection**

Stock code only had the NCCL path. The agent added a CPU branch:

```python
if is_ddp_requested and device_type == "cuda":
    device = torch.device("cuda", ddp_local_rank)
    torch.cuda.set_device(device)
    dist.init_process_group(backend="nccl", device_id=device)
elif is_ddp_requested and device_type == "cpu":
    device = torch.device("cpu")
    dist.init_process_group(backend="gloo")   # TCP-based, CPU collectives
dist.barrier()
```

**3. Key architectural discovery — no DDP wrapper needed**

The agent grepped for `DistributedDataParallel` and found nanochat doesn't use it. Gradient sync lives inside the custom `DistMuonAdamW` optimizer (ZeRO-2 style: `reduce_scatter` grads, shard optimizer state, `all_gather` params). So the only "make it distributed" change needed was the process-group init above — a genuinely nice insight about Karpathy's design.

**4. Launch scripts** — wrote `torchrun` master/worker scripts (`--nnodes=2 --node_rank=0/1 --master_addr=<MASTER_IP> --master_port=29500`), rsync'd code from master to worker.

**5. Side fires put out along the way**

- rsync brought over a uv-created `.venv` pinned to the wrong Python → deleted and recreated with system `python3 -m venv`.
- HuggingFace unreachable from the worker (China network) → killed the stuck `dataset.py` download and rsync'd 4 parquet shards (~352 MB) from the master instead. Tokenizer dir synced too — both nodes must have identical tokenizer/data.

## The three real bugs and their fixes

**Bug 1 — torchrun argument collision.** `--run=...` was swallowed by torchrun itself. Fix: separate launcher args from script args with `--`:

```bash
torchrun --nnodes=2 ... -m scripts.base_train -- --device-type cpu --run test-cpu-ddp
```

**Bug 2 — Flash Attention selected on CPU run.** `_resolve_impl()` in `flash_attention.py` chose FA2 based on `torch.cuda.is_available()` — true on the master (it has a GPU) even though training device was CPU → `flash_attn::_flash_attn_forward` blew up. Fix: an env-var escape hatch checked first:

```python
def _resolve_impl():
    if os.environ.get("NANOCHAT_FORCE_SDPA", "").lower() in ("1", "true", "yes"):
        return "sdpa"
    ...
```

Then `export NANOCHAT_FORCE_SDPA=1` in both launch scripts. (Note: the agent's first attempt was a mangled multi-line `sed -i` that it had to clean up with a Python patch script — a recurring pattern; sed kept failing on multi-line edits and Python `str.replace`/regex saved it each time.)

**Bug 3 — Gloo doesn't implement `Work.get_future()`.** `DistMuonAdamW` overlaps comm/compute via `dist.reduce_scatter(..., async_op=True).get_future()`. NCCL supports `get_future()`; Gloo raises `RuntimeError: Work::getFuture not implemented`. Fix: a compatibility shim wrapping the `Work` handle:

```python
class _AsyncWorkWrapper:
    def __init__(self, work): self._work = work
    def wait(self):
        self._work.wait()
        return None

def _async_op(work):
    try:
        return work.get_future()      # NCCL
    except RuntimeError:
        return _AsyncWorkWrapper(work)  # Gloo fallback
```

All 5 `.get_future()` call sites became `_async_op(dist.xxx(..., async_op=True))`.

## Result

Single-node 2-rank Gloo DDP validated on the master: **45 tok/s (1 rank) → 89 tok/s (2 ranks)** — near-linear scaling, proving gradient sync through the patched optimizer works. The log ends with patched code rsync'd to the worker and deps reinstalling there; the actual 2-node run hadn't fired yet.

## Takeaways worth keeping

1. **Backend API parity is the real porting cost**: NCCL→Gloo isn't just a string swap — `get_future()`, `device_id=`, and dtype support differ.
2. **Hardware-detection ≠ run-device**: `torch.cuda.is_available()` is the wrong predicate when the user explicitly requested CPU; dispatch on the actual device.
3. **Custom-optimizer DDP (à la Muon)** means you only touch process-group init + collectives in the optimizer — no model wrapping.
4. The agent's weakest tool was multi-line `sed`; every nontrivial edit ended up as a heredoc'd Python script. Worth wiring your agents to prefer AST/string-replace patching over sed from the start.
