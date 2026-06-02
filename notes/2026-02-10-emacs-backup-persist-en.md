---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Emacs Backup Files Persist Despite Setting
translated: false
type: note
---

**Question: Why does Emacs still create backup files like init.el~ even though I set (setq make-backup-files nil) in my init.el?**

**Answer:**

Your setting `(setq make-backup-files nil)` is **correct** and **works**, but it only takes effect **after** your init.el has been loaded. Emacs creates the backup file **before** it evaluates your init file — that's why you still see `init.el~`.

### Why this happens (most common cases)

1. **You edited init.el with Emacs itself**
   - When Emacs opens and saves `init.el`, it creates `init.el~` **right then**
   - Only **afterwards** (next time you start Emacs) does `(setq make-backup-files nil)` actually get evaluated
   - → the backup was already created in the previous session

2. **make-backup-files was set too late**
   - The variable `make-backup-files` is checked **when the file is saved**
   - If you only set it inside `init.el`, it doesn't protect `init.el` itself during the very first save

### Solutions (pick one)

#### Best & cleanest solution (prevents backup of init.el forever)

Put this **very early** — preferably before anything else:

```elisp
;; Prevent backup files from ever being created — even for init.el
(setq make-backup-files nil)
(setq backup-inhibited t)          ; even stronger — recommended
```

Or even more aggressive (many people use this combination):

```elisp
(setq make-backup-files nil
      backup-inhibited t
      auto-save-default nil        ; also disables #auto-save# files if you want
      create-lockfiles nil)
```

#### Quick fix right now (remove existing backup + prevent new ones)

```bash
# Remove the existing backup
rm -f ~/.emacs.d/init.el~

# Make sure Emacs doesn't create new ones from now on
# (add this at the VERY TOP of your init.el)
```

Then add to the top of your `init.el`:

```elisp
;; Disable backups globally - must be very early
(setq make-backup-files nil)
(setq backup-inhibited t)
```

#### Alternative: move backups to a hidden folder (popular choice)

If you ever change your mind and want to keep backups but don't want to see them:

```elisp
(setq backup-directory-alist
      `(("." . "~/.emacs.d/backups/")))
```

This puts all `~` files into `~/.emacs.d/backups/` instead of next to the original file.

### Summary – what you should do

1. Delete the existing backup:

   ```bash
   rm -f ~/.emacs.d/init.el~
   ```

2. Put **at the very top** of your `init.el`:

   ```elisp
   (setq make-backup-files nil)
   (setq backup-inhibited t)
   ```

3. Restart Emacs or re-evaluate the buffer (`M-x eval-buffer`)

After this, Emacs should **never** create `init.el~` (or any other `~` files) again.

Let me know if you still see backup files after making this change!
