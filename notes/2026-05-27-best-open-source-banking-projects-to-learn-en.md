---
audio: false
generated: true
image: false
lang: en
layout: post
title: Best Open Source Banking Projects to Learn
translated: false
type: note
---

**Question:** What are the best open source banking projects to learn from?

**Answer:**

Here's a curated map ranked by what you'll actually learn from them, not just stars — organized by layer of the stack.

---

## Tier 1 — Core Banking Systems (deepest learning)

### 1. **Apache Fineract** ⭐ TOP PICK

**Repo:** `github.com/apache/fineract`
**Stack:** Java, Spring Boot, MySQL/PostgreSQL, Liquibase, REST

This is the real deal. Apache Fineract is an open-source core banking platform providing a flexible, extensible foundation for a wide range of financial services. More than 20 million customers are reached by 400+ institutions using the Mifos and Fineract APIs.

**What you learn:**

- Robust features for client data management, loan and savings portfolio management, integrated real-time accounting, and extensive reporting capabilities.
- A comprehensive set of REST API endpoints to interact with clients, accounts, products, and transactions, with MySQL/PostgreSQL for data persistence, role-based access control with OAuth2, and scheduler jobs for recurring tasks like interest calculation and disbursement automation.
- Multi-tenancy: how real banks isolate tenant data at the DB level
- Liquibase migration patterns — how schema evolves in prod banking systems
- General ledger double-entry implementation in Java

**What to study first:** `/fineract-provider/src/main/java` — look at the loan lifecycle domain: `LoanApplicationWritePlatformServiceJpaRepositoryImpl`. It's a masterclass in how state machines work in financial systems.

---

### 2. **Open Bank Project (OBP-API)**

**Repo:** `github.com/OpenBankProject/OBP-API`
**Stack:** Scala, Lift framework, http4s

The Open Bank Project is an open-source API for banks that enables account holders to interact with their bank using a wider range of applications and services. The OBP API abstracts away the peculiarities of each core banking system so that a wide range of apps can interact with multiple banks on behalf of the account holder.

**What you learn:**

- PSD2 / Open Banking regulatory API design (the actual spec banks must follow in EU/UK)
- How to build an abstraction layer over legacy core banking (this is your job at the bank)
- Consent management and permission models (configurable views of transaction data)
- Lift framework's actor model for concurrent financial requests

---

## Tier 2 — Accounting Engine (most transferable concepts)

### 3. **Firefly III**

**Repo:** `github.com/firefly-iii/firefly-iii`
**Stack:** PHP/Laravel, REST API, Docker

Every transaction affects two accounts. Every dollar has a source and a destination — this is double-entry bookkeeping, and it's the foundation of professional accounting. It also features rule-based transaction handling with the ability to create your own rules.

**What you learn:**

- Double-entry ledger implementation (the data model is clean and readable)
- Rule engine architecture for auto-categorization — directly maps to the kind of transaction classification AI you'd build
- Reconciliation logic
- How REST APIs expose financial primitives cleanly

The codebase is smaller and more readable than Fineract — good for understanding the accounting layer without Java enterprise noise.

---

## Tier 3 — FINOS (Finance + Open Source, used by real banks)

### 4. **FINOS Projects** (`github.com/finos`)

**Notable:** Legend (Goldman Sachs data model), Perspective (JP Morgan streaming data grid), OpenMAMA, FDC3

FINOS' mission is to promote open innovation in financial services, with nearly 100 projects and 11 programs.

**Specifically for you:**

- **Legend** (Goldman Sachs) — their internal data modeling language, open-sourced. You'll understand how global banks model financial instruments.
- **Perspective** — JP Morgan's real-time streaming analytics library. WebAssembly + Arrow — this is how trading desks render billions of data points.

---

## Study Order (given your AI engineering trajectory)

```
Fineract → understand domain (loan lifecycle, GL, multi-tenancy)
    ↓
OBP-API → understand regulatory layer (PSD2, consent, abstraction)
    ↓
Firefly III → internalize double-entry accounting data model cleanly
    ↓
FINOS/Legend → understand how banks model complex instruments
```

---

## The Core Domain Concepts to Extract

From these repos, the high-leverage things to internalize:

1. **Double-entry ledger** — every credit has a debit, no exceptions. The data model is `(debit_account, credit_account, amount, timestamp)`. Simple but everything flows from it.

2. **Loan state machine** — `PENDING → APPROVED → ACTIVE → CLOSED/WRITTEN_OFF`. Real banks have 15+ states. Fineract has the full implementation.

3. **Interest calculation** — daily accrual vs. periodic, compounding, amortization schedules. Fineract's `LoanScheduleGenerator` is the reference.

4. **Multi-tenancy DB isolation** — Fineract uses schema-per-tenant. Look at how `ThreadLocalContextUtil` passes tenant context through the call stack.

5. **Idempotency in payments** — how to handle network retries without double-charging. Look for idempotency key patterns.

---

Since you're an AI engineer at a bank, the most directly applicable combo is: **Fineract domain knowledge** (so you understand what you're building AI on top of) + **OBP-API** (for the API abstraction patterns you see daily).

**References:**

- [Apache Fineract GitHub](https://github.com/apache/fineract)
- [Open Bank Project OBP-API](https://github.com/OpenBankProject/OBP-API)
- [Firefly III GitHub](https://github.com/firefly-iii/firefly-iii)
- [FINOS GitHub](https://github.com/finos)
- [awesome-open-finance](https://github.com/quantmind/awesome-open-finance)
