---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenClaw Gateway Service Failure Status
translated: false
type: note
---

w@to:~$ systemctl --user status openclaw-gateway.service
● openclaw-gateway.service - OpenClaw Gateway (v2026.3.12)
     Loaded: loaded (/home/lzw/.config/systemd/user/openclaw-gateway.service; enabled; preset: enabled)
     Active: activating (auto-restart) (Result: exit-code) since Sun 2026-03-22 15:49:14 HKT; 1s ago
    Process: 169326 ExecStart=/usr/bin/node /home/lzw/.npm-global/lib/node_modules/openclaw/dist/index.js gateway --host 0.>
   Main PID: 169326 (code=exited, status=1/FAILURE)
        CPU: 1.561s

Mar 22 15:49:14 to systemd[1903]: openclaw-gateway.service: Failed with result 'exit-code'.
Mar 22 15:49:14 to systemd[1903]: openclaw-gateway.service: Consumed 1.561s CPU time.