---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI-Guided Strategic Multi-Commit Cherry-Picking
translated: false
type: note
---

Question:
Can we use a code assistant like Copilot to cherry-pick dozens of commits from branch A to branch B, and control conflict strategy (prefer theirs vs ours) per feature by prompting carefully?

Answer:

Yes — this is actually a **very good use case** for a code assistant. It helps especially when:

* You must cherry-pick **tens of commits**
* Some features should **prefer theirs**
* Some features should **prefer ours**
* Manual conflict resolution would be **tedious and error-prone**

Your idea is correct. The assistant can act as a **guided merge operator**, while you define strategy per feature.

---

# Why this works well

Cherry-picking many commits usually causes:

* repeated conflicts
* mixed ownership (some files you want theirs, some yours)
* dependency ordering issues
* easy-to-miss semantic conflicts

A code assistant can:

* analyze conflict context
* follow rules you define
* apply different strategies per feature
* generate correct resolutions consistently

---

# Example Workflow (Best Practice)

### Step 1 — Define rules in prompt

Example:

```
We are cherry-picking commits from branch A into branch B.

Rules:
- For feature "payment", prefer theirs
- For feature "logging", prefer ours
- For config files, always prefer ours
- For new files, prefer theirs
- Do not remove existing API signatures
- Keep tests from both sides
```

This gives the assistant **merge policy**, not just commands.

---

### Step 2 — Cherry pick sequentially

```
git cherry-pick <commit1>
```

When conflict happens:

Ask Copilot / assistant:

```
Resolve conflicts using rules:
- payment: theirs
- logging: ours
- config: ours
- new files: theirs
```

This is **much safer** than blindly using:

```
git cherry-pick -X theirs
```

because `-X theirs` applies **globally**, not selectively.

---

# When this is MUCH better than git flags

Git only supports:

```
-X ours
-X theirs
```

But you want:

* feature A → theirs
* feature B → ours
* file C → manual merge
* test → combine both

Only an AI/code assistant can **reason per conflict**.

---

# Even better: batch strategy

You can tell assistant:

```
Cherry-pick these commits:

A1 A2 A3 A4 A5

Strategy:
- commits A1-A2: prefer theirs
- commits A3-A4: prefer ours
- A5: manual merge
```

This is very powerful.

---

# Another strong pattern

Let assistant generate commands:

```
git cherry-pick A1
git checkout --theirs src/payment/*
git checkout --ours config/*
git add .
git cherry-pick --continue
```

This combines:

* automation
* correctness
* auditability

---

# Important caution (you correctly noticed)

Prompt quality matters a lot.

Bad prompt:

> fix conflict

Good prompt:

```
Resolve conflict.
Rules:
- Keep branch B logging system
- Use branch A payment implementation
- Preserve both test cases
- Do not change public interfaces
```

Much safer.

---

# When this approach is especially useful

* backporting features
* partial feature migration
* long-lived branch sync
* refactor branch merge
* vendor fork updates
* large monorepo merges

---

# One more pro tip

Use **no-commit mode**:

```
git cherry-pick -n <commit>
```

Then let assistant resolve before commit.

This gives you **full control**.

---

# Summary

Yes — your understanding is correct:

* Cherry-pick many commits ✅
* Per-feature strategy (ours/theirs) ✅
* Code assistant helps reasoning ✅
* Prompt precision is critical ✅
* Safer than git flags alone ✅

This is actually a **very advanced Git workflow**.
