---
audio: false
generated: true
image: false
lang: en
layout: post
title: Emacs Document and Page Navigation Shortcuts
translated: false
type: note
---

**Question:** What are the Emacs keyboard shortcuts for navigating to the end of a document and moving to the next page?

**Answer:**

Core navigation shortcuts:

| Action | Shortcut | Notes |
|--------|----------|-------|
| End of document | `M->`  | Meta+Shift+. (Alt+Shift+>) |
| Beginning of document | `M-<` | Meta+Shift+, (Alt+Shift+<) |
| Next page | `C-v` | Ctrl+V, scrolls down |
| Previous page | `M-v` | Meta+V, scrolls up |
| End of line | `C-e` | Quick local navigation |
| Beginning of line | `C-a` | Quick local navigation |

**Why this design:** Emacs uses modifier + key combinations as a command language. `C-` = Ctrl (control), `M-` = Meta (Alt on most modern keyboards). The `<` and `>` keys (with Shift) visually represent "jump to beginning/end."

**If you want vim-like navigation**, consider evil-mode:

```elisp
;; In init.el or emacs config
(use-package evil
  :ensure t
  :init
  (evil-mode 1))
```

Then you get `G` (end of file), `gg` (start), `C-f` (page down) — familiar vim semantics.

**Customization tip:** You can rebind these if you prefer:

```elisp
(global-set-key (kbd "C-S-e") 'end-of-buffer)
(global-set-key (kbd "C-S-h") 'beginning-of-buffer)
```

Are you setting up Emacs for serious dev work, or just exploring it alongside your current stack?
