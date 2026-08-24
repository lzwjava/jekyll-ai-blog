---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hong Kong's Contractor Culture
translated: false
type: note
---

Question: **Why does Hong Kong have such a strong contract / consultancy / contractor culture, especially for professional engineers and IT workers?**

Answer: The short version is **Hong Kong is a high-cost, service-heavy, project-driven economy.** Companies often don't want to permanently own every capability they temporarily need.

Think of it as an economic optimization problem:

[
\text{Hire decision} =
\arg\min_{\text{employee vs contractor}}
(\text{cost}+\text{risk}+\text{commitment}+\text{management overhead})
]

### 1. A company doesn't always need an engineer forever

Suppose a bank needs:

```text
2026:
    migrate Oracle → PostgreSQL
    12 engineers
    9 months

2027:
    migration finished
    needs only 2 engineers for maintenance
```

Hiring 12 permanent engineers creates:

```text
salary
MPF
insurance
benefits
office
HR
termination cost
management
```

Instead:

```text
Bank
 │
 └── consultancy
       │
       ├── engineer
       ├── engineer
       ├── engineer
       └── ...
```

The bank buys **engineering capacity for 9 months**.

This is economically similar to renting GPUs instead of buying a 128-GPU cluster that sits idle after training.

---

### 2. Hong Kong has many project-based industries

This is particularly important.

Hong Kong has huge amounts of:

* banking
* insurance
* finance
* construction
* property
* infrastructure
* government projects
* telecommunications
* professional services
* IT transformation

Many of these naturally generate projects:

```text
Bank
 ├── core banking upgrade
 ├── AML system
 ├── mobile banking
 ├── cloud migration
 ├── cybersecurity
 ├── data platform
 └── AI transformation
```

Each project has a beginning and an end.

Therefore:

[
\text{project economy}
\rightarrow
\text{consultancy}
\rightarrow
\text{contractors}
]

---

### 3. Large enterprises don't necessarily want to recruit every skill themselves

Imagine HSBC needs:

```text
Kubernetes
Kafka
Java
Python
LLM
AWS
Cybersecurity
SAP
Oracle
Mainframe
Data engineering
```

It would be absurd to maintain a permanent organization containing the world's best specialist in every technology.

Instead:

```text
                    HSBC
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   Consultancy A  Consultancy B  Consultancy C
        │             │             │
     cloud team    AI team       security team
```

The consultancy company effectively becomes a **labor-market abstraction layer**.

The bank says:

> "Give me 20 engineers who can deliver this."

rather than:

> "I need to individually find 20 people."

---

### 4. There is also a risk-transfer mechanism

This is one of the most important reasons.

Suppose a company wants to build an AI system.

Permanent hiring:

```text
Company
   ↓
hire 10 engineers
   ↓
project fails
   ↓
company owns the people
```

Consulting:

```text
Company
   ↓
contract consultancy
   ↓
10 engineers
   ↓
project fails
   ↓
contract ends
```

The company has transferred part of the **execution risk** to the vendor.

This is why enterprise consulting isn't simply "selling programmers."

It's selling:

> **capacity + expertise + execution + accountability + risk transfer**

---

### 5. Procurement itself creates a market

Large companies often have procurement systems like:

```text
Requirement
     ↓
RFP / tender
     ↓
5 vendors
     ↓
technical proposal
     ↓
commercial proposal
     ↓
contract
     ↓
SOW
     ↓
milestones
     ↓
acceptance
     ↓
payment
```

Once an organization operates this way for decades, a whole ecosystem develops around it.

You get:

```text
Enterprise
   │
   ├── Accenture
   ├── Deloitte
   ├── IBM
   ├── local consultancy
   ├── system integrator
   └── staffing company
          │
          └── engineers
```

This is why **consultancy itself becomes an established industry**.

---

### 6. Hong Kong's high labor cost makes this particularly attractive

Suppose a specialist costs:

```text
Permanent employee:
    HK$80k/month
```

But the company only needs them for six months.

A consultancy might charge:

```text
HK$120k/month
```

At first glance:

> "Consultant is more expensive!"

But compare the total commitment.

Permanent:

[
80k \times 12 = 960k
]

Consultant:

[
120k \times 6 = 720k
]

Even though the **monthly unit price is higher**, the **total economic cost can be lower**.

That's a fundamental property of contractor markets:

[
\boxed{\text{higher unit price} \neq \text{higher total cost}}
]

You pay a premium for flexibility.

---

### 7. It also explains why "contractor → consultancy → client" is common

You might encounter:

```text
Bank
 │
 │ contract
 ▼
System Integrator
 │
 │ subcontract
 ▼
Consultancy
 │
 │ employs
 ▼
Engineer
```

So the engineer might technically work:

```text
at HSBC
```

every day, while legally being employed by:

```text
Company X
```

and Company X has a contract with another vendor.

This is extremely common in large enterprise IT.

---

### 8. And this creates an interesting opportunity for you

Instead of thinking only:

> "I need to find an AI engineering job."

There is another model:

```text
                 You
                  │
          AI consulting company
                  │
       ┌──────────┼──────────┐
       ▼          ▼          ▼
     Bank       Factory     SME
       │          │          │
       ▼          ▼          ▼
    AI agent    AI infra    LLM app
```

You don't necessarily sell:

> **"Zhiwei, 1 engineer × 1 month."**

You sell:

> **"I will build your private AI platform / agent / inference system for HK$X."**

Then internally:

```text
client
  ↓
SOW
  ↓
milestones
  ↓
deposit
  ↓
implementation
  ↓
acceptance
  ↓
payment
```

That is a much more scalable model.

The interesting progression is:

[
\boxed{
\text{employee}
\rightarrow
\text{contractor}
\rightarrow
\text{consultant}
\rightarrow
\text{consultancy}
\rightarrow
\text{productized service}
\rightarrow
\text{product}
}
]

And **Hong Kong's existing contract/procurement culture makes the middle of that ladder relatively natural**.