---
audio: false
generated: true
image: false
lang: en
layout: post
title: Maximizing GPU Utilization for LLM Training
translated: false
type: note
---

Question: For people who want to excel at LLM training, should they start experiments before sleeping and check results after to maximize experiment velocity?

---

Answer:

**Yes, but with specifics.**

The core insight is correct: training is **compute-bound, not developer-bound**. Your GPU doesn't care if you're watching it. Wall-clock time is the bottleneck — you want to maximize GPU utilization across 24/7, not just 9-5.

**The real strategy:**

1. **Batch experiments by wall-clock duration**
   - Pre-sleep: Start the longest runs (8-12 hour training jobs, full eval passes)
   - During day: Shorter, iterative experiments (1-2 hour runs for hyperparameter sweeps, ablations)
   - This keeps GPU hot while you sleep and work

2. **Design for async checking**

   ```python
   # Start training, write metadata to disk
   config = {
       "seed": 42,
       "lr": 1e-4,
       "batch_size": 64,
       "run_id": f"exp_{int(time.time())}"
   }

   # Save to jsonl for easy parsing later
   with open(f"runs/{config['run_id']}.jsonl", "w") as f:
       for step, loss in training_loop():
           f.write(json.dumps({"step": step, "loss": loss}) + "\n")
           f.flush()  # Critical: flush so you can read partial results
   ```

   Then wake up and check:

   ```bash
   # Quick check: final loss
   tail -1 runs/exp_*.jsonl | jq '.loss'

   # Trend analysis: did loss stabilize?
   jq '.loss' runs/exp_1234.jsonl | python3 -c "import sys; vals=list(map(float, sys.stdin)); print(f'final={vals[-1]:.4f}, improvement={vals[0]-vals[-1]:.4f}')"
   ```

3. **Use checkpointing strategically**

   ```python
   # Save every N steps so you don't lose work
   if step % checkpoint_interval == 0:
       torch.save({
           'model': model.state_dict(),
           'optimizer': optimizer.state_dict(),
           'step': step,
           'loss': loss
       }, f"checkpoints/step_{step}.pt")
   ```

4. **Queue multiple experiments**

   ```bash
   # Start 3 runs in sequence before sleep (won't all run in parallel, but queued)
   for seed in 42 43 44; do
       python train.py --seed $seed --output runs/seed_$seed &
   done
   wait
   ```

   Or better: use a job scheduler (Ray Tune, Weights & Biases, or simple queue):

   ```python
   # With Ray
   for config in [{"lr": 1e-4}, {"lr": 5e-5}, {"lr": 1e-5}]:
       trainer.fit(config)  # Ray queues and runs
   ```

5. **The hard constraint: what's actually actionable?**
   - If your runs take 12 hours, you can only iterate every day (at best 5 productive iterations/week)
   - Focus on experiments that are **statistically meaningful** — don't run 100 short ablations; run 5-10 longer, cleaner ones
   - One careful 12-hour run beats 10 sloppy 1-hour runs

**Practical reality from your setup:**

With RTX 4070 (12GB) or MI300X (192GB):

- **nanoGPT scale** (125M-760M params): 6-12 hour runs are normal
- **Pre-sleep workflow**: Start training job + eval pass at 10 PM, check results at 8 AM
- **During day**: Quick ablations on a subset of data (5-10 min), design next night's experiment

**What NOT to do:**

- Don't obsessively log/tensorboard during runs (adds overhead)
- Don't start experiments you won't analyze (analysis takes time too)
- Don't assume more experiments = better learning. One thoughtful experiment beats 20 random ones

**Tools for async checking:**

```bash
# Monitor from anywhere
watch -n 60 'tail -20 training.log | grep "loss"'

# Email yourself results (crude but works)
# At end of training, append to a persistent log
echo "exp_$run_id: final_loss=$(tail -1 results.jsonl | jq '.loss')" >> /var/log/ml_results.txt
```

---

**Bottom line:** Yes, maximize 24-hour GPU utilization. But couple it with thoughtful experiment design (not brute force). The bottleneck for learning speed isn't running more experiments — it's *understanding* what each one tells you and building on it.

What's your typical training loop length right now? That determines whether pre-sleep → post-sleep is worth optimizing vs. other velocity levers.
