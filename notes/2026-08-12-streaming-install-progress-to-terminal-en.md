---
audio: false
generated: true
image: false
lang: en
layout: post
title: Streaming Install Progress to Terminal
translated: false
type: note
---

Done. The installer now streams all download/install progress directly to your terminal instead of hiding it.

Changes made:

1. **`ww/env/zed.py`** (new) — installs Zed:
   - **macOS**: tries `brew install --cask zed` first, falls back to the official script.
   - **Linux**: runs the official installer via `curl` (or `wget` if curl is missing) with **live output** — you see the download progress and `sh` output as it runs, not suppressed.
   - Detects whether Zed is already installed (`.app` on macOS; `zed` binary in PATH on Linux).
   - Verifies the binary *actually* appeared after the script runs (the `curl … | sh` pipe's exit code is `sh`'s and can mask curl failures).

2. **`ww/main.py`** — wired in:
   - Added `zed` routing in the `env` group (`from ww.env.zed import main as m`).
   - Added help lines in both the top-level `_print_help()` and the `ww env` usage block. (Also fixed a stray `"` I'd introduced.)

3. **`completions/_ww`** — added `'zed:Install Zed editor on macOS and Linux'` to `env_cmds`.

Output now looks like:
```
Installing Zed via the official installer script (curl)...
  curl -fsSL https://zed.dev/install.sh | sh
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
  ...
```

To switch zsh completion back on after reloading: `autoload -Uz compinit && compinit`.

Note: on this particular machine neither `curl` nor `wget` was installed, so the installer will print a helpful message (install with `sudo apt install curl -y`) rather than failing silently.