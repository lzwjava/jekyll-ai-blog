---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenClacky Keys for Claude DeepSeek Gemini
translated: false
type: note
---

Right, mostly correct. Some refinements:

**Correct**
- `providers.rb:28-76` defines the OpenClacky preset: `base_url: https://api.openclacky.com`, get key at `https://www.openclacky.com/ai-keys`.
- Full Claude lineup is preset and selectable in the model dropdown: `abs-claude-opus-4-7 / 4-6`, `abs-claude-sonnet-4-6 / 4-5`, `abs-claude-haiku-4-5`.
- Domain is reachable from mainland China — no proxy/VPN needed.

**Worth adding**
- The same key also covers non-Claude models: `dsk-deepseek-v4-pro / flash` (DeepSeek, text-only) and `or-gemini-3-1-pro` (Gemini 3.1 Pro, multimodal). So "freely switch" isn't just within the Claude family — one key spans Claude + DeepSeek + Gemini.
- `api` field is `"bedrock"` (not the OpenAI or Anthropic shim), meaning requests follow the Bedrock protocol shape. Usually transparent, but matters if you front it with a custom proxy.
- Unlike OpenRouter (the one from the previous analysis with `models: []` and the "Dynamic - fetched from API" comment), OpenClacky ships a curated static list of 7 models — no dynamic fetch needed.

So a tighter pitch would be: "OpenClacky aikeys — one key, freely switch across Claude / DeepSeek / Gemini, direct connect from mainland China, no special network required."