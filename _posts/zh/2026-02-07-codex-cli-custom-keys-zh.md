---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 使用自定义密钥配置 Codex CLI
translated: true
type: note
---

**Question:** 如何在 Codex CLI 中使用我自己的 Key，以及如何配合 OpenRouter API 使用？

**Answer:**

**Codex CLI** 是 OpenAI 推出的开源终端代码代理工具（发布于 2025 年左右）。它就像一个交互式的 AI，可以读取你的代码库、建议/编辑文件、运行命令并迭代任务 —— 这一切都直接在你的终端中完成。

它通过配置支持多个 provider（包括 OpenAI 和 OpenRouter 等第三方平台）。

### 1. 安装（推荐 macOS/Linux；Windows 为实验性支持）

```bash
# 需要 Node.js ≥ 18
npm install -g @openai/codex
```

其他安装方法（Rust binary, brew 等）→ 请查阅官方文档。

### 2. 使用你自己的 OpenAI Key（官方 / 默认方式）

**选项 A – 最简单（交互式登录）**

运行一次：

```bash
codex
```

→ 浏览器打开 → 登录 ChatGPT 账号（Plus/Pro/... 包含访问权限）
或者选择 "Use API key" 并粘贴你从 <https://platform.openai.com/api-keys> 获取的 OpenAI API key。

**选项 B – 无头模式 / 脚本友好（环境变量）**

```bash
export OPENAI_API_KEY="sk-..."
codex
```

首次使用后它会缓存 token。

### 3. 使用 OpenRouter API（第三方模型，通常更便宜 / 更多选择）

Codex CLI 通过 `~/.codex/config.toml` 支持自定义 provider（该文件在首次运行后自动创建）。

**推荐的 OpenRouter 配置（2026 可用方案）：**

编辑（或创建）该文件：

```toml
# ~/.codex/config.toml

model = "anthropic/claude-4-sonnet"          # 或 deepseek/deepseek-r1, qwen/qwen2.5-coder-32b, google/gemini-2.5-pro 等
model_provider = "openrouter"                # ← 重要：必须与下方 section 名称匹配

[model_providers.openrouter]
name = "OpenRouter"
base_url = "https://openrouter.ai/api/v1"
env_key = "OPENROUTER_API_KEY"               # ← 从此环境变量读取
# 可选的额外 headers（有时需要）
# headers = { "HTTP-Referer" = "https://your-site.com", "X-Title" = "Codex CLI" }
```

然后设置你的 Key：

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
codex
```

或者使其永久生效 (zsh/bash)：

```bash
echo 'export OPENROUTER_API_KEY="sk-or-v1-..."' >> ~/.zshrc
source ~/.zshrc
```

**快速测试命令（非交互式）：**

```bash
codex "Explain the architecture of this project"
```

或者启动交互式 session 并直接输入自然语言请求。

### 4. 2026 年 2 月推荐通过 OpenRouter 在 Codex CLI 中使用的热门模型

| 模型 ID | 特点 |
| :--- | :--- |
| `deepseek/deepseek-r1` 或 `deepseek/deepseek-v3-0324` | 编程性价比最高 |
| `anthropic/claude-4-sonnet` 或 `claude-3.7-sonnet` | 最高质量 |
| `qwen/qwen2.5-coder-32b-instruct` | 非常强劲且便宜 |
| `google/gemini-2.5-pro` | 超大 context，多模态 |
| `openai/o3-mini` 或 `openai/o1` | 强大的 reasoning 能力 |

只需修改 `model = "..."` 行并重启 `codex` 即可。

### 5. 常用参数 / 模式

```bash
codex --suggest                # 仅建议修改，不自动应用
codex --approval-policy never  # 自动应用（请谨慎使用！）
codex --sandbox-mode workspace-write  # 更安全的文件写入
codex "fix bug in login flow"  # 一次性任务
```

**提示：** 许多用户反馈，与 Codex CLI 默认的 OpenAI 相比，使用 OpenRouter 搭配强大的开源模型拥有更好的稳定性、更高的可靠性以及更低的成本。

如果你遇到 "model_not_found" 错误 → 请仔细检查 `model_provider` 是否与 `[model_providers.xxx]` 部分的名称完全一致。

**参考资料：**

- [https://developers.openai.com/codex/cli](https://developers.openai.com/codex/cli)
- [https://github.com/openai/codex](https://github.com/openai/codex)
- [https://openrouter.ai/docs](https://openrouter.ai/docs)
- [https://openrouter.ai/models](https://openrouter.ai/models)
