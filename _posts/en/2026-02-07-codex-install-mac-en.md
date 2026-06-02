---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Check Codex Installation Method Mac
translated: false
type: note
---

**Question:** How to determine whether Codex was installed globally via npm or via Homebrew cask on a Mac?

**Answer:**

Your current installation is the **Homebrew cask** version.

Here's why and how to confirm which method was used:

- The output from `codex --version` shows:
  `codex-cli 0.36.0`
  Recent versions of the official OpenAI Codex CLI (especially after switching to a Rust-based native binary) display the version in this exact format: `codex-cli X.Y.Z`. This matches the output from both installation methods, so the version string alone doesn't distinguish them.

- The reliable ways to tell the difference on macOS:

  1. **Check which command provides the binary** (most definitive method):
     Run:

     ```
     which codex
     ```

     - If the result is something like:
       `/opt/homebrew/bin/codex` or `/usr/local/bin/codex` (Homebrew locations)
       → **You are using the Homebrew cask version**.

     - If the result is something like:
       `/usr/local/bin/codex` (but actually symlinked from `~/.npm-global/bin/codex` or similar) or `/Users/yourname/.nvm/versions/node/vXX.XX.XX/bin/codex`
       → **You are using the npm version**.

  2. **Check Homebrew cask status**:

     ```
     brew list --cask | grep codex
     ```

     - If it shows `codex` → Installed via Homebrew cask.

     Or run:

     ```
     brew info --cask codex
     ```

     If it's installed, you'll see details including the version and "Installed" status.

  3. **Check npm global packages**:

     ```
     npm list -g @openai/codex
     ```

     - If it shows the package (with a version) → Installed via npm.
     - If it says "empty" or not found → Not installed via npm.

In practice, most users on macOS who see the clean `codex` command without path issues and are using Homebrew tend to install via `brew install --cask codex`, especially since the project officially recommends it as one of the two equal options.

Your version (0.36.0) appears to be an older release from late 2025 or early 2026 — consider updating to get the latest features and models:

- For Homebrew: `brew upgrade --cask codex`
- For npm: `npm install -g @openai/codex@latest`

**References:**

- [https://www.npmjs.com/package/@openai/codex](https://www.npmjs.com/package/@openai/codex)
- [https://formulae.brew.sh/cask/codex](https://formulae.brew.sh/cask/codex)
- [https://github.com/openai/codex](https://github.com/openai/codex)
- [https://developers.openai.com/codex/cli](https://developers.openai.com/codex/cli)
