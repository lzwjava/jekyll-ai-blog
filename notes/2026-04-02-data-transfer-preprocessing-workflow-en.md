---
audio: false
generated: true
image: false
lang: en
layout: post
title: Optimizing Data Transfers and Preprocessing Workflows
translated: false
type: note
---

Here’s a breakdown of what’s happening in this sequence:

---

## **1. The Problem**
You had a **VPS** and a **GPU droplet** (likely a cloud server with an H200 GPU).
Initially, transferring **61 GB of data** between them over the **external (public) network** would have taken **~5 hours** (probably due to limited bandwidth or high latency).

---

## **2. Setting Up Internal Network Communication**
Both servers are on the same **internal network** (private IPs:
- VPS at `10.100.0.2`
- GPU droplet at `10.100.3`

You verified they can talk internally with **very low latency** (1.56 ms), much faster than going over the internet.

### **SSH Key Setup**
You set up **SSH key authentication** from VPS → GPU droplet so transfers wouldn’t require a password.
*One minor hiccup*: the key was concatenated without a newline, breaking authentication; you fixed it.

---

## **3. Internal Network Transfer Speed**
Once the internal network path was ready, you transferred the **61 GB dataset** directly:

- **Speed peaked at ~450 MB/s**
- **Total transfer time: ~5 minutes**
  (vs. 5 hours over external network)

This huge speedup comes from:
- **Private network** — no internet routing bottlenecks
- **High internal bandwidth** (likely 10 Gbps or more)
- **Low latency** between nodes

---

## **4. Data Preparation on GPU Droplet**
After the transfer, you started **data preprocessing** on the GPU droplet (the H200 machine).

You ran **12 parallel workers**, each using ~93% CPU — meaning the task was CPU-bound during preprocessing, not yet GPU-bound.

### **Processing Speed**
- **~40 million tokens per second**
- Each **shard** (likely a chunk of the dataset) processed in **~2 seconds**
- Total shards: **~610**
- After ~1 minute: **42 shards done (7.9 GB output)** → **~7% done**
- **ETA: ~14–20 minutes** to finish preprocessing

---

## **5. Why This Matters**
This workflow shows a **common ML data pipeline optimization**:

1. **Transfer data internally** — not over public internet — to avoid slow speeds.
2. **Use high-performance storage and compute** (H200 + many CPU cores) to preprocess quickly.
3. **Parallelize** tokenization/shuffling/writing to maximize throughput.

The result:
From raw data on a VPS → preprocessed dataset ready on a GPU server in **under 30 minutes total**, where the naïve approach would have taken hours just for the transfer.

Let me know if you’d like a deeper explanation of the internal networking setup, the parallel preprocessing logic, or how to monitor such pipelines.
