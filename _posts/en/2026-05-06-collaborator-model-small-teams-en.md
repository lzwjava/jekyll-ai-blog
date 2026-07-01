---
audio: false
generated: true
image: false
lang: en
layout: post
title: Collaborator Model for Small Teams
translated: false
type: note
---

Question: For a small GitHub project team (2–3 people), is adding someone as a collaborator and pushing directly to main faster and better than the fork → PR workflow?

Answer:

You are **mostly right**, but the full picture is a bit more nuanced. Here's a comprehensive breakdown:

---

## Two Core GitHub Collaboration Models

### 1. Shared Repository Model (Collaborator + Direct Push)

In the shared repository model, collaborators are granted push access to a single shared repository and topic branches are created when changes need to be made. This model is more prevalent with small teams and organizations collaborating on private projects.

Pros: fast, direct push access; simpler for small teams; fewer remotes to manage.

### 2. Fork and Pull Model

In the fork and pull model, anyone can fork an existing repository and push changes to their personal fork. You do not need permission to the source repository to push to a user-owned fork. This model is popular with open source projects as it reduces the amount of friction for new contributors and allows people to work independently without upfront coordination.

---

## For a Small Team (2–3 People): Collaborator Model Wins on Speed

The shared repository model is usually (but not always) put into practice on smaller projects with smaller amounts of collaborators.

Branching is ideal when you have write access to the original repo (e.g., you're a collaborator or team member). You create a branch in the original repo → make changes → submit a PR from your branch to the repo's main branch.

So the recommended fast workflow for a small team is:

- Add teammates as **collaborators** (Settings → Manage Access → Invite)
- Everyone works on **feature branches** in the same repo (not forks)
- Push branch → open PR from branch to `main` → merge

This is **faster than fork+PR** because:

- No need to manage multiple remotes (`origin` vs `upstream`)
- No need to keep forks in sync with the original repo
- This model is good for beginners to Git collaboration, since there is no need to sync anything after changes have been merged.

---

## Should You Push Directly to `main`? — Be Careful Here

Even for a small team, **pushing directly to `main` without any PR is generally not recommended**, even though it's technically faster. Here's why:

Use forks for outsiders; use collaborators for trusted teammates. Protect main or release/* branches. Require at least 1–2 approving reviews. Require passing CI checks. Disable force pushes on protected branches.

The **best practice for small teams** is:

- ✅ Add teammates as collaborators
- ✅ Create feature branches in the shared repo
- ✅ Open PRs **from branch → main** (not from fork)
- ✅ Optionally enable branch protection with 1 reviewer required
- ❌ Avoid direct push to `main` (even for small teams, this risks breaking the main branch)

---

## Summary Table

| Aspect | Fork + PR | Collaborator + Branch PR | Collaborator + Direct Push to Main |
| --- | --- | --- | --- |
| Speed | Slowest | Fast | Fastest |
| Safety | Highest | High | Risky |
| Best for | Open source / external contributors | Small trusted teams | Hobby / solo-ish projects |
| Remote complexity | High (upstream + origin) | Low (one origin) | Low |
| Recommended for 2–3 person team | ❌ Overkill | ✅ Best balance | ⚠️ Only if you trust everyone 100% |

---

## Bottom Line

Yes, for a 2–3 person small team, **adding collaborators and using branch-based PRs within the shared repo** is the fastest and cleanest workflow. Direct push to `main` is even faster but introduces risk. The fork model is best saved for open-source projects with unknown external contributors.

References:

- [Collaborating on GitHub — Pull Requests, Collaborators & Forks](https://medium.com/@morepravin1989/collaborating-on-github-pull-requests-collaborators-forks-step-by-step-32e51ae8db02)
- [GitHub for collaboration and best practices](https://rainsworth.github.io/intro-to-github/06_Collaboration.html)
- [How to Contribute to Others' Code on GitHub: Forking vs. Branching](https://www.codestudy.net/blog/how-do-i-contribute-to-other-s-code-in-github/)
- [Collaborating – Using Git to Code, Collaborate and Share](https://imperialcollegelondon.github.io/grad_school_git_course/l2-03-collaborating/index.html)
