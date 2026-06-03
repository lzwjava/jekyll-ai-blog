---
audio: false
generated: true
image: false
lang: en
layout: post
title: Disabling markdownlint's MD029 rule
translated: false
type: note
---

**Question:** What does `"MD029": false` mean in markdownlint config?

**Answer:**

`"MD029": false` **disables the MD029 rule entirely**.

**What MD029 does (default behavior):**

MD029 = "Ordered list item prefix" rule. By default, it enforces that ordered lists use sequential numbering:

```markdown
✅ Correct (enforced by MD029):
1. First
2. Second
3. Third

❌ Wrong (MD029 flags this):
2. First
1. Second
3. Third
```

**When you set `"MD029": false`:**

markdownlint stops checking that rule. Your list can be any order:

```markdown
2. MAIN COMPONENTS
1. MAIN COMPONENTS
3. MAIN COMPONENTS
```

✅ All pass — rule is disabled.

**Difference: `false` vs `{ "style": "any" }`**

| Config | Behavior |
|--------|----------|
| `"MD029": false` | Rule disabled — no checks at all |
| `"MD029": { "style": "any" }` | Rule enabled — allows any numbering style (1, 2, 3 OR 2, 1, 3 OR 1, 1, 1 — all valid) |

For your use case (preserve custom order), both work. Use `false` if you don't care about list validation at all. Use `{ "style": "any" }` if you want markdownlint to still validate list syntax but allow non-sequential numbering.
