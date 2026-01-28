---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5.2
title: Codex CLI 与 OpenRouter 指南
translated: true
type: note
---

问题：如何在 Codex CLI 中使用 OpenRouter API

回答：

以下是使用 **OpenRouter API** 与 **Codex CLI** 的**实用、逐步指南**。我会解释**概念模型**和**确切的命令**，这样你就可以实际运行而无需猜测。

---

## 1. 概念上发生了什么

* **Codex CLI** 是一个通过 **OpenAI-compatible API** 与 LLM 通信的命令行界面。
* **OpenRouter** 提供了一个 **OpenAI-compatible endpoint**，它代理了许多模型（Claude、GPT-4、DeepSeek、Qwen 等）。
* 因此，你**无需针对 OpenRouter 的特殊 Codex 支持**。
* 你只需将 Codex 指向：

  * 一个**自定义 API base URL**
  * 你的**OpenRouter API key**
  * **OpenRouter 支持的模型名称**

---

## 2. 获取 OpenRouter API key

1. 前往 OpenRouter 并登录。
2. 创建一个 API key。
3. 复制它——你将使用它作为 `OPENAI_API_KEY`。

> OpenRouter keys 看起来像：
> `sk-or-v1-xxxxxxxxxxxxxxxx`

---

## 3. 安装 Codex CLI（如果未安装）

```bash
npm install -g @openai/codex
```

验证：

```bash
codex --version
```

---

## 4. 配置环境变量（最重要步骤）

Codex CLI 读取 **OpenAI-style environment variables**。

### Bash / Zsh / Linux / macOS

```bash
export OPENAI_API_KEY="sk-or-v1-xxxxxxxxxxxxxxxx"
export OPENAI_BASE_URL="https://openrouter.ai/api/v1"
```

### 可选但推荐（OpenRouter headers）

OpenRouter 要求归属 headers。Codex 不会自动设置它们，但你可以：

```bash
export OPENROUTER_SITE_URL="https://your-site-or-github"
export OPENROUTER_APP_NAME="codex-cli"
```

> 这些是可选的，但有助于避免速率限制。

---

## 5. 选择 OpenRouter 支持的模型

示例：

* `anthropic/claude-3.5-sonnet`
* `openai/gpt-4o`
* `deepseek/deepseek-coder`
* `qwen/qwen-2.5-coder-32b`

你可以在 OpenRouter 的模型页面查看完整列表。

---

## 6. 使用 OpenRouter 运行 Codex

### 基本示例

```bash
codex \
  --model anthropic/claude-3.5-sonnet \
  "Explain how a TCP three-way handshake works"
```

### 代码生成示例

```bash
codex \
  --model deepseek/deepseek-coder \
  "Write a Python script that parses a log file and counts HTTP status codes"
```

### 交互模式

```bash
codex --model openai/gpt-4o
```

然后只需交互式输入提示。

---

## 7. 使用 Codex 进行 repo-aware 编码（常见用例）

在 Git repo 内：

```bash
codex \
  --model qwen/qwen-2.5-coder-32b \
  "Refactor this project to use dependency injection"
```

Codex 将：

* 读取文件
* 提出 diffs
* 在应用更改前询问（取决于 flags）

---

## 8. 常见问题与修复

### ❌ `401 Unauthorized`

* 你的 `OPENAI_API_KEY` 错误
* Key 未在当前 shell 中导出

检查：

```bash
echo $OPENAI_API_KEY
```

---

### ❌ `404 model not found`

* 模型名称必须**完全**匹配 OpenRouter 的模型 ID

示例错误：

```text
claude-3.5-sonnet   ❌
anthropic/claude-3.5-sonnet ✅
```

---

### ❌ Codex 仍在与 OpenAI 通信

* `OPENAI_BASE_URL` 未设置或设置不正确

正确值：

```text
https://openrouter.ai/api/v1
```

---

## 9. 推荐模型选择（实用）

| 使用场景               | 模型                         |
| ---------------------- | ---------------------------- |
| 大型重构               | `anthropic/claude-3.5-sonnet` |
| 竞技编程               | `deepseek/deepseek-coder`     |
| 平衡日常使用           | `openai/gpt-4o`               |
| 大型代码库推理         | `qwen/qwen-2.5-coder-32b`     |

---

## 10. 值得记住的心智模型

> **Codex CLI = OpenAI client**
> **OpenRouter = OpenAI-compatible proxy**

一旦你理解这一点，一切“就正常工作了”。

如果你想，我还可以：

* 显示 **`.env` 设置**
* 比较 **Codex CLI vs Aider vs Continue**
* 为长时间编码会话优化 **模型 + 成本**

只需说一声。🚀