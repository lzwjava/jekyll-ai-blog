---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Distributed Training with PyTorch DDP
translated: false
type: note
---

### Overview of Karpathy's Explanation

In his YouTube video "Let's build GPT: from scratch, in code, spelled out" (starting around the 2-hour 58-minute mark), Andrej Karpathy dives into distributed training for large language models using PyTorch. He focuses on scaling a single-GPU training loop across multiple GPUs (e.g., 8) without major code changes. The core idea is to run **identical processes** on each GPU, each handling a non-overlapping shard of the data, and synchronize gradients via averaging. This enables effective batch sizes that are multiples of the per-GPU batch size. He emphasizes simplicity, using PyTorch's DistributedDataParallel (DDP) module, and walks through code examples for a GPT-2-like model.

Karpathy uses an analogy: Imagine a team of researchers (GPUs) independently analyzing different parts of a dataset but periodically "comparing notes" (gradient averaging) to align on the solution. He launches training with `torchrun --standalone --nproc_per_node=8 train_gpt2.py`, which automatically sets environment variables like `RANK`, `WORLD_SIZE`, and `LOCAL_RANK`.

### Distributed Training

Karpathy explains distributed training as a way to parallelize across GPUs while keeping the core forward/backward pass mostly unchanged:

- Launch one process per GPU (e.g., 8 processes for 8 GPUs).
- Each process runs the **same model code** but on a **unique slice** of the dataset (sharded by rank).
- After the backward pass, gradients are **averaged across all processes** (via all-reduce operation) and applied to every model copy, mimicking a single large-batch update.
- Key benefit: Overlaps communication (gradient sync) with computation (backward pass) for efficiency.
- Data sharding: For a batch, start index = `rank * batch_size * seq_len`, stepping by `batch_size * seq_len * world_size`. Use the same random seed across processes for consistent ordering, but slice differently.
- For variable-length inputs (e.g., options in evaluation), pad to the max length in the batch and apply a mask to ignore padding in loss computation.

He notes: "The forward is unchanged and backward is mostly unchanged and we’re tacking on this average."

### Distributed Data Parallel (DDP)

DDP is Karpathy's go-to for multi-GPU training, preferred over the older `DataParallel` due to better handling of gradient sync and multi-node setups. Wrap the model like this: `model = DDP(model, device_ids=[local_rank])`.

- **Gradient flow**: Each GPU computes local gradients on its data shard. After `loss.backward()`, DDP triggers an **all-reduce** to average gradients across ranks and deposits the average back on every rank.
- **Sync details**: Communication happens **during** the backward pass (overlapped), not after, minimizing idle time.
- **Gradient accumulation**: To accumulate over multiple micro-steps (e.g., 4 steps for effective larger batches), sync only on the last micro-step. Karpathy toggles `model.require_backward_grad_sync = False` for early steps and `True` for the last, or uses `torch.distributed.barrier()` for simplicity. Avoids `no_sync()` context for cleaner code.
- Logging and checkpoints: Only the master process (rank 0) handles these to avoid spam.
- Cleanup: Always call `torch.distributed.destroy_process_group()` at the end.

Quote: "What DDP does for you is… once the backward pass is over, it will call what’s called all-reduce and it basically does an average across all the ranks of their gradients and then it will deposit that average on every single rank."

For loss logging (since gradients are averaged), reduce scalar losses: Sum them across ranks with `all_reduce` (op=`ReduceOp.SUM`), then divide by `world_size` on rank 0.

### The Concept of Rank

Rank is the unique integer ID for each process (0 to `world_size - 1`, e.g., 0-7 for 8 GPUs), set via `os.getenv('RANK')`. It determines:

- **Data assignment**: Shard the dataset so only examples where `i % world_size == rank` are processed by that rank.
- **Device binding**: Use `local_rank` (per-node GPU index, via `os.getenv('LOCAL_RANK')`) to set `torch.cuda.set_device(local_rank)`.
- **Control flow**: Rank 0 is the "master" for exclusive tasks like printing losses, saving checkpoints, or aggregating evaluation metrics. Other ranks compute silently.
- **Synchronization**: Used in barriers and reductions (e.g., all-reduce for stats).

In evaluation (e.g., on H-SWAG dataset), each rank computes local counts (correct predictions, total examples), all-reduces the sums, and rank 0 computes accuracy.

Karpathy stresses: Deterministic seeding ensures all ranks see the same shuffled order, but ranks filter their slices for non-overlap.

### Additional Notes on Evaluation and Implementation

Karpathy demonstrates distributed eval on a multiple-choice dataset (H-SWAG): Shard examples, compute local accuracy, all-reduce counts, and print on rank 0. For predictions, select the option with the lowest average loss (or highest prob) per example, using padding/masking.

Practical tips:

- Batch size is per-GPU; effective global batch = per-GPU *world_size* accumulation_steps.
- Seq len (context) stays fixed (e.g., 1024 tokens).

This section builds directly on prior single-GPU code, showing minimal changes for scaling.

[Let's build GPT: from scratch, in code, spelled out](https://www.youtube.com/watch?v=l8pRSuU81PU)
