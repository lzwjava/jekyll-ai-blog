---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 Gateway CLI 中使用 Bind Lan
translated: true
type: note
---

gateway CLI 使用 `--bind`（而不是 `--host`）。`--bind` 选项接受一种模式：`loopback`、`lan`、`tailnet`、`auto` 或 `custom` —— 而不是直接接受 IP 地址。

**修复：** 更新 systemd 服务文件，将 `--host 0.0.0.0` 替换为 `--bind lan`（或 `auto`）：

```
ExecStart=/usr/bin/node /home/lzw/.npm-global/lib/node_modules/openclaw/dist/index.js gateway run --bind lan --port 18789
```

在远程主机上：
```bash
systemctl --user edit openclaw-gateway.service
# or edit the file directly:
nano ~/.config/systemd/user/openclaw-gateway.service
```

修改 `ExecStart` 行 —— 将 `--host 0.0.0.0` 替换为 `--bind lan`。然后：
```bash
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway.service
```

使用 `--bind lan` 在 LAN 接口上监听，或者使用 `--bind auto` 让 openclaw 根据配置决定。`loopback` 将限制为仅 127.0.0.1（无法用于远程访问）。
