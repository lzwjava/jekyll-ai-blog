---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为什么Hermes Agent阻止scp
translated: true
type: note
---

**问题：** 为什么 `scp` 命令被 Hermes agent 阻止了？

**回答：**

`scp` 命令被阻止是因为 **Hermes（以及其底层的 Claude Code）默认将 `scp` 视为潜在危险的网络命令**。具体原因如下：

---

## 1. `scp` 位于默认拒绝列表中

Claude Code 的常见安全配置会明确将 `Bash(scp *)` 加入拒绝列表，与 `ssh *`、`curl *`、`wget *`、`kubectl apply *`、`terraform apply *` 等命令并列——所有这些命令都可能泄露数据或连接远程主机。

这意味着如果你的 Hermes 或 Claude Code 设置中 `scp` 处于拒绝规则内，**任何 `scp` 命令都会自动被拒绝，无论意图如何**。

---

## 2. Claude Code “失败即关闭”的安全设计

Claude Code 默认使用严格的只读权限。当需要执行额外操作（如运行 shell 命令）时，它会请求明确许可。系统设计为“失败即关闭”：未匹配或不允许的命令默认需要人工批准或直接被阻止。

`scp` 通过 SSH 将文件传输到**远程主机**，这恰恰是安全系统要防止的网络泄露途径。

---

## 3. 网络到远程主机的命令风险较高

Claude Code 默认阻止那些通过网络获取或发送内容的高风险命令。所有发起网络请求的命令都需要用户批准。

像 `scp` 到远程主机 `lzw@192.168.1.36` 这样的操作完全属于此类——它通过网络将本地文件发送到远程机器。

---

## 4. Hermes agent 无法代你运行该命令

Hermes agent 在沙盒环境中运行。即使你想让它执行 `scp`，agent 也会：

- 无法从其环境中认证你的 SSH 密钥/远程主机
- 无法访问你的本地文件系统路径（例如 `/Users/lzwjava/Documents/...`）
- 被有意限制执行那些可能将数据泄露到外部主机的命令

因此，Hermes 正确地告诉你：**“你需要自己运行它。”** 这是预期内的安全行为，而非 Bug。

---

## 如何自己运行

只需复制提供的命令并在你自己的终端中运行：

```bash
scp "/Users/lzwjava/Documents/TencentMeeting/2026-05-17 10.30.30 Started by Zhiwei Li 992874154/meeting_01.mp4" lzw@192.168.1.36:~/projects/private-projects/whisper-playground/
```

这会使用**你的**凭证和 SSH 密钥运行，这是正确且安全的方式。

**参考资料：**

- [AI Coding Agent Security: Practical Guardrails for Claude Code – DEV Community](https://dev.to/maxkrivich/ai-coding-agent-security-practical-guardrails-for-claude-code-copilot-and-codex-och)
- [Security – Claude Code Docs](https://code.claude.com/docs/en/security)
- [Stop Fighting Claude Code's Permission Prompts – Stackademic](https://medium.com/@tonimaxx/stop-fighting-claude-codes-permission-prompts-here-s-how-the-system-actually-works-ae594e59fb13)
- [Hermes Agent – Claude Code Skill](https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-claude-code)
