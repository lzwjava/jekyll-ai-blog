---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Knowledge from Public Questions
translated: false
type: note
---

Question: Is a **public, open LLM chat/search platform**—where questions and answers are public by default, answers become permanent searchable pages, and monetization comes from ads—a viable product?

Answer: **Yes. I think this is actually a strong idea, but the key is to think of it as “AI-generated public knowledge” rather than “free ChatGPT.”**

The interesting architecture is:

```text
                    ┌─────────────────────┐
User question ────> │       LLM           │
                    └──────────┬──────────┘
                               │
                     answer + citations
                               │
                               v
                    ┌─────────────────────┐
                    │   Public Question   │
                    │      + Answer       │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              v                v                v
         Search index      Categories       Recommendations
              │                │                │
              └────────────────┼────────────────┘
                               v
                         Google traffic
                               │
                            AdSense
```

### The really important insight

Traditional search has:

```text
question → documents → user reads
```

LLM chat has:

```text
question → answer
```

Your system would be:

```text
question
   ↓
LLM answer
   ↓
permanent public document
   ↓
indexed by Google
   ↓
future users discover it
   ↓
related questions
   ↓
more traffic
```

So **each inference potentially creates a reusable asset**.

That changes the economics considerably.

If someone asks:

> How does KV cache work in vLLM?

You don't just spend $0.01 generating an answer.

You create:

```text
/qa/how-does-kv-cache-work-in-vllm

Title:
How does KV cache work in vLLM?

Answer:
...

Related:
- PagedAttention explained
- vLLM vs llama.cpp
- KV cache memory calculation
- How much VRAM does KV cache consume?
```

Now that answer can potentially receive **10,000 future visits without another LLM inference**.

That's much more interesting than ordinary chatbot economics.

---

## I would make the default behavior public

Something like:

```text
┌────────────────────────────────────────────┐
│ Ask anything...                            │
│                                            │
│ How does KV cache work?               [→] │
└────────────────────────────────────────────┘

This question and answer will be public.
```

Then:

```text
Question
   ↓
Generate once
   ↓
Save forever
   ↓
Anyone can read
   ↓
Anyone can search
```

Private chat becomes an **explicit opt-out**, rather than the default.

That gives you a gigantic potential knowledge graph.

---

## The killer feature isn't actually the LLM

I'd build the product around **public questions**.

For example:

```text
                  AI Knowledge
                       │
       ┌───────────────┼───────────────┐
       ↓               ↓               ↓
     Search          Topics        Questions
       │               │               │
       ↓               ↓               ↓
 "KV cache"         LLMs           15,238 Qs
```

A question page could look like:

```text
How does KV cache work in vLLM?

[AI answer]

Sources:
- vLLM paper
- GitHub
- documentation

──────────────────────────────

Related questions

→ How much memory does KV cache use?
→ What is PagedAttention?
→ Why does vLLM use block tables?
→ How does KV cache differ from MQA?
→ How does llama.cpp implement KV cache?
```

This starts looking less like ChatGPT and more like:

**Wikipedia + Google + Stack Overflow + LLM.**

---

# There is an even better loop

Users don't necessarily need to ask completely new questions.

The system can generate questions automatically.

For example:

```text
Question:
How does KV cache work?

Answer
   ↓
LLM generates related questions

├── How is KV cache stored in GPU memory?
├── Why does KV cache grow with sequence length?
├── What is PagedAttention?
├── How does prefix caching work?
├── How does KV cache affect throughput?
└── How does vLLM manage fragmented KV cache?
```

Then:

```text
              one question
                    │
        ┌───────────┼───────────┐
        ↓           ↓           ↓
       Q1          Q2          Q3
        │           │           │
       Q4          Q5          Q6
        │           │           │
        └───────────┼───────────┘
                    ↓
              knowledge graph
```

That's where this gets powerful.

---

# And you don't need to answer every question live

This is probably the most important engineering/economic optimization.

Suppose:

```text
100,000 users
10 questions/user/month
= 1M questions
```

Naively:

```text
1M questions
→ 1M LLM inference requests
```

Expensive.

Instead:

```text
question
   ↓
normalize
   ↓
semantic search
   ↓
existing answer?
   ├── yes → return cached answer
   │
   └── no → generate
              ↓
           store answer
```

So:

```python
def ask(question):
    q = normalize(question)

    answer = semantic_search(q)

    if answer.similarity > 0.95:
        return answer

    answer = llm.generate(q)
    db.save(q, answer)

    return answer
```

Eventually the ratio becomes something like:

```text
100 questions
        │
        ├── 70 → existing answer
        │
        ├── 20 → synthesize from existing answers
        │
        └── 10 → expensive LLM generation
```

