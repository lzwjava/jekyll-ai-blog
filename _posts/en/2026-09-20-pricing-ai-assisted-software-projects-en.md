---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pricing AI-Assisted Software Projects
translated: false
type: note
---

Question: How should you negotiate software projects and estimate cost accurately now that AI/vibe coding makes LOC and commits poor measures? Should you measure tokens instead?

Answer:

**Don’t price AI-assisted software by LOC, commits, or tokens.** Those measure *activity*, not *delivered value*.

The fundamental unit should be:

> **Cost = engineering effort × risk × required quality + infrastructure/third-party costs**

AI changes the production function: one engineer can generate 10× more code. So the old `LOC → man-hours → price` model breaks.

### 1. Why LOC / commits / tokens are bad

| Metric              | Why it fails                                          |
| ------------------- | ----------------------------------------------------- |
| LOC                 | AI can generate 10,000 useless lines in seconds       |
| Commits             | One commit can be 10 lines or 10k lines               |
| Tokens generated    | Depends heavily on model, verbosity, retries, context |
| Tokens consumed     | Measures AI usage, not business value                 |
| Hours               | Better, but still doesn't capture project risk        |
| Features delivered  | Much better                                           |
| Acceptance criteria | **Best foundation for fixed-price projects**          |

For example:

```text
Traditional developer:
  500 LOC/day

AI-assisted developer:
  5,000 LOC/day

```

If you price by LOC, you have accidentally created an incentive to produce more code.

Instead:

```text
Client wants:
  API
  dashboard
  authentication
  payment
  deployment
  monitoring

You price the finished system.
```

---

## 2. Use a deliverable-based estimation model

Before giving a price, decompose the project:

```text
Project
├── Requirements
├── Architecture
├── Backend
├── Frontend
├── AI/LLM
├── Database
├── Integration
├── Deployment
├── Testing
└── Maintenance
```

Then turn each into **acceptance criteria**.

Example:

```text
Authentication

[ ] Email/password login
[ ] Password reset
[ ] JWT/session management
[ ] Rate limiting
[ ] Admin/user roles
[ ] 20 automated tests
[ ] Production deployment
```

Now the negotiation becomes:

> "When these criteria are satisfied, this milestone is complete."

That's much harder to argue about than:

> "I wrote 30,000 lines."

---

# 3. Estimate effort internally, but sell outcomes externally

I would maintain an internal calculation like:

```python
estimate = {
    "requirements": 2,
    "architecture": 2,
    "backend": 5,
    "frontend": 4,
    "integration": 3,
    "testing": 3,
    "deployment": 2,
}

hours = sum(estimate.values()) * 8
```

Suppose:

```text
26 engineer-days
```

Then account for uncertainty:

```text
26 × 1.3 = 34 engineer-days
```

If your internal target rate is:

```text
¥4,000/day
```

then:

```text
34 × ¥4,000 = ¥136,000
```

You might quote:

```text
Project: ¥150,000
```

The client doesn't need to see:

```text
backend = 5 days
frontend = 4 days
...
```

unless you want to negotiate scope.

---

# 4. AI makes your margin much more important

This is where AI coding becomes extremely interesting for your business.

Suppose historically:

```text
Client price:       ¥150k
Human engineering:  30 days
Cost:               ¥90k
Gross profit:       ¥60k
```

With strong AI tooling:

```text
Client price:       ¥150k

Your actual:
  human work:       12 days
  API/model cost:   ¥3k
  infra:             ¥2k

total cost ≈        ¥41k
gross profit ≈      ¥109k
```

**You should not automatically reduce the price to ¥60k.**

The client is buying:

> a working system with accountability

not:

> 30 days of typing.

This is the same reason a highly productive surgeon doesn't necessarily charge less because the operation takes less time.

---

# 5. Where tokens *are* useful

Tokens are useful for **your internal AI cost accounting**, especially if you're building an AI-native software company.

Track:

