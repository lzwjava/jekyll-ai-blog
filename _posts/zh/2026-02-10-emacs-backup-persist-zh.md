---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 尽管进行了设置，Emacs 备份文件仍然存在
translated: true
type: note
---

**Question: 为什么即使我在 init.el 中设置了 (setq make-backup-files nil)，Emacs 仍然会创建像 init.el~ 这样的 backup files？**

**Answer:**

你的设置 `(setq make-backup-files nil)` 是**正确**且**有效**的，但它只有在你的 init.el 被加载**之后**才会生效。Emacs 在评估（evaluates）你的 init file **之前**就已经创建了 backup file —— 这就是为什么你仍然能看到 `init.el~`。

### 为什么会发生这种情况（最常见的情况）

1. **你使用 Emacs 本身编辑了 init.el**
   - 当 Emacs 打开并保存 `init.el` 时，它会**立即**创建 `init.el~`
   - 只有在**之后**（下次启动 Emacs 时），`(setq make-backup-files nil)` 才会被实际评估
   - → backup file 在之前的 session 中就已经生成了

2. **make-backup-files 设置得太晚了**
   - `make-backup-files` 变量是在**文件保存时**被检查的
   - 如果你只是在 `init.el` 内部设置它，它在第一次保存 `init.el` 本身时无法起到保护作用

### 解决方案（任选其一）

#### 最好且最彻底的方案（永久防止 init.el 生成 backup）

将以下代码放在 **非常靠前** 的位置 —— 最好在其他任何内容之前：

```elisp
;; Prevent backup files from ever being created — even for init.el
(setq make-backup-files nil)
(setq backup-inhibited t)          ; even stronger — recommended
```

或者更彻底的组合（很多人使用这种组合）：

```elisp
(setq make-backup-files nil
      backup-inhibited t
      auto-save-default nil        ; also disables #auto-save# files if you want
      create-lockfiles nil)
```

#### 立即修复（删除现有 backup + 防止产生新 backup）

```bash
# Remove the existing backup
rm -f ~/.emacs.d/init.el~

# Make sure Emacs doesn't create new ones from now on
# (add this at the VERY TOP of your init.el)
```

然后在你的 `init.el` 顶部添加：

```elisp
;; Disable backups globally - must be very early
(setq make-backup-files nil)
(setq backup-inhibited t)
```

#### 替代方案：将 backups 移动到隐藏文件夹（热门选择）

如果你改变主意，想保留 backups 但又不想直接看到它们：

```elisp
(setq backup-directory-alist
      `(("." . "~/.emacs.d/backups/")))
```

这会将所有 `~` 文件放入 `~/.emacs.d/backups/`，而不是留在原文件旁边。

### 总结 – 你应该怎么做

1. 删除现有的 backup：
   ```bash
   rm -f ~/.emacs.d/init.el~
   ```

2. 在 `init.el` 的 **最顶部** 添加：

   ```elisp
   (setq make-backup-files nil)
   (setq backup-inhibited t)
   ```

3. 重启 Emacs 或重新评估 buffer (`M-x eval-buffer`)

完成这些步骤后，Emacs 应该**永远不会**再创建 `init.el~`（或任何其他 `~` 文件）。

如果更改后仍能看到 backup files，请告诉我！
