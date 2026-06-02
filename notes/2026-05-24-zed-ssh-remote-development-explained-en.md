---
audio: false
generated: true
image: false
lang: en
layout: post
title: Zed SSH Remote Development Explained
translated: false
type: note
---

**Question:** Does Zed have remote SSH server support like VS Code's Remote SSH extension?**Answer:**

Yes, Zed has SSH remote development support, and it's actually quite good — arguably cleaner than VS Code's Remote SSH in some ways.

## How it works

When editing over SSH, Zed runs a lightweight "remote server" process via `ssh.exe`, and all I/O operations are routed through that process. Most features work with remote editing: loading/saving files, git integration, terminals, tasks, language servers, and debuggers.

The UI runs fully locally (120fps GPU-rendered), but language servers, tasks, and terminals run on the remote server where they can take advantage of cloud hardware.

## Quick start

Use `ctrl-cmd-shift-o` (macOS) or `alt-ctrl-shift-o` (Linux) to open the "Remote Projects" dialog. Click "Connect New Server" and enter the SSH command. Zed will download a server binary on the remote host and start it automatically.

For simple cases, you can also just run:
```
zed ssh://[user@]host[:port]/path
```

## Key differences vs VS Code Remote SSH

| Feature | Zed | VS Code |
|---|---|---|
| UI rendering | Local (GPU, 120fps) | Local |
| LSP runs | Remote ✅ | Remote ✅ |
| Server binary | Auto-downloaded | Extension-based |
| Config source | Reads your `~/.ssh/config` | Same |
| ControlMaster reuse | Yes (recent) | No native support |

Zed recently changed to reuse existing SSH ControlMaster sessions instead of prompting for credentials again — very useful if you're already connected to your Ubuntu workstation or AMD Dev Cloud.

## Caveat

SSH remoting requires a single binary executable that communicates over SSH with Zed on your local machine. It auto-installs on the remote, but in air-gapped/restricted environments, `zed-remote-server` needs to be pre-installed manually.

## For your setup

For connecting to your `192.168.1.36` Ubuntu workstation with the RTX 4070, just do:

```bash
zed ssh://lzw@192.168.1.36/path/to/project
```

Or for AMD Dev Cloud (Atlanta), same pattern with your cloud host. Language servers and GPU-heavy processes all run remotely, while Zed UI stays snappy on your M2 Air.

**References:**

- [Zed Remote Development Docs](https://zed.dev/docs/remote-development)
- [SSH Remoting is Here — Zed Blog](https://zed.dev/blog/remote-development)
- [Zed for Windows (WSL/SSH architecture details)](https://zed.dev/blog/zed-for-windows-is-here)
