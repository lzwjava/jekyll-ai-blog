---
audio: false
generated: true
image: false
lang: en
layout: post
title: arXiv Endorsement Strategy for Individuals
translated: false
type: note
---

**Question:** I need an arXiv endorsement to submit to cs.AI. Who can endorse me, and what's the practical path to get one?

**Answer:**

The mechanics first, then the realistic strategy for someone in your exact situation (no academic affiliation, self-taught, building in public).

## The hard constraints

An endorser must:
- Have submitted **3+ papers** to an eligible cs.* category (the long list including cs.AI, cs.LG, cs.CL, cs.SE, etc.)
- Those papers submitted **>3 months ago and <5 years ago** (a specific recency window — a prolific author from 2015 doesn't qualify if they've gone quiet)
- Be in good standing as an arXiv submitter

You forward the unique code from your email to them; they enter it. They're vouching that your paper is plausibly appropriate for the category — not peer-reviewing it. It's a low bar of trust, but it requires a real human who qualifies.

## How to find qualified endorsers (the AI-native way)

Don't guess. arXiv exposes endorsement eligibility directly. The verification trick from the instructions: on any abstract page, the **"Which of the authors of this article can endorse?"** link tells you exactly who qualifies. So the workflow is:

1. Find recent (last 1–3 years) cs.AI/cs.LG papers **closely related to your submission's topic**.
2. Check the endorse link to confirm which author qualifies.
3. Reach out to that specific author.

You can automate the discovery side. arXiv has a clean API:

```bash
# Find recent cs.AI papers matching your topic keywords
curl -s "http://export.arxiv.org/api/query?search_query=cat:cs.AI+AND+all:nanoGPT&sortBy=submittedDate&sortOrder=descending&max_results=20" \
  | grep -E '<id>|<title>|<name>|<published>'
```

Or in Python to extract author + date and filter to the eligibility window:

```python
import urllib.request, feedparser, datetime as dt

def find_endorsers(query, want=30):
    url = ("http://export.arxiv.org/api/query?"
           f"search_query={query}&sortBy=submittedDate"
           f"&sortOrder=descending&max_results={want}")
    feed = feedparser.parse(urllib.request.urlopen(url).read())
    now = dt.datetime.now(dt.timezone.utc)
    for e in feed.entries:
        pub = dt.datetime(*e.published_parsed[:6], tzinfo=dt.timezone.utc)
        age_days = (now - pub).days
        # endorser needs a paper >3mo and <5yr old; recent active authors are best bets
        flag = "active" if 90 < age_days < 1825 else ""
        authors = ", ".join(a.name for a in e.authors)
        print(f"{pub.date()} [{flag}] {e.title.strip()[:60]}")
        print(f"    {authors}")

find_endorsers("cat:cs.AI+AND+all:large+language+model")
```

The author list from the API gives you candidates; the per-paper endorse link confirms eligibility (the API doesn't expose endorsement status directly, so that last check is manual).

## The realistic strategy for *you*

The instructions hint at the social reality: "find an endorser who is connected with you." You have no thesis advisor. So your leverage is **your public work**, which is actually substantial — 8,000 notes, 400 posts, real model-training experience. Use it:

1. **Pick the right category.** cs.AI is harder to endorse into than you'd think because it's broad and moderators reclassify aggressively. If your paper is about training/architecture, **cs.LG** is often a better fit and has a much larger pool of recent, active endorsers. If it's NLP/LLM-specific, **cs.CL**. Match the category to where your actual likely-endorsers publish.

2. **Co-author with someone already qualified.** This is the cleanest path and the one most people miss. If you collaborate with anyone who has an arXiv track record — even loosely — they endorse trivially and the connection is genuine. Given your network (ex-startup, bank AI team, open-source contributors), there may already be someone one hop away.

3. **Cold outreach that respects their time.** Authors get spammed with endorsement requests. The ones that work: short, specific, show you read their work, link your paper draft and your public track record so you're clearly not a crank. Something like — "I'm submitting [title] on [topic], closely related to your [paper]. I'm an independent researcher (not affiliated); here's the draft and my work at lzwjava.github.io. Would you consider endorsing for cs.LG?" Attach the draft. The draft quality does the persuading.

4. **arXiv's own escape hatch.** If you genuinely can't find an endorser, email arXiv moderation explaining your situation with a link to the paper. They sometimes review directly. It's slow and not guaranteed, but it exists.

One honest caveat worth internalizing: endorsement is necessary but not sufficient. Moderators reject/reclassify independent submissions that read as non-scholarly. So the same effort that gets you an endorser — a tight, well-structured paper with real results — is also what survives moderation. The draft is the bottleneck, not the endorsement.

**References:**

- [arXiv endorsement help](https://arxiv.org/help/endorsement)
- [arXiv moderation policy](https://arxiv.org/help/moderation)
- [arXiv API user manual](https://info.arxiv.org/help/api/user-manual.html)
