---
audio: false
generated: true
image: false
lang: en
layout: post
title: Accessing BigCode Datasets on Hugging Face
translated: false
type: note
---

**Question:** Where do I find the actual text/code data behind https://huggingface.co/bigcode?

**Answer:**

That URL is just the org profile page. The actual data lives under the org's **Datasets** tab: https://huggingface.co/bigcode — click "Datasets", or go directly to https://huggingface.co/datasets?other=bigcode. The main corpora:

- **The Stack v2** (the big one, ~67TB raw): https://huggingface.co/datasets/bigcode/the-stack-v2 — plus variants `the-stack-v2-dedup` and `the-stack-v2-train-full-ids` (the actual StarCoder2 training mix, ~900B tokens)
- **The Stack v1** (~3TB dedup): https://huggingface.co/datasets/bigcode/the-stack-dedup
- **starcoderdata** (~800GB, the cleaned StarCoder1 training set — the most practical one to actually use): https://huggingface.co/datasets/bigcode/starcoderdata

Two gotchas before you can read anything:

**1. They're gated.** You need a HF account, click "Agree and access" on the dataset page, then authenticate locally:

```bash
pip install -U huggingface_hub datasets
hf auth login   # paste a token from https://huggingface.co/settings/tokens
```

**2. The Stack v2 doesn't contain the file contents.** It only ships metadata + Software Heritage blob IDs; the actual text sits in SWH's S3 bucket, which you download separately (and need AWS credentials for):

```python
import os, boto3, smart_open
from datasets import load_dataset

session = boto3.Session(
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"])
s3 = session.client("s3")

def download_blob(blob_id, encoding):
    url = f"s3://softwareheritage/content/{blob_id}"
    with smart_open.open(url, "rb", compression=".gz",
                         transport_params={"client": s3}) as f:
        return f.read().decode(encoding)

ds = load_dataset("bigcode/the-stack-v2", "Python",
                  split="train", streaming=True)
for row in ds:
    print(download_blob(row["blob_id"], row["src_encoding"])[:500])
    break
```

For your use case (nanoGPT-scale training on the 4070 or MI300X), skip that complexity — **The Stack v1 and starcoderdata contain the text inline**, so streaming just works:

```python
from datasets import load_dataset

# stream, don't download 800GB
ds = load_dataset("bigcode/starcoderdata", data_dir="python",
                  split="train", streaming=True)
row = next(iter(ds))
print(row["content"][:1000])   # actual source code text
```

Or grab a single language subset to disk with the CLI:

```bash
hf download bigcode/the-stack-dedup \
  --repo-type dataset \
  --include "data/python/*" \
  --local-dir ./stack-python
```

The files are parquet, so you can also just read them with `pyarrow`/`polars` directly once downloaded. For a tokenize-and-train pipeline, the pattern in nanoGPT's `data/openwebtext/prepare.py` ports over directly: stream → tokenizer.encode → append to a memmapped `.bin`.

Rule of thumb for sizing: the `python` subset of starcoderdata alone is ~60B tokens — far more than you need for a 760M-param run (Chinchilla-optimal is ~15B tokens), so streaming a slice is the right move on your 916GB workstation, and definitely on the Air.

**References:**

- [bigcode datasets on Hugging Face](https://huggingface.co/bigcode)
- [The Stack v2 dataset card (includes the S3 download snippet)](https://huggingface.co/datasets/bigcode/the-stack-v2)
- [starcoderdata dataset card](https://huggingface.co/datasets/bigcode/starcoderdata)
