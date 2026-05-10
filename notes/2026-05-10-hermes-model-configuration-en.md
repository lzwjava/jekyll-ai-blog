---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Model Configuration Methods
translated: false
type: note
---

Question: How do I change Hermes Agent's default model?

Answer:

There are **four main ways** to change the default model in Hermes Agent (by Nous Research):

---

## Method 1: Interactive CLI Command (Recommended)

Run the interactive model selector from your terminal:

```bash
hermes model
```

This command lets you switch providers and models interactively. It also handles cases where you need to set up a new provider you haven't configured yet.

You can also set the model directly with a one-liner:

```bash
hermes model set anthropic/claude-opus-4.7 --provider openrouter
```

---

## Method 2: Edit `~/.hermes/config.yaml` Directly

When you save via the dashboard or CLI, Hermes writes to `~/.hermes/config.yaml`. A typical model configuration looks like this:

```yaml
model:
  provider: openrouter
  default: anthropic/claude-opus-4.7
  base_url: ''
  api_mode: chat_completions
```

In the `model:` config section, you can use either `default:` or `model:` as the key name for your model ID — both work identically.

After editing, restart your Hermes session for changes to take effect.

---

## Method 3: Hot-Swap Model in a Running Session (In-chat)

Use `/model <name>` inside the chat to hot-swap the model for that specific session without restarting. New sessions won't inherit this change — they read from `config.yaml`.

You can also use the `--global` flag to change the model both in the running session and persistently:

```bash
hermes model set anthropic/claude-opus-4.7 --global
```

---

## Method 4: Use Model Aliases

You can define short aliases for models you use often in `~/.hermes/config.yaml`, then use `/model <alias>` in chat or CLI:

```yaml
model_aliases:
  fav:
    model: claude-sonnet-4.6
    provider: anthropic
  grok:
    model: grok-4
    provider: x-ai
```

Or set them via CLI:

```bash
hermes config set model.aliases.fav anthropic/claude-opus-4.6
```

Then use `/model fav` in chat.

---

## Important Notes

- Configuration resolves in this priority order: **CLI overrides → config.yaml → .env → defaults**.
- Hermes Agent requires a model with at least **64,000 tokens of context**. Models with smaller context windows will be rejected at startup.
- The `LLM_MODEL` environment variable in `.env` is **no longer read** — use `hermes model` or `hermes setup` instead.
- A provider must have a working credential (API key, OAuth, or custom endpoint URL) before it appears as an option. Run `hermes setup` to wire up a new provider.

References:

- [Configuring Models | Hermes Agent](https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models)
- [Configuration | Hermes Agent](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)
- [AI Providers | Hermes Agent](https://hermes-agent.nousresearch.com/docs/integrations/providers)
- [cli-config.yaml.example | GitHub](https://github.com/NousResearch/hermes-agent/blob/main/cli-config.yaml.example)
- [Quickstart | Hermes Agent](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart)