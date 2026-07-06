---
audio: false
generated: true
image: false
lang: en
layout: post
title: VNC Remote Desktop Setup Guide
translated: false
type: note
---

**Question:** What is "connecting to a remote desktop via VNC" (通过VNC远程桌面连接)?

**Answer:**

VNC (Virtual Network Computing) is a protocol for viewing and controlling another machine's graphical desktop over the network. It works by shipping framebuffer updates: the server captures the remote screen, encodes changed pixel regions (RFB protocol, usually port 5900+display number), and streams them to your client; your keyboard/mouse events go back the other way. It's OS-agnostic — unlike RDP (Windows-native) or SSH (terminal-only), VNC just moves pixels, so it works Linux↔macOS↔Windows.

Typical setup for your case — controlling your Ubuntu workstation from the MacBook Air:

**On the Ubuntu box (server side):**

```bash
# Option A: share the existing physical desktop (X11)
sudo apt install x11vnc
x11vnc -display :0 -auth guess -passwd '<PASSWORD>' -forever -shared

# Option B: headless virtual desktop (doesn't need a monitor)
sudo apt install tigervnc-standalone-server
vncpasswd
vncserver :1 -geometry 1920x1080   # listens on port 5901
```

**On the Mac (client side):** macOS has a built-in VNC client — in Finder press `⌘K` and enter `vnc://192.168.x.x:5901`, or use the `open` command:

```bash
open vnc://192.168.x.x:5901
```

**Security note:** raw VNC traffic is unencrypted and the password auth is weak (DES, 8 chars max). On a LAN it's tolerable; across the internet, always tunnel it through SSH:

```bash
# On the Mac: forward local 5901 → remote's localhost:5901
ssh -L 5901:localhost:5901 lzw@192.168.x.x
# Then connect the VNC client to vnc://localhost:5901
```

and start the VNC server with `-localhost` so it only accepts tunneled connections.

Practical alternatives worth knowing: for your terminal-first workflow, plain `ssh` + `tmux` covers 95% of remote work with far less latency; VNC only earns its keep when you genuinely need a GUI (e.g., a browser on the remote box, GUI profilers, CUDA visual tools). If you do need remote GUI regularly, RustDesk (open-source, self-hostable relay) or Moonlight/Sunshine (GPU-accelerated, great since the workstation has an RTX 4070) give much better frame rates than classic VNC's tile-based encoding.
