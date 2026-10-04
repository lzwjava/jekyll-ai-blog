---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 添加键盘CapsLock-Ctrl切换
translated: true
type: note
---

完成。我新增了一个 `keyboard` 命令组，其中包含 `capslock-ctrl` 子命令，用于在 Ubuntu 上切换 Caps Lock ↔ Ctrl 交换。

## 新增内容

**新文件**

- `ww/keyboard/__init__.py`
- `ww/keyboard/main.py` — 组调度器（`ww keyboard capslock-ctrl`）
- `ww/keyboard/capslock_ctrl.py` — 实际的切换逻辑

**编辑过的文件**

- `ww/main.py` — 帮助文本、调度分支，以及"你是想找"建议列表
- `completions/_ww` — zsh 标签补全条目

## 工作原理

在 Ubuntu 上，它使用 **`gsettings`** 针对 `org.gnome.desktop.input-sources xkb-options`（同时适用于 GNOME Wayland 和 X11 — 现有的 `ww linux switch-keys` 仅处理 X11）。在纯 X11 会话中会回退到 `setxkbmap`。

切换行为，完全按需求：

- 无交换 → 启用 `ctrl:swapcaps`
- 已交换 → 移除（恢复默认）
- 其他 xkb 选项会被保留（仅添加/移除 `ctrl:swapcaps`）

额外的显式模式：

```
ww keyboard capslock-ctrl            # 切换
ww keyboard capslock-ctrl on         # 强制开启
ww keyboard capslock-ctrl off        # 强制关闭
ww keyboard capslock-ctrl status     # 显示状态
```

## 已验证

你的机器已经设置了 `['ctrl:swapcaps']`，所以我测试了完整流程 — 状态显示 `ON`，切换翻转为 `OFF`，再次切换恢复为 `ON`。原始状态（`['ctrl:swapcaps']`）已保留。
