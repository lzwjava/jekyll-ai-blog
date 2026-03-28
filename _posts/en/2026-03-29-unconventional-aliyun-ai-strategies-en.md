---
audio: false
generated: true
image: false
lang: en
layout: post
title: Unconventional Aliyun Strategies for AI Engineers
translated: false
type: note
---

As a software engineer in Guangzhou, you’re likely familiar with the standard "corporate" way of using Aliyun (Alibaba Cloud). However, when it comes to training models like **nanoGPT** or scaling toward **GPT-3** architectures, there are several "unpopular" or unconventional perspectives that seasoned Chinese AI engineers often discuss behind closed doors.

Below is a breakdown of these insights, organized by infrastructure, cost, and regional strategy.

---

### 1. The "Domestic vs. International" Region Arbitrage
Most developers default to Aliyun’s Mainland China regions (e.g., Hangzhou or Shenzhen) for lower latency.
* **The Unpopular Idea:** Use Aliyun’s **International regions** (Singapore or US East) even if you are based in Guangzhou.
* **Why:** GPU availability for high-end cards like the **H20** (the China-specific version) can be tight domestically. International nodes often have better access to global open-source mirrors (Hugging Face, GitHub), avoiding the "Great Firewall" headaches that slow down `pip install` or model weight downloads during training setup.

### 2. PAI-Designer vs. Bare Metal (ECS)
Aliyun heavily promotes **PAI (Platform for AI)** as a managed service for LLM training.
* **The Unpopular Idea:** Ignore PAI and stick to **GPU-enabled ECS (Elastic Compute Service)** with raw Docker containers.
* **Why:** While PAI is marketed as "low-code/managed," many engineers find it adds a layer of abstraction that makes debugging deep-seated CUDA errors or custom `torch.distributed` configurations harder. For a project like **nanoGPT**, the overhead of learning PAI’s proprietary workflow often outweighs the benefits of its "one-click" setup.

### 3. The "Spot Instance" Gamble for nanoGPT
Since nanoGPT is highly educational and uses relatively small datasets (like Shakespeare or OpenWebText), training is fast.
* **The Unpopular Idea:** Use **Spot Instances (抢占式实例)** exclusively.
* **Why:** You can get up to **90% off** the on-demand price. As of March 2026, Aliyun has increased prices for AI computing by up to 34% in some sectors. Spot instances allow you to run experiments for "coffee money."
* **The Pro Move:** Since `train.py` in nanoGPT already has a robust **checkpointing system**, if Aliyun reclaims your instance, you lose nothing but a few minutes of progress.

### 4. Storage Bottlenecks: The CPFS "Tax"
For GPT-3 scale models, data throughput is the silent killer. Aliyun recommends **CPFS (Cloud Parallel File System)**.
* **The Unpopular Idea:** Avoid CPFS for small-to-medium runs; use **local NVMe SSDs** and manually sync.
* **Why:** CPFS costs recently jumped by ~30%. For nanoGPT, the dataset fits in RAM or a cheap local SSD. Paying for high-performance parallel storage is often "over-engineering" unless you are running a cluster of 32+ GPUs.

### 5. Embracing "Dumbed-Down" Silicon (H20 & 910B)
Due to export controls, you might not get the "full" H100s easily on domestic Aliyun.
* **The Unpopular Idea:** Optimize specifically for the **Nvidia H20** or **Huawei Ascend 910B** rather than trying to port code written for Western H100s directly.
* **The Reality:** The H20 has high memory bandwidth but lower compute (TFLOPS). Engineers who win on Aliyun are those who adjust their **batch sizes** and **gradient accumulation steps** to favor the H20’s specific memory-to-compute ratio, rather than following Karpathy’s exact H100 hyperparameters.

---

### Comparison Table: Training nanoGPT on Aliyun

| Strategy | The "Standard" Way | The "Unpopular" Engineer Way |
| :--- | :--- | :--- |
| **Instance** | On-Demand GPU (Expensive) | **Spot Instance** (90% cheaper) |
| **Location** | Mainland China (Latency focus) | **Singapore/International** (Ease of `git clone`) |
| **Environment** | Aliyun PAI (Managed) | **Raw ECS + Docker** (Full control) |
| **Storage** | CPFS (High cost) | **Local NVMe** (Performance/Price balance) |
| **Dataset** | OSS (Object Storage Service) | **RAM Disk** (For small nanoGPT sets) |

---

### Next Step
Would you like me to help you draft a **Dockerfile** specifically optimized for Aliyun’s Ubuntu images to get nanoGPT running with the correct CUDA drivers?