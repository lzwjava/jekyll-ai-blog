---
audio: false
generated: true
image: false
lang: en
layout: post
title: Platform Reuse Beats Custom AI
translated: false
type: note
---

Question: Why is it hard for a small software outsourcing team to build enterprise AI agent platforms like Rasa or Salesforce Agentforce, and why does a third-party platform model have better ROI?

Answer:

Yes, your intuition is basically correct. The key issue is **economics of reuse**.

A small outsourcing team can build an AI agent system for one factory/company, but the business model usually becomes:

```
Customer A
   |
   +-- custom workflow
   +-- custom data integration
   +-- custom UI
   +-- custom permissions
   +-- custom deployment
   +-- custom maintenance

Revenue: one customer
Cost: almost everything repeated
```

The input/output ratio is bad.

---

## 1. Enterprise AI agents are not just an LLM wrapper

A demo:

```
User
 |
Chat UI
 |
GPT/Qwen
 |
Answer
```

A production enterprise agent:

```
                    +----------------+
                    | Model Gateway  |
                    +----------------+
                            |
User ---> Agent Runtime ---> Planner
             |
             +--> RAG
             |
             +--> Tool calling
             |
             +--> Workflow engine
             |
             +--> Memory
             |
             +--> Security policy
             |
             +--> Audit log
             |
             +--> Human escalation
             |
             +--> Monitoring
             |
             +--> Evaluation
             |
             +--> Multi-tenant management
```

The hard part is not calling GPT.

The hard part is:

* connecting SAP / Oracle / Salesforce / MES / ERP
* handling permissions
* preventing data leakage
* tracing decisions
* versioning prompts
* evaluating agent quality
* supporting thousands of users
* compliance

---

## 2. Why outsourcing loses money

Suppose a factory wants an AI maintenance agent.

Team builds:

```
Factory A

Agent:
- read machine sensor data
- query maintenance history
- generate reports
- call engineers
```

Maybe:

Development:

* 6 months
* 5 engineers
* $300k cost

Customer pays:

* $500k

Looks profitable.

But next factory:

```
Factory B
different:
- machines
- ERP
- database
- terminology
- workflow
```

You rebuild 60%.

Your previous asset reuse:

maybe only 30%.

So:

```
Customer 1:
Cost 300k
Revenue 500k

Customer 2:
Cost 200k
Revenue 500k

Customer 3:
Cost 200k
Revenue 500k
```

You are basically a consulting company.

Not a software company.

---

## 3. Platform companies flip the economics

Rasa, Salesforce Agentforce, ServiceNow AI, Microsoft Copilot Studio etc. build:

```
              Platform

              Core engine
                  |
       -----------------------
       |          |          |
   Company A  Company B  Company C

   config     config     config
   data       data       data
   workflow   workflow   workflow
```

The expensive part:

* agent runtime
* security
* connectors
* UI
* evaluation
* monitoring

is built once.

Then every customer pays subscription.

Example:

Development:

```
$20 million engineering investment
```

Customers:

```
10,000 companies
```

Cost per customer:

```
$20M / 10,000 = $2,000
```

The economics completely change.

---

## 4. This is the same reason Salesforce won

Before Salesforce:

```
Company hires IT team

build CRM:
$5M
2 years
maintenance forever
```

Salesforce:

```
One CRM platform

Customer pays:
$100/user/month
```

The same pattern:

```
custom software
        ↓
software platform
        ↓
ecosystem
```

---

## 5. But small teams can still win

Small teams should not compete with Salesforce horizontally.

Bad idea:

> "Let's build an enterprise agent platform for everyone."

You fight:

* Salesforce
* Microsoft
* Google
* ServiceNow
* AWS

Impossible.

Better:

Vertical AI agent.

Example:

```
AI Agent Platform for semiconductor factories
```

or:

```
AI Agent Platform for Chinese export companies
```

Then:

```
common layer:
- agent runtime
- RAG
- workflow
- evaluation

vertical layer:
- industry knowledge
- connectors
- templates
```

The moat becomes:

```
Domain knowledge
+
Data
+
Workflow
+
Distribution
```

not just code.

---

## 6. The future likely looks like this

General platform:

```
OpenAI
Anthropic
Google
Microsoft
Salesforce
```

↓

Industry platforms:

```
AI Agent for hospitals
AI Agent for factories
AI Agent for finance
AI Agent for legal
```

↓

Customized deployment:

```
Customer-specific workflows
```

Small teams can survive in the middle layer.

---

So your conclusion is right:

> One vendor customized project has poor ROI because every input/output is unique. A third-party platform creates leverage because the same engineering investment serves many companies.

The business transition is:

```
Selling engineering hours
        ↓
Selling reusable software
        ↓
Selling AI infrastructure + ecosystem
```

That is why companies like Rasa and Salesforce Agentforce are valuable. Their real product is not "a chatbot"; it is the **enterprise agent operating system**.
