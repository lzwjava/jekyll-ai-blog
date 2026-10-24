---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSH Scan Finds Two Ubuntu Hosts
translated: false
type: note
---

Found both SSH hosts. Results:

| IP | Hostname | OS |
| ---- | ---------- | ----- |
| **192.168.1.34** | `lzw-MS-7996` | Ubuntu 26.04.1 LTS |
| **192.168.1.36** | `to` | Ubuntu 24.04.5 LTS |

**None of the live IPs is a Debian box.** Both machines that answered SSH (`.34` and `.36`) are **Ubuntu**, and both accepted your key (authenticated via your SSH publickey, not the password). The rest of the hosts (`.1`, `.13`, `.14`, `.19`, `.27`, `.165`) have no SSH service open, and `.255` is the broadcast address.

A few possibilities to check on your end:

- The Debian machine may be **powered off or disconnected** right now.
- Its **SSH server may not be running** or uses a different port — want me to scan all 65535 ports on the live IPs, or scan more of the `192.168.1.0/24` range for an SSH host that responds as Debian?
