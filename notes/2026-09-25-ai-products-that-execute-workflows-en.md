---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Products That Execute Workflows
translated: false
type: note
---

Question: **What AI products can we realistically build today, in September 2026?**

Answer:

The big shift is that **AI products can now execute**, not just generate. Agents can use browsers/desktops, terminals, files, APIs, memory, and other agents; coding-agent adoption is already very high among professional developers. ([OpenAI Developers][1])

Given your stack — model training + agents + CLI + consulting — I’d think in terms of **“software that replaces a workflow”**, not another chatbot.

### 1. AI employee for SMBs

Give a company one agent with access to:

```text
Gmail
Slack
Google Drive
CRM
ERP
browser
SQL
internal APIs
```

Then:

```text
CEO: "Handle this week's inbound leads."

Agent:
  → read emails
  → qualify leads
  → research companies
  → update CRM
  → draft replies
  → schedule calls
  → follow up
  → report exceptions
```

This is technically viable now: current agent runtimes support tools, multi-step execution, state, orchestration and computer use. ([OpenAI Developers][2])

**Business model:** $500–5,000/mo per company.

The key isn't the model. It's owning a **specific business workflow**.

---

### 2. "Claude Code for X"

This is probably the most interesting category.

Claude Code proved that an agent can turn:

```text
issue → inspect repo → edit → run tests → debug → PR
```

into a product.

The same architecture works for:

```text
"AI accountant"
"AI SRE"
"AI data engineer"
"AI security engineer"
"AI researcher"
"AI compliance engineer"
"AI growth engineer"
```

For example:

```text
AI SRE

alert
  ↓
agent reads logs
  ↓
inspect metrics
  ↓
inspect recent deploy
  ↓
reproduce issue
  ↓
propose / execute fix
  ↓
run tests
  ↓
rollback or deploy
  ↓
write incident report
```

OpenAI's current agent cookbook is already explicitly showing patterns such as SRE agents, data analysts, support agents, security scanners, database-change analysis and iterative repair loops. ([OpenAI Developers][3])

**This is much more defensible than another general-purpose chat UI.**

---

### 3. AI software company inside a CLI

This one feels particularly aligned with what you're already building.

Imagine:

```bash
$ zz "ship Stripe subscription support"

> inspecting repo
> inspecting Stripe docs
> designing schema
> implementing backend
> implementing frontend
> writing tests
> running tests

✓ 43 files changed
✓ 127 tests passed

PR #184 created
```

But go one level further:

```bash
$ zz company

company/
  agents/
    engineer
    researcher
    designer
    qa
    growth
    support
  memory/
  tasks/
  evals/
  artifacts/
```

The product isn't "AI coding."

It's:

> **Give one person a virtual software company.**

The underlying infrastructure is increasingly commodity: sandbox execution, tools, multi-agent orchestration, long-running tasks and computer interaction are all available now. ([OpenAI][4])

---

### 4. AI research lab

Give an agent:

```text
web
papers
arxiv
GitHub
browser
Python
GPU
experiment runner
database
```

Then:

```text
research question
       ↓
literature search
       ↓
hypothesis
       ↓
experiment
       ↓
train / evaluate
       ↓
analyze
       ↓
new hypothesis
       ↓
repeat
       ↓
report
```

This is particularly interesting for **ML research** because the output is objectively testable.

For example:

```text
"Can we improve long-context training efficiency?"

agent generates 12 hypotheses
        ↓
runs experiments
        ↓
keeps promising 3
        ↓
runs ablations
        ↓
produces paper + code
```

The important product primitive here is not "AI researcher."

It's the **experiment loop**.

---

### 5. AI agent QA / eval company

Every company building agents eventually hits:

```text
works in demo
≠
works reliably
```

So build:

```text
production traces
       ↓
failure mining
       ↓
generate adversarial tasks
       ↓
run 1,000 agent trajectories
       ↓
judge outcomes
       ↓
regression detection
       ↓
automatically improve prompts/tools
```

You could sell:

```text
Agent Eval CI

$ agent-eval run

1,842 scenarios
1,842 trajectories

success:       91.7%
tool errors:    3.1%
hallucination:  1.8%
regression:    +4.2%

FAILED:
  billing/refund/17
  support/escalation/42
  ...
```

This is especially attractive because **agents are probabilistic software**, so traditional unit tests aren't enough.

---

### 6. AI browser worker

Computer use changes the economics of legacy software integration.

Instead of:

```text
company has no API
→ impossible integration
```

you can do:

```text
agent
 ↓
browser
 ↓
existing SaaS
```

