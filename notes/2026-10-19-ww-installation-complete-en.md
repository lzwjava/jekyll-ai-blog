---
audio: false
generated: true
image: false
lang: en
layout: post
title: WW Installation Complete
translated: false
type: note
---

Done. Here's what was installed:

1. **uv** — installed to `~/.local/bin` (already in your `PATH` via `.bashrc`)
2. **Python 3.13** — downloaded via uv because the system Python 3.14 isn't compatible with `torch`
3. **venv + all 230 dependencies** — synced into `.venv/` (includes torch, transformers, playwright, etc.)
4. **Global `ww` command** — symlinked `~/.local/bin/ww` → `.venv/bin/ww`
5. **Zsh completions** — copied to `~/.zsh/completions/_ww`

**Verify it works:**

```bash
ww
ww weather
```

**Notes:**

- Your `.env` is already present with `OPENROUTER_API_KEY` and `MODEL` configured.
- If you use **zsh**, run `autoload -Uz compinit && compinit` to reload completions.
- Run commands with `ww <group> <subcmd>` from anywhere, or `uv run ww <cmd>` if you prefer not using the symlink.
- Some modules (e.g. `ww screenshot`, `ww macos`) are macOS-only and will fail on Linux.
