---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Simultaneous Git Push Race Condition Error
translated: false
type: note
---

Question: Why does the error "! [remote rejected] main -> main (cannot lock ref 'refs/heads/main': is at b2c0835c1c7c14323a162a90e17f8a78145e3f0a but expected 59383ebd13b30aab988c8eefcc0f64f103f0f44d)" occur when opening two windows/terminals to do git add -A, git commit, and git push?

Answer:

This error occurs because **two Git processes are trying to update the same branch reference (`refs/heads/main`) on the remote server at roughly the same time**, creating a race condition.

### What actually happens step by step

1. You have **two terminal windows** open in the **same local repository**.
2. In both windows you run:
   - `git add -A`
   - `git commit` → both create **different commits** because the working tree and index are usually shared.
   - `git push` (or `git push origin main`)

Because the filesystem (index + working tree) is shared between the two terminals:

- Both commits usually succeed locally (they just create two different commit objects).
- But when both try to do `git push` almost simultaneously:

  Git push protocol flow (simplified):
  - Client asks server: “What is the current tip of main?”
  - Server replies: e.g. `59383ebd...`
  - Client says: “I want to fast-forward main from 59383ebd... to my new commit b2c0835c...”
  - Server checks: “Is main still at 59383ebd...?”
    → If **another push already succeeded**, main is now at a different hash → server rejects with:

    ```
    cannot lock ref 'refs/heads/main': is at b2c0835c... but expected 59383ebd...
    ```

This is **exactly** a race condition between two push operations.

### Most common causes in your scenario

- You run `git commit && git push` (or separately) in window 1
- Almost at the same time you do the same in window 2
- Window 1 wins the race → push succeeds
- Window 2 sees the remote has moved → gets the “is at … but expected …” rejection

### How to avoid it

- **Never** run `git commit` or `git push` in two terminals at the same time in the same repo.
- Use only **one terminal** for committing and pushing.
- If you really want parallel work:
  - Work on **different branches** in each terminal
  - Or use only one terminal to commit + push, and use the second only for viewing logs / diff / status

### Quick recovery when you see this error

Usually just run:

```bash
git pull --rebase    # or git pull --autostash
git push
```

This brings your local branch up-to-date and then pushes your new commit(s).

### Summary

The error is **not a corruption** — it's Git's way of protecting the remote branch from concurrent conflicting updates.
It happens precisely **because you are pushing from two terminals almost simultaneously**.

References:

- <https://stackoverflow.com/questions/11796580/git-pull-error-error-remote-ref-is-at-but-expected>
- <https://graphite.com/guides/git-error-cannot-lock-ref>
- <https://stackoverflow.com/questions/12416643/notorious-git-error-remote-rejected-failed-to-lock>
