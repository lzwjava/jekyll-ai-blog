---
audio: false
generated: true
image: false
lang: en
layout: post
title: DeepSeek Pipeline Now Works
translated: false
type: note
---

## Summary

### ✅ The DeepSeek LLM path now works end-to-end

The trial completed: **50 agent episodes, 1.12M input tokens, 8 min runtime** — the agent loop, Docker container, terminal sessions, and result collection all functioned correctly with DeepSeek. The task itself wasn't solved (it's a "hard" task, expert estimate ~240 min, capped at 20 min — an 8-min run with a 1.5B-param-class chat model isn't expected to finish it), but that's a model-capability question, not a pipeline problem.

### What was wrong & fixed this round

**The `BadRequestError` you saw**: DeepSeek's API rejects litellm's JSON-schema `response_format` ("This response_format type is unavailable now") — it only supports `{"type": "json_object"}`. The harness thought DeepSeek supported schemas and never used its built-in fallback.

**Fixes in the repo** (uncommitted so far):

| File | Change |
| --- | --- |
| `terminal_bench/llms/lite_llm.py` | On `BadRequestError` mentioning `response_format`, auto-retry using the prompt-template fallback (schema embedded in prompt) |
| `terminal_bench/utils/parsing.py` | New: strips markdown code fences before JSON parsing |
| `terminal_bench/agents/terminus_1.py` + `naive_agent.py` | Parse through fence-stripper |

**Also done**: reinstalled the `tb` tool from the patched repo (`uv tool install --force .`) so your installed `tb` command has the fix.

### Full session recap

1. **Benchmark harness verified** — oracle run passed (100%) once the network was fixed
2. **Network fix** — containers now route through your mihomo proxy (`host.docker.internal:7890`, ~30x faster): patched all 241 task compose files, added ufw rule for Docker subnet, fixed daemon.json
3. **Pushed to your fork** — `lzwjava/terminal-bench` `main` now has the compose proxy commit (`932e446`)
4. **DeepSeek integration** — harness now gracefully falls back for providers that reject schema-based `response_format`

### Next steps (say the word)

- **Commit & push the DeepSeek fixes** to your fork (4 files)
- **Run more tasks** with DeepSeek — e.g. an easy task to see a real pass, or a small batch
- **Raise the agent cap** (`--global-agent-timeout-sec`) if you want longer per-task attempts — note each hard task can cost ~1M+ tokens

Want me to commit/push the DeepSeek fixes now?
