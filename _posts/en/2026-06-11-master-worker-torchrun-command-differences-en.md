---
audio: false
generated: true
image: false
lang: en
layout: post
title: Master-Worker torchrun Command Differences
translated: false
type: note
---

**Question:** What are the differences between the master-node and worker-node torchrun launch commands in this 2-node CPU distributed nanochat training setup?

**Answer:**

Diff view (master → worker):

```diff
- ssh lzw@<MASTER_IP>          tmux session: dist-master
+ ssh xiaoxin@<WORKER_IP>      tmux session: dist-worker

- cd /mnt/data/nanochat
+ cd ~/projects/nanochat

- export NANOCHAT_DATA_DIR=~/.cache/nanochat/base_data_small
+ (not set on worker)

- export OMP_NUM_THREADS=8
+ export OMP_NUM_THREADS=4

- export GLOO_SOCKET_IFNAME=enp4s0    # wired ethernet
+ export GLOO_SOCKET_IFNAME=wlp3s0    # WiFi

- --node_rank=0
+ --node_rank=1

- tee /tmp/dist_master.log
+ tee /tmp/dist_worker.log
```

Everything else — `--nnodes=2 --nproc_per_node=1 --master_addr --master_port=29500`, and all training args (`--depth 4 --aspect-ratio 64 --head-dim 64 --max-seq-len 512 --device-batch-size 2 --total-batch-size 2048 --num-iterations 10` etc.) — is identical, which is correct: torchrun requires matching world topology and the training script requires matching hyperparameters across ranks.

What each difference means:

1. **`--node_rank=0` vs `1`** — the only torchrun arg that must differ. Rank 0 hosts the rendezvous (TCPStore) at `master_addr:29500`; rank 1 connects to it. Global ranks become 0 and 1 since `nproc_per_node=1`.

2. **`NANOCHAT_DATA_DIR` only on master** — potential bug. In DDP, *every* rank loads its own data shard; nanochat's dataloader uses `ddp_rank` to stride through shards. If the worker falls back to a default data dir that's empty or different, rank 1 will either crash on missing files or train on different data. Check the worker has the same `base_data_small` shards at whatever its default path resolves to (`$NANOCHAT_BASE_DIR/base_data` typically). Safer: set it explicitly on both.

3. **`GLOO_SOCKET_IFNAME` / `NCCL_SOCKET_IFNAME`** — these pin the collective backend to a specific NIC. Master uses wired (`enp4s0`), worker uses WiFi (`wlp3s0`). Since this is `--device-type cpu`, only Gloo matters; `NCCL_SOCKET_IFNAME` is inert here. The WiFi link will be your gradient all-reduce bottleneck — even a tiny depth-4 model syncs every step, and WiFi latency (~2-10ms RTT, plus jitter) will dominate. Expect the wired→WiFi hop to cap throughput well below what either CPU can compute.

4. **`OMP_NUM_THREADS=8` vs `4`** — per-machine tuning for core counts. Fine, but note DDP waits for the slowest rank every step, so the 4-thread worker sets the pace. If the worker box has spare cores, raising this directly speeds up the whole job.

5. **Paths/users/session names** — cosmetic, per-host layout.

Quick sanity check before the next run:

```bash
# verify worker actually has data where it expects
ssh xiaoxin@<WORKER_IP> 'ls ~/.cache/nanochat/base_data* 2>/dev/null | head'
```

If gradient sync over WiFi is killing step time, you can measure it: compare `tok/s` from a single-node run (`--nnodes=1`) on the master vs the 2-node run — the gap is almost entirely Gloo all-reduce over the wireless hop.
