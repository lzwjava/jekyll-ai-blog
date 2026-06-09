---
audio: false
generated: true
image: false
lang: en
layout: post
title: Accelerating NanoChat MI300X Training
translated: false
type: note
---

Question: How can I speed up this NanoChat MI300X training run?

Answer:

Based on the command you posted, you're already using some of the biggest optimizations:

* FP8 enabled (`--fp8`)
* FlashAttention 2 (from your earlier tests)
* Large batch size (`524288`)
* MI300X GPU
* Sequence length 2048

The remaining gains usually come from one of four areas:

## 1. Verify FlashAttention 2 is Actually Being Used

This is the biggest potential win.

Check the training log:

```bash
grep -i "flash" run_mi300x_d24_fa2_fp8.log
```

or

```bash
grep -i "attention" run_mi300x_d24_fa2_fp8.log
```

If NanoChat silently falls back to SDPA, you can lose 20–40% performance.

Your earlier benchmark showed:

| Config      | Step Time |
| ----------- | --------- |
| bf16 + SDPA | 7.7s      |
| FP8 + SDPA  | 6.4s      |
| FP8 + FA2   | ~4–5s     |

So FA2 is often the single largest speedup.

---

## 2. Increase Device Batch Size

You currently have:

```bash
--device-batch-size=32
```

On an MI300X (192 GB HBM), this is often conservative.

Try:

```bash
--device-batch-size=48
```

If stable:

```bash
--device-batch-size=64
```

Watch memory:

```bash
watch -n 1 rocm-smi --showmemuse
```

If utilization is under 160 GB, you're leaving performance on the table.

---

## 3. Increase Sequence Length (Sometimes Faster)

Counterintuitively, larger sequences can improve MFU.

Current:

```bash
--max-seq-len=2048
```

Try:

```bash
--max-seq-len=4096
```

if NanoChat supports it.

Why?

Longer sequences increase arithmetic intensity and keep matrix units busier.

Typical MI300X utilization:

| Seq Len | MFU    |
| ------- | ------ |
| 2048    | 25–35% |
| 4096    | 35–45% |
| 8192    | 45–55% |

---

## 4. Increase Model Size

You're training a 24-layer ~760M model:

```bash
--depth=24
```

Small models often become CPU/data-loader limited.

On MI300X, 760M is relatively small.

Common observation:

| Model | MFU    |
| ----- | ------ |
| 760M  | 25–35% |
| 3B    | 40–55% |
| 7B    | 55–70% |

The GPU likes bigger GEMMs.

---

## 5. Reduce Evaluation Frequency

Current:

```bash
--eval-every=1000
--eval-tokens=1048576
```

Each evaluation pauses training.

For pure throughput testing:

```bash
--eval-every=5000
```

or

```bash
--eval-every=-1
```

temporarily.

Also:

```bash
--sample-every=-1
```

```bash
--core-metric-every=-1
```

during benchmarking.

---

## 6. Check GPU Utilization

Run:

```bash
watch -n 1 rocm-smi
```

Look at:

```text
GPU Utilization
HBM Utilization
Power Draw
```

Healthy training should show:

```text
GPU Util: 90-100%
Power: 650-750W
```

If GPU utilization fluctuates:

```text
20%
100%
30%
100%
```

you are data-loader or CPU bottlenecked.

---

## 7. Use More Data Loader Workers

Check whether NanoChat exposes:

```bash
--num-workers
```

or similar.

If yes:

```bash
--num-workers=16
```

or

```bash
--num-workers=32
```

can significantly improve throughput.

---

## 8. Check Actual Tokens/sec

The most important metric is:

```text
tokens/sec
MFU
```

If you're seeing:

```text
300K tok/s
```

there is room for improvement.

If you're seeing:

```text
500K-700K tok/s
```

for a 760M model on MI300X, you're already in excellent territory.

---

## 9. Profile the First 100 Steps

Run:

```bash
python -m scripts.base_train \
  ... \
  --num-iterations=100
```

Then inspect:

```bash
grep -i "tok/s" run.log
grep -i "mfu" run.log
```

The bottleneck becomes obvious:

* low MFU → GPU not saturated
* high MFU but low tok/s → model too small
* fluctuating utilization → dataloader bottleneck
* high memory usage → batch size limit

## Recommended First Changes

I would try these in order:

```bash
--device-batch-size=64
```

then

```bash
--eval-every=5000
--sample-every=-1
--core-metric-every=-1
```

then verify FlashAttention 2 is active.

Those three changes typically yield the largest practical speedup without modifying NanoChat source code.
