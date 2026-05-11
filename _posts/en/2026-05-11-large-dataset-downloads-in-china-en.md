---
audio: false
generated: true
image: false
lang: en
layout: post
title: Large Dataset Downloads in China
translated: false
type: note
---

Question: In China, is there a better way to download large datasets like FineWeb, and how can I efficiently obtain such large datasets?

Answer:

Downloading extremely large datasets (~100B tokens, hundreds of GB) in China can be challenging due to network speed, restrictions, and reliability issues with international servers like Hugging Face. Here are practical approaches:

---

### 1. **Use Local Mirrors or Faster Hosts**

* Hugging Face datasets often have official mirrors, e.g., `hf.co` mirrors in Asia or `huggingface-asia` mirrors.
* Your script already supports `--mirror hf-mirror`, which can be significantly faster inside China.
* Check if other Chinese universities or open-source communities host FineWeb shards locally.

---

### 2. **Parallel Downloads**

* Your current script downloads shards sequentially.
* Use **`aiohttp`**, **`asyncio`**, or a tool like **`aria2c`** for multi-connection downloads.
* Example with `aria2c`:

  ```bash
  aria2c -x 16 -s 16 -i urls.txt
  ```

  Where `urls.txt` lists all shard URLs. This can saturate bandwidth and reduce download time from mirrors.

---

### 3. **Use a Cloud VM or Storage Near the Mirror**

* Renting a cloud VM in **Singapore, HK, or a nearby region** with high-speed links to HF mirrors is often faster than domestic home connections.
* Download the dataset there, compress it, and then transfer via high-speed transfer (e.g., `rclone`, `rsync`) to your local machine.

---

### 4. **Partial or Incremental Download**

* Instead of downloading the full ~100B tokens (~400 GB), select only a subset initially for experiments.
* Your `select_shards()` function already allows limiting by size. Consider starting with 5–10 shards (~20–40 GB) for local experiments.

---

### 5. **Using Data Hosting Services**

* Some Chinese users rehost datasets on **Baidu Cloud (Pan)**, **Aliyun OSS**, or **Tencent COS**. Search in GitHub issues or forums; sometimes, mirrors exist unofficially.
* Be careful about legality and license compliance when using unofficial mirrors.

---

### 6. **Optimize Storage**

* Parquet shards are often **compressible**; consider downloading `.parquet` and converting to `.jsonl` or other compressed formats to save space.
* Your `BYTES_PER_TOKEN = 4` is approximate; real storage might be reduced with compression.

---

### 7. **Automated Resumable Downloads**

* The `download_one()` function in your script already supports resumable downloads via `Range` headers. For China, combining this with retries and exponential backoff is critical for stability.

---

**Summary Recommendation:**

1. Use `--mirror hf-mirror` or a nearby Asian mirror.
2. Consider multi-threaded downloads (aria2 or asyncio).
3. Start with a subset of shards.
4. Use cloud VMs near the mirror for bulk downloads.
5. Make use of resumable downloads to avoid repeated failures.

---

References:

* [Hugging Face Datasets Documentation](https://huggingface.co/docs/datasets/)
* [aria2 Download Utility](https://aria2.github.io/)
* [FineWeb Dataset on Hugging Face](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu)