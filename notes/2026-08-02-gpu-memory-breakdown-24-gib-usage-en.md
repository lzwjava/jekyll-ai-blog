---
audio: false
generated: true
image: false
lang: en
layout: post
title: "GPU Memory Breakdown: 2.4 GiB Usage"
translated: false
type: note
---

Here's the breakdown of your **2362 MiB** GPU memory usage:

| Process | What it is | GPU Memory |
| --- | --- | --- |
| **Xorg** (4212) | X11 display server | 1430 MiB |
| **Chromium** (13976) | Chromium browser GPU process | 242 MiB |
| **warp-terminal** (138054) | Warp terminal | 204 MiB |
| **zed-editor** (1506768) | Zed editor | 191 MiB |
| **github-desktop** (32796) | GitHub Desktop GPU process | 85 MiB |
| **gnome-shell** (4623) | GNOME desktop compositor | 25 MiB |
| **nautilus** (756333) | GNOME file manager | 18 MiB |
| **WeChatAppEx** (1458258) | WeChat mini-program runtime | 13 MiB |
| **pycharm jcef** (784573) | PyCharm's embedded Chromium | 5 MiB |
| **xdg-desktop-portal-gnome** (12721) | Desktop portal | 3 MiB |
| **Subtotal** | | 2216 MiB |
| **Unaccounted** (driver/overhead) | | ~146 MiB |

**Key takeaways:**

1. **Xorg is the biggest consumer** — 1430 MiB (60%). This is unusually high for a plain X server. It's likely accumulating GPU buffers for every window/compositor surface that has been rendered. Restarting the X session (logging out/in) or switching to a lighter compositor would reclaim most of it.

2. **The rest is mostly Electron/Chromium-based apps**: Chromium, GitHub Desktop, Warp terminal, Zed (Chromium-based UI), PyCharm's JCEF — each keeps a GPU process that holds VRAM for rendering.

3. The ~146 MiB gap is driver/context overhead not attributed to any single process.

If you want to free memory, closing idle browser tabs, Warp, or restarting the display session will give the biggest wins. The GPU is otherwise idle (0% util, 40°C), so none of this is compute — it's just display buffers.
