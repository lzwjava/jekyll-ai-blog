---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Engineering Pod Service Plan
translated: false
type: note
---

Question: **Build me the concrete 2026 plan for an AI-native software outsourcing company: positioning, customers, pricing, delivery system, agent stack, unit economics, and path from $0 → $1M/year.**

Answer: **I would build this as a high-end “AI engineering team as a service,” not an outsourcing marketplace.**

The market signal is strong enough to justify testing now: McKinsey's 2026 survey reports ~20% of organizations are already scaling software coding agents, and 32% say agentic coding caused them to build something internally rather than buy software. ([McKinsey & Company][1]) OpenAI's current Codex stack explicitly supports long-running agents, subagents, code execution, repositories, and background work; OpenAI also describes its own agent-first engineering workflow as humans steering while agents execute. ([OpenAI][2])

The business I would build is:

```text
                  AI ENGINEERING CO.
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   New software     AI integration    Legacy rewrite
        │                │                │
        └────────────────┼────────────────┘
                         │
                Senior human engineer
                         +
                autonomous agents
                         │
                         ▼
                  shipped software
```

---

# 1. Start with one extremely specific customer

Don't start with:

> "We build software for everyone."

That creates an agency with an infinite sales surface.

I'd start with:

> **US startups and SMBs that need software but don't want to hire a 5–10 person engineering team.**

Ideal customer:

```text
Revenue:        $1M–$50M
Employees:     10–200
Engineering:   0–5 engineers
Problem:       software is blocking growth
Budget:        $10k–$40k/month
Decision maker: founder / CTO / COO
```

Examples:

```text
"Build our customer portal."

"Automate our operations."

"Replace this spreadsheet workflow."

"Integrate Salesforce + Stripe + our internal database."

"Build an AI support system."

"Modernize our old Rails application."

"Build the MVP for our new product."
```

You don't need to convince them that AI is valuable.

They already have a software problem.

**You sell the solution.**

---

# 2. Your first product

I would literally package this:

## AI Engineering Pod

```text
$15,000/month
```

Customer gets:

```text
1 senior engineer
+
AI engineering agents
+
QA agents
+
DevOps automation
+
architecture
+
deployment
+
maintenance
```

Don't expose the agent complexity to the customer.

From their perspective:

```text
Monday
  ↓
"Here are the requirements."

Tuesday
  ↓
"We have a working PR."

Wednesday
  ↓
"QA passed."

Thursday
  ↓
"Deployed to staging."

Friday
  ↓
"Production."
```

That's the product.

---

# 3. Three pricing tiers

I'd start with this:

| Product             |           Price | Use case                         |
| ------------------- | --------------: | -------------------------------- |
| **Build Sprint**    | $10k–$25k fixed | Specific project                 |
| **Engineering Pod** |    $15k–$30k/mo | Continuous development           |
| **Dedicated Pod**   |    $30k–$50k/mo | Larger company / critical system |

Don't sell hourly rates.

Never say:

```text
$150/hour
```

because then the customer starts calculating:

```text
"Why don't I just hire someone?"
```

Instead:

```text
$20k/month
→ continuous engineering capacity
→ predictable delivery
→ no recruiting
→ no engineering management overhead
```

You are selling **capacity + accountability**.

---

# 4. Your first $100k

Don't think about $1M yet.

Your first milestone:

```text
3 customers × $15k/month
=
$45k MRR

6 customers × $15k
=
$90k MRR
```

That's already:

```text
$1.08M ARR
```

You don't need 100 customers.

You need **6–10 good customers**.

That is the beautiful part of this model.

---

# 5. The delivery architecture

Here's where I think you can have a real advantage.

Don't run:

```text
customer
  ↓
human developer
  ↓
ChatGPT
```

Build an internal **agentic engineering OS**.

