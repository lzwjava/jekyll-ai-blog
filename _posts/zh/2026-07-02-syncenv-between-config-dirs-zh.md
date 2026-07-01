---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 配置目录间的.env同步
translated: true
type: note
---

完成。以下是完整摘要：

## 变更

### 新文件：`ww/sync/ww.py`
- `sync_ww_env(direction="forth")` — 在 `~/.config/ww/.env` 和 `$CONFIG_DIR/ww/.env` 之间复制 `.env`
- `forth`（默认）：从规范目录复制到配置目录
- `back`：从配置目录复制到规范目录
- 使用 `shutil.copy2` 保留元数据，并在需要时创建父目录
- 成功时打印确认行

### 修改：`ww/main.py`
- 在调度同步块中添加了 `ww sync ww` 处理程序（与 bashrc/zprofile 相同的模式 — `direction` 参数，默认值为 `forth`）
- 在主帮助页面和同步子命令帮助中添加了帮助文本

### 修改：`~/.zsh/completions/_ww`
- 在 `sync_cmds` 数组中添加了 `'ww:Sync .env to/from CONFIG_DIR'`
- 在 zsh 中运行 `autoload -Uz compinit && compinit` 以启用更新