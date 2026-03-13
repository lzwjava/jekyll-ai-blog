---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw 文件位置指南
translated: true
type: note
---

问题：当 OpenClaw 说它创建了一个带有 `index.html` 的 todo 应用时，该文件保存在 Linux 文件系统中的哪里？

答案：问题：当 OpenClaw 的 AI 代理创建一个带有 `index.html` 的 todo 应用时，该文件保存在 Linux 文件系统中的哪里？

答案：

## 默认位置

OpenClaw 使用专用的 workspace 目录作为代理的默认工作目录。默认路径是 `~/.openclaw/workspace` — 除非您配置了不同的 workspace 路径，否则代理创建的所有文件都保存在这里。

所以您的 todo 应用很可能位于：

```
~/.openclaw/workspace/todoapp/index.html
```

或者直接位于：

```
~/.openclaw/workspace/index.html
```

---

## 步骤 1 — 快速查找

在您的服务器 (`192.168.1.36`) 上运行：

```bash
find ~/.openclaw/workspace -name "index.html"
```

或者更广泛地搜索，以防它保存在其他地方：

```bash
find ~ -name "index.html" 2>/dev/null
```

---

## 步骤 2 — 列出工作区中的所有内容

```bash
ls -la ~/.openclaw/workspace/
```

查找 `todoapp/` 文件夹或直接的 `index.html`。

---

## 步骤 3 — 检查是否启用了 Sandbox

如果在您的配置中启用了 sandboxing，文件将保存在 `~/.openclaw/sandboxes/` 而不是主工作区。

检查 sandbox 文件是否存在：

```bash
find ~/.openclaw/sandboxes -name "index.html" 2>/dev/null
```

---

## 步骤 4 — 在浏览器中提供服务（可选）

找到文件后，使用 Python 内置的 HTTP 服务器提供服务：

```bash
cd ~/.openclaw/workspace/todoapp
python3 -m http.server 8080
```

然后在您的主 PC 上打开：

```
http://192.168.1.36:8080
```

不要忘记 UFW：

```bash
sudo ufw allow from 192.168.1.0/24 to any port 8080
```

---

## 步骤 5 — 直接询问 OpenClaw

最简单的方法 — 只需在聊天中询问代理：

```
where did you save the todo app? show me the full path
```

OpenClaw 将告诉您它写入文件的精确路径。

---

## 可能位置总结

| 场景 | 路径 |
| 默认工作区 | `~/.openclaw/workspace/todoapp/index.html` |
| 直接保存在工作区根目录 | `~/.openclaw/workspace/index.html` |
| 启用 Sandbox | `~/.openclaw/sandboxes/<id>/todoapp/index.html` |
| 旧版安装 | `~/openclaw/todoapp/index.html` |
| 配置中设置的自定义工作区 | 检查 `~/.openclaw/openclaw.json` 中的 `agents.defaults.workspace` |

参考资料：

- [OpenClaw Agent Workspace - Official Docs](https://docs.openclaw.ai/concepts/agent-workspace)
- [Managing Your OpenClaw Agent Workspace](https://open-claw.bot/docs/concepts/agent-workspace/)