```text
                         CUSTOMER
                            │
                            ▼
                     REQUIREMENT AGENT
                            │
                            ▼
                     ARCHITECT AGENT
                            │
                            ▼
                    TASK DECOMPOSITION
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
        CODE AGENT      CODE AGENT     RESEARCH AGENT
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                       TEST AGENT
                            │
                            ▼
                       REVIEW AGENT
                            │
                            ▼
                     SECURITY AGENT
                            │
                            ▼
                     HUMAN ENGINEER
                            │
                            ▼
                          MERGE
                            │
                            ▼
                        DEPLOY
```

This is where your technical background matters.

---

# 6. Don't build the orchestrator first

This is important.

**Do not spend six months building an "AI software factory."**

Use existing agents initially.

OpenAI's current Codex platform already supports multi-agent workflows, skills, background tasks and long-running execution. ([OpenAI][3])

Your first version can literally be:

```text
GitHub
Linear
Codex / Claude Code
Postgres
Docker
GitHub Actions
Sentry
Vercel / AWS
Slack
```

Then create your own thin layer around them.

For example:

```text
customer repo
     ↓
/agent
     ├── architect
     ├── implement
     ├── test
     ├── review
     └── deploy
```

You discover the bottlenecks **from real customers**.

Only automate what hurts.

---

# 7. Your internal repo template

This is much more important than it sounds.

Every customer project should start from your standard environment.

Something like:

```text
customer-project/
├── AGENTS.md
├── README.md
├── docs/
│   ├── architecture.md
│   ├── product.md
│   ├── decisions/
│   └── api.md
├── src/
├── tests/
├── scripts/
├── infra/
├── .github/
│   └── workflows/
└── observability/
```

`AGENTS.md` becomes extremely valuable.

Example:

```md
# Engineering Rules

## Stack

- TypeScript
- Next.js
- PostgreSQL
- Drizzle
- Vitest
- Playwright

## Rules

- Every feature requires tests.
- Never modify production data directly.
- All database migrations must be reversible.
- Every API endpoint requires validation.
- Never introduce a dependency without justification.
- Run `npm test` before committing.
- Run Playwright for user-facing changes.

## Architecture

...

## Product requirements

...
```

The agent now has a **company operating system**.

OpenAI's own harness-engineering work makes essentially this point: as coding agents become capable of writing huge amounts of code, the engineering bottleneck shifts toward specifications, repository structure, tests, documentation, and feedback loops. ([OpenAI][4])

---

# 8. Your real moat

Not:

```text
GPT
Claude
Codex
Gemini
```

Those are commodities.

Your moat becomes:

```text
                  YOUR DATA
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
  requirements   architectures   bugs
        │            │            │
        └────────────┼────────────┘
                     ▼
              engineering playbook
                     │
                     ▼
                 agents
                     │
                     ▼
              better delivery
                     │
                     ▼
              more customers
                     │
                     ▼
              more knowledge
```

Over 50 projects, you'll know:

```text
how to build SaaS
how to integrate Stripe
how to migrate Rails
how to build RAG
how to deploy AWS
how to implement auth
how to build admin panels
how to instrument observability
how to test browser workflows
```

Your agents encode that knowledge.

That's the compounding loop.

---

# 9. Your first vertical

I'd actually go narrower than "SMB."

For example:

### Option A — AI-native startups

```text
Founder has idea
        ↓
You build MVP
        ↓
$20k–$40k
        ↓
monthly engineering retainer
```

Very easy to demonstrate.

But churn can be high.

### Option B — established SMBs

```text
$5M revenue company
        ↓
30 employees
        ↓
terrible internal software
        ↓
$20k/month
        ↓
you become their engineering department
```

This is probably the model I'd test first.

### Option C — legacy modernization

```text
old Rails/.NET/Java
        ↓
AI-assisted analysis
        ↓
tests
        ↓
incremental migration
        ↓
modern stack
```

This can support larger contracts, but requires more trust and domain expertise.

---

