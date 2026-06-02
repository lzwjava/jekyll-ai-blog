---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Remote Desktop from MacBook to Ubuntu
translated: false
type: note
---

Question: How can I use my MacBook Air M2 as just a screen/monitor to remotely access and control my powerful desktop PC running Ubuntu while lying in bed, without using SSH?

Answer:

To achieve this—using your **MacBook Air M2** as the display and input device for your **Ubuntu desktop PC** over your local network (Wi-Fi or Ethernet)—you need a **remote desktop solution**. This streams the Ubuntu desktop to your MacBook in fullscreen, with mouse, keyboard, and trackpad control passed to the PC. It will feel close to using the MacBook as a direct monitor, though there will be some network latency (minimal on a good home Wi-Fi, especially 5GHz or wired).

MacBooks (including M2 Air) do not support being a physical external monitor via cable (no Target Display Mode). All solutions are software-based remote access.

Here are the best options for low-latency, graphical remote desktop from macOS client to Ubuntu host:

### Recommended: Sunshine + Moonlight (Best for Performance)
This combination is designed for low-latency streaming (originally for gaming, but perfect for desktop use). It leverages your RTX 4070 GPU for hardware encoding, providing the smoothest experience.

- **On Ubuntu PC (Host)**:
  - Install **Sunshine** (open-source server).
  - Follow the official guide: Download the Debian package or use the AppImage/Flatpak from https://github.com/LizardByte/Sunshine.
  - Sunshine includes a built-in "Desktop" app for streaming the full Ubuntu desktop (no need to launch a game).
  - Run it as a service for auto-start.

- **On MacBook Air M2 (Client)**:
  - Install **Moonlight** (open-source client) from https://moonlight-stream.org or the Mac App Store (Moonlight app).
  - Pair with your PC on the local network.
  - Select the "Desktop" entry and stream in fullscreen.

- **Advantages**:
  - Very low latency.
  - Excellent video quality.
  - Hardware acceleration via NVIDIA GPU.
  - Full audio support.
  - Free and open-source.

This is ideal for your high-end PC and relaxed bed use.

### Simple Alternative: Built-in Ubuntu Remote Desktop (RDP Protocol)
Ubuntu 22.04+ has excellent built-in RDP support (better than VNC).

- **On Ubuntu PC**:
  - Go to Settings > Sharing > Enable "Sharing".
  - Enable "Remote Desktop" (uses RDP).
  - Set a username/password or enable automatic login if secure.
  - Note the PC's IP address (via `ip addr show` in terminal).

- **On MacBook Air**:
  - Download the free **Microsoft Remote Desktop** app from the Mac App Store.
  - Add a new connection with your Ubuntu PC's IP and credentials.
  - Connect and go fullscreen.

- **Advantages**:
  - No extra software installation on Ubuntu.
  - Good performance.
  - Clipboard/audio sharing.
  - Native feel on macOS.

### Other Options
- **NoMachine**: Very fast and reliable. Install server on Ubuntu, client on Mac (free for personal use). Download from https://www.nomachine.com.
- **RustDesk**: Open-source alternative to TeamViewer, low latency, easy setup. Works well cross-platform.

Avoid classic VNC (like Ubuntu's older Screen Sharing)—it's higher latency than the above.

### Tips for Best Experience
- Connect both devices to the same fast Wi-Fi (5GHz) or use Ethernet adapters for even lower lag.
- On the client, enable fullscreen mode and high bitrate/quality settings.
- Ensure your Ubuntu PC is logged in (or set auto-login) for seamless access.
- For bed comfort: Prop the MacBook on a pillow/stand, use fullscreen, and adjust brightness.

Sunshine + Moonlight will give you the closest to "just a monitor" feel due to its gaming-grade low latency.

References:

- https://github.com/LizardByte/Sunshine
- https://moonlight-stream.org
- https://www.nomachine.com
- https://ubuntu.com/tutorials/access-remote-desktop
