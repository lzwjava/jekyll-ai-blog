---
audio: false
generated: true
image: false
lang: en
layout: post
title: Engineering Influence in Tech Companies
translated: false
type: note
---

Question: In large companies, should engineers have more influence, and should PMs understand engineering deeply to avoid bad technical decisions?

Answer:

Yes, in strong technology companies, **engineering usually has much more decision power than in traditional companies**, but not because "coders are above business." It is because many business decisions eventually become **system design decisions**, and bad technical decisions can create years of cost.

A good structure is usually:

```
Business / Users
        |
        v
Product strategy
        |
        v
Engineering design + implementation
        |
        v
System capability
        |
        v
Business outcomes
```

The mistake is treating engineering as only "people who write code." In reality, engineers often understand:

* feasibility
* architecture trade-offs
* operational cost
* scalability
* security
* maintenance burden
* developer productivity

For example:

Bad decision:

```
Team A: build iOS app
Team B: build Android app
Team C: later build web app
```

Three codebases:

```
iOS       Swift
Android   Kotlin
Web       React
```

Same business logic:

```
login
payment
user profile
notifications
```

duplicated 3 times.

A technically strong team might propose:

```
Flutter / React Native / Kotlin Multiplatform
             |
             v
     shared business logic
             |
     -----------------
     |       |       |
    iOS   Android   Web
```

The decision is not "engineers want fancy technology." It is a business decision:

* faster iteration
* lower cost
* fewer bugs
* smaller team

However, using cross-platform technology blindly is also a mistake. For example, a high-performance camera app, game engine, or deeply native UX may require native development.

The key is **technical judgment**.

---

A strong PM does not necessarily need to be a senior engineer, but a good PM in a technical company should understand:

* APIs
* databases
* distributed systems basics
* mobile/web architecture
* AI model capabilities
* engineering trade-offs

The best product leaders often have engineering backgrounds.

Examples:

* Kevin Scott has a computer science and engineering background.
* Linus Torvalds is an extreme example of engineering-driven product creation.
* Many successful founders are technical because they can directly connect user problems with implementation possibilities.

---

But there is another failure mode:

```
Engineer thinks:
"I built a technically beautiful system."

User thinks:
"I don't need this."

Business dies.
```

A technically excellent architecture with no market value is also waste.

The strongest companies combine:

```
Excellent product sense
        +
Excellent engineering judgment
        +
Fast execution
```

The ideal relationship:

PM:

> "What problem should we solve? Why does it matter?"

Engineer:

> "What is the best way to solve it? What are the trade-offs?"

Both sides influence each other.

---

Large companies often become inefficient when:

```
Business says:
"Just build this."

Engineering says:
"We don't know why, but okay."
```

or:

```
Engineering says:
"We will build the perfect system."

Business says:
"Nobody wants this."
```

High-performing companies avoid both extremes.

A mature technology company usually gives engineers **technical authority** and PMs **product authority**. Neither side dominates; decisions are made by the people with the deepest understanding of that dimension.
