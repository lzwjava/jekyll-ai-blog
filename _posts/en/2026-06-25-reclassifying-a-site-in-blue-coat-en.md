---
audio: false
generated: true
image: false
lang: en
layout: post
title: Reclassifying a Site in Blue Coat
translated: false
type: note
---

**Question:** How to change a site's category in Symantec Blue Coat's system to get it unblocked?

**Answer:**

Directly on `sitereview.bluecoat.com`:

---

## Steps

### 1. Look up the site

Go to:

```
https://sitereview.bluecoat.com/#/lookup-result/huggingface.co
```

### 2. See current category

It shows what category Blue Coat currently assigns — e.g. `Technology/Internet`, `File Storage`, `Malicious Sources` etc.

### 3. Submit reclassification

On the same page there's a **"Submit for Review"** or **"Suggest a Category Change"** button.

Fill in:

- **Your suggested category** → pick something benign like `Technology/Internet` or `Research/Reference`
- **Reason** → write 1-2 sentences

Example reason:

```
HuggingFace is a legitimate AI/ML research platform used by
engineers and researchers worldwide for accessing open-source
models and documentation. It should be categorized as
Technology/Internet or Research/Reference.
```

### 4. Submit — no account needed

Symantec accepts anonymous submissions. They review and update their global database.

---

## What happens after

```
Your submission
      ↓
Symantec reviews (1-2 weeks)
      ↓
Global Blue Coat DB updated
      ↓
All corporate proxies using Blue Coat
auto-pull the new category
      ↓
Your bank's proxy unblocks it automatically
```

---

## Realistic outcome

| Current Category | Chance of success |
| ----------------- | ------------------- |
| `Malicious Sources` | Low — hard to reclassify |
| `File Storage` | Medium |
| `Technology/Internet` already | Already correct, IT policy is blocking it — different problem |
| `Uncategorized` | High — easy win |

If it's already correctly categorized but your bank's policy blocks that category — then reclassification won't help. That becomes an internal IT whitelist request instead.
