---
audio: false
generated: true
image: false
lang: en
layout: post
title: Smoke test now passes
translated: false
type: note
---

Done — your smoke test now **passes**. Here's the full story:

## What happened

| Run | Result | Why |
| --- | --- | --- |
| 1st (`00-08-32`) | ✗ test timeout @60s | Test script downloads apt + uv + pytest from the internet; your network is ~70 kB/s direct |
| 2nd (`00-14-54`) | ✗ timeout @600s | Even 10 min wasn't enough — the 35 MB `uv` binary alone takes ~10 min |
| 3rd (`00-35-42`) | **✅ 100% accuracy** | Proxy fix — test completed in **31.3s** |

The harness itself was never broken — it was purely a network speed issue: the task containers had no internet proxy, while your host has mihomo on `127.0.0.1:7890` (5.4 MB/s via GitHub through it).

## What I fixed (3 changes)

1. **`/etc/docker/daemon.json`** — proxy was already configured but pointing at `localhost:7890` (useless inside containers) and never loaded. Now: `http://172.17.0.1:7890` (helps image pulls too). Backup saved at `daemon.json.bak`.
2. **ufw rule** — your existing rule allowed port 7890 only on `docker0`, but each benchmark trial creates a *new* compose bridge. Added: `ufw allow from 172.16.0.0/12 to any port 7890 proto tcp`.
3. **All 241 `docker-compose.yaml` files** in `original-tasks/` — injected proxy env vars + `host.docker.internal:host-gateway` (overridable via `T_BENCH_HTTP_PROXY`). This is what actually gets the proxy *into* the containers.

## Run your real benchmark now

```bash
cd /mnt/data/terminal-bench

# one task with DeepSeek
tb run --dataset-path original-tasks --agent terminus \
  --model deepseek/deepseek-chat -t "3d-model-format-legacy" \
  --n-concurrent 1 --no-rebuild

# full 241-task run (the actual benchmark)
tb run --dataset-path original-tasks --agent terminus \
  --model deepseek/deepseek-chat --n-concurrent 4
```

## Notes

- `git status` shows 241 modified compose files — revert anytime with `git checkout -- original-tasks` (but then re-run the patch: `python3 /tmp/patch_proxy2.py`). I can add the script to the repo if you like.
- Your Docker services all restarted cleanly. **nextcloud-app-1 has a pre-existing issue** (image 33.0.0.16 vs data version 33.0.2.2 — needs `docker compose pull` for the newer image; the fast proxy makes that quick now).
- Full benchmark tips: use `--no-rebuild` after the first run per task, watch disk space (each trial builds ~1.5 GB images, cleaned by default), and consider `--n-concurrent 4` for throughput.

Want me to kick off the DeepSeek run on one task to verify the LLM path too?
