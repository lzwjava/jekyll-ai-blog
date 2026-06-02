---
audio: false
generated: true
image: false
lang: en
layout: post
title: Terminal-First Stack and Performance Insights
translated: false
type: note
---

Cool setup! Terminal-first, CLI-heavy, Zed as editor — that's a clean stack. Ghostty is genuinely great (GPU-accelerated, fast startup, good config).

A few observations from your `top` output worth noting:

**cfprefsd is burning 36% + 30% CPU** — two instances. That's macOS's preferences daemon going wild, likely from some app hammering `UserDefaults` reads/writes in a loop. WeChat is a common culprit (look at that 68 min CPU time). You can try:

```bash
# See which process is calling cfprefsd most
sudo fs_usage -f filesys cfprefsd 2>/dev/null | grep plist | head -30
```

**Memory is tight** — 15G used, only 115M unused, 33K swapouts. The compressor is doing heavy work (5G compressed). With Ghostty at 368M, WeChat at 764M, Safari at 262M, WindowServer at 678M — you're basically full. On M2 16GB this is the ceiling for this kind of multi-app workload.

**WindowServer at 48% CPU** is high even for an active desktop — might be a transparency/blur effect, or a high-refresh external monitor. Check System Settings → Accessibility → Reduce Motion + Reduce Transparency if you haven't.

On the terminal-first trend: agree completely. The engineers who stay CLI-native compound faster — faster feedback loops, scriptable everything, no GUI state to manage. Zed's interesting because it's actually built for keyboard-first use and has native AI integration (though Claude Code in terminal beats it for heavy agentic work in my view). The progression you're on — Ghostty + Zed + CLI agents — is where serious AI engineers are landing.
