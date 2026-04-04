---
audio: false
generated: true
image: false
lang: en
layout: post
title: Image Analysis Fix Post-Mortem
translated: false
type: note
---

**Image Analysis Fix - Full Post-Mortem**

---

## Root Cause

The `image` tool defaults to `openai/gpt-5-mini`, but the configured OpenAI API key was expired (`999VUv4m...`), causing a 401 error.

---

## Fix Steps

**Step 1: Locate the config**
```bash
openclaw config get agents.defaults.imageModel
# No output (not set)
cat ~/.openclaw/openclaw.json | grep image
```
Found that `imageGenerationModel` was set, but `imageModel` (for analysis) was missing.

**Step 2: Attempted to set Gemini model**
```bash
openclaw config set agents.defaults.imageModel.primary google/gemini-3-pro-image-preview
```
→ Failed — `gemini-3-pro-image-preview` doesn't exist in the google provider (models array was empty).

**Step 3: Use available model on OpenRouter**
```bash
openclaw config get agents.defaults.models
```
Found the available Gemini model on OpenRouter: `openrouter/google/gemini-3-flash-preview`

**Step 4: Set correctly**
```bash
openclaw config set agents.defaults.imageModel.primary openrouter/google/gemini-3-flash-preview
```
→ ✅ Success

**Step 5: Restart Gateway**
```bash
openclaw gateway restart
```
→ SIGTERM sent, but gateway didn't auto-restart. Manually ran `start` to fix.

---

## Final Config

```json
"agents": {
  "defaults": {
    "imageModel": {
      "primary": "openrouter/google/gemini-3-flash-preview"
    },
    "imageGenerationModel": {
      "primary": "google/gemini-3-pro-image-preview"
    }
  }
}
```

- **Analysis (image tool)**: `openrouter/google/gemini-3-flash-preview` ✅
- **Generation (image_generate)**: `google/gemini-3-pro-image-preview` ✅ (using Google native key)

---

## Lessons Learned

1. OpenRouter model format is `openrouter/provider/model-id`
2. Google provider's models array was empty — all models need to be accessed via OpenRouter
3. Gateway didn't auto-restart after SIGTERM — possibly systemd startup timeout. Adding `sleep` or checking dependencies next time