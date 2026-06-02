---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 添加用于Caps Lock键交换的切换键
translated: true
type: note
---

以下是此次提交的完整说明：

**提交：** `cf64c23` — `feat: add ww linux switch-keys — 在 X11 上交换 Caps Lock 和左 Ctrl`

---

**新文件：`ww/linux/switch_keys.py`**（260 行）

核心模块包含 3 项职责：

- **状态检测** — 检查 3 个来源以确定交换是否激活：
  - `setxkbmap -query` 中的 `ctrl:swapcaps` 选项
  - 实时 `xmodmap -pke` 输出，查看键码 37/66 是否被重新映射
  - 磁盘上的 `~/.Xmodmap` 文件用于持久配置

- **运行时应用/恢复：**
  - `on` → 运行 `setxkbmap -option ctrl:swapcaps`
  - `off` → 清除所有选项（`setxkbmap -option`），重新添加 `terminate:ctrl_alt_bksp`，并重置键码 37 和 66 的 xmodmap

- **持久性管理：**
  - `--persist` 在 `on` 时：写入 `~/.Xmodmap` 文件，包含基于键码的交换（`keycode 66 = Control_L`，`keycode 37 = Caps_Lock`，清除/添加 Lock/Control），并将 xmodmap 加载行追加到 `~/.xprofile`
  - `--persist` 在 `off` 时：删除 `~/.Xmodmap` 并从 `~/.xprofile` 中移除与交换相关的行
  - 不使用 `--persist` 时，交互式提示："是否也跨重启持久化此设置？"

- **参数解析** 通过 argparse，包含一个可选的位置参数（`on`/`off`）和一个 `--persist` 标志

**修改：`ww/linux/main.py`**（+3 行）

- 在帮助列表中增加了 `switch-keys`
- 添加了导入并调用的路由：`elif subcmd == "switch-keys"` → `from ww.linux.switch_keys import run; run()`

**修改：`ww/main.py`**（+1 行）

- 在顶层帮助输出中添加了 `"  ww linux switch-keys  Swap Caps Lock and Left Control keys"`

**设计选择：**

- 仅针对 X11（如果未设置 `DISPLAY` 或 `XDG_SESSION_TYPE=x11`，则报错）
- 运行时使用 `setxkbmap`（轻量级，无需重置 Xmodmap），持久化使用 `~/.Xmodmap`（大多数 X11 显示管理器自动加载）
- 同时跟踪 `setxkbmap -query` 选项和实时 `xmodmap` 状态，因为两者可以独立设置交换
