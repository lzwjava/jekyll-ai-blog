---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Pi模型命令实现
translated: true
type: note
---

已完成。命令 `ww pi set-model` 已实现并接入，pi agent 的默认模型已设置为 `openrouter/xiaomi/mimo-v2.6-flash`。

## pi 实际读取的内容

Pi 的启动模型来自 `<agent-dir>/settings.json` 中的 `defaultProvider` + `defaultModel`（默认路径为 `~/.pi/agent/settings.json`，可通过 `PI_CODING_AGENT_DIR` 覆盖）。

## 变更

**新文件**

- `ww/pi/__init__.py`
- `ww/pi/set_model.py` — 解析 `<provider>/<model>`（在第一个 `/` 处分割），或通过 `--provider` 指定完整模型 ID，合并到 `settings.json` 中并保留其他键，输出旧值 → 新值
- `ww/pi/show_model.py` — 输出当前的 `provider/model`

**`ww/main.py`**

- 新增 `elif group == "pi":` 分发块（`set-model`, `show-model`）
- 在 `_print_help()` 中添加帮助文本段 `Pi:`
- 将 `"pi"` 添加到未知命令建议列表

**`completions/_ww`**（仓库源；使用 `ww completion install` 然后执行 `autoload -Uz compinit && compinit` 刷新你的 shell）

- 在顶层 `commands` 数组中添加 `pi` 条目
- 添加 `pi_cmds` 子命令数组
- 在子命令分发器中添加 `pi)` 分支
- 添加 `subcmd2` 分支，为 `set-model` 提供 `--provider` 标志补全

## 验证

```
$ uv run ww pi set-model openrouter/xiaomi/mimo-v2.6-flash
Previous: openrouter/xiaomi/mimo-v2.6-flash
Set:      openrouter/xiaomi/mimo-v2.6-flash
Saved to: /home/lzw/.pi/agent/settings.json

$ uv run ww pi show-model
openrouter/xiaomi/mimo-v2.6-flash
```

`~/.pi/agent/settings.json` 现在包含 `defaultProvider: openrouter`、`defaultModel: xiaomi/mimo-v2.6-flash`（之前已经是这个值；写入已确认）。对 `ww/pi` 和 `ww/main.py` 进行了 Ruff 检查和格式处理。

注意：AGENTS.md 提到了 `~/.zsh/completions/_ww`，但此机器上不存在该安装副本——仓库文件 `completions/_ww` 是 `ww completion install` 复制的源文件，因此我更新了它。
