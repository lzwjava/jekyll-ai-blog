---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Qwen 9B with 10 H200s
translated: false
type: note
---

Question: What happens if I use **10× H200 GPUs** on separate DigitalOcean droplets with **PyTorch distributed training** for Qwen-3.5 9B?

Answer:

Using **10 GPUs with PyTorch DDP / FSDP** drastically changes feasibility, but full training from scratch is still challenging. Let’s break it down carefully.

---

## 1. Full pretraining requirements

* **Qwen-3.5 9B**

  * Parameters: 9B
  * Dataset: ~300B tokens
  * Full training FLOPs: ~2–3e23 FLOPs (rough estimate for 9B model)

---

## 2. GPU throughput scaling

* **Single H200** → ~30M tokens/day
* **10× H200 in ideal distributed scaling** → 10× throughput (~300M tokens/day)

> Realistic scaling: 80–90% efficiency (network overhead, gradient sync). So practical: ~240–270M tokens/day.

---

## 3. Time estimate for full pretraining

* Dataset: 300B tokens
* Throughput: ~250M tokens/day
* Time:

[
300,\text{B tokens} ÷ 0.25,\text{B/day} ≈ 1200,\text{days} \approx 3.3,\text{years}
]

✅ Even with 10 H200 GPUs, **full training from scratch still takes multiple years**, which shows why research labs use **tens or hundreds of GPUs**.

---

## 4. Practical alternatives

1. **LoRA / PEFT fine-tuning**

   * Use pre-trained Qwen-3.5 9B weights
   * Fine-tune 1–10B tokens:

     * 10 GPUs → 1–2 days for small datasets
     * 1–2 weeks for medium datasets (~50B tokens)

2. **Partial pretraining / proof-of-concept**

   * Train **10–50B tokens** for research:

     * 10 GPUs → 1–2 weeks
     * Good for experimenting with hyperparameters or small-scale curriculum learning

3. **Model parallelism / FSDP**

   * FSDP allows **splitting 9B parameters across 10 GPUs** efficiently
   * Gradient synchronization will introduce ~10–20% overhead
   * You can train larger batch sizes than single GPU

---

## 5. Key points for 10 GPU distributed setup

* **Networking:** Make sure your droplets have **high-speed NVLink or RDMA-equivalent networking**; DigitalOcean inter-droplet network latency can reduce scaling efficiency.
* **Batch size:** Can scale roughly 10× vs single GPU
* **Checkpointing:** Use **frequent checkpoints**; multi-GPU runs are more sensitive to network / droplet failures
* **Cost:**

  * $3.44/GPU/hr × 10 GPUs → $34.4/hr
  * Continuous week → ~$5,700 (168h × 34.4)

---

### ✅ Summary

| Scenario                   | Tokens/day   | Time for 300B tokens             |
| -------------------------- | ------------ | -------------------------------- |
| 1× H200                    | 30M          | 27 years                         |
| 10× H200                   | 250M         | ~3.3 years                       |
| LoRA / partial pretraining | 1–50B tokens | 1–14 days (depending on dataset) |

**Conclusion:**

* **Full scratch pretraining**: still impractical on 10 H200 GPUs.
* **Fine-tuning / partial pretraining**: entirely feasible; 10 GPUs can get **substantial progress in a week or two**.

---

I can also make a **practical plan showing exactly what 10× H200 GPUs can achieve week by week for LoRA or partial pretraining** for Qwen-3.5 9B. This will give you a realistic operational timeline.

Do you want me to make that plan?