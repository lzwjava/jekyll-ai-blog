---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 配置Codex CLI以使用OpenRouter
translated: true
type: note
---

### 配置 OpenRouter 的 Codex CLI

Codex CLI（来自 OpenAI）是一款基于终端的编程助手，支持通过配置文件自定义模型提供商（如 OpenRouter）。OpenRouter 提供与 OpenAI 兼容的 API，因此您可以通过定义具有适当基础 URL 的提供商来将请求路由至 OpenRouter。这使得在使用 Codex 的同时能够访问更广泛的模型（例如来自 Anthropic、Google 或开源提供商的模型）。

配置存储在 `~/.codex/config.toml` 的 TOML 文件中（如果文件不存在，请创建它）。您需要为 OpenRouter 定义一个**模型提供商**部分，然后在**配置文件**中引用它以使用特定模型。

#### 第一步：获取您的 OpenRouter API 密钥
- 如果您尚未注册，请在 [openrouter.ai](https://openrouter.ai) 上注册。
- 从您的账户仪表板生成一个 API 密钥。
- 将其设置为环境变量：
  ```
  export OPENROUTER_API_KEY=您的 API 密钥
  ```
  将此行添加到您的 shell 配置文件（例如 `~/.bashrc` 或 `~/.zshrc`）中以使其持久化。

#### 第二步：编辑配置文件
在编辑器中打开 `~/.codex/config.toml` 并添加以下部分。这将基础 URL 设置为 OpenRouter 的端点（`https://openrouter.ai/api/v1`），该端点是 OpenAI 兼容的（Codex 会自动附加 `/chat/completions`）。

```toml
# 定义 OpenRouter 提供商
[model_providers.openrouter]
name = "OpenRouter"
base_url = "https://openrouter.ai/api/v1"
env_key = "OPENROUTER_API_KEY"  # 从您的环境变量中读取以进行身份验证

# 定义使用此提供商的配置文件（示例：使用类似 GPT 的模型）
[profiles.openrouter-gpt]
model_provider = "openrouter"
model = "openai/gpt-4o-mini"  # 替换为任何 OpenRouter 模型 ID，例如 "anthropic/claude-3.5-sonnet"
```

- **关键字段说明**：
  - `base_url`：指向 OpenRouter 的 API 端点。这会覆盖默认的 OpenAI 基础 URL。
  - `env_key`：指定用于 Bearer token 认证头的环境变量。
  - `model`：使用 [OpenRouter 模型列表](https://openrouter.ai/models) 中的确切模型 ID。对于编码任务，可以尝试 "openai/codex-mini-latest" 或 "meta-llama/llama-3.1-405b-instruct"。
  - 您可以为不同的模型添加多个配置文件（例如，使用 `model = "anthropic/claude-3.5-sonnet"` 的 `[profiles.openrouter-claude]`）。

#### 第三步：使用配置
- 如果需要，安装 Codex CLI：`npm install -g @openai/codex`（或通过 Homebrew：`brew install codex`）。
- 使用您的配置文件运行 Codex：
  ```
  codex --profile openrouter-gpt
  ```
  或在配置中设置默认配置文件：
  ```toml
  [default_profile]
  name = "openrouter-gpt"
  ```
- 测试：运行 `codex` 并给它一个简单的编程提示。检查 OpenRouter 的仪表板以查看使用情况。

#### 故障排除
- **认证错误**：确保 `OPENROUTER_API_KEY` 已设置并导出。
- **未找到模型**：在 OpenRouter 上验证模型 ID — 它区分大小写并且带有前缀（例如 "provider/model-name"）。
- **版本检查**：使用 Codex CLI v0.13+ 以获得完整的提供商支持。使用 `npm update -g @openai/codex` 更新。
- **高级路由**：对于 OpenRouter 特定功能（如成本优化路由），在配置文件下添加可选参数，如 `provider = { sort = "price" }`（新版本支持）。

此设置使您的请求与 Codex 的 OpenAI 风格 API 保持兼容，同时利用 OpenRouter 的生态系统。有关更多详细信息，请参阅 [npm 上的 Codex CLI 文档](https://www.npmjs.com/package/@openai/codex) 或 OpenRouter 的 [API 指南](https://openrouter.ai/docs)。如果您使用的是像 Open Codex 这样的分支，配置类似，但可能具有额外的 Gemini 支持。