```text
project
├── input tokens
├── output tokens
├── model/API cost
├── tool calls
├── agent runtime
├── human intervention
├── iterations
└── infrastructure
```

For example:

```text
Project A

Claude/Codex/etc:
    input:   80M tokens
    output:  12M tokens
    API cost: $420

Agent execution:
    1,800 tool calls

Human:
    38 hours

Infrastructure:
    $90
```

This gives you a very useful metric:

```text
AI cost / project
AI cost / accepted feature
AI cost / engineering hour
```

But **don't tell the customer**:

> "This project consumed 80M tokens, therefore it costs ¥X."

That's analogous to a construction company charging according to the number of keystrokes its workers made.

---

# 6. The metric I'd actually build for your company

Since you're doing AI consulting/agent development, I'd track **four layers**:

```text
                    CLIENT
                       │
                 Business outcome
                       │
                 Acceptance criteria
                       │
               Engineering production
                       │
        ┌──────────────┴──────────────┐
        │                             │
     Human work                  AI production
        │                             │
     hours                         tokens
     decisions                    tool calls
     reviews                      model cost
        │                             │
        └──────────────┬──────────────┘
                       │
                 Actual COGS
```

Your financial model becomes:

```text
Revenue
  ↓
Project price
  ↓
- human labor
- model/API cost
- cloud/GPU
- software
- subcontractors
  ↓
Gross profit
```

And your productivity model becomes:

```text
Delivered value
-------------------------
Human hours + AI cost
```

That is far more meaningful than LOC/hour.

---

# 7. For fixed-price projects, negotiate scope—not hours

This is probably the most important part.

Bad:

> "I'll develop this for 30 engineer-days."

Better:

> "¥150k includes A, B, C and production deployment. Anything outside these acceptance criteria is a change request."

Then define:

```text
Milestone 1 — ¥30k
Requirements + architecture

Milestone 2 — ¥50k
Core application

Milestone 3 — ¥40k
AI/integration

Milestone 4 — ¥30k
Production + acceptance
```

And explicitly define exclusions:

```text
Not included:
- new third-party integrations
- major UI redesign
- new business workflows
- >N concurrent users
- additional languages
- new AI models
```

This prevents **scope creep**, which is usually much more dangerous than whether your original estimate was off by 20%.

---

# 8. When hourly/day-rate pricing is better

Use time-based billing when the uncertainty is high:

```text
"Build me an AI agent that automates our workflow."
```

You don't yet know:

* API limitations
* data quality
* model performance
* integration complexity
* customer's actual workflow
* security requirements

Then sell a **discovery/prototype phase** first:

```text
Phase 0
¥20k–50k

1–2 weeks

Deliver:
  architecture
  prototype
  benchmark
  technical risks
  detailed implementation estimate
```

Then:

```text
Discovery
   ↓
known requirements
   ↓
fixed-price implementation
   ↓
maintenance
```

This is particularly powerful for AI projects because uncertainty is often concentrated in the **first experiment**.

---

## My recommended pricing system for an AI-native consultancy

I'd use:

```text
              DISCOVERY
                  │
             fixed price
                  ↓
          PROTOTYPE / POC
                  │
          fixed price
                  ↓
       PRODUCTION PROJECT
                  │
          milestone pricing
                  ↓
            MAINTENANCE
                  │
          monthly / retainer
```

Internally, collect **hours + tokens + tool calls + infrastructure + defects + rework**.

Externally, sell **scope + acceptance criteria + business outcome + SLA**.

So the key distinction is:

```text
Measurement of COST:
    human hours
    model tokens/$
    infrastructure
    rework

Measurement of VALUE:
    accepted features
    business outcome
    reliability
    performance
    SLA

Measurement of SCOPE:
    acceptance criteria
```

**Tokens are therefore useful, but as a COGS metric—not a pricing unit.**

For your specific AI consulting business, I can also build a concrete **`project_estimator.py`** that takes requirements, risk, human hours, model tokens, GPU/API costs, and target margin and outputs a quote + milestone schedule.
