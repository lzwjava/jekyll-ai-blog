---
audio: false
generated: true
image: false
lang: en
layout: post
title: Investigate Before Migrating
translated: false
type: note
---

Question: When doing frontend/backend upgrades or large refactors, should we investigate deeply before committing because reversing later is expensive?

Answer:

Yes. Large technical changes have **high reversibility cost**, so the optimal strategy is usually:

**Explore broadly → validate assumptions → commit gradually → migrate incrementally.**

The reason is that software refactors are often **path-dependent**. Once many decisions depend on an early choice, changing direction becomes expensive.

Example:

```
Old system
    |
    | investigate
    v
Architecture decision
    |
    | build months
    v
New system
    |
    | discover wrong assumption
    v
Rollback?
```

The rollback cost is not only code:

* engineers' time already spent
* new APIs already adopted
* database schema changes
* deployment pipelines changed
* monitoring/logging changed
* team knowledge shifted
* users already affected

A simple frontend example:

You decide:

```
React + Redux
```

then after 3 months discover:

```
Actually the app is mostly server-state.
React Query + simpler state management would fit better.
```

You cannot just "replace Redux". You have hundreds of components depending on it.

Backend example:

You migrate:

```
Monolith
   |
   v
Microservices
```

but later discover:

* network latency increased
* debugging became harder
* team is too small
* deployment complexity exploded

Going back is difficult because the organization has already adapted.

---

A good engineering pattern is:

### 1. Do a "spike" first

Before committing:

```
1-2 weeks prototype

Questions:
- Can we migrate?
- What are hidden problems?
- Performance?
- Developer experience?
- Operational cost?
```

Throwaway code is cheap.

Production migration is expensive.

---

### 2. Prefer reversible decisions

Good:

```
Add new API
keep old API
migrate clients gradually
remove old API later
```

Bad:

```
Delete old system
rewrite everything
hope new system works
```

The first is like:

```
old ---> new

```

The second is:

```
old
 |
 X
 |
new
```

The second creates a cliff.

---

### 3. Separate "migration" from "innovation"

Many failures mix two things:

Bad:

```
Rewrite backend
+
change database
+
change business logic
+
change frontend framework
+
change deployment
```

Too many variables.

Better:

```
Phase 1:
same behavior, new architecture

Phase 2:
optimize

Phase 3:
new features
```

---

### 4. But don't over-investigate forever

There is also a cost to analysis paralysis.

A useful heuristic:

| Change                   | Investigation            |
| ------------------------ | ------------------------ |
| CSS library              | hours                    |
| frontend framework       | days/weeks               |
| database migration       | weeks                    |
| distributed architecture | months                   |
| ML infrastructure        | experiments + benchmarks |

The bigger the blast radius, the more upfront thinking pays.

---

A mature engineering team thinks like this:

```
Small change:
  code first, adjust later

Large change:
  think first, experiment, then code
```

The best engineers are not the ones who write the most code. They are the ones who avoid writing **the wrong code at scale**.

For AI systems this is even more important now. For example, choosing:

* vLLM vs custom inference engine
* RAG vs fine-tuning
* vector DB architecture
* agent framework

can create months of technical debt if chosen only because of hype. Small benchmarks and prototypes before committing save enormous time.
