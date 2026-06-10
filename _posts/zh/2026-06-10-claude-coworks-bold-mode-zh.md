---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude Cowork的勇敢模式
translated: true
type: note
---

**问题：** Claude Mac（桌面）应用中的“Act without asking”是什么？

**答案：**

“Act without asking”是 Claude Cowork（Claude 桌面应用中的代理模式，包括 macOS）以及 Chrome 中的 Claude 的一种权限模式。它是聊天输入中双模式切换的自主端：

- **Ask before acting**（默认，更安全）：Claude 根据你的提示制定一个计划——指定它将触及哪些站点/资源以及方法——在你批准后执行。然后它会在此参数范围内行动，但在执行购买、创建账户或下载等不可逆操作前仍会征求你的确认。
- **Act without asking**：Claude 执行多步骤任务时不会在步骤之间暂停等待批准。对于定义明确的任务来说速度更快，但会显著增加提示注入攻击的风险——一条嵌入在 Claude 读取的网页、电子邮件或文件中的恶意指令，可能在任务中途引导它，而没有任何人工检查点来拦截。

即使在“Act without asking”模式下，某些防护措施仍不可协商：

- 文件删除仍需明确的“允许”权限提示，计算机使用在访问每个应用程序前也会询问。
- 无论处于何种模式，某些行为始终被禁止——绕过机器人检测/CAPTCHA、执行金融交易、永久删除文件，以及被标记为可能提示注入的行为。
- Anthropic 在背后设置了多层防御：通过 RL 训练使其在恶意指令即使看似权威时也能拒绝，以及分类器扫描进入 Claude 上下文的所有不可信内容以检测注入。

**针对你的设置的实际指导：** 把它视为 Claude Code 中的 `--dangerously-skip-permissions`，但带有分类器作为后盾。适用于明确定义的本地任务，在你的 M2 Air 上（例如“重新整理这个笔记文件夹”、“批量重命名这些文件”）。当任务涉及凭据、你的银行工作上下文、浏览不受信任的页面，或任何涉及 `~/.ssh`、环境文件中的 API 密钥、以及通过 SSH 访问 `192.168.1.36` 工作站时，应避免使用——注入内容加上无审批循环正是攻击面所在。从概念上讲，它对应 Claude Code 权限光谱中的 `bypassPermissions` 端（`ask` → `auto` → `allow`），而 Claude Code 较新的“auto mode”则是中间路径，将每个操作传递给风险分类器——自动批准安全操作，并阻止或升级危险操作（如文件删除）。

**参考资料：**

- [Claude in Chrome Permissions Guide — Claude Help Center](https://support.claude.com/en/articles/12902446-claude-in-chrome-permissions-guide)
- [Use Claude Cowork safely — Claude Help Center](https://support.claude.com/en/articles/13364135-use-claude-cowork-safely)