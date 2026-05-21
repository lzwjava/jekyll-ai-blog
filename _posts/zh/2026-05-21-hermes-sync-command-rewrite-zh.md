---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes同步命令重写
translated: true
type: note
---

以下是所有变更的摘要：

## 变更内容

### `ww/sync/remote.py` — `sync_hermes()` 重写

- **之前**：仅将 `~/.hermes/config.yaml` 同步到/从硬编码的远程主机（通过环境变量 `WW_REMOTE_IP`/`WW_REMOTE_USER`）
- **之后**：同步整个 `~/.hermes/` 目录，并显式引入 `from_host` 和 `to_host` 参数
- 每个主机为 `localhost` 或 `user@ip`
- `forth` = 从 `from_host` 到 `to_host`
- `back` = 从 `to_host` 到 `from_host`
- 当 `to_host` 为空时回退至环境变量（向后兼容）

### `ww/main.py` — 调度逻辑更新

- 将 `direction = _pop_subcmd() or "forth"` 移至需要它的每个子命令（bashrc、zprofile、ssh）中，而非在 sync 组级别处理
- 对于 `hermes`，使用 `argparse` 正确解析 `--from-host`、`--to-host` 和 `--help`
- 更新了帮助文本

## 用法

```
# 将本地 ~/.hermes/ 推送至远程
ww sync hermes forth --from-host localhost --to-host lzw@192.168.1.36

# 将远程 ~/.hermes/ 拉取回本地
ww sync hermes back --from-host localhost --to-host lzw@192.168.1.36

# 使用环境变量（向后兼容 - 无需标志）
ww sync hermes forth

# 帮助
ww sync hermes --help
```