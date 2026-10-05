---
audio: false
generated: true
image: false
lang: en
layout: post
title: Publishing Knowledge, Not the Moat
translated: false
type: note
---

Question: **Why does Meituan—and companies like Netflix—publish so much valuable engineering knowledge publicly? Doesn't this help competitors copy them and reduce their competitive advantage?**

Answer:

Yes, **competitors can learn from it**. But for companies like Meituan and Netflix, the expected benefits are usually much larger than the cost.

The key distinction is:

> **They are publishing knowledge, not publishing the whole competitive system.**

Meituan has been doing this for more than 12 years. Its blog started in 2013; by early 2026 it had published 640+ technical articles, and it continues to package hundreds of pages of engineering material into annual collections. ([Meituan Tech][1])

### 1. The real moat is not the blog post

Imagine Meituan publishes:

> "How we designed our distributed scheduling system."

A competitor learns:

```text
problem
  ↓
architecture
  ↓
algorithm
  ↓
tradeoffs
```

But they don't receive:

```text
10 years of production data
+ 10,000 engineers
+ millions of merchants
+ billions of transactions
+ internal tooling
+ operational experience
+ organizational knowledge
+ proprietary datasets
+ deployment infrastructure
+ accumulated edge cases
```

The blog might give you **the map**, but not the accumulated ability to operate the city.

This is particularly true for engineering.

Knowing:

```python
def shard(key):
    return hash(key) % N
```

is trivial.

Knowing **when your sharding strategy breaks at 100 million users, how to migrate without downtime, how to debug it at 3 AM, how to measure the failure modes, and how the organization responds** is much harder.

---

### 2. Publishing can actually make Meituan stronger

Meituan explicitly describes its technology culture as one of learning and sharing, and its external blog, internal community, training, and technical events are connected to that ecosystem. ([Meituan Tech][2])

There is a powerful flywheel:

```text
engineering work
      ↓
write it down
      ↓
public technical reputation
      ↓
engineers discover Meituan
      ↓
better recruiting
      ↓
better engineers
      ↓
better technology
      ↓
more interesting engineering work
      ↓
more things worth publishing
```

That is **very different from traditional IP protection**.

For a company whose biggest asset is engineering talent, a technical blog can function partly as a **recruiting machine**.

Meituan's own articles explicitly connect its technical material with recruitment. ([Meituan Tech][2])

And this isn't theoretical: Meituan says its technical blog/WeChat ecosystem has attracted a large engineering audience and that its technical salon has had tens of thousands of registrations. ([Meituan Tech][3])

---

### 3. It also gives them status in the engineering community

Think about Netflix.

If Netflix publishes:

> "How we solved X at massive scale"

then engineers around the world think:

> "Netflix has interesting engineering problems."

That creates:

```text
technical reputation
       ↓
engineer attention
       ↓
recruiting
       ↓
conference invitations
       ↓
open-source adoption
       ↓
industry influence
       ↓
more talent / partners
```

So the blog isn't just documentation.

It is **distribution for engineering reputation**.

In today's AI world, this is even more important.

Companies such as OpenAI, Anthropic, Google, Meta, DeepMind, NVIDIA, etc. publish papers, benchmarks, engineering posts, open-source software, and research.

Sometimes they are effectively saying:

> **"Look at the level of problems we are capable of solving."**

That's employer branding for extremely technical people.

---

### 4. There is also a "rising tide" effect

This is one of the deeper reasons.

Suppose Meituan develops some infrastructure technology and publishes it.

Other engineers copy the idea.

Now:

```text
Meituan
   ↓
industry adopts technique
   ↓
ecosystem gets better
   ↓
developers get better
   ↓
libraries/tools get better
   ↓
Meituan can hire from that ecosystem
```

Meituan itself wrote about this philosophy when discussing its early technical sharing: it acknowledged that its own engineering progress depended heavily on open-source projects, papers, books, and technical communities, and described external sharing as a way of giving back. ([Meituan Tech][4])

This is basically **compound knowledge creation**.

---

### 5. But they don't necessarily publish the most sensitive stuff

This is the important boundary.

A company can publish:

```text
"Here is our architecture."
```

without publishing:

```text
"Here is our exact production configuration,
our proprietary dataset,
our ranking weights,
our fraud-detection rules,
our business thresholds,
our secret supplier contracts,
our internal incident database,
our exact optimization tricks,
our unreleased product roadmap."
```

