---
audio: false
generated: true
image: false
lang: en
layout: post
title: GitHub Copilot API Codex Integration Analysis
translated: false
type: note
---

Here's the answer based on a deep dive into the Codex codebase:

---

Short answer: **No, not out of the box.** GitHub Copilot API only exposes Chat Completions (`/chat/completions`), but Codex exclusively speaks the **Responses API** (`/v1/responses`). The chat wire API was explicitly removed (see `codex-rs/model-provider-info/src/lib.rs:45`).

Here's why and what you can do:

## The Problem

Codex's `WireApi` enum only has one variant:

```rust
// codex-rs/model-provider-info/src/lib.rs:52-56
pub enum WireApi {
    #[default]
    Responses,  // Only option — "/v1/responses"
}
```

GitHub Copilot exposes:
- `https://api.githubcopilot.com/chat/completions` — Chat Completions format
- `https://models.inference.ai.azure.com/v1/chat/completions` — GitHub Models

Neither speaks Responses API.

## Option 1: API Gateway (No Code Changes)

Use **LiteLLM** as a translation proxy:

```bash
pip install litellm[proxy]
```

`litellm_config.yaml`:
```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: github_copilot/gpt-4o
      api_key: "your-copilot-token"
```

```bash
litellm --config litellm_config.yaml --port 4000
```

Then in `~/.codex/config.toml`:
```toml
model_provider = "copilot"

[model_providers.copilot]
name = "GitHub Copilot"
base_url = "http://localhost:4000/v1"
experimental_bearer_token = "sk-litellm-dummy"
```

Problem: LiteLLM translates Chat Completions -> Responses format? **Not yet** — this direction isn't well-supported. You'd need a custom translation layer.

## Option 2: Add Chat Wire API Support (Code Changes Required)

The places to modify:

1. **`codex-rs/model-provider-info/src/lib.rs`** — Re-add `WireApi::Chat`:
   - Line 50-56: Add `Chat` variant back to `WireApi`
   - Line 67-79: Add `"chat"` deserialization
   - Line 74: Remove the `CHAT_WIRE_API_REMOVED_ERROR` rejection

2. **`codex-rs/codex-api/src/endpoint/`** — Add a `chat_completions.rs` module:
   - New `ChatCompletionsClient` that posts to `{base_url}/chat/completions`
   - Convert Responses API request format -> Chat Completions format
   - Convert Chat Completions SSE response -> internal response events
   - Map tool calls, function outputs between formats

3. **`codex-rs/codex-api/src/api_bridge.rs`** — Route to the right client based on `WireApi`:
   - When `WireApi::Chat`, use `ChatCompletionsClient`
   - When `WireApi::Responses`, use existing `ResponsesClient`

4. **`config.toml`** for your enterprise:
```toml
model_provider = "copilot"

[model_providers.copilot]
name = "GitHub Copilot"
base_url = "https://api.githubcopilot.com"
wire_api = "chat"  # Re-enabled
env_key = "COPILOT_API_KEY"
# Or for token-based auth:
# experimental_bearer_token = "ghu_xxx"

[model_providers.copilot.http_headers]
"Copilot-Integration" = "vscode"
"Editor-Version" = "1.0.0"
"Editor-Plugin-Version" = "copilot/1.0"
```

## Option 3: Use Azure OpenAI Instead (Easiest)

If your enterprise has GitHub Copilot, you likely also have Azure OpenAI access. Codex already supports Azure Responses API:

```toml
model_provider = "azure"

[model_providers.azure]
name = "Azure OpenAI"
base_url = "https://YOUR-RESOURCE.openai.azure.com/openai/deployments/YOUR-DEPLOYMENT"
env_key = "AZURE_OPENAI_API_KEY"

[model_providers.azure.query_params]
"api-version" = "2025-04-01-preview"
```

Azure OpenAI endpoints support the Responses API natively.

## Option 4: Command-Based Auth for Copilot Token

If you do get a Copilot token somehow (e.g., via `gh` CLI), you can use the `auth` config to auto-refresh it:

```toml
[model_providers.copilot]
name = "GitHub Copilot"
base_url = "https://api.githubcopilot.com/v1"
wire_api = "responses"  # Only if Copilot adds Responses API

[model_providers.copilot.auth]
command = "gh"
args = ["auth", "token"]
refresh_interval_ms = 300000
```

But this still requires the Responses API endpoint to exist on the Copilot side.

## Recommendation

**Option 3 (Azure OpenAI)** is the path of least resistance if available. If you must use Copilot, **Option 2** (adding ~500 lines of Rust to re-enable chat wire API) is the most principled fix. The format translation layer between Chat Completions and Responses API is the hard part — tool calling format differs significantly between the two.