# 10. The sales pitch

Don't say:

> "We use AI to build software 10x faster."

That invites skepticism.

Say:

> **"We act as your engineering team. You give us the roadmap; we design, build, deploy and maintain the software."**

Then:

> "Instead of hiring five engineers, you get a senior engineering lead backed by an AI-native delivery system."

That's concrete.

---

# 11. Your sales funnel

Keep it brutally simple.

```text
Outbound
   │
   ▼
30-minute technical discovery
   │
   ▼
Free architecture / automation audit
   │
   ▼
$10k–$20k pilot
   │
   ▼
Successful delivery
   │
   ▼
$15k–$30k/month retainer
```

The pilot is important.

Don't ask someone to trust you with a $300k system immediately.

Give them:

```text
2–4 weeks
one meaningful project
fixed price
production deployment
```

Then expand.

---

# 12. Example customer

Imagine:

```text
Company:
B2B logistics company

Employees:
80

Engineering:
2 developers

Problem:
Operations use 17 spreadsheets.

Request:
"Build an internal operations platform."
```

Traditional agency:

```text
PM
designer
architect
4 engineers
QA
DevOps

6 months
$300k+
```

Your company:

```text
1 senior engineer
+
agent swarm

6–10 weeks
$50k initial build

then:

$15k/month
maintenance + new features
```

Internally:

```text
Day 1
architecture

Day 2
DB schema

Day 3
CRUD

Day 4
auth

Day 5
first UI

...
```

Agents work overnight.

Human reviews in the morning.

McKinsey's 2026 research describes this emerging model as near-continuous software delivery and cites organizations reporting 3–5× productivity improvements alongside substantial reductions in team size. Those are reported outcomes, not guarantees for a new company, but they illustrate why the delivery model is worth testing. ([McKinsey & Company][5])

---

# 13. Unit economics

Let's model a $20k/month customer.

```text
Revenue                         $20,000

Human engineering               $5,000
AI inference                    $1,500
Cloud/tools                     $1,000
PM/customer success             $1,500
───────────────────────────────────────
Gross contribution             $11,000
```

That's:

```text
55% contribution margin
```

With optimization:

```text
Revenue                         $20,000

Human                         $3,500
AI                              $800
infra/tools                     $700
CS                              $800
────────────────────────────────
Contribution                  $14,200
```

71%.

**Don't assume you'll get these margins.**

Measure them.

Your first 10 projects are essentially an experiment to discover:

```text
human hours / $ revenue
tokens / $ revenue
bugs / project
rework %
gross margin
time to production
```

Those are the numbers that tell you whether the business actually works.

---

# 14. The $1M/year target

I would set this progression:

```text
MONTH 1–2
────────────────────────
1 pilot
$10k–20k revenue


MONTH 3–4
────────────────────────
2–3 customers
$30k–45k MRR


MONTH 5–8
────────────────────────
4–6 customers
$60k–100k MRR


MONTH 9–12
────────────────────────
6–10 customers
$100k–150k MRR
```

You don't actually need $150k MRR.

At:

```text
$85k MRR
```

you're already at:

```text
$1.02M ARR
```

The objective is therefore:

> **Get 6 customers paying ~$14k/month.**

Not:

> Get 100 customers.

---

# 15. Hiring strategy

I'd resist hiring developers for as long as possible.

First:

```text
YOU
+
AI
```

Then:

```text
YOU
+
Senior Engineer #2
+
AI
```

Then:

```text
2 senior engineers
+
1 customer/product person
+
AI
```

Only add engineers when the bottleneck is genuinely human engineering capacity.

The ideal organization might eventually look like:

```text
             Founder
                │
       ┌────────┴────────┐
       │                 │
   Sales/Product      Engineering
                         │
              ┌──────────┼──────────┐
              │          │          │
           Engineer   Engineer   Engineer
              │          │          │
             agents     agents     agents
```

Not:

