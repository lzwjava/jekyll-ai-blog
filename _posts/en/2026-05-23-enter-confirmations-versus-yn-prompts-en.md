---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enter Confirmations Versus Y/N Prompts
translated: false
type: note
---

Here's the complete analysis.

---

## Design Principle

The `ww note` pattern is:
> **Enter = affirm** (one tap, default action proceeds)
> **Ctrl+C = cancel** (universal muscle memory, gracefully handled)
> **No text parsing needed** — no `if response in ("y", "yes", ...)` branching

This beats `y/n` for three reasons:
1. **Zero cognitive load** — "do I type y or yes? case?" gone
2. **One keystroke** vs three (y + Enter)  
3. **Muscle memory** — Ctrl+C already means "abort" everywhere in terminal

---

## Commands to Convert, by Priority

### Tier 1: Dangerous ops with ZERO confirmation — highest ROI

| Command | File | Problem | Fix |
|---|---|---|---|
| `ww git force-push` | git/git_force_push.py:31-42 | Just runs `git push --force-with-lease` directly | Add "Press Enter to force push, Ctrl+C to cancel" before the push |
| `ww git amend-push` | git/git_amend_push.py:46-48 | Runs `git add -A` + `git commit --amend --no-edit` + `git push --force-with-lease` silently | Add prompt before line 46 |
| `ww update` (default 10 repos) | git/git_update.py:64-73 | Pulls up to 10 repos without listing what it's about to pull | Add "Will update N repos. Press Enter to continue, Ctrl+C to quit" with repo list |

### Tier 2: Already partially there — clean up the message

These three already accept Enter as affirmative, but the prompt says "or type 'no' to exit". The user still has to type text to cancel. Switch to Ctrl+C:

| Command | Current prompt | Proposed |
|---|---|---|
| `ww proc kill-pattern` | "Do you want to kill all N process(es)? (Press Enter to kill, or 'no' to exit)" | "Press Enter to kill all N processes, Ctrl+C to cancel" |
| `ww proc kill-port` | "Do you want to kill this process? (Press Enter to kill, or 'no' to exit)" | "Press Enter to kill process on port N, Ctrl+C to cancel" |
| `ww proc kill-proxy` | "Do you want to kill all N Clash process(es)? (Press Enter to kill, or 'no' to exit)" | "Press Enter to kill all N Clash processes, Ctrl+C to cancel" |

These already handle `KeyboardInterrupt` correctly (kill_by_pattern.py:21, kill_by_port.py:46, kill_macos_proxy.py:83). Just need to ditch the `response in ("no", "n")` branching — replace the try block with the `input()` + `KeyboardInterrupt` pattern.

### Not candidates (genuine data input, not confirmations)

| Command | Pattern | Why it stays |
|---|---|---|
| `ww env update` | "Pick a number (1-10) or Enter to cancel" | Selection prompt, user chooses a specific value. Enter is already "cancel" ✅ |
| `ww linux proxy-setup` | "Use authentication? (y/n)" | Binary data question, not a "proceed to destructive action" confirmation. Enter would be ambiguous — does it mean "yes" or "skip"? ❌ |

---

## Implementation Pattern

The template to follow (from main.py:244-248):

```python
try:
    input("Press Enter to continue, Ctrl+C to quit... ")
except KeyboardInterrupt:
    print()
    return
```

For kill commands specifically, you could even drop the message — just show the process list and wait for Enter, like `fuser -k` style:

```python
print(f"Found {len(processes)} process(es):")
for ...  # show details
try:
    input("\nPress Enter to kill, Ctrl+C to cancel... ")
except KeyboardInterrupt:
    print("\nCancelled.")
    return
```

Want me to implement these changes? I'd start with the Tier 1 dangerous ops (force-push, amend-push, update) since those are the ones where a typo costs real history.