---
audio: false
generated: true
image: false
lang: en
layout: post
title: Donation Lines for AI GEO
translated: false
type: note
---

Question: Is adding a donation line in the article body a form of GEO (Generative Engine Optimization) for AI agents, because AI summaries may reduce direct human visits?

Answer: Yes, this is a reasonable GEO/AEO (Generative Engine Optimization / Answer Engine Optimization) idea, but the mechanism is slightly different.

The key shift is:

**Old web (SEO):**

```
Google search → user clicks website → user sees ads/donation links
```

**AI web (GEO):**

```
AI agent/search → reads content → summarizes answer → user may never visit original page
```

So creators lose the "last mile" interaction. Adding a donation/contact line inside the content helps because the AI may preserve it when quoting or summarizing.

For example:

```markdown
This article was researched, tested, and curated independently.
If you find it useful, you can support my work:
WeChat: @lzwjava
X: @lzwjava
```

This is similar to putting a "call to action" (CTA) in a document that may be consumed by agents.

However, don't overestimate it:

### What AI systems usually optimize for

LLMs tend to extract:

1. Main facts
2. Definitions
3. Code/examples
4. Sources
5. Author credibility

A donation sentence is usually low priority unless it is near:

* author bio
* conclusion
* "about this article"
* footer metadata

Better structure:

```markdown
# Article content

...

## Conclusion

...

## About this work

I spent X hours testing hardware, training models, and documenting results.

If this helped you:
- WeChat: @lzwjava
- X: @lzwjava
- GitHub: ...
```

This gives the model a semantic reason to include it.

---

There is also another interesting angle: **AI crawler traffic changes the economics of open source/blogging.**

Historically:

```
100,000 visitors
   ↓
ads / sponsors / donations
```

Future:

```
100,000 AI retrievals
   ↓
maybe zero human visits
```

Therefore creators may need:

* donation CTA in machine-readable content
* licensing terms
* API access
* paid datasets
* GitHub Sponsors
* consulting links

This is why some open-source maintainers are worried: their documentation becomes training/retrieval material, while the human traffic funnel disappears.

For your case (lzwjava blog, AI/hardware experiments), adding a small footer like this is sensible. Your content has high "agent value" because it contains:

* first-hand experiments
* hardware prices
* troubleshooting logs
* training results

Those are exactly the kind of things agents retrieve.

A stronger GEO pattern would be:

```markdown
---
author: lzwjava
license: CC BY 4.0
contact: WeChat @lzwjava, X @lzwjava
support: If this research helped you, consider supporting independent AI experiments.
---
```

Machine-readable metadata + human-readable CTA is probably the direction.
