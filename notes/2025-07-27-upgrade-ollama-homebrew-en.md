---
audio: false
generated: true
image: false
lang: en
layout: post
title: Upgrade Ollama with Homebrew
translated: false
type: note
---

To upgrade Ollama to the latest version (currently v0.10.0 as of July 2025) using Homebrew on macOS, follow these steps:

1. Update Homebrew's formulae to ensure it knows about the latest available versions:
   ```
   brew update
   ```

2. Upgrade Ollama specifically:
   ```
   brew upgrade ollama
   ```

3. Verify the upgrade by checking the version:
   ```
   ollama --version
   ```

If you're running Ollama as a background service, restart it after the upgrade:
```
brew services restart ollama
```

Alternatively, if you run it manually, stop any existing process and start it again with your preferred command (e.g., from the caveats in your install output):
```
OLLAMA_FLASH_ATTENTION="1" OLLAMA_KV_CACHE_TYPE="q8_0" /opt/homebrew/opt/ollama/bin/ollama serve
```

No special upgrade instructions are needed beyond this standard process.

[Ollama Releases](https://github.com/ollama/ollama/releases)
