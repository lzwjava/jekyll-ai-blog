---
audio: false
generated: true
image: false
lang: en
layout: post
title: HuggingFace China Download Guide
translated: false
type: note
---

**Two env vars do all the work:**

| Variable                            | What it does                                                                                                             |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `HF_ENDPOINT=https://hf-mirror.com` | Route all HF Hub traffic through the China mirror. No proxy needed, doesn't touch your DMIT VPS.                         |
| `HF_HUB_ENABLE_HF_TRANSFER=1`       | Use the Rust `hf_transfer` client for parallel multi-chunk downloads (5–10× faster). Requires `pip install hf_transfer`. |

## One-off command

```bash
HF_ENDPOINT=https://hf-mirror.com HF_HUB_ENABLE_HF_TRANSFER=1 \
  python3.11 sample.py --init_from=gpt2-medium --start="Hello" --num_samples=1
```

## Make it permanent (recommended)

Add to `~/.bashrc` so you never forget:

```bash
export HF_ENDPOINT=https://hf-mirror.com
export HF_HUB_ENABLE_HF_TRANSFER=1
```

Then `source ~/.bashrc`. Every Python script that uses `transformers` / `datasets` / `huggingface_hub` will pick it up automatically.

## Pre-download (avoid downloading mid-training)

```bash
huggingface-cli download gpt2-medium                              # model
huggingface-cli download HuggingFaceFW/fineweb --repo-type=dataset --include="sample/10BT/*"  # dataset
```

Files land in `~/.cache/huggingface/hub/` and are reused by every subsequent `from_pretrained()` call.

## What it applies to

- `GPT.from_pretrained("gpt2-medium")` ← what nanoGPT's `sample.py` uses
- `AutoModel.from_pretrained(...)`, `AutoTokenizer.from_pretrained(...)`
- `datasets.load_dataset("HuggingFaceFW/fineweb", ...)` ← your fineweb runs
- `huggingface-cli download ...`

## Gotchas

- **`hf_transfer` has no progress retry** — if a download fails mid-way, it errors out instead of resuming. Unset `HF_HUB_ENABLE_HF_TRANSFER` if you hit repeated failures, then retry with the standard client.
- **Mirror lag** — `hf-mirror.com` mirrors the public hub with a short delay. Brand-new models (released today) may 404 for a few hours.
- **Private/gated models** — the mirror serves public files only. For gated repos (Llama, etc.) you still need `HF_TOKEN` and may need the real endpoint.
- **Don't combine with a proxy** — if `HTTPS_PROXY` is set, unset it for HF calls, otherwise you're back to burning DMIT bandwidth.

## Verify it's working

```bash
HF_ENDPOINT=https://hf-mirror.com huggingface-cli download gpt2 --quiet
echo $?   # 0 = success
```

Or watch the URL in the progress bar — should say `hf-mirror.com`, not `huggingface.co`.
