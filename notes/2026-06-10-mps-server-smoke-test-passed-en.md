---
audio: false
generated: true
image: false
lang: en
layout: post
title: MPS Server Smoke Test Passed
translated: false
type: note
---

Server is up on MPS. Now the smoke test — a chat completion:

Smoke test passed — killing the server now.

nanochat runs fine on this laptop. Summary:

- **Command:** `uv run python -m scripts.chat_web --source base --port 8000` (run from the repo root)
- The existing `.venv` works via `uv run`, torch 2.9.1 with **MPS** (Apple GPU) acceleration was auto-detected
- Only the base `d4` checkpoint exists locally (no SFT/RL checkpoints), hence `--source base` — the default `--source sft` would fail
- Smoke test passed: `/health` returned ready, and `/chat/completions` streamed tokens. Output is gibberish ("attention Place Francis species…"), which is expected — d4 is a tiny base model with no instruction tuning
- Server killed afterward (exit code 144 is just the pkill, not an error)

For PyCharm debugging: set the run config to module `scripts.chat_web` with parameters `--source base --port 8000`, working directory the repo root, and the `.venv` interpreter. The CLI alternative is [chat_cli.py](scripts/chat_cli.py) (`python -m scripts.chat_cli -i base`) if you want a simpler single-process target to step through.
