---
audio: false
generated: true
image: false
lang: en
layout: post
title: IP Scan Adds SSH Testing
translated: false
type: note
---

Done. `ww network ip-scan --hostname lzw` now scans the network and tests SSH access on each live host.

**Changes made:**

1. **`ww/network/ip_scan.py`** — added SSH access testing:
   - `--hostname USER` — SSH username to test on live hosts
   - `--ssh-port PORT` — SSH port to test (default 22)
   - `test_ssh_access()` — runs `ssh -o BatchMode=yes -o PasswordAuthentication=no -o StrictHostKeyChecking=accept-new <user>@<ip> true` (key-based auth only, no password prompt; new host keys are saved to known_hosts)
   - Tests run in parallel threads (same semaphore pattern as the ping scan)

2. **`ww/main.py`** — updated network help text to mention the `--hostname` flag

3. **`completions/_ww`** — added `network ip-scan` flag completion (`--hostname`, `--ssh-port`, `--delay`, `-p`)

**Live test results on your network:**

- Port 22 open: `192.168.1.36` (auth denied), `192.168.1.34`, `192.168.1.62`, `192.168.1.137`
- **SSH accessible as `lzw`:** `192.168.1.34`, `192.168.1.62`, `192.168.1.137`
- `.36` has SSH running but rejected the key (permission denied)

Ruff shows no new lint errors vs. baseline, and pyright passes. Reload completions with `compinit` in your zsh shell to pick up the new flags.
