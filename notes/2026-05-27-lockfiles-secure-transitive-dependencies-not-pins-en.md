---
audio: false
generated: true
image: false
lang: en
layout: post
title: Lockfiles secure transitive dependencies, not pins
translated: false
type: note
---

Pin in pyproject.toml solves **direct** deps, but not **transitive** ones. That's the gap.

Example:

```
# pyproject.toml
dependencies = ["requests==2.31.0"]
```

requests pulls in `urllib3`, `idna`, `charset-normalizer`, `certifi`. You don't pin those — the resolver picks versions freely. Next month, `urllib3` releases 2.1.0 with a breaking change, and your CI breaks while your laptop still works (cached old version).

**You could** pin every transitive dep in pyproject.toml too, but:

1. You'd be manually maintaining ~20-50 lines of deps you never explicitly asked for
2. Any time you add one dep, you'd need to resolve and pin all its children too
3. You lose integrity hashes (uv.lock includes SHA256 hashes per package)
4. You lose platform markers (some transitive deps differ on linux vs macos)

The lockfile is literally the output of "resolve everything once, commit the result, replay everywhere." It's the standard pattern — Cargo.lock, poetry.lock, package-lock.json, Gemfile.lock all exist for the same reason.

**Bottom line:** Pinning direct deps in pyproject.toml is good practice (specify version ranges or minimum versions). But the lockfile is the reproducibility guarantee for the full dependency graph. They serve different purposes. Commit both.