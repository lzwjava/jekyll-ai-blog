---
audio: false
generated: true
image: false
lang: en
layout: post
title: One machine, separate contexts
translated: false
type: note
---

**Question:** Is it a good approach to use a different laptop for each project, so each project's context stays separate?

**Answer:**

Splitting context per project is a good idea. Splitting by physical laptop usually isn't needed, and it can cost you more than it helps.

**Why separating context is good**

- Agents work best with a focused context. Mixing Client A's code, requirements and conventions with Client B's causes confusion and mistakes.
- It protects confidentiality. You don't want one client's code or data leaking into another's work.
- It makes your own thinking cleaner, since each project has its own state and decisions.

**Why separate laptops are usually overkill**

- Context separation is a software boundary, not a hardware one. One decent machine can handle all of these:
  - One git repo (or git worktree) per project
  - One agent session per project
  - A short notes file per project (goals, decisions, conventions, current status) that the agent reads at the start
  - A container or dev environment per project when dependencies differ
- Each extra laptop adds overhead: syncing code, updates, credentials, backups and security patches multiplied by the number of machines.
- Most agent work runs in the cloud anyway, so extra laptops don't add much thinking power.
- Hardware doesn't fix your real bottleneck. You still have to switch attention between projects and review the output, and a row of laptops can make that worse by tempting you to run more projects than you can supervise.

**When separate machines do make sense**

- A client's contract or security rules require isolated hardware or accounts.
- You need different operating systems or toolchains, such as iOS builds that need a Mac.
- A project needs heavy local compute, such as running local models or large builds.
- You want a clean wall between a high-risk project, such as one handling sensitive data, and everything else.

**A practical setup for one person**

1. One machine, with a separate folder, repo and agent session per client.
2. Separate accounts, API keys and credentials per client, never shared.
3. A short project notes file the agent reads at the start of each session.
4. A cap on active projects, often 2–4, matched to how much you can review in a day.
5. Scheduled review blocks instead of constant switching. Check one project's output in a batch, then move on.
6. Remote or cloud dev environments if you want isolation without buying more hardware.

In short, keep contexts separate, but do it with repos, sessions and notes rather than more laptops. Add hardware only when a security, platform or compute requirement forces it.

**References:**

- None new. This answer is general engineering judgment rather than drawn from specific sources.
