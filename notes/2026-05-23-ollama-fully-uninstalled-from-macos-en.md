---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ollama Fully Uninstalled from macOS
translated: false
type: note
---

Done. Here's what was removed:

- /Applications/Ollama.app — the app (auto-started on login)
- /Applications/Ollamac.app — GUI client
- /usr/local/bin/ollama — CLI binary
- ~/.ollama — 6.1GB of model blobs
- ~/Library/Application Support/Ollama — Electron app data
- ~/Library/LaunchAgents/com.ollama.ollama.plist — auto-start daemon
- Caches, preferences, HTTP storage — all Electron leftovers

~6.1GB freed. No Ollama login items remain. The only leftover is a tiny SIP-protected Ollamac container (~1KB metadata) in ~/Library/Containers/ which macOS won't let you delete — harmless.
