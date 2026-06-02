---
audio: false
generated: true
image: false
lang: en
layout: post
title: Coordinate consistent git cherry-pick strategy across multiple branches
translated: false
type: note
---

**Question:**
How can I coordinate consistent `git cherry-pick` strategy across multiple branches (B and C) when syncing ~70 Angular upgrade commits from branch A, while using a probabilistic AI assistant like Copilot and avoiding divergence?

**Answer:**

You're solving a **multi-branch backporting problem with AI in the loop**. The core issue is not Git — it's **determinism**.
If you run AI twice on B and C, you'll get **different conflict resolutions**, which leads to **code drift**.

You need to **make the process deterministic**, not prompt-based.

---

# The real problem

You currently:

* Cherry-pick A → B (AI resolves conflicts)
* Cherry-pick A → C (AI resolves conflicts again)
* Same prompt, but AI ≠ deterministic → results diverge

So B ≠ C even though logic should be identical.

---

# Best solutions (ranked)

## ✅ Best: Create an intermediate "upgrade base" branch (deterministic)

Instead of applying A→B and A→C separately:

```
          A (Angular 21)
         /
upgrade-base
       /   \
      B     C
```

### Steps

### 1. Create base from shared ancestor

```
git checkout common-ancestor
git checkout -b angular21-upgrade-base
```

### 2. Cherry-pick ALL 70 commits ONCE

```
git cherry-pick A~70..A
```

Resolve conflicts **once** (with AI if needed)

Now this branch contains **canonical resolution**

---

### 3. Merge base into B and C

```
git checkout B
git merge angular21-upgrade-base

git checkout C
git merge angular21-upgrade-base
```

Now:

* Same commits
* Same conflict resolution
* Same file structure
* No divergence

This is **how big companies do mass upgrades**

---

## ✅ Second best: Use rerere (Git remembers conflict resolution)

Enable:

```
git config --global rerere.enabled true
```

Then:

1. Cherry-pick A → B
2. Resolve conflicts manually/AI
3. Cherry-pick A → C

Git auto-applies **same conflict resolution**

This is extremely powerful.

Git stores:

```
conflict input -> resolution output
```

So second branch becomes deterministic.

---

## ✅ Third: Use strategy-based cherry-pick (automate yours/theirs)

Your rule:

```
tool/ -> theirs
business/logic -> ours
```

You can automate this.

Example:

```
git cherry-pick -X theirs <commit>
```

or

```
git cherry-pick -X ours <commit>
```

But that's global — you need **path-based strategy**

Use `.gitattributes`

```
tool/** merge=theirs
business/** merge=ours
```

Then define merge drivers.

This removes AI randomness entirely.

---

## Your current method (what's wrong)

You do:

```
git cherry-pick ca^..cb
AI fix
repeat
```

Problems:

* AI decisions differ per run
* batch size changes context
* conflict order changes
* results drift

So B and C diverge.

---

# Most robust workflow (recommended)

### Step 1 — enable rerere

```
git config --global rerere.enabled true
```

### Step 2 — cherry-pick to B

```
git checkout B
git cherry-pick A~70..A
```

resolve with AI

---

### Step 3 — cherry-pick to C

```
git checkout C
git cherry-pick A~70..A
```

Git auto resolves same conflicts.

No divergence.

---

# Even better (enterprise method)

Use **patch series instead of cherry-pick**

```
git format-patch A~70..A
```

Then apply:

```
git am *.patch
```

Apply to B and C → deterministic.

---

# Ultra-enterprise solution (best for 1000+ differences)

Use **stacked branches**

```
common-base
   ├── region-A-upgrade
   ├── region-B-upgrade
   └── region-C-upgrade
```

Then rebase each on same upgrade commits.

This is how:

* Chromium
* Android
* Linux kernel

handle mass backports.

---

# Key insight

Don't try to make **AI deterministic**
Make **Git deterministic**, then use AI once.

---

# Your case summary

You have:

* 2000 shared commits
* 1000 region differences
* 70 upgrade commits

Best solution:

```
create angular21-base
apply once
merge into B and C
```

This guarantees:

* identical Angular upgrade
* no drift
* same behavior
* less debugging

---

# Extra tip (important)

Cherry-pick **small batches**:

Bad:

```
git cherry-pick 70 commits
```

Good:

```
git cherry-pick 5 commits
```

Conflict resolution becomes stable.

---

# Final recommendation

Use this combo:

1. enable rerere
2. cherry-pick to B
3. cherry-pick to C
4. OR create upgrade-base branch

This removes AI randomness completely.

---

References:

* [https://git-scm.com/docs/git-rerere](https://git-scm.com/docs/git-rerere)
* [https://git-scm.com/docs/git-cherry-pick](https://git-scm.com/docs/git-cherry-pick)
* [https://git-scm.com/docs/git-format-patch](https://git-scm.com/docs/git-format-patch)
* [https://git-scm.com/book/en/v2/Git-Tools-Rerere](https://git-scm.com/book/en/v2/Git-Tools-Rerere)
