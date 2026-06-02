---
audio: false
generated: true
image: false
lang: en
layout: post
title: Unconventional H100 Strategies for GPT-2 Training
translated: false
type: note
---

Here are some **unpopular** (but technically sound) ideas for training GPT-2 124M on cloud H100s:

---

### 1. **Use 1 H100 for a 124M model**
Most people would use a single A100 or even a V100 for this tiny model. Using an H100 is overkill—but that’s the point.
**Unpopular twist**: Don’t parallelize. Run it on **one H100** with a massive batch size, leveraging the H100’s FP8 support to simulate a much larger effective batch size via gradient accumulation. This keeps it simple, avoids communication overhead, and wastes no GPU potential.

---

### 2. **Train in FP8 with no master weights in FP32**
H100 supports FP8 natively. Most would keep master weights in FP32 for stability. The unpopular idea: **go full FP8** for both forward and backward, using the H100’s transformer engine to automatically handle scaling. It’s risky but speeds up training and cuts memory—on a model this small, you can even increase batch size beyond what seems reasonable.

---

### 3. **Use 8 H100s but disable all parallelism**
Instead of data parallelism, tensor parallelism, or pipeline parallelism, just launch **8 independent training runs** on the same instance, each with a different random seed. Hyperparameter sweep in parallel.
Why unpopular? People expect distributed training to speed up one model, but here you get 8 trained variants in the same time as one.

---

### 4. **Deliberately underfit for faster iteration**
Train for far fewer tokens than Chinchilla-optimal. With H100s, you can hit compute-optimal in hours. Instead, train for **1/10th the tokens** to iterate on architecture changes, data mix, or evaluation protocols. Most people optimize for final model quality; unpopular is optimizing for **insight per dollar**.

---

### 5. **Use a CPU-based dataloader with no GPU prefetch**
On H100s, IO can become a bottleneck even for a 124M model. The unpopular fix: avoid fancy GPU dataloaders. Use a single-threaded CPU dataloader with `pin_memory=False` and let the GPU idle slightly. This exposes bottlenecks early and forces you to think about data pipelines—unpopular because everyone chases 100% GPU utilization.

---

### 6. **Run on H100s but throttle power limits**
Set the H100s to lower power limits (e.g., 300W instead of 700W) to save cost and reduce cooling needs. Performance drops, but for a model this small, you’re still massively over-provisioned. Most people want maximum speed; unpopular is optimizing for **cost efficiency** on overkill hardware.

---

### 7. **No distributed optimizer (like ZeRO)**
Even with 8 H100s, skip ZeRO stages. Just use DDP with full model replication. The model is tiny; you waste memory but gain simplicity and avoid communication overhead. Unpopular because everyone reaching for H100s assumes they need sharding.

---

### 8. **Train with extremely low precision and aggressive gradient clipping**
Use FP8 with a tiny gradient clipping threshold (e.g., 0.1) to stabilize training. Combined with no warmup, this is unconventional but can yield fast convergence curves at the cost of final perplexity—great for prototyping.

---

### 9. **Use synthetic data generated on the fly by a small auxiliary model**
Instead of using a static dataset, use another small model (e.g., GPT-2 124M itself) running in parallel on the same H100 to generate synthetic text, and train on that. This is inefficient in theory but allows endless data variation—unpopular because it’s seen as wasteful.

---

### 10. **Reserve one H100 just for logging and evaluation**
Take an 8×H100 node, use 7 for training, and keep 1 idle for continuous evaluation, logging, and checkpointing. This is “wasteful” by conventional distributed training standards but gives you real-time insights without slowing training steps.

---

If you want, I can sketch out a **slurm script** or **PyTorch DDP config** for one of these approaches.
