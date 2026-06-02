---
audio: false
generated: true
image: false
lang: en
layout: post
title: GitHub Archive to HF Sync
translated: false
type: note
---

## Summary

### 1. Switched GitHub remote from HTTPS to SSH

- Changed `origin` from `https://github.com/lzwjava/zz.git` to `git@github.com:lzwjava/zz.git`
- Pulled with `git pull --rebase` — remote had no new commits, so it was a no-op
- GitHub repo `lzwjava/zz` is **archived** (read-only) — this is intentional, stays as-is

### 2. Authenticated with Hugging Face

- `huggingface-cli` is deprecated → migrated to `hf` CLI
- Logged in with `hf auth login --token hf_...`
- Token saved to `~/.cache/huggingface/token`

### 3. Set up HF remote

- Initially added HF remote pointing to `datasets/lzwjava/zz` — wrong (repo not found, and datasets was incorrect type)
- Corrected to **models repo**: `https://huggingface.co/lzwjava/zz`
- Added as remote named `hf`

### 4. Resolved diverged histories

- HF repo had 3 independent commits (created via HF web UI/upload):
  - `3dbedad` initial commit
  - `0980be1` Upload folder using huggingface_hub
  - `3894b4d` Update README
- Local had completely different history (unrelated root commits)
- **Force-pushed** local `main` (8977f51) to HF, overwriting HF's old commits

### Current state

```
origin  → git@github.com:lzwjava/zz.git  (archived, read-only)
hf      → https://huggingface.co/lzwjava/zz  (active, synced)
```

Local branch `main` is in sync with HF. Future workflow: `git push hf main` to sync.
