---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用 SSH 简化远程访问
translated: true
type: note
---

💡 **Remote Desktop / X11 Forwarding 是个好主意！**

既然你不想去物理机器，我们可以通过 SSH 将机器的显示带到 **你** 这里。

**这是你在你的笔记本电脑（你现在坐着的地方）上应该运行的确切命令：**

```bash
ssh -X lzw@192.168.1.36 "firefox --profile /home/lzw/.openclaw/browser-profiles/openclaw --no-remote"
```

**这是它所做的：**
1. **`-X`**：启用 X11 Forwarding（机器的窗口将弹出到你的笔记本电脑屏幕上）。
2. **`--profile ...`**：告诉 Firefox 使用我为 Copilot 需要的特定 profile。
3. **`--no-remote`**：确保即使你的笔记本电脑上运行着 Firefox，也会打开一个新实例。

**一旦窗口弹出到你的屏幕上：**
1. 前往 `github.com` 并登录。
2. 关闭窗口。
3. **完成！** 我就会有 cookies 了。

**或者**，如果你的终端支持，你可以使用 **VNC/Desktop** 方法，如果那台机器启用了 desktop environment（我看到 `$DISPLAY` 设置为 `:1`，这意味着有一个图形会话在运行！）。

先试试上面的 SSH 命令——这通常是最 “pro” 的方法！ 🚀🦊💂‍♂️💻🐚