```text
Founder
  ↓
20 junior developers
```

---

# 16. Security becomes a product feature

This is where enterprise customers will challenge you.

Agents can:

```text
read code
execute commands
modify files
access APIs
deploy infrastructure
```

So you need hard boundaries.

OpenAI's own guidance for running coding agents emphasizes access control, approval gates, telemetry, and explicit boundaries for higher-risk actions. ([OpenAI][6])

Your standard environment should therefore have:

```text
sandbox
   ↓
least privilege
   ↓
temporary credentials
   ↓
no production credentials by default
   ↓
PR required
   ↓
CI required
   ↓
human approval
   ↓
production
```

Never allow:

```text
agent → production → arbitrary shell
```

by default.

---

# 17. Build your own "factory" only after ~10 customers

At first:

```text
Codex
Claude Code
GitHub
Linear
Docker
CI
```

At customer #10, you'll notice repeated work.

Then build:

```text
             COMPANY PLATFORM
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
   project       agent         quality
   setup        orchestration   control
       │            │            │
       ▼            ▼            ▼
   templates     task queue     evals
```

One particularly interesting direction is the orchestration layer. OpenAI's Symphony project describes turning a project-management system into a control plane where every task can get an agent, agents work continuously, and humans review the results. ([OpenAI][7])

That's very close to the internal infrastructure I'd eventually build.

---

# 18. Your 30-day execution plan

If you actually want to do this, I'd make the first month brutally concrete.

### Week 1

Build:

```text
landing page
+
one-page offer
+
standard repo template
+
agent instructions
+
deployment template
```

Your landing page only needs:

```text
AI Engineering Team

We design, build and operate
custom software for growing companies.

• Fixed-price projects
• Monthly engineering pods
• AI-native development
• Production deployment
• Ongoing maintenance

Book a technical assessment.
```

---

### Week 2

Build 2–3 impressive demos.

Not toy demos.

Build things a business would actually pay for:

```text
1. CRM / operations platform

2. AI document processing workflow

3. Internal analytics / admin platform
```

Put the code on GitHub.

Deploy them.

Record 2-minute demos.

---

### Week 3

Start outbound.

Target:

```text
100 companies
```

Not random companies.

Search for companies saying:

```text
"we're hiring software engineers"

"need internal platform"

"manual process"

"spreadsheet"

"legacy system"

"AI automation"

"looking for CTO"
```

The pitch:

```text
Hey X,

I noticed you're hiring for [engineering problem].

We're experimenting with an AI-native engineering model:
one senior engineer + autonomous coding/QA agents.

Instead of adding 3–5 engineers,
we can take ownership of [specific project].

I'd be happy to do a free technical assessment
of [their system/problem].

— Zhiwei
```

---

### Week 4

Close **one customer**.

Don't optimize the website.

Don't build a SaaS platform.

Don't hire ten people.

Don't spend six months building an orchestration framework.

Just:

```text
SELL
 ↓
BUILD
 ↓
SHIP
 ↓
MEASURE
 ↓
REPEAT
```

---

# 19. Your first internal dashboard

I'd track this from day one:

```text
CUSTOMER
────────────────────────
MRR
project revenue
human hours
AI cost
cloud cost
gross margin


ENGINEERING
────────────────────────
PRs/week
agent tasks/week
agent success rate
test pass rate
bugs/week
rework %
deployments/week


DELIVERY
────────────────────────
lead → contract
contract → first PR
contract → production
production incidents
customer satisfaction
```

And one metric above everything:

```text
                 CUSTOMER VALUE
AI leverage = ─────────────────────
               HUMAN ENGINEERING
```

You want this number increasing every month.

---

# 20. The strategic endgame

There are actually **three businesses** hiding inside this.

### Phase 1 — Service

```text
customer
  ↓
you + agents
  ↓
software
```

Cash flow.

Learn the problems.

---

### Phase 2 — Internal platform

