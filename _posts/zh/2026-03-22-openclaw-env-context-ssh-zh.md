---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过 SSH 定义 OpenClaw 环境上下文
translated: true
type: note
---

**问题：** 当通过 SSH 隧道（`ssh -N -L 18789:127.0.0.1:18789 lzw@192.168.1.36`）访问 OpenClaw（AI 代理）时，如何清楚地向 OpenClaw 传达它实际运行在哪台机器上，以避免混淆——特别是因为远程机器上还部署了像 Gitea 这样的服务，但我是从笔记本电脑访问它们？

---

**回答：**

这是 OpenClaw 的一个重要的上下文感知问题。因为 Gateway 默认仅绑定到 `localhost`，并且你通过 SSH 隧道远程访问，OpenClaw 没有固有方式知道它*物理上执行在哪台机器*上，除非你明确告诉它。如果你不告诉它，它可能会错误地假设它运行在你的笔记本电脑上（你输入命令的那台机器），而实际上它是部署在你的第二台电脑（`192.168.1.36`）上。

---

## 核心问题

你的设置：

| Layer | Reality |
|---|---|
| **你的笔记本电脑** | 你在这里输入，浏览器通过 SSH 隧道打开 `localhost:18789` |
| **远程机器** (`192.168.1.36`) | OpenClaw Gateway 实际运行在这里，连同 Gitea 等服务 |

OpenClaw 的上下文引擎和内存系统通过读取文件、运行 shell 命令以及访问服务来工作——所有这些都在它**物理运行的机器**上进行。它读取文件系统中的实际文件，执行 shell 命令，并连接到 localhost 服务。如果它认为自己在你的笔记本电脑上，它可能会尝试访问错误的 file system 或错误的 `localhost`。

---

## 如何清楚地告诉 OpenClaw 它运行在哪台机器上

### 1. 在系统提示 / 代理身份中设置它（最重要）

当你配置代理（通过 onboarding 或 `openclaw.json` / 代理配置）时，在代理的角色或系统指令中明确说明部署上下文：

```
你运行在机器 “lzw-server” (192.168.1.36) 上。
这不是笔记本电脑。它是一台专用的第二台电脑（Linux 服务器）。
用户通过 SSH 隧道远程访问你：ssh -N -L 18789:127.0.0.1:18789 lzw@192.168.1.36
当用户在 URL 中说 “localhost” 时，他们可能指的是他们笔记本电脑上的 localhost，
而不是这个服务器。在对任何 localhost 引用采取行动之前，始终澄清是否意指像 Gitea（运行在这台机器 192.168.1.36 上）这样的服务。
这台机器上的服务包括：Gitea、OpenClaw 本身。
用户的笔记本电脑是一台独立的机器，有它自己的文件系统。
```

### 2. 在远程机器上使用 `HEARTBEAT.md` 或 `SYSTEM_CONTEXT.md` 文件

每 30 分钟，代理会醒来，读取 `HEARTBEAT.md` 文件以获取指令，并决定是否需要做些什么。你可以在那里嵌入机器身份：

```markdown
# 系统上下文
- **主机机器**：lzw-server (192.168.1.36)
- **OS**：Linux (Ubuntu)
- **访问方式**：用户通过端口 18789 的 SSH 隧道连接
- **重要**：这里的 localhost = 192.168.1.36，不是用户的笔记本电脑
- **这台机器上的服务**：Gitea (端口 3000)、OpenClaw (端口 18789)
- **不要混淆**：用户的笔记本电脑文件系统 ≠ 这个服务器的文件系统
```

### 3. 在每个会话的第一个消息中直接告诉它

养成一个习惯，在会话开始时发送上下文设置消息：

```
上下文：你运行在我的第二台电脑 (192.168.1.36, Linux) 上。
我在笔记本电脑上通过 SSH 隧道访问你。
当我说 “Gitea” 时，它运行在你身上 (192.168.1.36:3000)，不是我的笔记本电脑。
当我说 “我的笔记本电脑” 时，我指的是独立的机器——你无法直接访问它。
```

### 4. 在所有指令中使用明确的命名

避免模糊术语。始终使用：

| ❌ 模糊 | ✅ 明确 |
|---|---|
| "localhost" | "服务器上的 localhost (192.168.1.36)" 或 "我笔记本电脑上的 localhost" |
| "my machine" | "服务器" 或 "我的笔记本电脑" |
| "this computer" | "lzw-server" 或 "192.168.1.36" |
| "Gitea" | "服务器上 192.168.1.36:3000 的 Gitea" |

---

## 为什么这很重要——Gitea 示例

如果你告诉 OpenClaw “去检查 Gitea”，它会尝试连接到 Gitea。但是：

- Gitea 运行在 `192.168.1.36:3000` 上——与 OpenClaw **同一台机器**
- 从 OpenClaw 的视角，这是 `http://localhost:3000` ✅
- 但如果 OpenClaw 认为它在你的笔记本电脑上，它可能会失败或做出错误假设

通过明确告诉它 **OpenClaw 和 Gitea 都位于 `192.168.1.36`**，它将正确使用 `localhost:3000` 来访问 Gitea——这是正确的，因为它们是共置的。

---

## 总结检查清单

- [ ] 将机器身份添加到代理的 **系统提示 / 角色配置**
- [ ] 在远程服务器上将上下文放入 **`HEARTBEAT.md`**
- [ ] 用 **上下文设置消息** 开始会话
- [ ] 始终用 **明确名称** 指代机器（服务器 IP 或主机名，而不是模糊的 "localhost"）
- [ ] 绝不要假设 OpenClaw 会自动推断自己的部署位置

---

**参考资料：**

- [OpenClaw Architecture Explained](https://ppaolo.substack.com/p/openclaw-system-architecture-overview)
- [What Is OpenClaw — MindStudio](https://www.mindstudio.ai/blog/what-is-openclaw-ai-agent)
- [OpenClaw Security Docs](https://docs.openclaw.ai/gateway/security)
- [OpenClaw Deployment Guide — FreeCodeCamp](https://www.freecodecamp.org/news/how-to-deploy-your-own-24x7-ai-agent-using-openclaw/)
