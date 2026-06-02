---
audio: false
generated: true
image: false
lang: en
layout: post
title: Configure Hermes Agent Tools Menu
translated: false
type: note
---

**Question:** How to use the tools configuration menu (with options like Exa API key, Firecrawl, Tavily, Browserbase, etc.) in Hermes Agent?

**Answer:**

Hermes Agent (by Nous Research) provides an interactive setup system for configuring its many built-in tools, which extend the agent's capabilities like web search, content extraction, browser automation, image generation, TTS, memory, and more.

The menu you see is part of the interactive configuration interface (likely shown during `hermes setup`, `hermes tools`, or when enabling specific toolsets). Here's how to use and configure it step by step:

### 1. **Accessing the Tools Configuration**
- Run one of these commands in your terminal (after installing Hermes Agent):
  - `hermes setup` → Full interactive wizard (recommended for first-time setup; covers model + tools).
  - `hermes tools` → Specifically for enabling/disabling and configuring tools.
  - `hermes setup tools` → Targeted tools setup.
- Use arrow keys (`↑ ↓`) to navigate options.
- Press **SPACE** to toggle checkboxes (`[ ]` → `[x]`).
- Press **ENTER** to confirm selections.
- Press **ESC** to cancel/go back.

### 2. **What the Options Do**
The listed items are API keys and settings for different tool backends:

- **Web Search & Extraction Tools**:
  - Exa API key → Powers AI-native web search/extract (alternative backend).
  - Parallel API key → Another AI-native search/extract option.
  - Firecrawl API key → For web search, scraping, and crawling (highly recommended for robust performance).
  - Firecrawl API URL → Optional; use this for **self-hosted** Firecrawl instances (e.g., `http://localhost:3002`) instead of the cloud service.
  - Tavily API key → AI-native search, extract, and crawl.

- **Browser Automation**:
  - Browserbase API key / Project ID → Cloud browser support.
  - Browser Use API key → Alternative cloud browser backend.
  - Firecrawl browser session TTL → Timeout setting for browser sessions (default: 300 seconds).
  - Camofox browser server URL → For local anti-detection browsing (e.g., `http://localhost:9377`).

- **Other Tools**:
  - FAL API key → Image generation.
  - Tinker API key → RL (reinforcement learning) training.
  - Weights & Biases API key → Experiment tracking for RL.
  - OpenAI API key → Voice transcription (Whisper) and TTS.
  - ElevenLabs API key → Premium text-to-speech voices.
  - GitHub token → Higher rate limits and publishing skills in Skills Hub.
  - Honcho API key / Base URL → AI-native persistent memory (self-hosted option available).

Once toggled on, the interface will usually prompt you to paste the corresponding API key or URL.

### 3. **How Configuration is Saved**
- **API keys and secrets** are automatically saved to `~/.hermes/.env` (secure, owner-only permissions).
- **Non-secret settings** (e.g., which tools are enabled, backends) go to `~/.hermes/config.yaml`.
- You can also set values manually:
  ```bash
  hermes config set FIRECRAWL_API_KEY fc-YourKeyHere
  hermes config set FIRECRAWL_API_URL http://localhost:3002
  ```
- For web search backend preference, you can configure it in `config.yaml` under `web: backend: firecrawl` (or `tavily`, `exa`, etc.).

### 4. **Recommended Quick Setup Flow**
1. Run `hermes setup` or `hermes tools`.
2. Enable the tools you need (start with Firecrawl or Tavily for web capabilities — they are very reliable).
3. Paste your API keys when prompted.
4. For self-hosted options (e.g., local Firecrawl or Camofox), provide the local URL instead of a cloud key.
5. Confirm and exit — Hermes will load the tools on next run.

### 5. **Tips**
- You don't need every tool enabled. Start minimal (e.g., one web search backend + memory) to avoid unnecessary dependencies.
- Many tools work out-of-the-box with local models (via Ollama, vLLM, etc.).
- After configuration, test by chatting with the agent (CLI or via Telegram/Discord integration) and asking it to perform a web-related task.
- For full documentation, refer to the official Hermes Agent docs on tools and configuration.

This setup makes Hermes Agent highly extensible without writing custom code.

**References:**
- [Tools & Toolsets | Hermes Agent](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools/)
- [Configuration | Hermes Agent](https://hermes-agent.nousresearch.com/docs/user-guide/configuration/)
- [Environment Variables Reference](https://mintlify.com/NousResearch/hermes-agent/reference/environment-variables)
- [GitHub README - Hermes Agent](https://github.com/NousResearch/hermes-agent/blob/main/README.md)
