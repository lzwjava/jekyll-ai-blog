---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw 网关服务故障状态
translated: true
type: note
---

w@to:~$ systemctl --user status openclaw-gateway.service
● openclaw-gateway.service - OpenClaw Gateway (v2026.3.12)
     Loaded: loaded (/home/lzw/.config/systemd/user/openclaw-gateway.service; enabled; preset: enabled)
     Active: activating (auto-restart) (Result: exit-code) since Sun 2026-03-22 15:49:14 HKT; 1秒前
    Process: 169326 ExecStart=/usr/bin/node /home/lzw/.npm-global/lib/node_modules/openclaw/dist/index.js gateway --host 0.>
   Main PID: 169326 (code=exited, status=1/FAILURE)
        CPU: 1.561s

Mar 22 15:49:14 to systemd[1903]: openclaw-gateway.service: 以 'exit-code' 结果失败。
Mar 22 15:49:14 to systemd[1903]: openclaw-gateway.service: 消耗了 1.561s CPU 时间。
