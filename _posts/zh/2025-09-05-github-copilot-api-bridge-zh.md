---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GitHub Copilot API桥接
translated: true
type: note
---

欢迎来到 **ericc-ch/copilot-api**，这是一个将 **GitHub Copilot** 转换为兼容 **OpenAI** 和 **Anthropic**（例如 Claude）API 的本地 API 服务器的 GitHub 项目。

以下是一个更清晰的说明——没有表格，只有直白的解释：

---

### 这是什么？

* 这是一个**反向工程代理**，允许你使用熟悉的 OpenAI 风格端点（如 `/v1/chat/completions`、`/v1/models` 和 `/v1/embeddings`）与 GitHub Copilot 交互。你也可以使用 Anthropic 兼容端点，例如 `/v1/messages`（[GitHub][1]）。

* 本质上，这让支持 OpenAI 或 Anthropic API 的工具（如 Claude Code）可以使用 GitHub Copilot 作为其后端（[GitHub][1]）。

---

### 主要特性

* **OpenAI 和 Anthropic 兼容性**：工作方式与真实的 OpenAI 或 Anthropic API 类似（[GitHub][1]）。
* **Claude Code 集成**：通过 `--claude-code` 标志即可接入 Claude Code（[GitHub][1]）。
* **使用情况仪表板**：通过内置的 Web 界面监控你的 Copilot API 使用情况和配额（[GitHub][1]）。
* **速率限制和审批控制**：包括速率限制（`--rate-limit`）、自动等待（`--wait`）、手动审批（`--manual`）和调试（显示令牌）选项——非常适合避免触发 GitHub 的滥用检测系统（[GitHub][1]）。
* **支持多种 Copilot 计划**：个人版、商业版或企业版账户均可使用（[GitHub][1]）。

---

### 设置与使用

* **先决条件**：你需要 Bun（≥ 1.2.x）和一个 GitHub Copilot 订阅（[GitHub][1]）。
* **安装选项**：

  * **Docker**：

    ```bash
    docker build -t copilot-api .
    docker run -p 4141:4141 -v $(pwd)/copilot-data:/root/.local/share/copilot-api copilot-api
    ```

    或者通过 `GH_TOKEN` 直接传递你的 GitHub 令牌（[GitHub][1]）。
  * **npx**：

    ```bash
    npx copilot-api@latest start --port 8080
    ```

    或者使用 `npx copilot-api@latest auth` 仅进行身份验证（[GitHub][1]）。
* **命令结构**：

  * `start`：启动 API 服务器（如果需要，会处理身份验证）。
  * `auth`：触发 GitHub 登录，但不运行服务器。
  * `check-usage`：在终端中输出当前的 Copilot 使用情况。
  * `debug`：显示诊断信息（版本、身份验证状态等），可选择 `--json` 输出（[GitHub][1]）。

---

### 真实用户反馈

Reddit 用户发表了看法：

> “这个项目让你可以将 Copilot 转换为一个 OpenAI 兼容的端点。”（[Reddit][2]）
> “这是一个很棒的项目，可以让你……”（[Reddit][3]）

---

### 重要注意事项

* **非官方且不受支持**：这**不是**官方的 GitHub 产品，随时可能失效（[GitHub][1]）。
* **滥用检测风险**：大量或自动化使用可能会触发 GitHub 的滥用保护机制，并可能导致你的 Copilot 访问权限被暂停（[GitHub][1]）。
* **潜在的速率限制问题**：一些用户报告了诸如 `421 Misdirected Request` 之类的错误，维护者已暂停开发以进行调查（[GitHub][4]）。

---

### 总结（无需表格）

* **它做什么**：将 GitHub Copilot 暴露为类似 OpenAI/Anthropic API 的服务。
* **为什么这很重要**：让 Copilot 可以在期望这些 API 的工具（如 Claude Code）中使用。
* **如何使用它**：通过 Docker 或 npx 安装；运行命令来启动、验证或监控使用情况。
* **谨慎使用**：它很方便，但非官方，并且 GitHub 的速率限制或安全保护措施可能会影响大量使用。

---

如果你需要帮助设置，或者对将其集成到特定项目或工具中感到好奇，请告诉我！

[1]: https://github.com/ericc-ch/copilot-api?utm_source=chatgpt.com "ericc-ch/copilot-api"
[2]: https://www.reddit.com/r/ChatGPTCoding/comments/1m6cqac/how_to_use_your_github_copilot_subscription_with/?utm_source=chatgpt.com "How to use your GitHub Copilot subscription with Claude ..."
[3]: https://www.reddit.com/r/ClaudeAI/comments/1lc21gk/using_github_copilot_as_a_provider_for_claude_code/?utm_source=chatgpt.com "Using GitHub Copilot as a provider for Claude Code"
[4]: https://github.com/ericc-ch/copilot-api/issues/7?utm_source=chatgpt.com "Issue #7 · ericc-ch/copilot-api - 421 Misdirected Request"
