---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSH server active but login fails
translated: false
type: note
---

**Conclusion: The SSH server IS installed and running on 192.168.1.137.** The connection failure is due to authentication, not a missing server.

Evidence gathered:

| Check | Result |
|---|---|
| Host reachability (ping) | ✅ Reachable (~2.9ms latency) |
| TCP port 22 | ✅ Open (`ssh` service detected) |
| SSH server (sshd) | ✅ Installed & running — returned the SSH protocol handshake with `publickey,password` auth methods |
| Login authentication | ❌ Failed: `Permission denied (publickey,password)` |

Why I'm confident the server is installed: `nc` reported port 22 as `ssh`, and the SSH client reached the **authentication stage**, receiving the server's list of auth methods (`publickey,password`) — that response only happens when sshd is actively running.

**Why login currently fails:** I tried 3 local keys (`~/.ssh/id_rsa`, `~/.ssh/id_ed25519`, `private_key.pem`) and the remote host rejected all of them for user `lzw`. Also, `BatchMode=yes` prevented interactive password entry.

Ways to log in:
1. **Interactive password login**: `ssh lzw@192.168.1.137` (it will prompt for lzw's password)
2. **Set up key auth**: once you can log in, run `ssh-copy-id lzw@192.168.1.137` to install your public key for passwordless access afterward

Want me to attempt an interactive login (you'd need to provide the password), or run some other check?
