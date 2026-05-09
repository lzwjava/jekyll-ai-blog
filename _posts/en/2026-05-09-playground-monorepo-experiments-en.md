---
audio: false
generated: true
image: false
lang: en
layout: post
title: Using a Playground Monorepo for Experiments
translated: false
type: note
---

Question: I have too many abandoned GitHub repos with fewer than 100 commits. Should I use a single "playground" monorepo for experiments, and then promote successful ones to separate repos?

Answer:

Yes — your instinct is exactly right, and this is a well-recognized pattern used by many developers. Here's a comprehensive breakdown:

---

## The Problem You're Describing

You're experiencing **"repo sprawl"** — the graveyard of half-started projects that felt important at the time. Each one got its own repo, you lost motivation after a few commits, and now your GitHub profile is full of ghost projects. This is extremely common.

---

## The Solution: A `playground` Monorepo

### What it is

A single GitHub repo (e.g. `yourname/playground`) where you dump all experiments, spikes, and exploratory code — organized by folder. This is a monorepo for all your experiments and small projects, and also a chance to try out new tools you wouldn't get to use on larger projects.

### Folder structure example

```
playground/
├── experiments/
│   ├── rust-wasm-try/
│   ├── openai-agent-poc/
│   └── svelte-dashboard/
├── snippets/
│   └── useful-utils.ts
└── README.md
```

---

## The Graduation Workflow

This is the key pattern — treat the playground as an **incubator**:

```
playground/feature-folder  →  (proven valuable?)  →  standalone repo
```

| Stage | Location | Criteria to Graduate |
|---|---|---|
| Idea / Spike | `playground/` folder | — |
| Growing traction | Still in playground | 50+ commits, clear purpose |
| Real project | New standalone repo | Has users, docs, CI/CD needs |

You can use `git subtree split` or `git filter-repo` to extract a folder's full history into a new repo cleanly when you're ready to graduate it.

---

## Why This Works Better Than Separate Repos

**For exploration projects specifically:**

- **Lower friction** — No need to set up a new repo, README, license, CI just to try an idea. Just make a folder and code.
- **One place to find your experiments** — Instead of 40 repos nobody visits, one repo with organized folders.
- **Shared tooling** — One `.editorconfig`, `prettier`, `eslint` config for everything.
- When projects live in their own repositories, their code is mostly seen by maintainers. When they move on, the code usually lies untouched and starts to rot, falling behind on best practices and dependencies.

---

## When NOT to use a monorepo

Monorepos work best when your projects share significant code, need atomic commits across services, or you want to enforce consistent tooling. For small, unrelated projects or teams needing strict access controls, it can be less suitable.

For a **personal playground**, the "unrelated projects" concern doesn't matter — the point is exploration, not production architecture.

---

## Practical Tips for Your Playground Repo

1. **Use a clear folder naming convention** — e.g. `YYYY-topic` like `2025-rust-http-server`
2. **Write a one-liner README per experiment** — even just `# What this is: trying X to solve Y`
3. **Use GitHub Topics** — Tag the repo with `playground`, `experiments`, `learning`
4. **Set a graduation threshold** — define your personal rule, e.g.: *"If I come back to this 3+ times or someone else finds it useful, it becomes a real repo."*
5. **Don't over-engineer the monorepo itself** — For personal exploration, you don't need Turborepo or Nx. A simple folder structure is enough.

---

## Extracting to a Standalone Repo (When You Graduate)

```bash
# Extract a subfolder with full git history
git filter-repo --subdirectory-filter experiments/my-cool-project
```

This preserves all commit history from that folder into the new repo — clean and professional.

---

## Bottom Line

Your idea is solid and battle-tested. The playground repo acts as a **low-commitment sandbox**, and the graduation process keeps your public repos meaningful. Stop creating repos for ideas — create folders first, earn the repo later.

References:

- [GitHub Well-Architected: Monorepos](https://wellarchitected.github.com/library/scenarios/monorepos/)
- [Atlassian: Monorepos in Git](https://www.atlassian.com/git/tutorials/monorepos)
- [island-is Handbook: Monorepo rationale](https://github.com/island-is/handbook/blob/master/monorepo.md)
- [Example: playground monorepo](https://github.com/Ashishamar99/playground)