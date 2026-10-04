---
audio: false
generated: true
image: false
lang: en
layout: post
title: One Workstation, Multiple Headless Servers
translated: false
type: note
---

Question: Do we only need one main machine with 2-3 big monitors, and use a Raspberry Pi (or similar) to control the other computers/servers from one seat, using terminals like Warp or Ghostty?

Answer: Yes, that setup works, and it is how many developers run things. The key point is that servers do not need their own monitor, keyboard, or mouse.

**The idea**
- You sit at one workstation (your RTX 4070 PC) with 2-3 monitors, one keyboard, and one mouse.
- Everything else (the Pi, servers, other machines) runs "headless", with no screen attached.
- You reach them over the network, mostly through SSH.

**How to control the other machines**
- **SSH (terminal access):** The best option for Linux servers and the Pi. You open a terminal tab or pane per machine and work in each. It uses almost no bandwidth and is very reliable.
- **Remote desktop (only when you need a GUI):** RDP for Windows, VNC or NoMachine for Linux/Pi, or tools like Parsec and Moonlight if you need smooth graphics.
- **KVM-over-IP (for emergencies):** A device like a PiKVM (which can be built on a Raspberry Pi) lets you see the screen and control the keyboard and mouse of a machine even during boot or BIOS, or when the OS has crashed. This is useful if some machines are physical servers.
- **Physical KVM switch:** Only needed if you want to share one keyboard, mouse, and monitor between several real computers. It is not needed if you use SSH or remote desktop.

**Does the Pi control the others?**
- The Pi is not required for this. Your main PC can SSH directly into every machine.
- The Pi is useful as a small always-on **jump host** (a gateway into your network), a PiKVM, a Tailscale or VPN node for remote access, or a lightweight server itself.

**Monitors and layout**
- Yes, 2-3 big monitors work well for this: for example, one screen with terminals for different servers, one with your editor or browser, one with logs, dashboards, or docs.
- Use a **tiling or multiplexing tool** inside the terminal, such as tmux or Zellij, so you can split one window into many panes and keep sessions alive if the connection drops.

**About Warp and Ghostty**
- **Ghostty:** A fast, GPU-accelerated terminal with tabs and splits. It is a good fit for SSH-heavy work, and pairs well with tmux.
- **Warp:** A modern terminal with built-in AI features, command history search, and workflows. It supports SSH, though some features work best on your local machine.
- Both are only the "window" where you type commands. The real work happens over SSH on the remote machines.
- Be careful with AI agents that can run commands on servers. Keep them on non-critical machines, review commands before running them, and avoid giving them broad credentials.

**Things to set up**
- SSH keys instead of passwords, and a `~/.ssh/config` file with a short name for each machine.
- Static IPs or local DNS names for each server.
- Tailscale or WireGuard if you also want to reach them from outside your home.
- Wake-on-LAN or smart plugs if you want to power machines on and off remotely.

**Caveats**
- GPU-heavy work (gaming, video editing, AI training with a GUI) needs a real display or a capable remote streaming setup, so remote access is not equivalent for those.
- If a machine is the only way into the network, a failure there can lock you out, so keep one backup access path (such as PiKVM).

If you tell me what the other machines are (Linux servers, Windows PCs, Pis) and what you run on them, I can suggest the exact tools and layout.

References:
- No external sources were used for this answer.