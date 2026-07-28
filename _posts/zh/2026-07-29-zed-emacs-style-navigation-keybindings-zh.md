---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Zed Emacs 风格导航键绑定
translated: true
type: note
---

完成。以下是我设置的内容：

**`~/.config/zed/keymap.json`**

| 按键 | 操作 | 风格 |
| --- | --- | --- |
| `Ctrl+x Ctrl+←` / `Ctrl+x Ctrl+→` | 后退 / 前进 | **Emacs 风格**（`C-x` 前缀） |
| `Ctrl+x ←` / `Ctrl+x →` | 后退 / 前进 | Emacs 风格（更短） |
| `Alt+←` / `Alt+→` | 后退 / 前进 | 编辑器标准（后备） |

### 工作原理

在使用 **Alt+点击** 变量/函数跳转到其定义后：

1. **`Ctrl+x ←`**（或 `Alt+←`）→ 跳回你之前的位置
2. **`Ctrl+x →`**（或 `Alt+→`）→ 再次向前跳转

### 为什么选择这些绑定

既然你提到了 Emacs：`Ctrl+x`（`C-x`）是规范的 Emacs 前缀键，因此 `C-x ←` / `C-x →` 对 Emacs 用户来说感觉很自然。同时添加了 `Alt+←`/`Alt+→` 作为熟悉的备选方案，该方案在许多编辑器中都通用。

### 如果你在 Zed 中使用 Vim 模式

如果你在设置中启用了 `vim_mode`，上下文将不匹配。对于 Vim 用户，Zed 默认使用 `Ctrl+o`（后退）和 `Ctrl+i`（前进）—— 已经是 Vim 标准。如果你也需要这些按键，请告诉我。
