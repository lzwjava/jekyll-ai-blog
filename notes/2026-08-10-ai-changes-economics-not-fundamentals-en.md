---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Changes Economics, Not Fundamentals
translated: false
type: note
---

Question: Is using AI to one-shot rewrite an old Java/web system into newer frameworks the right approach?

Answer:

AI makes large-scale migration much cheaper, but the software engineering principle still applies: **reduce uncertainty before increasing change size**.

A legacy system upgrade is usually not just a code translation problem. The hard parts are:

* hidden business rules
* undocumented dependencies
* production behavior
* data migration
* performance characteristics
* integrations
* operational assumptions

AI is very good at:

* Java version upgrades
* Spring/Spring Boot migration suggestions
* converting old frontend code to Vue 3
* generating tests
* explaining unfamiliar modules
* refactoring repetitive code

But AI does not automatically know:

* "this ugly code exists because a bank API breaks if called twice"
* "this field looks unused but is used by a nightly job"
* "this transaction order is required by accounting"

So the better pattern is usually:

```
Old System
    |
    | 1. map architecture
    v
Documentation + dependency graph
    |
    | 2. add safety net
    v
Tests / monitoring / logs
    |
    | 3. migrate incrementally
    v
New System
```

A practical AI-assisted migration workflow:

### 1. First, let AI read, not rewrite

Example:

```
Find all modules.
Explain dependencies.
Identify risky areas.
Generate migration plan.
```

Create:

```
docs/
  architecture.md
  api-map.md
  database-map.md
  migration-plan.md
```

### 2. Pick a small vertical slice

Not:

```
1000 files -> rewrite everything
```

Instead:

```
user login module
        |
        v
new Spring Boot
        |
        v
production traffic
```

Then:

```
order module
payment module
report module
```

### 3. Keep old and new running together

Typical patterns:

```
              nginx
                |
        +-------+-------+
        |               |
    old service     new service
```

or:

```
old API
   |
adapter layer
   |
new service
```

### 4. Use AI as many junior engineers, not as the architect

A good prompt:

```
You are helping migrate a Spring MVC application to Spring Boot 3.

Before changing code:
1. analyze dependencies
2. list risks
3. propose migration steps
4. wait for approval

Do not rewrite blindly.
```

Bad prompt:

```
rewrite this whole repository into Spring Boot 3 + Vue3
```

The second one may produce a beautiful project that does not run.

---

The interesting thing is: **AI changes the economics, not the fundamentals.**

Before AI:

```
migration cost:
10 engineers * 6 months
```

After AI:

```
2 engineers + AI * 2 months
```

But the "understand first, change second" rule remains.

The biggest mistake in software is not writing bad code. It is making a large irreversible change before knowing what you don't know.

For your situation (old Java + old web framework + Vue 3), I would do:

```
Week 1:
AI scans repo
generate architecture docs
identify modules

Week 2:
upgrade build system
upgrade Java version
make tests pass

Week 3:
migrate frontend page by page

Week 4+:
replace backend modules gradually
```

A thousand-file migration can work, but only if the first thousand-file change is generated **after** you already understand the system. Otherwise you are effectively paying AI to accelerate a gamble.
