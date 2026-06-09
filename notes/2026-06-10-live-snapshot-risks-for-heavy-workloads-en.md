---
audio: false
generated: true
image: false
lang: en
layout: post
title: Live Snapshot Risks for Heavy Workloads
translated: false
type: note
---

Question: Can I use the 20-minute snapshot creation window on an AMD Developer Cloud (DigitalOcean) MI300X instance to run tests or hyperparameter tuning?

Answer:

Yes, you can absolutely keep using your instance during this time, but doing heavy GPU workloads like LLM training or hyperparameter tuning while a **live snapshot** is running comes with critical risks that you should keep in mind.

Because the AMD Developer Cloud underlying infrastructure is powered by DigitalOcean, understanding how live snapshots handle data and hardware resources will help you decide if running these tests is the right move.

---

### 1. Risk of Data Inconsistency (The Primary Catch)

DigitalOcean live snapshots are taken while the system is running. To achieve this safely, the filesystem utilizes a **Copy-on-Write (CoW)** or a frozen metadata state at the exact moment you hit "Take Snapshot."

* **If your test involves massive disk writes:** (e.g., saving large LLM checkpoints, heavy logging, or shuffling 200 GB+ datasets), the live disk performance will drop. The hypervisor must track changes to blocks while copying the old ones to the snapshot storage.
* **Database/State corruption:** If an LLM training run or hyperparameter script updates a database or heavily relies on multi-file sequence logs while the snapshot is mid-process, the resulting snapshot might capture a fractured, inconsistent state.

### 2. GPU vs. Storage Performance

* **GPU Tasks are fine:** The snapshot process primarily taxes the CPU, hypervisor, and disk I/O (NVMe/SSD array storage). Your AMD Instinct MI300X GPU and its 192GB of HBM3 VRAM are completely free from the snapshot overhead.
* **Storage Bottlenecks:** LLM hyperparameter testing often requires caching tokenized datasets or reading weights. Because the underlying storage is heavily stressed by reading data to build the snapshot (moving ~200+ GB), your active code will likely suffer from high **Disk I/O wait times**, which will slow down your training loops significantly.

---

### Best Practices for Your 20-Minute Window

If you want to maximize that time without ruining your active instance or corrupting your snapshot, focus on **memory-bound** or **GPU-bound** tasks rather than storage-heavy operations:

* **Good Use Cases:**
* Running lightweight, quick inference checks on a model already fully loaded into the MI300X VRAM.
* Adjusting python script logic, reviewing logs, or writing code inside your JupyterLab / SSH environment.
* Running small prototype tests that do not write heavy checkpoints back to the disk.

* **Things to Avoid:**
* Initiating massive training jobs that immediately write multi-gigabyte `.safetensors` or `.bin` weights to the filesystem.
* Shuffling or preprocessing raw, large datasets on the local drive.

> **Recommendation:** If your ultimate goal for taking the snapshot is to create a perfect "save point" or baseline before a massive experiment, the safest approach is always to **power down the instance** first, take the snapshot, and turn it back on. If you must do it live, keep your disk activities to an absolute minimum during those 20 minutes.
