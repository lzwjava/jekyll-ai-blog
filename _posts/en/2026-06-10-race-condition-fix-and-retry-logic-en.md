---
audio: false
generated: true
image: false
lang: en
layout: post
title: Race Condition Fix and Retry Logic
translated: false
type: note
---

The fix is applied. Here's a summary:

---

**What failed:** Run `27260998201` (Deploy Jekyll, 2026-06-10 07:39 UTC)

**Where it failed:** "Lint Markdown files" step — committed `chore(lint): Fix markdown lint issues`, then the push was rejected twice.

**Root cause:** Race condition. The workflow has 4 separate commit+push steps (lang update, notes translation, table fix, lint). Each used this fragile pattern:

```
git push || { git pull --rebase; git push; }
```

When another concurrent run pushes between the rebase and the second push, it fails with no recovery. This time the lint step was the unlucky one.

**What I fixed:** Replaced all 4 push blocks with a `push_with_retry()` function that retries up to 3 times with `git pull --rebase` and a 2-second backoff between attempts:

```bash
push_with_retry() {
  for attempt in 1 2 3; do
    git push && return 0
    echo "Push failed (attempt $attempt/3), pulling and rebasing..."
    git pull --rebase || true
    sleep 2
  done
  echo "Push failed after 3 attempts"
  return 1
}
```

---

**Side note:** There's also a deprecation warning — `actions/checkout@v4` and `actions/setup-python@v4` run on Node.js 20, which will be forced to Node.js 24 starting June 16, 2026 (6 days from now). You may want to bump to `actions/checkout@v5` and `actions/setup-python@v5` if they're available, or set `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24=true` to opt in early.

Want me to commit and push this fix?
