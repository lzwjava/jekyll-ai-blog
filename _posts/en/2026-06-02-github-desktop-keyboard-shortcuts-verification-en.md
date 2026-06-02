---
audio: false
generated: true
image: false
lang: en
layout: post
title: GitHub Desktop Keyboard Shortcuts Verification
translated: false
type: note
---

Here's what the code actually says:

```
VERIFICATION: GitHub Desktop Keyboard Shortcuts
════════════════════════════════════════════════

Source: app/src/ui/repository.tsx:687-715
        app/src/main-process/menu/build-default-menu.ts

1. Ctrl+Tab — Changes ↔ History
   ─────────────────────────────
   CONFIRMED. In repository.tsx line 699:

     if (event.ctrlKey && event.key === 'Tab') {
       this.changeTab()
       event.preventDefault()
     }

   changeTab() toggles between RepositorySectionTab.Changes
   and RepositorySectionTab.History. Works on ALL platforms
   (macOS, Windows, Linux) — it uses event.ctrlKey, not
   event.metaKey.

   Note: Shift is ignored intentionally — the comment says:
   "we don't care about the shift key here, we can get away
   with that as long as there's only two tabs."

2. ⌘G / Ctrl+G — Go to Summary (commit message field)
   ────────────────────────────────────────────────────
   CONFIRMED. build-default-menu.ts line 211:

     label: 'Go to Summary'
     accelerator: 'CmdOrCtrl+G'

   ⌘G on macOS, Ctrl+G on Windows/Linux.

3. F5 — "refresh all git data"
   ──────────────────────────
   FALSE. No F5 accelerator anywhere in the codebase.
   Zero matches for 'F5' across all .ts/.tsx files.
   There is no dedicated refresh shortcut.

4. ⌘1 / Ctrl+1 — Show Changes
   ────────────────────────────
   CONFIRMED. build-default-menu.ts line 180.

5. ⌘2 / Ctrl+2 — Show History
   ────────────────────────────
   CONFIRMED. build-default-menu.ts line 186.

COMPLETE SHORTCUT LIST (from build-default-menu.ts):
────────────────────────────────────────────────────

  View menu:
    ⌘1 / Ctrl+1        → Show Changes
    ⌘2 / Ctrl+2        → Show History
    ⌘T / Ctrl+T        → Show Repository List
    ⌘B / Ctrl+B        → Show Branches List
    ⌘⌥W / Ctrl+Alt+W   → Show Worktrees List
    ⌘G / Ctrl+G        → Go to Summary (commit message)
    Ctrl+H              → Toggle Stashed Changes
    ⌘L / Ctrl+L        → Toggle Changes Filter
    ⌘0 / Ctrl+0        → Reset Zoom
    ⌘= / Ctrl+=        → Zoom In
    ⌘- / Ctrl+-        → Zoom Out
    ⌘9 / Ctrl+9        → Expand Active Resizable
    ⌘8 / Ctrl+8        → Contract Active Resizable

  Repository menu:
    ⌘P / Ctrl+P        → Push
    ⌘⇧P / Ctrl+Shift+P → Pull
    ⌘⇧T / Ctrl+Shift+T → Fetch
    ⌘⇧G / Ctrl+Shift+G → View on GitHub
    ⌘⇧F / Ctrl+Shift+F → Show in Finder/Explorer
    Ctrl+`              → Open in Shell
    ⌘⌫ / Ctrl+Backspace → Remove Repository

  Edit menu:
    ⌘F / Ctrl+F        → Find
    ⌘, / Ctrl+,        → Preferences

  Global (not in menu):
    Ctrl+Tab            → Toggle Changes/History tab
    Alt+⌘I / Ctrl+Shift+I → Toggle DevTools
```

So the claim about `Ctrl+Tab` is correct. The `⌘G` claim is correct but it's "Go to Summary" (focus commit message), not labeled as "focus commit message field" in the UI — it says "Go to Summary". The `F5` claim is **completely made up** — there's no F5 shortcut anywhere in the codebase.
