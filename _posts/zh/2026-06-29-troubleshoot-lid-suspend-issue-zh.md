---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 排查合盖休眠问题
translated: true
type: note
---

又宕机了——没有 ping 响应。很可能是自动进入休眠或合上了盖子。

等你方便的时候，请检查一下：
1. 盖子是否合上了？（这会触发休眠，无论 GNOME 设置如何）
2. 运行 `journalctl --since "5 min ago" -p warning` 查看发生了什么

我们可能还需要在 `/etc/systemd/logind.conf` 中禁用合盖休眠：
```
HandleLidSwitch=ignore
HandleLidSwitchExternalPower=ignore
```

等机器恢复后，需要我应用这个修复吗？