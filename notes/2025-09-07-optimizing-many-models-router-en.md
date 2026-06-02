---
audio: false
date: 2025-09-07
generated: true
image: false
lang: en
layout: post
title: Optimizing Your Many-Models Code Router
translated: false
type: note
---

Short answer: yes—your “many-models router” can absolutely underperform compared to a tightly-integrated stack like Codex (OpenAI’s code assistant) that’s tuned end-to-end on one family of models plus deep IDE context. Here’s why and how to fix it fast.

### Why Codex can feel better

* **One brain per task.** Staying on a single model preserves its latent plan and coding style. Jumping between models mid-task resets that plan and often introduces conflicting conventions.
* **Vertical integration.** Codex (OpenAI) controls model → tool calls → repo index → tests → inline edits. That closed loop gives it richer signals (symbol graph, file heatmaps, failing tests) with less glue code latency.
* **Prompt + policy alignment.** Their prompts, code formatters, and “make a minimal, compilable diff” heuristics are co-designed for GPT-5 family. A general router can easily mis-specify temperature, stop sequences, or patch format for some models.
* **Latency/throughput.** Each extra hop (proxy, OpenRouter middleware, model negotiation) adds jitter. Coding workflows are feedback-tight; 300–800 ms of added latency per turn noticeably hurts “flow”.
* **Context quality.** IDE integrations that compute a repo map (topology of files, symbols, recent changes) beat “just dump long context”. Long contexts without structure waste tokens and dilute attention.

### What in your config is likely hurting you

* **Model sprawl.** You’re mixing generalists, coders, and thinking models. The “thinking” variants (e.g., `claude-3.7-sonnet:thinking`, `deepseek-r1`) are great for proofs but slower and chattier for code edits.
* **Default route mismatch.** `default: "openrouter,x-ai/grok-code-fast-1"` looks like you want Grok Code Fast, but it isn’t listed in your `models` array. That can cause silent fallback and inconsistency.
* **Unscoped intents.** One “default” for everything means small edits, heavy refactors, and long-context reads all fight through the same path.
* **Temperature/format drift.** If you don’t enforce low-temp + strict patch format per model, outputs vary wildly across providers.

### Make your router feel “Codex-like”

1. **Pick a primary and stick per task.** Choose one strong coder as default (e.g., `openai/gpt-5` or `x-ai/grok-code-fast-1` or `qwen/qwen3-coder`) and only switch for clear reasons (very long context or heavy math).
2. **Shard by intent (not by brand).**

   * *Small edit / quick fix:* fast model (GPT-5-mini or Gemini-Flash).
   * *Refactor / multi-file change:* GPT-5 (or Claude Sonnet 3.7 non-thinking).
   * *Ultra-long context read:* Kimi-K2.
   * *Hard reasoning before coding:* DeepSeek-R1 to outline → hand off to coder model to produce the patch.
3. **Enforce a strict patch contract.** Always ask for a unified diff or explicit “ApplyPatch” JSON with file paths + hunks. Reject anything else and reprompt automatically.
4. **Lower randomness for code.** `temperature: 0–0.2`, no frequency/presence penalties, and cap `top_p` \~0.9.
5. **Give a repo map, not just tokens.** Feed a compact symbol index: entry points, key classes/functions, test targets, recent diffs. This beats dumping 200k tokens of raw files.
6. **Keep tool loop tight.** One model proposes patch → you run build/tests/linters → feed failures back to the *same* model to iterate. Avoid switching models mid-loop.
7. **Cut the model list.** Keep 3–5 max. Every extra increases variance and routing errors.
8. **Remove “thinking” models from hot paths.** Use them only to produce a short design plan, then swap to a coder for actual edits.

### A leaner config (drop-in idea; adapt names to your framework)

```json
{
  "PROXY_URL": "http://127.0.0.1:7890",
  "LOG": true,
  "Providers": [
    {
      "name": "openrouter",
      "api_base_url": "https://openrouter.ai/api/v1/chat/completions",
      "api_key": "",
      "models": [
        "openai/gpt-5",
        "openai/gpt-5-mini",
        "x-ai/grok-code-fast-1",
        "moonshotai/kimi-k2",
        "anthropic/claude-3.7-sonnet",
        "qwen/qwen3-coder"
      ],
      "transformer": {"use": ["openrouter"]}
    }
  ],
  "Router": {
    "default": "openrouter,openai/gpt-5",
    "quickEdit": "openrouter,openai/gpt-5-mini",
    "refactor": "openrouter,openai/gpt-5",
    "reasonPlan": "openrouter,anthropic/claude-3.7-sonnet",
    "longContext": "openrouter,moonshotai/kimi-k2",
    "longContextThreshold": 220000,
    "webSearch": "openrouter,qwen/qwen3-coder"
  }
}
```

### Prompt scaffolds that stabilize outputs (no tables)

* **System:** “You are a senior software engineer. Produce minimal, compilable patches. Keep style consistent with the repo. If unsure, ask a single clarifying question, otherwise proceed.”
* **Rules:** “Output ONLY a unified diff (git format). Never include commentary. If a file doesn’t exist, create it and include in the diff. Preserve license headers.”
* **Context block:** repo map (files, key symbols), current errors, test targets.
* **Tool loop:** after diff, automatically run `build + tests + lints`; return only failures back to the same model.

### Practical hygiene

* Strip your model list down and fix the default to a model that actually exists in `models`.
* Set per-route temperatures; keep code at 0–0.2.
* Cache the repo map between turns; don’t resend giant contexts unless files changed.
* Avoid mid-task model switches.
* Prefer “diff” over “replace this whole file” to reduce hallucinated imports.

If you want, paste your router’s prompt and temperature settings, and I’ll tighten them for each route so Claude Code and your stack behave more consistently with Codex-style reliability.
