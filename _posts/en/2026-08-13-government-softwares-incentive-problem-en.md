---
audio: false
generated: true
image: false
lang: en
layout: post
title: Government Software's Incentive Problem
translated: false
type: note
---

Question: Is it true that government software projects in China often become bureaucratic, slow, legacy-heavy, and lack ownership?

Answer:

Yes, many large government IT projects (not only in China, but globally) have these characteristics. However, it is better understood as a **system incentive problem** rather than simply "people are bad" or "government cannot build software."

Typical patterns:

### 1. Many stakeholders → slow decisions

A government project usually has many parties:

```
Central / local government department
        |
        +-- project owner
        |
        +-- procurement department
        |
        +-- IT department
        |
        +-- security department
        |
        +-- finance department
        |
        +-- external vendor
        |
        +-- users in different offices
```

Each group has different goals:

* Finance cares about budget compliance.
* Security cares about risk.
* Leaders care about political/administrative outcomes.
* Users care about convenience.
* Vendors care about contract delivery.

The result:

```
decision speed ↓
coordination cost ↑
innovation incentive ↓
```

A startup can decide in one meeting. A large public project may need months because nobody wants to take responsibility for a wrong decision.

---

### 2. Procurement model encourages "deliver project", not "maintain product"

Many government software projects are purchased as:

```
Requirement document
        ↓
Tender
        ↓
Vendor wins contract
        ↓
Development
        ↓
Acceptance testing
        ↓
Payment
        ↓
Project ends
```

The problem:

The vendor's economic incentive is often:

```
maximize contract revenue
```

not:

```
maximize software quality over 10 years
```

After acceptance:

* original developers leave
* vendor team changes
* documentation becomes outdated
* nobody deeply understands the system

---

### 3. Legacy software accumulates

A system built in 2012:

```
Java 6
Spring old version
Oracle database
WebSphere middleware
old Linux
old frontend framework
```

Ten years later:

```
business depends on it
nobody dares rewrite
original engineers gone
new engineers afraid to touch
```

This creates the classic:

> "Nobody knows why this code works, but nobody can delete it."

---

### 4. Maintenance is less visible than new projects

A new system:

```
new platform launch
new features
leadership attention
budget approval
```

Maintenance:

```
upgrade dependency
fix security issue
clean database
refactor code
```

Maintenance prevents disasters but gets little recognition.

So organizations often optimize for:

```
build something new > maintain something existing
```

---

### 5. Lack of "ownership"

Good software usually has:

```
one strong owner
clear responsibility
fast feedback loop
continuous iteration
```

Example:

A startup:

```
User complains
    ↓
Engineer sees problem
    ↓
Fix tomorrow
    ↓
Measure result
```

Large government systems:

```
User complains
    ↓
report
    ↓
department meeting
    ↓
vendor communication
    ↓
budget discussion
    ↓
change request
    ↓
next year's plan
```

The feedback loop is much slower.

---

But there are exceptions.

Some government IT systems are very strong:

* high-speed payment systems
* tax systems
* public security systems
* large-scale infrastructure platforms

These usually succeed because they have:

* strong technical leadership
* clear ownership
* long-term funding
* high operational requirements

The core difference is similar to the difference between **a product company and a contractor company**:

```
Product mindset:
"Users depend on this every day. Improve continuously."

Project mindset:
"Complete requirements. Pass acceptance. Move on."
```

So your observation is pointing at a real organizational pattern: when software is treated as a one-time construction project instead of a living product, bureaucracy, legacy, and lack of initiative naturally emerge.