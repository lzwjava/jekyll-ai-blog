---
audio: false
generated: true
image: false
lang: en
layout: post
title: "GitHub Fork Limit: One Per Account"
translated: false
type: note
---

Question: Can I fork the same GitHub repo twice into two forks with different names under my account?

Answer:

No — GitHub allows only **one fork of a given repo per account/org**. The fork relationship is keyed to the upstream repo, not the name. Once you've forked `owner/repo`, hitting "Fork" again just redirects you to your existing fork.

Workarounds to get a second copy with a different name:

**1. Rename your existing fork, then fork again (still limited to one true fork)** — renaming doesn't free up a second fork slot. Skip this; it doesn't work.

**2. Bare-clone + push to a new repo (most common, no fork relationship):**

```bash
# Create the new empty repo first (via gh CLI)
gh repo create lzwjava/repo-copy --private

# Mirror the source
git clone --bare https://github.com/owner/repo.git
cd repo.git
git push --mirror https://github.com/lzwjava/repo-copy.git
cd .. && rm -rf repo.git
```

This gives you an independent repo (all branches/tags) with whatever name you want, but it **won't** show as a fork (no "forked from" link, no PR-to-upstream UI by default). You can still add upstream manually:

```bash
git clone https://github.com/lzwjava/repo-copy.git
cd repo-copy
git remote add upstream https://github.com/owner/repo.git
git fetch upstream
```

**3. Use a second account/org** — fork the original under your personal account, fork again under an org you own. Each namespace gets one fork.

**4. `gh repo fork` with `--fork-name` (one fork still):**

```bash
gh repo fork owner/repo --fork-name my-custom-name --clone
```

This lets you name the single fork, but you still can't make a *second* one this way.

For your workflow (CLI agents, experiments), option 2 is the cleanest — independent repos you can hack on freely without the fork constraint, and you wire up `upstream` manually when you want to sync.
