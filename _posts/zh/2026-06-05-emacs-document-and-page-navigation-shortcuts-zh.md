---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Emacs 文档和页面导航快捷键
translated: true
type: note
---

**问题：** Emacs 中快速跳转到文档末尾和下一页的键盘快捷键是什么？

**答案：**

核心导航快捷键：

| 操作 | 快捷键 | 说明 |
|------|--------|------|
| 文档末尾 | `M->` | Meta+Shift+. (Alt+Shift+>) |
| 文档开头 | `M-<` | Meta+Shift+, (Alt+Shift+<) |
| 下一页 | `C-v` | Ctrl+V，向下滚动 |
| 上一页 | `M-v` | Meta+V，向上滚动 |
| 行尾 | `C-e` | 快速局部导航 |
| 行首 | `C-a` | 快速局部导航 |

**为什么这样设计：** Emacs 使用修饰键+按键组合作为命令语言。`C-` = Ctrl（控制键），`M-` = Meta（在现代键盘上通常为 Alt）。`<`和`>`键（配合 Shift）在视觉上表示“跳转到开头/结尾”。

**如果你希望使用类似 vim 的导航方式**，可考虑 evil-mode：

```elisp
;; 在 init.el 或 Emacs 配置中
(use-package evil
  :ensure t
  :init
  (evil-mode 1))
```

之后即可使用 `G`（文件末尾）、`gg`（文件开头）、`C-f`（向下翻页）——熟悉的 vim 语义。

**自定义提示：** 如果你偏好不同按键，可重新绑定：

```elisp
(global-set-key (kbd "C-S-e") 'end-of-buffer)
(global-set-key (kbd "C-S-h") 'beginning-of-buffer)
```

你是在为严肃的开发工作搭建 Emacs，还是仅仅在现有工作流中探索它？
