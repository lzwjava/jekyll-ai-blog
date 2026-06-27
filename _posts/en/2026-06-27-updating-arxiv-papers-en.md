---
audio: false
generated: true
image: false
lang: en
layout: post
title: Updating arXiv Papers
translated: false
type: note
---

Question: If I've already published a paper on arXiv, can I update it afterward?

Answer:

Yes. arXiv is versioned — you submit revisions and they become v2, v3, etc. The original stays accessible; nothing is deleted.

How it works:

- Log in, go to your paper, click **"Submit a new version"** (or use the article's admin page). Upload the new source/PDF. It publishes as a new version (`v2`) usually after the next announcement cycle.
- The abstract page shows all versions with a `[v1] [v2] ...` selector and dates. The base identifier (e.g. `arXiv:2401.12345`) always resolves to the **latest** version; `arXiv:2401.12345v1` pins the original.
- Adding your GitHub + Hugging Face links is exactly the kind of edit that justifies a revision — it's a substantive reproducibility improvement, not a typo fix.

Important constraints:

- **You cannot remove a version.** All prior versions remain public forever. So v1 without the links stays visible, but v2 with them becomes the default. That's fine — versioning is expected and reviewers don't penalize it.
- **The arXiv ID never changes**, which is the whole point: citations to your paper keep working and automatically point at the latest version. This is *better* than a tweet precisely because the canonical link is stable while the content can still be updated.
- **Withdrawal** is possible but different — it marks the paper as withdrawn (with a tombstone note), it doesn't erase it. You don't want this; you just want a revision.
- There's a soft etiquette of not spamming trivial daily updates. Batch meaningful changes into a version. Adding artifact links (plus any text polish you've accumulated) in one v2 is perfectly normal.

So your plan holds: publish, then push a v2 that adds the pinned GitHub/HF links in the footnote and the Code-and-Model-Availability section. The arXiv ID stays the same, the tweet can link to the stable ID, and the paper stays canonical.

Reference:

- [arXiv — Revising/updating an article](https://info.arxiv.org/help/replace.html)
