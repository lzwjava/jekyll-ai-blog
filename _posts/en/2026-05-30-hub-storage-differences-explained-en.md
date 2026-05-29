---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hub Storage Differences Explained
translated: false
type: note
---

Great question. Let me explain from the storage layer up.

## The Core Difference: Git vs Git LFS vs Xet

**GitHub** stores everything in standard git objects (packfiles). Git was designed for source code — it delta-compresses text beautifully but chokes on large binaries. Every version of a binary gets stored essentially in full. A 7GB model file with 10 versions = ~70GB on the server.

**Hugging Face Hub** is git on the surface but uses **two different backends** for large files:

### 1. Git LFS (legacy, still default)

When you ran `hf upload lzwjava/zz .`, here's what happened for large files:

```
Your machine                    HF Hub
───────────                     ──────
git commit (small files)  ───>  standard git repo
                                (README.md, config.json, etc.)

LFS pointer files         ───>  LFS batch API
(large files tracked in         Stores actual blobs in
 .gitattributes)                object storage (S3/GCS)
```

The git repo itself only contains **pointer files** — tiny text stubs like:

```
version https://git-lfs.github.com/spec/v1
oid sha256:abc123...
size 7000000000
```

The actual model weights live in **blob storage** (S3/GCS). When you `git clone` or `hf_hub_download`, the LFS smudge filter fetches the real content from the blob store, not from git.

This is why HF can host repos with 100GB+ of model files — git never sees the actual bytes.

### 2. Xet (new, being rolled out)

HF has been building a new backend called **Xet** (based on content-defined chunking, similar to rsync/restic). Instead of storing whole files in blob storage:

```
Traditional LFS:     store entire 7GB file as one blob
Xet (CDC):           chunk file into ~64KB variable-size chunks,
                     deduplicate chunks across files/versions
```

This means if you fine-tune a model and only 5% of weights change, Xet only uploads/stores the modified chunks. Huge win for iterative ML workflows. Your `hf_api.py` references Xet support in `_upload_large_folder.py` and throughout the download path.

## Architectural Comparison

```
                    GitHub                  HuggingFace Hub
─────────────────────────────────────────────────────────────
Protocol            Git (smart HTTP)        Git (smart HTTP)
                                              + LFS batch API
                                              + Xet CAS API

Large file storage  Git LFS (optional,      Git LFS (default)
                    per-repo opt-in)        + Xet (content-addressed
                                              chunked storage)

Max file size       ~2GB recommended        50GB+ supported
                    (hard limit ~100GB)

Deduplication       None (git delta only)   Xet: cross-file chunk
                                              deduplication

Clone/download      git clone (fetches      hf_hub_download:
                    everything)               selective file fetch,
                                              symlink-based caching,
                                              parallel downloads

Repo types          Just "repo"             models, datasets, spaces
                                              (each with different
                                               metadata schemas)

Metadata            Just README             Model card (YAML front
                                              matter), dataset tags,
                                              library name, metrics,
                                              license, etc.

Pull model weights  N/A (not designed       First-class feature:
                    for this)                 snapshot_download(),
                                              from_pretrained() all
                                              pull from Hub

Web hosting         GitHub Pages            Spaces (Gradio/Streamlit
                                              apps hosted with GPU
                                              support)
```

## Why GitHub Can't Do This (and Doesn't Try)

GitHub's value is **code collaboration** — PRs, issues, Actions CI/CD, code review. Git's object model is optimized for text diffing. Running `git diff` on a 7B parameter `.safetensors` file is meaningless.

HF Hub's value is **model distribution**. The entire storage layer is designed around "a few small config files + several multi-GB binary blobs that change infrequently." The selective download in `hf_hub_download` (fetch only `model-00002-of-00004.safetensors`, not the whole repo) would be impossible with plain git.

## What Your Upload Did

```
Start hashing 36 files.      # hash each file to detect changes
Finished hashing 36 files.   # only upload new/changed files
✓ Uploaded                   # commit pushed via HF API
```

The hashing step is HF's way of doing incremental uploads — it checks which files already exist on the Hub (by SHA256) and skips them. This is smarter than `git push` which would re-send unchanged LFS objects.

For `zz` (your CLI tool), the repo is probably all small files so it's essentially just a normal git push. But if you uploaded a 7GB `.safetensors` model, it would go through the LFS/Xet path transparently.