The agent can literally:

```text
open Salesforce
click lead
copy information
open ERP
create customer
upload document
send email
```

Current computer-use systems explicitly support operating browser and desktop interfaces. ([OpenAI Developers][5])

This creates a fascinating wedge:

> **Automate software that was never designed to be automated.**

Potential verticals:

* insurance operations
* logistics
* accounting
* recruiting
* healthcare administration
* real estate
* government paperwork
* manufacturing back office

---

### 7. Personal "chief of staff"

Not:

> "Ask me anything."

Instead:

```text
you
 ↓
persistent agent
 ↓
email
calendar
documents
browser
contacts
purchases
travel
tasks
```

Every morning:

```text
Good morning.

3 things require your attention:

1. Client X hasn't paid invoice #392.
2. Your 14:00 meeting conflicts with flight departure.
3. Research task finished overnight.

I already:
✓ drafted the payment follow-up
✓ moved the meeting
✓ summarized the experiment

Approve #1?
```

The industry is explicitly moving toward persistent personal agents that can perform tasks such as shopping, booking and calendar management. ([Axios][6])

The hard problem isn't intelligence.

It's **trust + permissions + memory + identity**.

---

### 8. AI-native ERP

This is more radical.

Instead of:

```text
human
 ↓
ERP UI
 ↓
forms
 ↓
database
```

do:

```text
human
 ↓
agent
 ↓
business state
```

Example:

```text
"How much inventory should we order next month?"

agent:
  reads sales
  reads seasonality
  reads suppliers
  reads cash position
  runs forecast
  simulates scenarios
  proposes order
```

Then:

```text
"Execute it."

→ creates PO
→ negotiates supplier
→ updates inventory
→ schedules shipment
```

The UI becomes secondary.

**Intent → agent → state transition** becomes the primitive.

---

## The 3 I'd personally attack

If I were sitting next to you and we wanted something we could **ship this month**, I'd narrow it to:

| Product                                |       MVP |                              Moat |
| -------------------------------------- | --------: | --------------------------------: |
| **AI employee for one vertical**       | 1–2 weeks |                     workflow/data |
| **AI software company / coding agent** |    1 week |    agent + developer distribution |
| **Agent eval/QA infrastructure**       | 1–2 weeks | eval datasets + production traces |

And I would **avoid**:

```text
❌ generic chatbot
❌ generic RAG
❌ generic "AI assistant"
❌ prompt marketplace
❌ AI wrapper around one API
❌ another image generator
```

The interesting unit in 2026 is increasingly:

```text
                OLD SOFTWARE
                     │
               ┌─────▼─────┐
               │    UI     │
               └─────┬─────┘
                     │
                   human
                     │
               ┌─────▼─────┐
               │   intent  │
               └───────────┘


                AI SOFTWARE

                   human
                     │
                natural intent
                     │
                     ▼
              ┌──────────────┐
              │    AGENT     │
              │              │
              │ reason       │
              │ plan         │
              │ use tools    │
              │ execute      │
              │ verify       │
              │ retry        │
              └──────┬───────┘
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       browser      code       APIs
          │          │          │
          └──────────┼──────────┘
                     ▼
                business state
```

That's the fundamental product opportunity.

And there's a useful second-order observation: **the frontier is moving from "make the model smarter" to "give the model a workplace."** Current agent platforms already expose sandboxes, tools, memory, orchestration and computer use, while Anthropic is also pushing toward multiple persistent coding agents operating against shared projects. ([OpenAI][4])

I can next turn this into a **10-product idea list specifically optimized for a 1–3 person AI startup: MVP scope, first customer, pricing, moat, and what we'd build in the first 7 days**.

[1]: https://developers.openai.com/api/docs/guides/agents/sdk?utm_source=chatgpt.com "Agents SDK | OpenAI API"
[2]: https://developers.openai.com/api/docs/guides/agents?utm_source=chatgpt.com "Agents | OpenAI API"
[3]: https://developers.openai.com/cookbook/topic/agents?utm_source=chatgpt.com "Agents • Cookbook"
[4]: https://openai.com/index/the-next-evolution-of-the-agents-sdk/?utm_source=chatgpt.com "The next evolution of the Agents SDK | OpenAI"
[5]: https://developers.openai.com/api/docs/guides/tools-computer-use?utm_source=chatgpt.com "Computer use | OpenAI API"
[6]: https://www.axios.com/2026/09/20/ai-assistant-openai-meta-muse-instinct-grok-apple?utm_source=chatgpt.com "The era of the personal agent has finally arrived"
