---
audio: false
generated: true
image: false
lang: en
layout: post
title: Git Pull Strategies for Divergent Branches
translated: false
type: note
---

Question: What do the Git “divergent branches” options mean, and which one should I use (merge, rebase, or fast-forward only)?

Answer:

This message appears when your **local branch and remote branch have both diverged** (each has new commits the other doesn’t), so Git doesn’t know how you want to combine them during `git pull`.

You have 3 main strategies:

---

## 1. `merge` (safe default for teams)

```bash
git config pull.rebase false
```

### What it does

* Creates a **merge commit**
* Preserves *exact history* of both branches

### Pros

* Very safe
* No history rewriting
* Good for collaboration

### Cons

* History can become “messy” (many merge commits)

### When to use

* Working in teams
* You don’t want to rewrite history
* You prefer explicit merge points

---

## 2. `rebase` (clean linear history — popular choice)

```bash
git config pull.rebase true
```

### What it does

* Re-applies your local commits on top of the updated remote branch
* Produces a **linear history**

### Pros

* Clean, readable history
* No merge commits
* Common in modern workflows (GitHub, open source)

### Cons

* Rewrites commit history locally
* Can be confusing if conflicts happen repeatedly
* Avoid rebasing shared/public branches

### When to use

* Personal feature branches
* You want clean history
* You understand conflict resolution

---

## 3. `fast-forward only` (strict, safest in production pipelines)

```bash
git config pull.ff only
```

### What it does

* Only allows pull if no divergence exists
* If divergence exists → Git refuses to pull

### Pros

* Extremely safe
* Prevents accidental merges/rebases
* Keeps history strictly linear

### Cons

* Often fails unless your branch is perfectly up-to-date
* You must manually resolve by rebase/merge

### When to use

* CI/CD environments
* Strict release branches
* Teams enforcing clean history rules

---

## 🔥 What should YOU choose?

Based on typical modern development workflows:

### 👉 Best general recommendation:

```bash
git config --global pull.rebase true
```

Why:

* Keeps history clean
* Works well for solo + modern GitHub workflows
* Most flexible in practice

---

### 👉 If you're working in a team with less Git discipline:

```bash
git config --global pull.rebase false
```

---

### 👉 If you're in a strict production/release environment:

```bash
git config --global pull.ff only
```

---

## 💡 Practical tip (important)

You don’t have to set one globally—you can override per pull:

```bash
git pull --rebase
git pull --no-rebase
git pull --ff-only
```

---

## Simple mental model

* **merge** → “combine histories”
* **rebase** → “rewrite my work on top”
* **ff-only** → “only proceed if no conflict exists”

---

If you tell me your workflow (solo dev, team, open-source, etc.), I can recommend a more precise setup and Git config template.
