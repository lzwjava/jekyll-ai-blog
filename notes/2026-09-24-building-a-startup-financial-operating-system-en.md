---
audio: false
generated: true
image: false
lang: en
layout: post
title: Building a Startup Financial Operating System
translated: false
type: note
---

Question: **How do you manage budget, R&D expenses, and operations when running a ~500-person startup?**

Answer:

At 500 people, the key shift is: **you stop managing expenses directly and start managing a financial operating system.**

The simplest mental model is:

> **Strategy → annual budget → org budgets → monthly forecast → spending controls → weekly operating metrics**

### 1. Start with a company-level P&L

Don't start with individual expenses. Start with:

```text
Revenue
- COGS
= Gross Profit

- R&D
- Sales & Marketing
- G&A
= Operating Profit / Loss

+/- financing / other
= Cash change
```

For an AI company, I'd make the R&D line more explicit:

```text
R&D
├── People
│   ├── Engineering
│   ├── Research
│   └── Product
├── Compute
│   ├── Training
│   ├── Inference
│   └── Evaluation
├── Data
├── Software / API
└── Contractors
```

And **compute should be treated almost like headcount**. At an AI company, "GPU budget" can become one of the largest controllable costs.

---

### 2. Build a 12–18 month financial model

You need one spreadsheet/model that answers:

> "If we keep operating like this, how much cash do we have 12 months from now?"

At minimum:

```python
months = 18

cash = initial_cash

for month in range(months):
    revenue = forecast_revenue(month)

    payroll = forecast_headcount(month)
    compute = forecast_compute(month)
    infra = forecast_infra(month)
    sales = forecast_sales(month)
    g_and_a = forecast_g_and_a(month)

    burn = payroll + compute + infra + sales + g_and_a - revenue
    cash -= burn

    print(month, cash)
```

But don't make it a single forecast.

Maintain three scenarios:

```text
             Base       Aggressive       Downside
Revenue      $100M      $140M             $70M
Hiring       500        600               450
Compute      $20M       $30M              $15M
Burn         $60M       $75M              $50M
Runway       20 mo      16 mo             24 mo
```

The important number isn't "this year's budget."

It's:

> **What assumptions cause us to run out of cash?**

---

# 3. Every organization gets a budget

At 500 people, don't let everyone spend against one giant company budget.

Create cost centers:

```text
CEO
├── Research
├── Engineering
├── Product
├── Sales
├── Marketing
├── Operations
├── Finance
├── Legal
├── People
└── IT
```

Each leader gets something like:

```text
Engineering
────────────────────
Headcount       $18M
Cloud            $4M
Software         $1M
Contractors      $1M
Travel           $0.5M
Other            $0.5M
────────────────────
Total           $25M
```

Then the leader owns the number.

The CFO/finance team shouldn't constantly ask:

> "Can I approve this $8,000 invoice?"

Instead:

> "Engineering has a $25M annual budget. Are they managing it toward the company's objectives?"

That's the scalable model.

---

# 4. Separate three different concepts

This is extremely important.

### Budget

What you **plan** to spend.

```text
Engineering FY27 budget = $25M
```

### Actual

What you've **already spent**.

```text
Engineering YTD actual = $14.2M
```

### Forecast

What you now believe you'll spend.

```text
Engineering FY27 forecast = $27.8M
```

So your dashboard becomes:

```text
              Budget    Actual    Forecast    Variance
Engineering    $25M      $14.2M     $27.8M      +11%
R&D            $40M      $22.1M     $42.0M       +5%
Sales          $18M       $9.0M     $17.5M       -3%
G&A            $12M       $5.8M     $11.7M       -3%
```

**Budget is not the truth. Forecast is the truth.**

This is one of the biggest differences between amateur and mature financial management.

---

# 5. Headcount is usually the biggest budget

At 500 people, don't manage hiring as:

> "Can we afford another engineer?"

Manage it as a **headcount plan**.

Example:

