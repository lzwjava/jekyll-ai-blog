---
audio: false
generated: true
image: false
lang: en
layout: post
title: Accelerating Hugging Face Dataset Downloads
translated: false
type: note
---

Question: Is there a better way to download Hugging Face models? 20 MB/s is slow. Would using two desktops at home in Guangzhou, with one downloading Parquet files 1–20 and the other 21–40, help?

Answer:

Yes. **20 MB/s is fairly slow** if you're downloading hundreds of GB of training data. For example:

* 20 MB/s ≈ 72 GB/hour
* 1 TB takes about **14–15 hours**
* 10 TB takes nearly **6 days**

For LLM pretraining datasets, download speed quickly becomes a bottleneck.

### Option 1: Parallel downloads (recommended)

If the dataset is made up of many Parquet shards (like FineWeb, FineWeb-Edu, BigCode, etc.), then yes—your idea works well.

Machine A:

```bash
download shard_00000.parquet
...
download shard_00019.parquet
```

Machine B:

```bash
download shard_00020.parquet
...
download shard_00039.parquet
```

Afterward:

```bash
rsync -av machineB:/data/*.parquet /data/
```

or copy them onto an SSD.

Since each Parquet file is independent, there is no issue combining them later.

---

### Option 2: Use `hf_transfer` (much faster)

Install:

```bash
pip install "huggingface_hub[hf_transfer]"
```

Enable it:

```bash
export HF_HUB_ENABLE_HF_TRANSFER=1
```

Then use:

```bash
huggingface-cli download \
    HuggingFaceFW/fineweb-edu \
    --repo-type dataset
```

`hf_transfer` opens many concurrent HTTP connections and is often **2–5× faster** than the default downloader if your network isn't the bottleneck.

---

### Option 3: aria2c

Instead of a single HTTP stream:

```bash
aria2c \
    -x16 \
    -s16 \
    URL
```

or run many downloads in parallel:

```bash
cat urls.txt | xargs -n1 -P16 aria2c
```

---

### Option 4: Download on cloud (often the best)

If you're ultimately training on RunPod, Lambda, or another cloud GPU:

* download directly there
* store on persistent volume
* avoid uploading from home

Cloud datacenters often achieve **100–1000 MB/s** to Hugging Face.

---

### Option 5: Hugging Face mirror (for China)

If you're physically in Guangzhou, the international route to Hugging Face can be the limiting factor.

Many people use mirrors such as:

```bash
export HF_ENDPOINT=https://hf-mirror.com
```

Performance varies by ISP and time of day, but users in mainland China often report significant improvements.

---

### Option 6: Increase download workers

The Hugging Face Python API supports multiple workers:

```python
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="HuggingFaceFW/fineweb-edu",
    repo_type="dataset",
    max_workers=32,
)
```

Going from the default to 16–32 workers can noticeably improve throughput.

---

## Is two desktops worth it?

Yes, especially if:

* your ISP gives each machine its own bandwidth allocation,
* the dataset has hundreds or thousands of Parquet shards,
* both machines write to local SSDs.

For example:

Desktop 1:

```
0000.parquet
...
0999.parquet
```

Desktop 2:

```
1000.parquet
...
1999.parquet
```

Then merge the directories. This is a simple and effective strategy.

---

### For your workflow

Since you're downloading **multi-terabyte pretraining datasets** (FineWeb, BigCode, etc.), I'd prioritize:

1. `hf_transfer`
2. `max_workers=32`
3. Split shards across multiple machines
4. Download directly on cloud when possible

Using all four together can reduce download time dramatically compared with a single 20 MB/s stream.
