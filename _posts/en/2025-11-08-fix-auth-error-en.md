---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Fix Translation API Authentication Error
translated: false
type: note
---

### Analysis of the Workflow and Error Cause

Your GitHub Actions workflow for "Translate Recent Notes" looks well-structured overall—it's checking out the repo, setting up Python, installing deps, running a translation script on the N most recent posts, and committing changes to `_notes/`. However, based on the logs you shared earlier (with the 401 errors during translation to languages like ar, de, fr, etc.), the issue is in the authentication for the translation API calls inside `scripts/translation/update_lang_notes.py`.

#### Root Cause
- The error `"No cookie auth credentials found"` (HTTP 401) is specific to the **OpenRouter API** (or a Python client/library interacting with it, like LiteLLM or an unofficial SDK). This happens when the API request lacks proper authentication headers.
- OpenRouter expects `Authorization: Bearer <your_openrouter_api_key>` in requests. If the key isn't passed correctly, some clients fall back to (or misinterpret as needing) cookie-based session auth, triggering this exact error.
- In your workflow:
  - You're setting `OPENROUTER_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}`, which passes a secret value to the script's environment.
  - But the script likely isn't reading/using this env var correctly. Common mismatches:
    - The script expects `OPENAI_API_KEY` (for OpenAI-compatible endpoints like OpenRouter).
    - Or it's using a library (e.g., `openai` Python SDK) without setting the base URL to `https://openrouter.ai/api/v1`.
    - The secret `DEEPSEEK_API_KEY` might actually hold your **OpenRouter API key** (routed to DeepSeek/Grok models), but if it's a direct DeepSeek key, it won't work for OpenRouter.
- From the logs, the script is using model `'x-ai/grok-4-fast'` (Grok 4 via OpenRouter), and it's processing front matter/titles successfully but failing on content translation per language.
- This isn't a GitHub Actions issue—it's in the Python script's API client setup. The workflow continues to the commit step (hence the `git config user.name "github-actions[bot]"` log), but without translations, only English files get added.

#### Recommended Fixes
1. **Update Environment Variables in Workflow**:
   - Align with common OpenRouter setups (OpenAI-compatible). Change the `env` block in the "Translate posts" step to:
{% raw %}
     ```
     env:
       GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
       OPENAI_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}  # Rename var to what the script expects
       OPENAI_BASE_URL: https://openrouter.ai/api/v1   # Required for routing to OpenRouter
     ```
{% endraw %}
   - If `DEEPSEEK_API_KEY` is your OpenRouter key, great. If it's a direct DeepSeek key, create a new secret `OPENROUTER_API_KEY` in repo settings with your actual OpenRouter key (get one at [openrouter.ai/keys](https://openrouter.ai/keys)).
   - Test: Add `echo $OPENAI_API_KEY` (redacted) to the run step for debugging in logs.

2. **Fix the Python Script (`update_lang_notes.py`)**:
   - Ensure it initializes the OpenAI client like this (assuming `openai` library):
     ```python
     import os
     from openai import OpenAI

     client = OpenAI(
         api_key=os.getenv("OPENAI_API_KEY"),
         base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")  # Defaults to OpenAI if not set
     )

     # Then use client.chat.completions.create(..., model="x-ai/grok-4-fast")
     ```
   - If using LiteLLM (common for multi-provider): Install it if not in `requirements.txt`, and call `completion(model="openrouter/x-ai/grok-4-fast", api_key=os.getenv("OPENAI_API_KEY"), api_base="https://openrouter.ai/api/v1", ...)`.
   - For the translation loop: Add error handling per language (e.g., `try/except` around API calls, log failures, skip if 401).
   - Handle cookies explicitly? Unlikely needed—stick to API keys. If the script has browser/Selenium code, remove it for CI reliability.

3. **Workflow Improvements**:
   - **Input Validation**: Add a check for N=0 or invalid `--n` to avoid processing nothing.
   - **Conditional Commit**: Your `git diff --cached --quiet || git commit` is good, but update the message to reflect all languages: `-m "Add translated posts (ar, de, es, fr, hi, ja, zh, hant)"`.
   - **Caching**: Add `actions/cache` for `pip` to speed up installs.
   - **Debug Mode**: Add an optional input `debug: true` and `--debug` flag to the script for verbose logging.
   - **Permissions**: Ensure the `github-pages` environment has read/write access if needed.
   - Full updated YAML snippet for the "Translate posts" step:
{% raw %}
     ```
     - name: Translate posts
       run: |
         python scripts/translation/update_lang_notes.py --n ${{ inputs.n }}
       env:
         GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
         OPENAI_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
         OPENAI_BASE_URL: https://openrouter.ai/api/v1
     ```
{% endraw %}

4. **Testing Steps**:
   - **Local Test**: Run `python scripts/translation/update_lang_notes.py --n 1` locally with env vars exported (e.g., `export OPENAI_API_KEY=your_key`).
   - **Workflow Test**: Trigger with `workflow_dispatch` and N=1, check logs for API calls.
   - **Verify Secret**: In repo settings > Secrets, confirm `DEEPSEEK_API_KEY` has a valid OpenRouter key (starts with `sk-or-...`).
   - If still failing, add `--verbose` to the script and inspect request headers (e.g., via `print(client.api_key)`).

This should resolve the 401s and get translations flowing. If you share snippets from `update_lang_notes.py` (e.g., the API client init), I can pinpoint more precisely.

#### References
- [OpenRouter Quickstart (API Auth Setup)](https://openrouter.ai/docs/quickstart)
- [LiteLLM OpenRouter Integration](https://docs.litellm.ai/docs/providers/openrouter) (if using)
- [GitHub Issue on Similar OpenRouter Auth Error](https://github.com/mendableai/firecrawl/issues/1352)
- [Reddit Thread on OpenRouter 401 Errors](https://www.reddit.com/r/openrouter/comments/1oqiaol/error_401_no_cookie_auth_credentials_found/)