```text
              Current   Dec     Cost/year
Research        80       110      $15M
Engineering    180       220      $32M
Product         40        50       $7M
Sales            70        90      $12M
G&A              50        55       $8M
─────────────────────────────────────────
Total           420       525      $74M
```

Every hiring request should have:

```text
Role
Org
Manager
Start date
Annual compensation
Recruiting cost
Equipment
Expected business purpose
```

Then finance can calculate:

```text
New hire annualized cost = salary
                          + bonus
                          + benefits
                          + payroll taxes
                          + equipment
                          + recruiting
```

Don't underestimate the compounding effect of hiring.

If you hire 100 people at an average fully-loaded cost of $250k:

```text
100 × $250k = $25M/year
```

And hiring them halfway through the year doesn't mean they're "only $12.5M."

Next year, the full $25M becomes structural.

---

# 6. R&D needs a different management system

You don't want to tell researchers:

> "You have to justify every dollar."

That kills research.

Instead, divide R&D into:

```text
Core research
Product engineering
Infrastructure
Experimental projects
```

Then use **portfolio budgeting**.

For example:

```text
R&D = $60M

$25M  Core product
$15M  Foundation/model research
$8M   Infrastructure
$5M   New bets
$4M   Data/evaluation
$3M   Reserve
```

The interesting part is **new bets**.

Give teams capital:

```text
Project A → $1M
Project B → $2M
Project C → $500k
```

But define an explicit checkpoint:

```text
$0 → prototype
$100k → technical validation
$500k → user validation
$1M → productization
```

This is essentially **venture capital inside the company**.

You don't know which R&D project will work.

So don't pretend you can forecast it perfectly.

Instead:

> Allocate small amounts of capital → observe evidence → increase allocation.

---

# 7. AI compute deserves its own CFO-style dashboard

For an AI startup, I'd literally have:

```text
GPU Dashboard
─────────────────────────────
Training             $8.2M
Inference            $5.7M
Evaluation           $1.1M
Research experiments $2.3M
Idle / waste         $0.8M
─────────────────────────────
Total                $18.1M
```

Then connect cost to technical metrics:

```text
$/training run
$/1M tokens
$/successful experiment
$/eval point
$/production request
$/customer
GPU utilization
```

This lets research leadership ask:

> "Did we spend $2M because experiments were productive, or because infrastructure was inefficient?"

Those are completely different problems.

---

# 8. Operations should have its own operating metrics

Don't put everything into finance.

Finance tells you:

```text
We spent $10M.
```

Operations tells you:

```text
Why?
```

For example:

### Engineering

```text
headcount
deployment frequency
cloud cost
incident rate
availability
cycle time
```

### Research

```text
experiments/week
GPU hours
training runs
evaluation improvement
research → production conversion
```

### Sales

```text
pipeline
new ARR
CAC
win rate
sales cycle
NRR
```

### Customer operations

```text
tickets
response time
resolution time
churn
customer satisfaction
```

Finance shouldn't replace operating metrics.

It connects them.

---

# 9. Establish spending authority

You need a simple approval matrix.

For example:

```text
<$5k
Manager

$5k–$25k
Director

$25k–$100k
VP + Finance

$100k–$500k
Executive

>$500k
CFO + CEO / investment committee
```

But importantly:

**Approval thresholds should apply to commitments, not merely invoices.**

Otherwise someone can sign a:

```text
$2M/year × 3 year contract
```

because the first invoice is only $100k.

---

# 10. Use procurement for recurring spend

At 500 people, SaaS becomes surprisingly expensive.

Imagine:

```text
500 employees

Slack
GitHub
Notion
Linear
Datadog
AWS
Cloudflare
OpenAI
Anthropic
Google
Security tools
HR systems
Finance systems
...
```

You eventually get:

```text
$5k here
$20k there
$50k there
```

and nobody owns the aggregate.

Create a vendor registry:

```text
Vendor
Owner
Annual contract value
Renewal date
Users
Cost/user
Contract term
Cancellation notice
Business purpose
```

Then every quarter:

```text
Who owns it?
Who uses it?
What happens if we cancel it?
```

