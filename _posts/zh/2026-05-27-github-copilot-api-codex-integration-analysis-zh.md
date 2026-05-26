---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GitHub Copilot API Codex 集成分析
translated: true
type: note
---

以下是基于对 Codex 代码库的深入研究得出的答案：

---

简短回答：**不，开箱即用不支持。** GitHub Copilot API 只暴露了 Chat Completions (`/chat/completions`)，但 Codex 只使用 **Responses API** (`/v1/responses`)。Chat wire API 已被明确移除（参见 `codex-rs/model-provider-info/src/lib.rs:45`）。

以下是原因以及你可以采取的措施：

## 问题

Codex 的 `WireApi` 枚举只有一个变体：

```rust
// codex-rs/model-provider-info/src/lib.rs:52-56
pub enum WireApi {
    #[default]
    Responses,  // 唯一选项 — "/v1/responses"
}
```

GitHub Copilot 暴露了：
- `https://api.githubcopilot.com/chat/completions` — Chat Completions 格式
- `https://models.inference.ai.azure.com/v1/chat/completions` — GitHub Models

两者都不支持 Responses API。

## 选项 1：API 网关（无需修改代码）

使用 **LiteLLM** 作为翻译代理：

```bash
pip install litellm[proxy]
```

`litellm_config.yaml`：
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

然后在 `~/.codex/config.toml` 中：
```toml
model_provider = "copilot"

[model_providers.copilot]
name = "GitHub Copilot"
base_url = "http://localhost:4000/v1"
experimental_bearer_token = "sk-litellm-dummy"
```

问题：LiteLLM 会将 Chat Completions 转换为 Responses 格式吗？**目前还没有**——这个方向的支持并不完善。你需要一个自定义的翻译层。

## 选项 2：添加 Chat Wire API 支持（需要修改代码）

需要修改的地方：

1. **`codex-rs/model-provider-info/src/lib.rs`** — 重新添加 `WireApi::Chat`：
   - 第 50-56 行：将 `Chat` 变体加回到 `WireApi`
   - 第 67-79 行：添加 `"chat"` 的反序列化
   - 第 74 行：移除 `CHAT_WIRE_API_REMOVED_ERROR` 拒绝逻辑

2. **`codex-rs/codex-api/src/endpoint/`** — 添加 `chat_completions.rs` 模块：
   - 新的 `ChatCompletionsClient`，向 `{base_url}/chat/completions` 发送请求
   - 将 Responses API 请求格式转换为 Chat Completions 格式
   - 将 Chat Completions SSE 响应转换为内部响应事件
   - 在两种格式之间映射工具调用、函数输出

3. **`codex-rs/codex-api/src/api_bridge.rs`** — 根据 `WireApi` 路由到正确的客户端：
   - 当 `WireApi::Chat` 时，使用 `ChatCompletionsClient`
   - 当 `WireApi::Responses` 时，使用现有的 `ResponsesClient`

4. **`config.toml`** 用于你的企业：
```toml
model_provider = "copilot"

[model_providers.copilot]
name = "GitHub Copilot"
base_url = "https://api.githubcopilot.com"
wire_api = "chat"  # 重新启用
env_key = "COPILOT_API_KEY"
# 或者用于基于令牌的认证：
# experimental_bearer_token = "ghu_xxx"

[model_providers.copilot.http_headers]
"Copilot-Integration" = "vscode"
"Editor-Version" = "1.0.0"
"Editor-Plugin-Version" = "copilot/1.0"
```

## 选项 3：改用 Azure OpenAI（最简单）

如果你的企业有 GitHub Copilot，很可能也有 Azure OpenAI 的访问权限。Codex 已经支持 Azure Responses API：

```toml
model_provider = "azure"

[model_providers.azure]
name = "Azure OpenAI"
base_url = "https://YOUR-RESOURCE.openai.azure.com/openai/deployments/YOUR-DEPLOYMENT"
env_key = "AZURE_OPENAI_API_KEY"

[model_providers.azure.query_params]
"api-version" = "2025-04-01-preview"
```

Azure OpenAI 端点原生支持 Responses API。

## 选项 4：使用基于命令的认证获取 Copilot 令牌

如果你通过某种方式获得了 Copilot 令牌（例如通过 `gh` CLI），可以使用 `auth` 配置自动刷新它：

```toml
[model_providers.copilot]
name = "GitHub Copilot"
base_url = "https://api.githubcopilot.com/v1"
wire_api = "responses"  # 仅当 Copilot 添加了 Responses API 时有效

[model_providers.copilot.auth]
command = "gh"
args = ["auth", "token"]
refresh_interval_ms = 300000
```

但这仍然需要 Copilot 端存在 Responses API 端点。

## 建议

**选项 3（Azure OpenAI）** 是目前阻力最小的路径（如果可用）。如果必须使用 Copilot，**选项 2**（添加约 500 行 Rust 代码以重新启用 chat wire API）是最有原则的修复方式。Chat Completions 与 Responses API 之间的格式翻译层是难点——两者在工具调用格式上差异显著。