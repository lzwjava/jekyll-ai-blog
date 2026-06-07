---
audio: false
generated: true
image: false
lang: en
layout: post
title: "ww: Developer Productivity Toolkit"
translated: false
type: note
---

## This is **`ww`** — a cross-platform CLI toolkit for developer productivity 🚀

It's a Python-based command-line tool (version 0.1.0) that serves as a **Swiss Army knife** for developers with **LLM-powered intelligence** integrated throughout. Here's what it covers:

### Core Capabilities

| Category | What it does |
|----------|-------------|
| **🔄 Git** | AI commit messages, squash commits, force push, diff trees, commit classification |
| **🐙 GitHub** | Repo listing, notifications, starred repos, follower management, AI commit generation |
| **🖼️ Image** | Screenshot capture, crop, compress, background removal, EXIF scanning, image generation |
| **📄 PDF** | Convert PDF to Markdown/LaTeX, code-to-PDF, parse Cloudflare Analytics PDFs |
| **🌐 Web Search** | Multi-engine search (Tavily, etc.) with AI-powered results |
| **🔍 Network** | WiFi scanning, IP/port scanning, network topology, DNS queries, speed tests |
| **💻 System** | macOS/Linux monitoring, process management, host info |
| **📝 Notes** | Git-integrated note-taking, log entries, sensitive data obfuscation |
| **🗣️ Speech** | Whisper transcription with AI refinement |
| **📊 Cloudflare** | Web Analytics (page views, visits), zone management |
| **🛡️ Clash Proxy** | Proxy management, speed testing, DNS resolution, Wi-Fi toggling |
| **🎓 Education** | Self-study degree notice scraper with AI categorization |
| **🤖 LLM** | Model comparison, RAG document indexing, OpenRouter management |
| **🛠️ Other** | Marp presentations, Ghostty terminal control, GitHub Actions triggering, Java/Maven analysis, Cloudflare analytics, and much more |

### Technical Stack

- **Python ≥ 3.11** with `uv` as the recommended package manager
- Integrates with **Google Gemini**, **OpenRouter**, **Whisper**, **Tavily**
- macOS-specific features leverage native frameworks (Quartz, CoreWLAN, CoreText)
- Cross-platform (macOS, Linux)

In short, it's a **personal developer productivity powerhouse** that automates everything from git workflows to network diagnostics, all accessible via `ww <group> <command>`.
