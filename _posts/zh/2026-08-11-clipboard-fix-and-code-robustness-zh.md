---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 剪贴板修复与代码健壮性
translated: true
type: note
---

已修复。同时完成了系统级根本原因修复和代码级健壮性修复：

## 根本原因
该机器（Linux，Wayland/GNOME）**完全未安装任何剪贴板工具**——没有 `xclip`、`xsel` 或 `wl-paste`。`pyperclip.paste()` 执行失败，`note_queue.py` 中的回退机制调用了 `xclip`，而该命令也不存在 → 导致原始 `FileNotFoundError` 回溯。

## 修复方案

**1. 系统修复——无需 sudo 安装 `wl-clipboard`**（根本原因）：
- 将 `wl-clipboard` 从 apt 包解压至 `~/.local/wl-clipboard`，并将 `wl-paste`/`wl-copy` 软链接到 `~/.local/bin`（该路径已在您的 PATH 中，且系统已包含 `libwayland-client`）。
- 此修复使整个项目的剪贴板功能恢复正常，因为 pyperclip 1.11 支持 `wl-paste`——所有依赖 `pyperclip.paste()` 的其他模块（`ww/main.py`、`create_note_utils.py`、`canvas_card.py`、`maps.py` 等）现在也能正常工作。已验证复制/粘贴的往返操作。

**2. 代码修复——`ww/note/note_queue.py` 中的 `_get_clipboard()`**：
- 现在按顺序优先尝试原生工具：`wl-paste`（Wayland）→ `xclip`/`xsel`（X11）→ `pyperclip` 作为最后手段，每个工具设置 5 秒超时。
- 如果完全失败，将抛出明确且可操作的 `RuntimeError`，并附带安装说明，而非 `FileNotFoundError` 回溯。

## 已验证结果
- `uv run ww note` → `[ok] Queued (id=5c6306d7debc, 254 chars, ...)` ✅
- 无剪贴板工具场景 → 返回带有修复建议的清晰 `RuntimeError` ✅
- 测试队列条目已清理 ✅

如果您希望系统级安装 `wl-clipboard`（确保不受 PATH 影响），请运行 `sudo apt install wl-clipboard`——不过目前在 `~/.local` 中的配置也能正常工作。