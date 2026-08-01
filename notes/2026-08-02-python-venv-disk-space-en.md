---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python venv disk space
translated: false
type: note
---

Question: Does a Python venv take up a lot of disk space?

Answer: The venv shell itself is tiny (~10-20MB — just a python symlink + pip + basic stdlib stubs). The space hog is whatever you `pip install` into it, and that duplicates per-venv unless you dedupe.

Check the actual breakdown:

```bash
python3 -m venv /tmp/test-venv
du -sh /tmp/test-venv
# ~10-20MB

source /tmp/test-venv/bin/activate
pip install torch
du -sh /tmp/test-venv
# 2-6GB depending on CUDA build
```

Where it actually blows up for your workflow (GPU/LLM stuff):

```bash
# torch+cuda wheels are the killer
pip show torch | grep Location
du -sh $(python -c "import torch, os; print(os.path.dirname(torch.__file__))")
# torch alone: ~2.5GB with CUDA 12.x bundled
```

If you spin up a venv per project (agent dev, fine-tuning experiments), N venvs × torch = N × 2-6GB. This adds up fast on a dev box.

**Fixes, in order of what I'd actually use:**

1. **`uv` instead of `pip`/`venv`** — hardlinks packages from a global cache, so 10 venvs with torch cost ~1x the disk, not 10x:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv .venv
uv pip install torch
# subsequent venvs installing torch reuse the cache via hardlinks
```

2. **Check/clean uv's cache size:**
```bash
uv cache dir
du -sh $(uv cache dir)
uv cache clean  # nuke it if disk pressure
```

3. **`pip cache` also helps somewhat** (not hardlinked, but avoids re-downloading):
```bash
pip cache info
pip cache purge
```

4. **`--system-site-packages`** if you want a shared base venv and only isolate a few packages:
```bash
python3 -m venv .venv --system-site-packages
```

For your setup (MI300X training, multiple CLI agents), `uv` is the real fix — pip/venv's per-project duplication is the actual disk problem, not venv itself.

References:
- [uv docs — cache](https://docs.astral.sh/uv/concepts/cache/)
- [uv install](https://docs.astral.sh/uv/getting-started/installation/)