That is a **completely different cost structure**.

---

# Static pages are extremely valuable

I would actually render every answer as an ordinary HTML page.

Not:

```text
/api/chat
```

but:

```text
/q/how-does-kv-cache-work
```

with:

```html
<h1>How does KV cache work?</h1>

<article>
    ...
</article>

<nav>
    Related questions...
</nav>
```

Then:

```text
Google
   ↓
public HTML
   ↓
answer
   ↓
related questions
   ↓
another answer
```

You are effectively building an **AI-generated SEO corpus**.

But there's an important caveat: Google increasingly cares about useful/original content rather than simply pages generated at scale. So blindly generating millions of thin AI pages is likely to be a bad SEO strategy.

The pages need to have:

* useful answers
* citations
* stable URLs
* good internal linking
* deduplication
* correction/edit history
* strong topical structure
* preferably user contributions

---

# Revenue

Your AdSense idea makes sense for the free/public layer.

Potential funnel:

```text
Google
   ↓
free public answer
   ↓
ads
   ↓
$ revenue
```

But I'd add several revenue sources later:

```text
                     Public AI
                         │
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
      Ads             API            Premium
        │                │                │
    AdSense        developers        private chat
                                     no ads
                                     better models
```

Potentially:

### Free

```text
Unlimited questions
Public by default
Cached answers
Ads
```

### Premium

```text
Private conversations
No ads
Better models
File upload
Long context
```

### API

```text
GET /search?q=...
GET /answer?id=...
```

And interestingly, **your public corpus itself becomes valuable**.

---

# I'd also add voting/correction

This is where you can beat pure AI-generated websites.

```text
Answer

👍 1,284
👎 31

Was this answer useful?

[Correct] [Add source] [Discuss]
```

Then eventually:

```text
LLM answer
    +
human feedback
    +
sources
    +
version history
```

You get something much closer to a living knowledge base.

Stack Overflow has:

```text
human → answer → votes
```

You could have:

```text
LLM → answer → humans → votes/corrections → better answer
```

---

# One danger: garbage explosion

This is the biggest problem.

Imagine:

```text
"What is Bitcoin?"

"What is Bitcoin really?"

"Bitcoin explained"

"Explain Bitcoin to me"

"Bitcoin meaning"

"How does Bitcoin work?"
```

You don't want six independent pages.

You need:

```text
semantic clustering
        ↓
canonical question
        ↓
aliases
```

For example:

```text
Canonical:

How does Bitcoin work?

Aliases:

- What is Bitcoin?
- Explain Bitcoin
- Bitcoin explained
- How does Bitcoin actually work?
```

Then one canonical answer.

This is essentially an **LLM-powered deduplication/indexing problem**.

And that's a very solvable engineering problem for you.

---

# I would build the MVP surprisingly small

You could probably prototype this with:

```text
Next.js
Postgres
pgvector
one LLM API
Cloudflare
Google Search Console
AdSense
```

Schema:

```sql
CREATE TABLE questions (
    id          BIGSERIAL PRIMARY KEY,
    slug        TEXT UNIQUE,
    question    TEXT NOT NULL,
    answer      TEXT NOT NULL,
    embedding   VECTOR(1536),
    created_at  TIMESTAMP DEFAULT now()
);

CREATE INDEX questions_embedding_idx
ON questions
USING hnsw (embedding vector_cosine_ops);
```

Request:

```python
q = embed(user_question)

existing = db.semantic_search(q, limit=5)

if existing[0].score > 0.94:
    return existing[0]

answer = llm(user_question)

db.insert(
    question=user_question,
    answer=answer,
    embedding=q,
)

return answer
```

Then generate:

```text
/sitemap.xml
/robots.txt
/q/...
/topic/...
/search?q=...
```

That's basically the first version.

---

# The strategic question

I wouldn't position it as:

> **Free ChatGPT**

because you can't win that battle.

I'd position it conceptually as:

> **The internet's public AI knowledge base.**

The distinction is:

```text
ChatGPT
    ↓
conversation

Your product
    ↓
knowledge
```

And the fundamental asset becomes:

```text
                millions of questions
                         ↓
                 millions of answers
                         ↓
                 semantic graph
                         ↓
             searchable AI knowledge
```

That's potentially much more defensible than another chat UI.

**I think this is worth prototyping.** The MVP could be extremely cheap: one public question page, cached answers, semantic deduplication, search, related questions, and ads. The interesting experiment is not whether people like chatting with it—that's already proven. The experiment is whether **public LLM answers compound into organic search traffic faster than inference + moderation + hosting costs grow.**
