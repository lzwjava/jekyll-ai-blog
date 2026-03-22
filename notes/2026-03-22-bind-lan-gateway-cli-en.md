---
audio: false
generated: true
image: false
lang: en
layout: post
title: Use Bind Lan in Gateway CLI
translated: false
type: note
---

The gateway CLI uses `--bind` (not `--host`). The `--bind` option accepts a mode: `loopback`, `lan`, `tailnet`, `auto`, or `custom` — not an IP address directly.

**Fix:** Update the systemd service file to replace `--host 0.0.0.0` with `--bind lan` (or `auto`):

```
ExecStart=/usr/bin/node /home/lzw/.npm-global/lib/node_modules/openclaw/dist/index.js gateway run --bind lan --port 18789
```

On the remote host:
```bash
systemctl --user edit openclaw-gateway.service
# or edit the file directly:
nano ~/.config/systemd/user/openclaw-gateway.service
```

Change the `ExecStart` line — replace `--host 0.0.0.0` with `--bind lan`. Then:
```bash
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway.service
```

Use `--bind lan` to listen on LAN interfaces, or `--bind auto` to let openclaw decide based on config. `loopback` would restrict to 127.0.0.1 only (won't work for remote access).