---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Zed 配置同步命令
translated: true
type: note
---

完成。以下是发生的变化：

**`~/.config/zed/settings.json`** — 将 `"existing_window"` 改为 `"new_window"`，使得通过 CLI 或双击打开时始终新建窗口。

**`ww sync zed`** — 新增子命令。与 `sync_ssh` / `sync_bashrc` 模式一致：

```
ww sync zed         同步 ~/.config/zed/ 从本地到远程
ww sync zed back    同步 ~/.config/zed/ 从远程到本地
```

修改的文件（提交 `210276a`，已推送到 `main`）：

| 文件 | 变更 |
|---|---|
| `ww/sync/remote.py` | +`sync_zed()` 函数 — 通过 scp 同步 `~/.config/zed/` |
| `ww/main.py` | +帮助文本行，+`zed` 的分发块 |
| `README.md` | +同步表格中的一行 |
| `~/.config/zed/settings.json` | `existing_window` → `new_window` |

验证是否正常运行：

```
ww sync --help       # 确认 zed 出现在列表中
ww sync zed forth    # 将本地 zed 配置推送到远程
```

（除非远程主机可通过 `WW_REMOTE_IP` 访问，否则 scp 会超时 — 分发逻辑本身已验证正常。）
