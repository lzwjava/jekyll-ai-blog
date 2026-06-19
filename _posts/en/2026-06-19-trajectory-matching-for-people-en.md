---
audio: false
generated: true
image: false
lang: en
layout: post
title: Trajectory Matching for People
translated: false
type: note
---

Yes, exactly. You've described a real emerging infrastructure problem. Let me be precise about what this actually is.

---

## It's Three Problems Collapsed Into One

**1. Signal Aggregation** — collect public activity streams
**2. Representation Learning** — embed people/orgs into latent space
**3. Matching/Recommendation** — find alignment across that space

This is literally the same architecture as:

- Netflix recommendation (user ↔ content)
- LinkedIn job matching (candidate ↔ role)
- Paper recommendation on Semantic Scholar (researcher ↔ paper)

Except the **entities are people + their evolving intellectual trajectory**.

---

## The Data Sources That Actually Matter for AI/Tech World

```
Person Signal:
  GitHub     — stars, forks, commits, repo topics, language drift
  HuggingFace — models uploaded, datasets, spaces, paper likes
  arXiv      — papers submitted, cited, which authors they follow
  Twitter/X  — who they RT, what threads they engage, keyword drift
  LinkedIn   — job changes, posts, skills endorsements
  Blog/RSS   — writing topics over time

Org Signal:
  GitHub org — repo activity, contributor graph
  HuggingFace org — model releases, download trends
  arXiv affiliations — paper output velocity, topic clustering
  Job postings — what skills they're hiring = what they're building
  Funding news — Crunchbase, PitchBook
```

---

## The Matching Architecture

```python
# Conceptually what this looks like end-to-end

class PersonEmbedder:
    def embed(self, person):
        signals = [
            github_activity(person.github),      # repo stars = interest graph
            arxiv_activity(person.arxiv),         # papers = deep focus areas
            hf_activity(person.huggingface),      # models = what they build
            twitter_activity(person.twitter),     # discourse = current thinking
        ]
        # Each signal → text summary → LLM embed
        texts = [summarize(s) for s in signals]
        vectors = [embed(t) for t in texts]
        return weighted_avg(vectors, weights=[0.3, 0.3, 0.2, 0.2])

class Matcher:
    def match(self, query_person, candidate_pool):
        q_vec = embedder.embed(query_person)
        scores = [
            (p, cosine_sim(q_vec, embedder.embed(p)))
            for p in candidate_pool
        ]
        # But also: temporal alignment — are they moving in same direction?
        drift_scores = [
            (p, trajectory_similarity(query_person, p))
            for p in candidate_pool
        ]
        return merge(scores, drift_scores)
```

**The key insight**: static embedding isn't enough. You want **trajectory matching** — two people both moving toward MoE + inference optimization are more aligned than two people who are currently similar but diverging.

---

## Trajectory Matching Is the Hard Part

```python
def trajectory_similarity(person_a, person_b, window_months=6):
    # Get embeddings at t-6, t-3, t-0
    a_vecs = [embed_at_time(person_a, t) for t in [-6, -3, 0]]
    b_vecs = [embed_at_time(person_b, t) for t in [-6, -3, 0]]

    # Direction vector in embedding space
    a_drift = a_vecs[-1] - a_vecs[0]
    b_drift = b_vecs[-1] - b_vecs[0]

    # Are they moving in the same direction?
    return cosine_sim(a_drift, b_drift)
```

This is what frontier labs actually care about — not "is this person good at transformers now" but "is this person's learning trajectory converging with where we're going."

---

## Who's Actually Building This

| Company | What They Do |
|---|---|
| **Clay.com** | enriches contact data from 50+ sources, some ML matching |
| **Momen/Glean** | enterprise people graph from internal signals |
| **LinkedIn Recruiter** | the closest to this at scale, but closed |
| **Zeta Alpha** | arXiv/paper recommendation for researchers |
| **papers.cool / paper digest** | early signal on trending papers |
| **Exploding Topics** | trend detection, not people-level |

Nobody has done the **full-stack people × research × code × discourse** graph yet. That's the gap.

---

## What Frontier Labs Actually Do (Informally)

Anthropic, OpenAI, DeepSeek — they track:

- arXiv submissions by known researchers + unknown first-authors
- GitHub orgs of universities / competing labs
- Twitter discourse from researchers (who's complaining about what = what's unsolved)
- HuggingFace model upload patterns (sudden activity = something shipping)
- Job postings from competitors (hiring CUDA kernel engineers = inference push)

This is mostly **manual + informal** right now. A few people at each lab do this by hand. The infrastructure to automate it doesn't fully exist yet.

---

## The LLM Layer on Top

Once you have embeddings, LLM adds:

```
Query: "Find researchers likely working on long-context efficiency
        who haven't published yet but show signals"

LLM reasons over:
  - GitHub: who's been starring flash-attention, ring-attention repos
  - arXiv: who's citing Mamba/SSM papers but hasn't submitted yet
  - Twitter: who's asking questions about KV cache compression

Output: ranked list with reasoning per person
```

This is basically **talent/collaboration radar** — and it's a real product waiting to be built.

---

## For You Specifically

You already have the right instinct. A CLI tool that:

1. Tracks a curated list of ~200 people (researchers, engineers, potential collaborators/clients)
2. Pulls their public signals weekly
3. Embeds + clusters them
4. Surfaces "this person just shifted hard into your space" alerts

...would be genuinely useful and buildable in a weekend with your stack. The arXiv and GitHub APIs are open. HuggingFace has a good API. That's already 70% of the signal.
