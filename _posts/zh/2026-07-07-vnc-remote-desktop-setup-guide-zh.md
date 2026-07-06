---
audio: false
generated: true
image: false
lang: zh
layout: post
title: VNC远程桌面设置指南
translated: true
type: note
---

**问题：** 什么是“通过VNC远程桌面连接”？

**答案：**

VNC（虚拟网络计算）是一种通过网络查看和控制另一台机器图形化桌面的协议。它通过传输帧缓冲更新来工作：服务器捕获远程屏幕，编码已更改的像素区域（RFB协议，通常使用端口5900+显示编号），并将它们流式传输到你的客户端；你的键盘/鼠标事件则反向传回。它与操作系统无关——与RDP（Windows原生）或SSH（仅终端）不同，VNC只传输像素，因此适用于Linux↔macOS↔Windows之间的控制。

针对你的场景（从MacBook Air控制Ubuntu工作站）的典型设置：

**在Ubuntu机器上（服务器端）：**

```bash
# 方案A：共享现有的物理桌面（X11）
sudo apt install x11vnc
x11vnc -display :0 -auth guess -passwd '<密码>' -forever -shared

# 方案B：无头虚拟桌面（无需显示器）
sudo apt install tigervnc-standalone-server
vncpasswd
vncserver :1 -geometry 1920x1080   # 监听端口5901
```

**在Mac上（客户端）：** macOS自带VNC客户端——在Finder中按`⌘K`并输入`vnc://192.168.x.x:5901`，或使用`open`命令：

```bash
open vnc://192.168.x.x:5901
```

**安全提示：** 原始VNC流量未加密，密码认证较弱（DES，最多8个字符）。在局域网内尚可接受；通过互联网时，务必通过SSH隧道传输：

```bash
# 在Mac上：将本地5901端口转发到远程的localhost:5901
ssh -L 5901:localhost:5901 lzw@192.168.x.x
# 然后将VNC客户端连接到 vnc://localhost:5901
```

并启动VNC服务器时使用`-localhost`参数，使其仅接受隧道连接。

值得了解的实际替代方案：对于你以终端为主的工作流程，单纯的`ssh` + `tmux`可以覆盖95%的远程工作，且延迟低得多；VNC只有在真正需要图形界面时（例如远程机器上的浏览器、图形分析器、CUDA可视化工具）才值得使用。如果你经常需要远程图形界面，RustDesk（开源，可自建中继）或Moonlight/Sunshine（GPU加速，鉴于工作站配有RTX 4070，效果很好）能提供比传统VNC好得多的帧率。
