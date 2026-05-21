---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ollama Completely Removed from System
translated: false
type: note
---

Comprehensive summary — **Ollama is fully removed from startup, and not running anywhere**:

| Check | Result |
|-------|--------|
| **launchd (user agent)** `com.ollama.ollama` | ❌ Not registered |
| **LaunchAgent plist** (user) | ❌ No plist file found |
| **LaunchAgent plist** (system) | ❌ No plist file found |
| **LaunchDaemon plist** (system) | ❌ No plist file found |
| **brew services** | ❌ Not loaded, not running |
| **ollama process running** | ❌ Zero processes |
| **macOS login items** | ❌ Not listed |
| **OLLAMA_ env vars** | ❌ None set |
| **Port 11434 listener** | ❌ No listener on default Ollama port |
| **Docker Ollama container** | ❌ Not running |

All nine attack surfaces for auto-start are clean. Nothing will start Ollama on boot, and nothing is currently serving or listening.