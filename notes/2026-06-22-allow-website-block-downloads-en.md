---
audio: false
generated: true
image: false
lang: en
layout: post
title: Allow Website, Block Downloads
translated: false
type: note
---

**Question:** Can we allow employees to visit the HuggingFace website (huggingface.co) but block the HuggingFace CLI/API model download functionality?

**Answer:**

Yes, cleanly separable. The website and the download mechanism use different endpoints and authentication patterns. Here's how to split them:

## How HuggingFace Downloads Work

`huggingface_hub` CLI and `transformers` auto-download use:

- `https://huggingface.co/<model>/resolve/main/<file>` — actual file blobs
- `https://cdn-lfs.huggingface.co/` — LFS (large file storage) for model weights
- `https://cdn-lfs-us-1.huggingface.co/` — US CDN mirror
- API calls to `https://huggingface.co/api/models/...`

The web UI uses standard HTML pages at `https://huggingface.co/` — same domain, different paths.

## Strategy Options

### Option 1: Firewall/Proxy URL Path Filtering (Best)

If you control a proxy (Squid, nginx, Zscaler, Palo Alto, etc.):

```
# Allow HuggingFace website browsing
ALLOW  GET  huggingface.co/*  (HTML pages, JS, CSS)

# Block model download paths
BLOCK  GET  huggingface.co/*/resolve/*
BLOCK  GET  huggingface.co/api/*
BLOCK  GET  cdn-lfs.huggingface.co/*
BLOCK  GET  cdn-lfs-us-1.huggingface.co/*
```

**Squid ACL example:**

```squid
acl hf_downloads url_regex huggingface\.co/.*/resolve/
acl hf_lfs dstdomain cdn-lfs.huggingface.co cdn-lfs-us-1.huggingface.co
acl hf_api url_regex huggingface\.co/api/

http_access deny hf_downloads
http_access deny hf_lfs
http_access deny hf_api
http_access allow huggingface.co
```

### Option 2: Block CDN + LFS Domains Only (Simpler, Less Precise)

Block the CDN subdomains entirely — model weights live there, not on the main domain:

```
BLOCK: cdn-lfs.huggingface.co
BLOCK: cdn-lfs-us-1.huggingface.co
ALLOW: huggingface.co
```

This breaks `huggingface-cli download` and `snapshot_download()` without touching the website. Limitation: the `/resolve/` blobs on the main domain still get through (smaller files like tokenizer configs).

### Option 3: Block HF_TOKEN Environment + Endpoint at OS/MDM level

For employee machines you control — deploy a policy that:

1. Prevents setting `HF_TOKEN` or `HUGGING_FACE_HUB_TOKEN` env vars
2. Blocks outbound to `cdn-lfs.*` via endpoint firewall (e.g., Jamf on macOS, Intune on Windows)

```bash
# Detect download attempts via audit log (Linux)
auditctl -a always,exit -F arch=b64 -S connect \
  -F exe=/usr/bin/python3 \
  -k hf_download_attempt
```

### Option 4: DNS-based (Rough, Not Recommended Alone)

```
# Unbound / Pi-hole / corporate DNS
local-zone: "cdn-lfs.huggingface.co." refuse
local-zone: "cdn-lfs-us-1.huggingface.co." refuse
```

Works but employees can bypass with DoH. Combine with TLS inspection for teeth.

## What Actually Breaks Download

| What you block | Effect |
|---|---|
| `cdn-lfs.huggingface.co` | Breaks weight downloads (>99% of model size) |
| `/resolve/` path on main domain | Breaks config/tokenizer file pulls |
| `/api/models` | Breaks `huggingface_hub` metadata queries |
| `HF_TOKEN` auth | Breaks gated model access only |

## Recommended Stack

```
TLS-inspecting proxy (Zscaler/Squid)
  └── ALLOW huggingface.co  (path: /, /models, /datasets, /spaces — HTML only)
  └── BLOCK huggingface.co/*/resolve/*
  └── BLOCK huggingface.co/api/*
  └── BLOCK cdn-lfs.huggingface.co
  └── BLOCK cdn-lfs-us-1.huggingface.co
```

This gives employees full read access to model cards, docs, leaderboards, and Spaces demos — while making `huggingface-cli download` and `snapshot_download()` fail with connection errors.
