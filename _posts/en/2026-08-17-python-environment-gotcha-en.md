---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python environment gotcha
translated: false
type: note
---

Everything needed is already set up on this machine — the only tricky part is the Python environment. Here's the situation and how to run it:

## Key gotcha: which Python to use

- `minisgl` 0.1.0 is installed **editable** from this repo (`/usr/local/lib/python3.12/dist-packages` → `/mnt/data/mini-sglang`), so no install step is needed.
- The **system** site-packages has the compatible combo: `torch 2.9.1 + sgl_kernel 0.3.21 + flashinfer 0.6.16`.
- Your **user** site-packages (`~/.local`) shadows it with `torch 2.11.0`, which breaks `sgl_kernel` (undefined symbol `c10_cuda_check_implementation`).

So **don't** run plain `python -m minisgl` — use the repo's wrapper, which runs `/usr/bin/python3.12 -s` (skips the user site):

## Run the OpenAI-compatible server

```bash
cd /mnt/data/mini-sglang
./run_python.sh -m minisgl --model "Qwen/Qwen3-0.6B"
```

`Qwen3-0.6B` is already cached in `~/.cache/huggingface`, and it fits easily on your RTX 4070 (12 GB, ~1.5 GB currently in use). Defaults: port `1919`, host `localhost`.

## Test it

```bash
curl http://localhost:1919/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "Qwen/Qwen3-0.6B", "messages": [{"role": "user", "content": "Hello!"}], "max_tokens": 64}'
```

## Alternatives

- **Terminal chat**: `./run_python.sh -m minisgl --model "Qwen/Qwen3-0.6B" --shell-mode` (note: the CLI flag is `--shell-mode`, not `--shell` as the README shows)
- **Custom port**: `--port 30000`
- **Tensor parallelism** (multi-GPU): `--tp-size 4`
- **Disable radix cache** (ablation): `--cache-type naive`

Want me to launch the server now and verify it responds?
