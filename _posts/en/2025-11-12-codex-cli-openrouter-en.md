---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Configuring Codex CLI for OpenRouter
translated: false
type: note
---

### Setting Up Codex CLI Configuration for OpenRouter

Codex CLI (from OpenAI) is a terminal-based coding agent that supports custom model providers like OpenRouter via its configuration file. OpenRouter provides an OpenAI-compatible API, so you can route requests through it by defining a provider with the appropriate base URL. This allows access to a wider range of models (e.g., from Anthropic, Google, or open-source providers) while using Codex.

The configuration is stored in a TOML file at `~/.codex/config.toml` (create it if it doesn't exist). You'll define a **model provider** section for OpenRouter and then reference it in a **profile** for specific models.

#### Step 1: Get Your OpenRouter API Key

- Sign up at [openrouter.ai](https://openrouter.ai) if you haven't.
- Generate an API key from your account dashboard.
- Set it as an environment variable:

  ```
  export OPENROUTER_API_KEY=your_api_key_here
  ```

  Add this to your shell profile (e.g., `~/.bashrc` or `~/.zshrc`) for persistence.

#### Step 2: Edit the Config File

Open `~/.codex/config.toml` in your editor and add the following sections. This sets the base URL to OpenRouter's endpoint (`https://openrouter.ai/api/v1`), which is OpenAI-compatible (Codex appends `/chat/completions` automatically).

```toml
# Define the OpenRouter provider
[model_providers.openrouter]
name = "OpenRouter"
base_url = "https://openrouter.ai/api/v1"
env_key = "OPENROUTER_API_KEY"  # Reads from your env var for auth

# Define a profile using this provider (example: using a GPT-like model)
[profiles.openrouter-gpt]
model_provider = "openrouter"
model = "openai/gpt-4o-mini"  # Replace with any OpenRouter model ID, e.g., "anthropic/claude-3.5-sonnet"
```

- **Key fields explained**:
  - `base_url`: Points to OpenRouter's API endpoint. This overrides the default OpenAI base URL.
  - `env_key`: Specifies the env var for the Bearer token auth header.
  - `model`: Use exact model IDs from [OpenRouter's models list](https://openrouter.ai/models). For coding tasks, try "openai/codex-mini-latest" or "meta-llama/llama-3.1-405b-instruct".
  - You can add multiple profiles for different models (e.g., `[profiles.openrouter-claude]` with `model = "anthropic/claude-3.5-sonnet"`).

#### Step 3: Use the Configuration

- Install Codex CLI if needed: `npm install -g @openai/codex` (or via Homebrew: `brew install codex`).
- Run Codex with your profile:

  ```
  codex --profile openrouter-gpt
  ```

  Or set a default profile in the config:

  ```toml
  [default_profile]
  name = "openrouter-gpt"
  ```

- Test it: Run `codex` and give it a simple coding prompt. Check OpenRouter's dashboard for usage.

#### Troubleshooting

- **Auth errors**: Ensure `OPENROUTER_API_KEY` is set and exported.
- **Model not found**: Verify the model ID on OpenRouter—it's case-sensitive and prefixed (e.g., "provider/model-name").
- **Version check**: Use Codex CLI v0.13+ for full provider support. Update with `npm update -g @openai/codex`.
- **Advanced routing**: For OpenRouter-specific features like cost-optimized routing, add optional params like `provider = { sort = "price" }` under the profile (supported in newer versions).

This setup keeps your requests compatible with Codex's OpenAI-style API while leveraging OpenRouter's ecosystem. For more details, see the [Codex CLI docs on npm](https://www.npmjs.com/package/@openai/codex) or OpenRouter's [API guide](https://openrouter.ai/docs). If you're using a fork like Open Codex, the config is similar but may have extra Gemini support.
