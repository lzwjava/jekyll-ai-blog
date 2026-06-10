---
audio: false
generated: true
image: false
lang: en
layout: post
title: Distributed Training Launch Command Breakdown
translated: false
type: note
---

**Question:** Explain each argument in this SSH + tmux + torchrun command that launches the master node of a 2-node distributed CPU training run for nanochat.

**Answer:**

This is a layered command: `ssh → tmux → shell → torchrun → base_train`. Breaking it down layer by layer.

## Layer 1 — SSH wrapper

```bash
ssh lzw@<WORKSTATION_IP> "..."
```

Runs the quoted string as a remote shell command on your Ubuntu workstation. The trailing `&& echo OK` prints `OK` only if tmux session creation succeeded — a cheap success signal back to your Mac. The `0.6` at the very end is not part of the command — it looks like a stray paste artifact (possibly a Warp timing annotation or shell history fragment). The shell would treat it as an argument to `echo OK` only if it were inside the quotes; outside, `ssh` would treat it as part of the remote command string only if quoting allowed — as written, it's after the closing quote, so ssh actually receives it as additional remote command text appended with a space, i.e. the remote runs `... && echo OK 0.6`. Harmless, but worth deleting.

## Layer 2 — tmux session management

```bash
tmux kill-session -t dist-master 2>/dev/null
```

Idempotency: kill any prior session named `dist-master` so re-running the command doesn't fail with "duplicate session". `2>/dev/null` swallows the "session not found" error on first run.

```bash
tmux new-session -d -s dist-master '...'
```

- `-d` — detached: create the session but don't attach a terminal to it. Critical because SSH will disconnect; tmux keeps the training process alive (survives the SSH session ending).
- `-s dist-master` — session name, so you can later `tmux attach -t dist-master` to watch live.
- The quoted string is the command the session runs. When it exits, the session dies — hence the `sleep 600` at the end: keeps the pane alive 10 minutes after training finishes so you can attach and read the final output/error before tmux reaps it.

```bash
2>&1 | tee /tmp/dist_master.log
```

Merge stderr into stdout (torchrun and PyTorch log heavily to stderr), then `tee` duplicates the stream to both the tmux pane and a log file you can `tail -f` from another SSH session.

## Layer 3 — Environment variables

| Var | Purpose |
|---|---|
| `NANOCHAT_BASE_DIR=~/.cache/nanochat` | nanochat's root for tokenizer, checkpoints, eval bundles |
| `NANOCHAT_DATA_DIR=.../base_data_small` | Points pretraining at your small FineWeb shard subset instead of the full dataset |
| `NANOCHAT_FORCE_SDPA=1` | Forces PyTorch `scaled_dot_product_attention` instead of FlashAttention — necessary on CPU, where FA kernels don't exist |
| `OMP_NUM_THREADS=8` | Caps OpenMP threads per process for CPU matmuls. Without this, each rank tries to grab all cores; with 2 nodes × 1 proc each, 8 threads avoids oversubscription |
| `PYTHONUNBUFFERED=1` | Disables Python stdout buffering so `tee` and the log file get lines in real time, not in 8KB chunks |
| `GLOO_SOCKET_IFNAME=enp4s0` | Tells the Gloo backend (the CPU collective backend) which network interface to bind. Without it, Gloo may pick `lo` or a Docker bridge and rank 1 can't connect |
| `NCCL_SOCKET_IFNAME=enp4s0` | Same for NCCL — harmless here since CPU training uses Gloo, but cheap insurance if you flip to GPU |

The `IFNAME` pair is the most failure-prone part of multi-node setups. Wrong interface → rendezvous hangs forever at "waiting for workers".

## Layer 4 — torchrun (the launcher)

```bash
torchrun --nnodes=2 --nproc_per_node=1 --node_rank=0 \
  --master_addr=<WORKSTATION_IP> --master_port=29500 \
  -m scripts.base_train -- ...
```

- `--nnodes=2` — world has 2 machines. torchrun blocks until both nodes rendezvous.
- `--nproc_per_node=1` — 1 worker process per machine (1 CPU rank each). Total world size = 2 × 1 = 2.
- `--node_rank=0` — this machine is the master (rank-0 host). Your second machine runs the identical command with `--node_rank=1`.
- `--master_addr` / `--master_port=29500` — the TCP rendezvous point. Rank 0 listens here; rank 1 connects to it. 29500 is the PyTorch convention default. Both nodes must pass the *same* addr/port.
- `-m scripts.base_train` — run the training script as a module (so `scripts/` package imports resolve from the nanochat repo root, which is why the `cd` earlier matters).
- `--` — separator: everything after it goes to `base_train`'s argparse, not torchrun's.

torchrun sets `RANK`, `LOCAL_RANK`, `WORLD_SIZE`, `MASTER_ADDR`, `MASTER_PORT` env vars in each spawned process; `base_train` reads these in its `dist.init_process_group()` call.

## Layer 5 — base_train args (the model & run config)

- `--device-type cpu` — use Gloo backend, no CUDA. This is a plumbing test of distributed training, not a real run.
- `--depth 4` — 4 transformer layers. nanochat derives the rest of the architecture from depth:
- `--aspect-ratio 64` — `model_dim = depth × aspect_ratio = 4 × 64 = 256`. So a 256-dim model.
- `--head-dim 64` — with `model_dim=256`, that's `256/64 = 4` attention heads.
- `--max-seq-len 512` — context length 512 tokens (keeps the attention cost tiny on CPU).
- `--device-batch-size 2` — micro-batch per rank per forward pass: 2 sequences × 512 tokens = 1,024 tokens per step per rank.
- `--total-batch-size 2048` — target tokens per optimizer step. Gradient accumulation is derived: `2048 / (2 ranks × 1024 tokens) = 1` accumulation step. So each optimizer step is exactly one forward/backward per rank, then a Gloo all-reduce.
- `--num-iterations 10` — only 10 optimizer steps. Pure smoke test.
- `--eval-every 5` — run val loss at steps 5 and 10.
- `--eval-tokens 2048` — evaluate on just 2,048 tokens (one tiny val batch).
- `--core-metric-every -1` — disable the CORE benchmark eval entirely (`-1` = never). It's far too expensive for a 10-step CPU run.
- `--sample-every 10` — generate sample text at step 10 so you can eyeball the (gibberish, at this scale) output.
- `--tracker none` — no wandb/logging backend.
- `--run dist-cpu-2node` — run name, used for checkpoint/log directory naming.

## The mental model

The whole thing exists to answer one question: *does my 2-node Gloo rendezvous and gradient all-reduce work over the LAN?* Every model hyperparameter is shrunk to near-zero (depth 4, dim 256, 10 steps) so the run completes in minutes and any failure is a networking failure, not a compute one. Once `OK` prints and the log shows both ranks stepping in lockstep, you swap `--device-type`, the IFNAME backend, and the model size for the real run.

One thing to verify: rank 1's command must match on `--nnodes`, `--master_addr`, `--master_port`, total batch size, and all model args — torchrun won't catch hyperparameter mismatches, and divergent configs across ranks cause silent shape errors or hangs at the first collective.