---

# 11. The CFO should run a monthly business review

I'd structure the meeting like this:

```text
1. Revenue
2. Gross margin
3. Cash
4. Burn
5. Runway
6. Headcount
7. R&D spend
8. Compute
9. Major budget variances
10. Forecast changes
11. Decisions required
```

Not:

> "Here are 147 pages of financial statements."

The CEO needs to know:

```text
Cash             $180M
Monthly burn      $12M
Runway             15mo

Revenue            $9M/mo
Growth              8% MoM
Gross margin       62%

Headcount           487
Hiring plan         +73

R&D spend           $5M/mo
Compute             $1.8M/mo

Forecast variance  +$7M
```

Then:

> **What changed? Why? What decision do we need to make?**

---

# 12. Weekly vs monthly vs quarterly

A good cadence:

### Weekly

CEO / COO:

```text
cash
revenue
pipeline
headcount
compute
major incidents
major purchases
```

### Monthly

Finance + executives:

```text
P&L
budget vs actual
forecast
cash flow
headcount
department performance
```

### Quarterly

Board / executives:

```text
strategy
capital allocation
R&D portfolio
hiring plan
runway
major investments
```

### Annually

Company:

```text
strategy
annual budget
headcount plan
capital plan
R&D allocation
revenue plan
```

---

# 13. The organizational architecture

For ~500 people, I'd expect something roughly like:

```text
                         CEO
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
       CFO               COO              CTO/Chief Scientist
        │                 │                 │
   Finance            Operations            R&D
   FP&A                People              Engineering
   Accounting          Legal               Infrastructure
   Treasury            IT                  Research
   Procurement         Security            Product
```

And underneath:

```text
Finance
├── Accounting
├── FP&A
├── Treasury
├── Tax
└── Procurement

Operations
├── People
├── Legal
├── Security
├── IT
└── BizOps
```

You don't necessarily need all of these as separate departments, but **the functions need owners**.

---

# 14. The most important concept: capital allocation

At 500 people, the CEO's fundamental job becomes:

> **Where should the next $1M go?**

Suppose you have $100M available.

You could allocate:

```text
$35M → existing product
$20M → model research
$15M → compute
$10M → sales
$5M  → international
$5M  → infrastructure
$5M  → hiring reserve
$5M  → experimental bets
```

The allocation itself is the strategy.

Finance gives you the constraints.

R&D gives you technical evidence.

Sales gives you market evidence.

Operations gives you execution capacity.

**CEO decides how capital moves between them.**

That's essentially how you scale from "founder managing expenses" to "CEO running a company."

---

## If I were building the system from zero

I'd make exactly **5 core artifacts**:

```text
1. Company P&L
2. 18-month cash forecast
3. Department budget
4. Headcount plan
5. Vendor / commitment registry
```

And one dashboard:

```text
┌─────────────────────────────────────┐
│ COMPANY                              │
│                                     │
│ Revenue        $XXM                 │
│ Gross Margin   XX%                  │
│ Cash           $XXXM                │
│ Burn           $XXM/mo              │
│ Runway         XX months            │
│                                     │
│ Headcount      XXX                  │
│ R&D            $XXM                 │
│ Compute        $XXM                 │
│ Sales          $XXM                 │
│                                     │
│ Budget variance  +X%                │
│ Forecast change +$XM                │
└─────────────────────────────────────┘
```

Then every manager gets a smaller version of the same system.

The core principle is **one source of truth, but different levels of abstraction**:

```text
CEO
 ↓
Company P&L
 ↓
Department
 ↓
Team
 ↓
Project
 ↓
Individual commitment
```

You don't want the CEO approving every $10k expense. You want the CEO deciding whether **Engineering should receive $30M or $35M next year**, and have the organization reliably turn that decision into thousands of individual transactions.

If you want, I can next build you a **real 500-person AI startup operating model** — including the org chart, $100M annual budget, headcount plan, R&D/compute allocation, approval matrix, and the actual monthly FP&A spreadsheet structure.