```text
customer
  ↓
your engineering factory
  ↓
agents
  ↓
software
```

Higher margins.

More repeatability.

---

### Phase 3 — Product

Eventually you may discover:

```text
"We've built the same system
for 30 logistics companies."
```

Then:

```text
service
   ↓
repeatable workflow
   ↓
vertical SaaS
```

Now you have:

```text
services revenue
+
software revenue
```

That's where this gets really interesting.

---

## What I would do in your position

Given your existing experience building products, training models, and building CLI/agent systems, **I would not start by creating a conventional outsourcing company at all.**

I'd create:

> **An AI-native engineering company whose unit of production is one senior engineer + an agent swarm.**

Start with:

```text
                    YOU
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
      Codex       Claude        custom
                   Code         agents
        │            │            │
        └────────────┼────────────┘
                     ▼
              YOUR HARNESS
                     │
                     ▼
               CUSTOMER CODE
                     │
                     ▼
                PRODUCTION
```

**First target: 3 customers × $15k/month.**

Once you can reliably deliver that, push toward:

```text
6 customers
×
$15k/mo
=
$90k MRR
=
$1.08M ARR
```

The biggest question isn't whether AI can write enough code. The 2026 evidence strongly suggests it can. The question is whether **you can turn agent capability into a reliable, repeatable customer-delivery machine**. That is the company worth building. ([Gartner][8])

### References

* [McKinsey — The State of AI 2026](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai?os=av.&utm_source=chatgpt.com)
* [McKinsey — Rewiring software delivery for the agentic era](https://www.mckinsey.com/capabilities/mckinsey-technology/our-insights/rewiring-software-delivery-for-the-agentic-era?utm_source=chatgpt.com)
* [OpenAI — Introducing the Agents API](https://openai.com/index/introducing-the-agents-api/?utm_source=chatgpt.com)
* [OpenAI — Harness engineering](https://openai.com/index/harness-engineering/?utm_source=chatgpt.com)
* [OpenAI — Codex for software engineering teams](https://openai.com/business/solutions/engineering/?utm_source=chatgpt.com)
* [Gartner — Enterprise AI coding agents in 2026](https://www.gartner.com/en/newsroom/press-releases/2026-05-20-gartner-says-the-market-for-enterprise-ai-coding-agents-is-entering-a-new-phase-of-expansion-and-competitive-realignment?utm_source=chatgpt.com)

[1]: https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai?os=av.&utm_source=chatgpt.com "The State of AI: Global Survey 2026 | McKinsey"
[2]: https://openai.com/index/introducing-the-agents-api/?utm_source=chatgpt.com "Introducing the Agents API | OpenAI"
[3]: https://openai.com/index/introducing-the-codex-app/?utm_source=chatgpt.com "Introducing the Codex app | OpenAI"
[4]: https://openai.com/index/harness-engineering/?utm_source=chatgpt.com "Harness engineering: leveraging Codex in an agent-first world | OpenAI"
[5]: https://www.mckinsey.com/capabilities/mckinsey-technology/our-insights/rewiring-software-delivery-for-the-agentic-era?utm_source=chatgpt.com "Rewiring software delivery for the agentic era | McKinsey"
[6]: https://openai.com/index/running-codex-safely/?utm_source=chatgpt.com "Running Codex safely at OpenAI | OpenAI"
[7]: https://openai.com/index/open-source-codex-orchestration-symphony/?utm_source=chatgpt.com "An open-source spec for Codex orchestration: Symphony. | OpenAI"
[8]: https://www.gartner.com/en/newsroom/press-releases/2026-05-20-gartner-says-the-market-for-enterprise-ai-coding-agents-is-entering-a-new-phase-of-expansion-and-competitive-realignment?utm_source=chatgpt.com "Gartner Says the Market for Enterprise AI Coding Agents Is Entering a New Phase of Expansion and Competitive Realignment"
