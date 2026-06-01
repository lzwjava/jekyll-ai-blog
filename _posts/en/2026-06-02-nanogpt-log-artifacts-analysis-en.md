---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nanogpt Log Artifacts Analysis
translated: false
type: note
---

The raw log covers iter 27,800 → 74,950 (1,042 lines). Here's what I see:

```
Content:  Clean training output from iter 27800 to 74950
Lines:    1,042
Size:     53 KB
Start:    iter 27800, loss 3.3310, MFU 113.01%
End:      iter 74950, loss 3.2078, MFU 113.75%

Issues:
  - Escape sequences at the end (arrow key artifacts from tmux scroll)
    ^[[A (up arrow) and ^[[B (down arrow) mixed into iter 74850 line
  - iter 74850 line is split: "loss 3" on one line, ".2751..." on next

These are tmux capture artifacts, not training issues.
```

The clean version (`nanogpt_760m_train_clean.log`) filters these out. The raw log is fine for reference — the escape sequences are just from scrolling the tmux pane during capture.