---
audio: false
generated: true
image: false
lang: en
layout: post
title: Precision Fixes via HTML Context
translated: false
type: note
---

Question: Why is providing HTML elements (before and after) to AI tools like Copilot/Claude an effective strategy when upgrading Angular/Bootstrap, and how does this approach help with issues like removed classes (e.g., `form-group`)?

Answer:

## Why Providing HTML Before/After Context Works So Well for Angular/Bootstrap Upgrades

### The Core Problem with "Natural Language Only" Prompts

When you just say:
> *"The form doesn't look right after Bootstrap upgrade"*

The AI has **no concrete evidence** — it guesses. But when you provide actual HTML, it has **ground truth**.

---

### The "Before & After HTML" Strategy

#### ✅ What to give the AI

```
BEFORE (Bootstrap 4):
<div class="form-group">
  <label for="email">Email</label>
  <input type="email" class="form-control" id="email">
  <small class="form-text text-muted">Help text</small>
</div>

AFTER UPGRADE (Bootstrap 5 - broken now):
<div class="form-group">   <!-- ❌ form-group removed in BS5 -->
  <label for="email">Email</label>
  <input type="email" class="form-control" id="email">
  <small class="form-text text-muted">Help text</small>
</div>

PROBLEM: Spacing between fields is gone, layout collapsed
```

Now Claude/Copilot **immediately knows**:

- Exactly what class is wrong (`form-group`)
- What the structure looks like
- What the expected visual behavior was

---

### Why HTML Elements Are Better Than Natural Language

| Approach | AI Understanding | Quality of Fix |
|---|---|---|
| "The form looks broken" | Vague, guesses | Generic answer |
| "form-group doesn't work" | Partial | Might fix wrong thing |
| **Paste full before/after HTML** | **Precise, unambiguous** | **Targeted, correct fix** |

---

### Common Bootstrap 4 → 5 Breaking Changes (Where This Helps Most)

```html
<!-- ❌ BS4: form-group REMOVED in BS5 -->
<div class="form-group"> → <div class="mb-3">

<!-- ❌ BS4: text-left REMOVED in BS5 -->
<p class="text-left"> → <p class="text-start">

<!-- ❌ BS4: float-left REMOVED -->
<div class="float-left"> → <div class="float-start">

<!-- ❌ BS4: ml-* mr-* REMOVED (replaced with ms-* me-*) -->
<div class="ml-2 mr-3"> → <div class="ms-2 me-3">

<!-- ❌ BS4: badge-primary changed -->
<span class="badge badge-primary"> → <span class="badge bg-primary">
```

When you paste the **actual broken HTML**, Claude can spot ALL of these at once — not just the one you noticed.

---

### Angular-Specific: Also Include Component Context

For Angular upgrades, add the **component selector + template snippet**:

```html
<!-- Tell AI: This is Angular 15 → 17, standalone component -->

<!-- BEFORE (worked in ng15): -->
<mat-form-field appearance="legacy">  <!-- ❌ legacy removed in Angular Material 15+ -->
  <input matInput placeholder="Name">
</mat-form-field>

<!-- What error shows: No provider for MAT_FORM_FIELD_DEFAULT_OPTIONS -->
```

This tells the AI: version context + broken element + error message — a **complete picture**.

---

### The Ideal Prompt Template

```
Upgrading from [Bootstrap 4 / Angular X] to [Bootstrap 5 / Angular Y].

This HTML worked before:
--- BEFORE ---
[paste old HTML]
--- END ---

After upgrade it now looks/behaves like:
--- AFTER ---
[paste current broken HTML]
--- END ---

Problem: [one sentence — e.g., "spacing is gone between form fields"
          or "button alignment shifted right"]

Please fix the AFTER HTML to match the BEFORE behavior.
```

---

### Why This is the "Easy Win" You Described

- AI tools don't need to **imagine** your layout — they **see** it
- They can do a **diff in their head** between before/after
- They catch **multiple issues at once**, not just the one you described
- Fixes are **copy-paste ready**, not abstract suggestions
- Less back-and-forth, faster iteration

> The HTML element **is** the specification. Natural language describes intent; HTML shows **reality**.
