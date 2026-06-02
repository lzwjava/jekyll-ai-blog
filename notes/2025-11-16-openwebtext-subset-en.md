---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Downloading a Portion of OpenWebText
translated: false
type: note
---

Ah, got it — you want to stick with **Hugging Face CLI** but still only grab a small portion. The problem is: the CLI is designed to download **whole files**, not slices. OpenWebText is split into 21 `.tar` subset files; if you use the CLI, it will download entire tarballs, so you can’t get exactly “1%” without downloading large chunks.

Here’s a practical approach:

---

### 1. Download only a subset of files

Instead of the full 21 files, pick just a few tarballs:

```bash
huggingface-cli download \
  --repo-type dataset openwebtext/subsets/urlsf_subset00.tar \
  --local-dir ./openwebtext
huggingface-cli download \
  --repo-type dataset openwebtext/subsets/urlsf_subset01.tar \
  --local-dir ./openwebtext
```

* Each tarball is ~625MB, so if you download 1–2 of them, that’s roughly 1–2% of the dataset.
* You can adjust which subsets you pick; HF doesn’t enforce sequential order.

---

### 2. Extract only what you need

After download:

```bash
cd ./openwebtext
tar -xvf urlsf_subset00.tar
tar -xvf urlsf_subset01.tar
```

Then you can process only a few documents from these subsets.

---

### 3. Optional: Combine with HF Transfer

To speed up CLI downloads:

```bash
pip install hf_transfer
export HF_HUB_ENABLE_HF_TRANSFER=1
```

Then retry the CLI commands — downloads will be much faster.

---

If you want, I can make a **tiny command snippet that automatically picks ~1% of OpenWebText using CLI only**, so you don’t have to manually select tarballs. Do you want me to do that?
