---
audio: false
generated: true
image: false
lang: en
layout: post
title: SGLang Compiled and Running
translated: false
type: note
---

Everything is set up and verified working. Here's the full summary:

## Done: SGLang compiled & running

**Build** (installed into system Python 3.12's user site, no venv):

```
/usr/bin/python3.12 -m pip install -e "python" --user --break-system-packages
```

- PEP 668 needed `--break-system-packages`; packages went to `~/.local/lib/python3.12/site-packages`
- Editable install: Python changes in `/mnt/data/sglang/python/` are live immediately
- All 3 Rust extensions (`sglang.srt.grpc._core`, `sglang.srt.multimodal._core`, `sglang.srt.server._core`) compiled into the source tree
- Fixed a pre-existing torch/torchvision/torchaudio CUDA mismatch — all now `2.11.0+cu130`

**Currently running:** Qwen2.5-0.5B-Instruct server at `http://localhost:30010` (PID 2170340). Verified: chat completion → "Paris" ✓

## Two machine-specific gotchas discovered

1. **HF Xet downloads stall** — model downloads froze at ~84 MB until I disabled the transfer protocol. Always set:

   ```bash
   export HF_HUB_DISABLE_XET=1
   ```

2. **Ports 30000/30001 are taken** by other apps on this machine (`cef_server` and PyCharm). Use e.g. `--port 30010`.

## Working with the project

```bash
# Start the server (recommended entrypoint)
export HF_HUB_DISABLE_XET=1
python3.12 -m sglang.launch_server --model-path Qwen/Qwen2.5-0.5B-Instruct --port 30010

# Send requests (OpenAI-compatible)
curl http://localhost:30010/v1/chat/completions -H "Content-Type: application/json" \
  -d '{"model": "Qwen/Qwen2.5-0.5B-Instruct", "messages": [{"role": "user", "content": "Hi!"}]}'

# Unit tests (mirror python/sglang/srt/ under test/registered/unit/)
pytest test/registered/unit/ -v

# Lint before committing
pre-commit install && pre-commit run --all-files
```

**Dev workflow notes:**

- Python edits → just restart the server (editable install)
- Rust edits (`rust/`) → re-run `pip install -e "python"` to rebuild
- Use `sglang serve` as CLI (it's the new recommended entrypoint; `launch_server` still works with a deprecation warning)
- Work on a feature branch, never `main`; check `.github/CI_PERMISSIONS.json` for CI-trigger commands (`/rerun-failed-ci`, etc.)

The server is left running — stop it anytime with `pkill -f sglang.launch_server`. Want me to stop it, or set up something else (e.g., a `bench_serving` run or a different model)?
