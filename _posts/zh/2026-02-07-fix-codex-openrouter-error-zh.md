---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 修复 Codex OpenRouter 模型名称错误
translated: true
type: note
---

**Question:** 为什么即使在将 model_provider 设置为 openrouter 后，Codex CLI 仍显示错误 "anthropic/claude-4-sonnet is not a valid model ID"，该如何修复？

**Answer:**

模型名称 `anthropic/claude-4-sonnet` **不是** 2026 年 OpenRouter 所期望的正确格式。

OpenRouter 使用的命名规范与你在其网站下拉菜单中看到的或人们随手写的名称不同。

### OpenRouter 的正确模型名称（截至 2026 年 2 月）

以下是在使用 OpenRouter provider 时，你应该在 `model = "..."` 字段中填入的实际字符串：

| 常用称呼                          | 正确的 OpenRouter 模型字符串                              | 备注                               |
|----------------------------------|----------------------------------------------------------|------------------------------------|
| Claude 4 Sonnet                  | `anthropic/claude-sonnet-4-20250514`                     | 最新的 Claude 4 Sonnet             |
| Claude 3.7 Sonnet                | `anthropic/claude-3-7-sonnet-20250219`                   | 2026 年初非常流行                  |
| Claude 3.5 Sonnet                | `anthropic/claude-3.5-sonnet`                            | 依然出色且更便宜                   |
| DeepSeek R1                      | `deepseek/deepseek-r1`                                   | 最佳性价比                         |
| DeepSeek V3 0324                 | `deepseek/deepseek-v3-0324`                              | 非常强大的 coding model            |
| Qwen 2.5 Coder 32B               | `qwen/qwen2.5-coder-32b-instruct`                        | 出色的 coding 能力且便宜           |
| Gemini 2.5 Pro                   | `google/gemini-2.5-pro-exp-03-25`                        | 或检查准确的日期后缀               |
| Gemini 2.5 Flash                 | `google/gemini-2.5-flash`                                | 快速且便宜                         |
| Grok 3                           | `xai/grok-3`                                             | 极具创意且擅长代码                 |

### 如何立即修复你的配置

编辑 `~/.codex/config.toml` 并将 model 行更改为上述有效名称之一。

**推荐的快速修复方案 – 使用一个经过验证的高效且便宜的模型：**

```toml
model = "deepseek/deepseek-r1"           # ← 这几乎总是有效
model_provider = "openrouter"

[model_providers.openrouter]
name     = "OpenRouter"
base_url = "https://openrouter.ai/api/v1"
env_key  = "OPENROUTER_API_KEY"
# 可选但建议添加
headers = { "HTTP-Referer" = "https://github.com/lzwjava", "X-Title" = "Codex CLI" }
```

然后在 terminal 中：

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
codex
```

或者如果你确实需要 Claude 级别的质量（价格更贵）：

```toml
model = "anthropic/claude-sonnet-4-20250514"
# ... 其余部分同上
```

### 快速诊断命令

1. 查看 Codex 实际加载的内容：

```bash
codex --debug config
```

2. 列出 Codex 所知的模型（有助于确认 provider）：

```bash
codex --debug models
```

导致 "not a valid model ID" 的最常见错误：

- 使用了网站友好型名称而不是 OpenRouter API 官方名称
- 模型字符串拼写错误（尤其是连字符 / 日期部分）
- `model_provider` 行缺失或拼写错误
- section header 错误：必须完全匹配 `[model_providers.openrouter]`
- 旧配置残留 — 有时删除 `~/.codex/config.toml` 并重新开始会更有效

修复模型名称后 → 重启 `codex`（直接退出并再次运行）。

你应该不再看到 400 错误，并且模型名称应该正确显示在 header 中。

**References:**

- [https://openrouter.ai/models](https://openrouter.ai/models)
- [https://openrouter.ai/docs#models](https://openrouter.ai/docs#models)
- [https://github.com/openai/codex](https://github.com/openai/codex)