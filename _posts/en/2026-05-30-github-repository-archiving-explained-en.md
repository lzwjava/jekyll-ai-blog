---
audio: false
generated: true
image: false
lang: en
layout: post
title: GitHub Repository Archiving Explained
translated: false
type: note
---

**Question:** What does "archive" mean in the context of a GitHub repository?

**Answer:**

Archiving a repository in GitHub marks it as **read-only and no longer actively maintained**. Here's what happens:

**When you archive:**
- The repo becomes read-only — no one can push code, create issues, or submit PRs
- All CI/CD workflows stop running
- Security features (code scanning, Dependabot, etc.) disable
- The repo still exists and is publicly visible, but clearly marked as archived

**Why archive instead of delete:**
- Preserves history and allows people to fork or reference it
- Signals "this project is done/unmaintained" without losing the codebase
- Better than deleting when others depend on it or for historical reference

**Common use cases:**
- Deprecated projects
- Proof-of-concept code you're not maintaining
- Old versions of active projects
- Sunsetting features

**The GitHub checklist before archiving:**
- Update repository settings (disable unnecessary features)
- Close open issues and PRs (or document why they're unresolved)
- Add a note to README explaining the archive status and pointing to alternatives if applicable

**If you need to reverse it:** You can unarchive the repo anytime from repository settings.

**Practical note:** If it's a public project others use, archiving + a clear README note is better UX than sudden deletion or abandonment.

Is this for one of your projects, or are you evaluating whether to archive something?
