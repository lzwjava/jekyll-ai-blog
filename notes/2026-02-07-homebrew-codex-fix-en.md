---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix Homebrew Codex Binary Conflict
translated: false
type: note
---

**Question:** Why does `brew install --cask codex` fail with the error "It seems there is already a Binary at '/opt/homebrew/bin/codex'" on macOS, and how to fix it?

**Answer:**

This error occurs because **Homebrew detects an existing `codex` binary** already present at `/opt/homebrew/bin/codex` (the standard location for Homebrew-linked binaries on Apple Silicon Macs). Homebrew's cask installation process refuses to overwrite or replace an existing file there to avoid accidentally breaking your current setup.

The most common cause in your case (given your earlier `codex --version` showed `codex-cli 0.36.0`) is that you **previously installed Codex via npm** (`npm install -g @openai/codex`), which placed its binary in a global npm bin directory (often `/opt/homebrew/bin` on Apple Silicon when using Homebrew-installed Node, or `~/.npm-global/bin`, with a symlink). Later, when you try the Homebrew cask method, it conflicts because both methods try to manage the same command name (`codex`) in the same path.

### How to confirm the current installation source
Run:
```bash
which codex
```
- If it shows `/opt/homebrew/bin/codex` → likely from npm (symlinked) or an old/partial Homebrew install.
- Run `ls -l /opt/homebrew/bin/codex` to see if it's a symlink (pointing to an npm location → npm install).

### Recommended solutions (pick one)

1. **Keep using npm (simplest if you prefer npm ecosystem)**
   - Uninstall the attempted cask first (if partially installed):
     ```bash
     brew uninstall --cask codex
     ```
   - Update your existing npm version to the latest (as of February 2026, versions are in the 0.9x range):
     ```bash
     npm install -g @openai/codex@latest
     codex --version   # should show something like 0.98.0 or higher
     ```

2. **Switch to Homebrew cask (recommended by many for macOS, avoids npm/Node dependency)**
   - First, remove the conflicting binary (most likely from npm):
     ```bash
     npm uninstall -g @openai/codex
     ```
     - If the binary still exists, manually remove the link:
       ```bash
       rm /opt/homebrew/bin/codex
       ```
       (Be careful: only do this if you're sure it's from npm and not needed elsewhere.)
   - Now retry the cask install:
     ```bash
     brew install --cask codex
     ```
   - It should succeed and place a fresh binary at `/opt/homebrew/bin/codex`.
   - Verify:
     ```bash
     codex --version   # expect a recent Rust-based version like 0.98.0+
     ```

3. **Clean everything and reinstall via one method**
   - Uninstall both:
     ```bash
     brew uninstall --cask codex   # ignore if not installed
     npm uninstall -g @openai/codex
     rm -f /opt/homebrew/bin/codex   # force-remove symlink/binary if still there
     ```
   - Then install via your preferred method (npm or brew --cask).

**Notes:**
- The official documentation currently emphasizes `npm i -g @openai/codex` as the primary install method, with Homebrew as an alternative.
- Both methods install the same Rust-based Codex CLI binary in recent versions (post-0.5x or so), so functionality is identical.
- After switching methods, you may need to re-authenticate (`codex login`) or reconfigure any settings.
- Your proxy settings (127.0.0.1:7890) were detected and used successfully during the download, so that's not the issue.

**References:**

- [https://developers.openai.com/codex/cli](https://developers.openai.com/codex/cli)
- [https://github.com/openai/codex](https://github.com/openai/codex)
- [https://www.npmjs.com/package/@openai/codex](https://www.npmjs.com/package/@openai/codex)
- [https://github.com/openai/codex/issues/5607](https://github.com/openai/codex/issues/5607) (related Homebrew formula vs cask confusion, though your case is binary conflict)
- [https://formulae.brew.sh/cask/codex](https://formulae.brew.sh/cask/codex)