There is an enormous information space between:

**secret**

and

**public blog post**.

Good companies deliberately choose the layer that is safe to expose.

---

### 6. Some knowledge has surprisingly little value once isolated

This is another important economic point.

Suppose Meituan spent:

```text
3 years
100 engineers
$50M
```

building some infrastructure.

Then they publish a 30-minute technical article.

A competitor reads it.

Does the competitor suddenly obtain the same capability?

No.

The competitor still needs:

```text
engineers
implementation
integration
testing
production traffic
monitoring
operations
organizational coordination
years of iteration
```

The article might reduce their implementation time from:

```text
2 years → 1 year
```

That's real competitive leakage.

But Meituan may get:

```text
+ recruiting
+ reputation
+ ecosystem influence
+ open-source contributors
+ conference presence
+ industry relationships
+ employee retention
```

The economics can still favor publishing.

---

### 7. And sometimes publishing creates a standard

This is particularly powerful.

Suppose Company A builds an internal technology.

If everybody uses it internally:

```text
A's technology
    ↓
A only
```

But if A open-sources it:

```text
A
↓
open source
↓
10,000 developers
↓
100 companies
↓
ecosystem
↓
standard
```

Now Company A becomes one of the **center points of the ecosystem**.

That's why companies sometimes open-source things that are strategically important.

For example, Meituan has open-sourced engineering projects such as Logan and explicitly described building an ecosystem around it. ([Meituan Tech][5])

---

## The interesting lesson for you

This is actually very relevant to what you're doing with **AI/LLM/agent engineering content**.

You don't necessarily want:

> "Keep all knowledge secret until somebody pays me."

A stronger strategy can be:

```text
knowledge
   ↓
public content
   ↓
technical reputation
   ↓
people discover you
   ↓
trust
   ↓
consulting / implementation
   ↓
revenue
```

Your public content can explain:

```text
how to build an agent
how to deploy vLLM
how to train a small model
how to repair/test GPUs
how to build a coding CLI
how to optimize inference
```

But the **paid value** can be:

```text
"Come into my company and make this actually work."
```

That's the same fundamental distinction:

> **Knowledge is increasingly cheap. Execution is still valuable.**

And AI makes this even more interesting because LLMs are rapidly reducing the cost of reproducing *known* engineering patterns.

So the competitive moat moves upward:

```text
information
   ↓
implementation
   ↓
execution
   ↓
proprietary data
   ↓
distribution
   ↓
customer relationships
   ↓
organizational capability
   ↓
taste / speed / iteration
```

That is why **sharing more can sometimes make a strong company stronger rather than weaker**.

References:

* [Meituan Technology Blog](https://tech.meituan.com/?utm_source=chatgpt.com)
* [Meituan — 2025 Technology Annual Collection](https://tech.meituan.com/2026/02/02/2025-Spring-Festival-Present.html?utm_source=chatgpt.com)
* [Meituan — Technical Salon](https://tech.meituan.com/tech-salon.html?utm_source=chatgpt.com)
* [Meituan — 2018 Technical Sharing Summary](https://tech.meituan.com/2018/03/20/2018summary.html?utm_source=chatgpt.com)
* [Netflix Technology Blog](https://netflixtechblog.com/?utm_source=chatgpt.com)

[1]: https://tech.meituan.com/2026/02/02/2025-Spring-Festival-Present.html?utm_source=chatgpt.com "2025美团技术年货，「马」上到来 | 美团 · 技术团队"
[2]: https://tech.meituan.com/2020/03/26/Meituan-Tech-Corporate-Recruitment-new.html?utm_source=chatgpt.com "想进美团不知道选哪个技术岗位?这里有一份通关秘籍! | 美团 · 技术团队"
[3]: https://tech.meituan.com/tech-salon.html?utm_source=chatgpt.com "技术沙龙 | 美团 · 技术团队"
[4]: https://tech.meituan.com/2018/03/20/2018summary.html?utm_source=chatgpt.com "2018开春大礼：750页电子书 + 33场技术沙龙资料 + 17场线上课程分享 | 美团 · 技术团队"
[5]: https://tech.meituan.com/2018/10/11/logan-open-source.html?utm_source=chatgpt.com "Logan：美团开源移动端基础日志库 | 美团 · 技术团队"