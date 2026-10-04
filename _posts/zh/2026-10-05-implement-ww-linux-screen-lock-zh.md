---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 实现 ww Linux 屏幕锁定
translated: true
type: note
---

已完成。`ww linux screen-lock` 命令已在此 Ubuntu/GNOME 机器上实现并测试（测试后已恢复原始设置）。

## 变更

**新增：`ww/linux/screen_lock.py`** — 基于 GNOME `gsettings` 的屏幕锁定控制：

| 命令 | 效果 |
| --- | --- |
| `ww linux screen-lock` / `status` | 显示 lock-enabled、lock delay、blank delay、suspend password、lockdown 及警告 |
| `ww linux screen-lock delay` | 屏幕空白后 **2 小时**锁定（默认），启用 `lock-enabled` |
| `ww linux screen-lock delay 30m` | 任意时间：`2h`、`1h30m`、`45s`、纯秒数 `7200` |
| `ww linux screen-lock off` | `lock-enabled false` — 无空闲锁定（打印关于 suspend/login 密码的提示） |
| `ww linux screen-lock on` | 重新启用自动锁定，显示当前延迟 |
| `ww linux screen-lock blank [time\|never]` | 设置/显示 `idle-delay`（空白时间） |
| `ww linux screen-lock suspend-pw on\|off` | `ubuntu-lock-on-suspend` — 唤醒后需要密码 |
| `ww linux screen-lock lockdown on\|off` | `org.gnome.desktop.lockdown disable-lock-screen`（极端） |

行为细节：

- 时间解析器接受 `2h`、`30m`、`45s`、`1h30m`、纯秒数、`never`；无效输入 → 错误并退出 1
- 当 `idle-delay` 为 0 时发出警告（屏幕从不空白 → 空闲锁定永不触发），并解释 `lock-delay` 从空白开始计时，以及来自你回答的“空闲后 N 小时”方案
- 优雅处理缺失的键（非 Ubuntu GNOME 上缺少 `ubuntu-lock-on-suspend`），并在 `gsettings`/GNOME schema 不可用时以明确错误退出

**集成到：**

- `ww/linux/main.py` — `elif subcmd == "screen-lock":` 分发 + 帮助行
- `ww/main.py` — 在 `ww --help` 的 `Linux:` 部分中的帮助行
- `completions/_ww` — 将 `screen-lock`（以及之前过时的 `setup`、`switch-keys`、`pinyin`、`check-fan`）添加到 `linux_cmds`，新增 `screen_lock_cmds` 数组，以及一个 `subcmd2` 分支，使 `ww linux screen-lock <TAB>` 补全动作

注意：此机器上不存在 `~/.zsh/completions/_ww` — 补全源位于仓库中的 `completions/_ww`，因此我更新的是该文件（将其复制到 `$fpath` 中的某个目录并重新运行 `compinit` 以激活）。

尚未提交 — 如果你想要一个 `feat: add ww linux screen-lock command` 提交，请告知。
