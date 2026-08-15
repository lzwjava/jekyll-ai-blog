---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hong Kong Company for US Clients
translated: false
type: note
---

**Question: Can a Hong Kong LLC/company do software projects for US clients?**

**Answer: Yes.** A Hong Kong limited company can legally provide software development, AI consulting, SaaS development, outsourcing, and engineering services to US clients. This is actually a common international structure.

Typical setup:

```
US Client
    |
    |  Software Development Contract
    |
Hong Kong Limited Company
    |
    |  hires developers / founders
    |
Engineering work
```

The US client pays your Hong Kong company. You invoice them in USD, receive payment through a bank account/payment provider, and deliver software.

---

## 1. What you need

### Hong Kong company side

Usually:

* Hong Kong Limited Company
* Business Registration Certificate
* Company bank account
* Accounting records
* Service agreement / MSA + SOW with US clients
* Invoice system

Hong Kong companies can conduct international business; business registration is a registration requirement, not a restriction on trading with overseas customers. ([Government of Hong Kong][1])

---

## 2. US client usually does not care where your company is

A US startup may hire:

* US LLC
* Hong Kong Ltd
* Singapore Pte Ltd
* India Pvt Ltd
* Individual contractor

For software engineering, they mainly care about:

* capability
* IP ownership
* security
* contract terms
* payment method

Example:

```
Contract:
"ABC HK Limited will develop AI agent platform for XYZ Inc."

Payment:
$10,000/month

Deliverables:
- GitHub repository
- deployment
- documentation

IP:
All source code assigned to client after payment
```

---

## 3. Tax considerations

### Hong Kong

Hong Kong uses a territorial tax system. Generally, profits arising in or derived from Hong Kong are subject to profits tax; foreign-source situations depend on facts such as where operations generating profits occur. ([Inland Revenue Department][2])

For a software company:

Example A:

```
You live in Hong Kong
You code in Hong Kong
Your HK company invoices US customers

=> likely Hong Kong business income
```

Example B:

```
HK company owns IP
Developers are outside HK
Management outside HK

=> more complex source analysis
```

You should have a Hong Kong accountant structure this properly.

---

## 4. Do you need a US company?

Usually **no**.

You only need a US entity if you want:

* US investors
* US employees
* US bank account
* US government contracts
* easier YC/VC fundraising
* US presence for sales

For pure consulting/software outsourcing:

```
HK Ltd
   |
   +-- US clients
```

is perfectly normal.

---

## 5. Payment methods

Common:

* Wise Business
* Airwallex
* HSBC Hong Kong
* Bank wire (SWIFT)
* Stripe (if SaaS)

Example invoice:

```
Invoice #2026-001

From:
ABC Technology Limited
Hong Kong

To:
XYZ AI Inc.
California, USA

Service:
AI Agent Development

Amount:
USD 20,000

Payment:
Wire transfer
```

---

## 6. If you are physically in China/Hong Kong

This becomes the more important question.

Example:

```
Hong Kong company
        |
        |
You live in mainland China
        |
        |
Develop software for US clients
```

Possible issues:

* where management happens
* where developers work
* personal tax residency
* foreign exchange
* employment arrangements

Many Chinese founders use:

```
Hong Kong Ltd
       |
       |
Mainland China engineering team
       |
       |
US customers
```

but they need proper accounting/legal setup.

---

## 7. For an AI/software consulting company

A practical structure:

```
Hong Kong Ltd
      |
      +-- US AI startups
      |
      +-- AI consulting
      |
      +-- Model training
      |
      +-- Agent development
      |
      +-- SaaS products
```

Advantages:

* international credibility
* USD contracts
* easier overseas payments
* simpler than US company formation
* good bridge between China engineering talent and global customers

For someone building AI agents/model training services, HK Ltd is a very common route.

References:

* Hong Kong Inland Revenue Department — Profits Tax: [IRD Profits Tax](https://www.ird.gov.hk/eng/tax/bus_pft.htm?utm_source=chatgpt.com)
* Hong Kong Government — Business registration and tax obligations: [GovHK Tax Obligations of Non-Resident Business Operators](https://www.gov.hk/en/nonresidents/investinghk/doingbusiness/taxinhk.htm?utm_source=chatgpt.com)

[1]: https://www.gov.hk/en/nonresidents/investinghk/doingbusiness/taxinhk.htm?utm_source=chatgpt.com "GovHK: Tax Obligations of Non-Resident Business Operators"
[2]: https://www.ird.gov.hk/eng/tax/bus_pft.htm?utm_source=chatgpt.com "IRD : Profits Tax"
