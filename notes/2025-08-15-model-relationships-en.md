---
audio: false
generated: true
image: false
lang: en
layout: post
title: Model Relationships, Not Data
translated: false
type: note
---

You’re absolutely right—“one-to-one, one-to-many, many-to-many” are everywhere: families, teams, payments; classes, repos, pull requests. Here’s a compact playbook for **settling relationships** so designs stay simple and match how things are used.

# A practical modeling playbook

## 1) Start from behavior, not data

* Write **top 5 user tasks** (“place order”, “approve expense”, “assign reviewer”).
* Under each task, list **nouns** (entities) and **verbs** (relationships/actions).
* Keep only relationships that **change outcomes** in those tasks; everything else is metadata.

## 2) Decide ownership & boundaries first

* Ask: *Who owns the lifecycle of whom?*

  * If A can’t exist without B → A is **part of** B (composition).
  * If A and B live independently → **reference** relationship.
* Use **bounded contexts**: the same “Customer” can be different in Billing vs. Marketing. Don’t force one mega-model.

## 3) Choose the **simplest cardinality** that works

* Prefer **1→1** only when two records are operationally inseparable but need different security or volatility (e.g., User ↔ Credentials).
* Prefer **1→N** when there’s clear ownership and frequent parent→children access (Order → LineItems).
* Use **M↔N** only when both sides are peers and linking is its own business concept (Student ↔ Course via “Enrollment” that has grade, status, dates).

## 4) Make relationships explicit with invariants

For each relation, write invariants in plain language:

* **Cardinality**: “One user has at most one primary email.”
* **Optionality**: “An invoice must have ≥1 line item.”
* **Temporal**: “Membership is valid during \[start,end).”
* **Uniqueness**: “A product code is unique per tenant.”
  These convert directly into constraints, indexes, and checks.

## 5) Model patterns by cardinality (without tables 😉)

### One-to-one

* Use when splitting volatile/secure fields or when an entity grows modularly.
* Enforce with a unique key on the foreign key.
* Consider **embedding** (documents) if it’s always read together.

### One-to-many

* If children never move between parents → keep **parent key** on child; cascade deletes as policy.
* If reparenting happens → allow nullable FK + business rule for transitions.
* If reads are parent-centric → denormalize summary fields on parent (counts, last\_updated).

### Many-to-many

* Promote the link to a **first-class entity** (Enrollment, Membership, Assignment).
* Put the **business data** on the link (role, priority, weight, timestamps).
* If the link has no attributes and is huge, choose storage & indexes for the heavier side’s queries.

## 6) Choose storage by access patterns

* **Relational**: strongest integrity, complex joins, reporting.
* **Document**: aggregate-first, read-heavy parent-centric flows, localized updates.
* **Graph**: path queries, recommendations, permission inheritance, variable-depth traversals.
  Pick one **per bounded context**; sync via events, not shared tables.

## 7) API surface mirrors relationships—intentionally

* **Aggregates** become primary API resources.
* **Child collections** as nested routes (e.g., `/orders/{id}/items`).
* **Join entities** get their own resource when they matter (`/enrollments`).
* For client flexibility, expose **GraphQL** only when the domain is graph-like or clients vary widely; otherwise keep REST simple.

## 8) Keep it evolvable (temporal + soft change)

* Track **valid-time** on important links (`valid_from`, `valid_to`), not just `updated_at`.
* Prefer **soft deletes** on relationship rows so you can rebuild history.
* Use **surrogate IDs** for all entities and link rows; never embed meaning in IDs.

## 9) Simplify aggressively

* Merge entities if users never perceive the difference.
* Collapse 1→1 splits when security/performance reasons disappear.
* Replace wide M↔N webs with a **hierarchy** if business rules are truly tree-shaped.
* Introduce **roles** instead of multiple link types (e.g., one Membership with role=owner/viewer instead of separate links).

## 10) Reverse-research (reverse-engineer) an existing tangle

* Map **actual queries** (slow logs, dashboards). Keep only relationships used by ≥1 critical query.
* Draw **context maps**: which team/system owns which entities and who consumes which events.
* Identify **hot joins** → either denormalize, cache, or turn into aggregates.
* Elevate noisy M↔N links to **first-class concepts** with clear invariants.
* Add **contracts**: constraints, tests, and linters for schema & API to prevent drift.

# Common pitfalls to avoid

* Treating M↔N as “just a join table” when it’s actually the business heart (e.g., permissions, allocations).
* Over-normalizing read-paths that need low latency; fix with **read models** (CQRS) or materialized views.
* Under-specifying optionality—`NULL` explodes complexity. Prefer explicit “Unknown/NotApplicable” states when meaningful.
* Ignoring **multi-tenancy**: always scope uniqueness and queries by tenant early.
* Forgetting **directionality**: “follows” vs “friends” are not the same.

# A lightweight checklist you can reuse

* What are the top tasks and their success metrics?
* What are the aggregates (ownership/lifecycle)?
* What are the invariants (cardinality, optionality, temporal, uniqueness)?
* Which relationships carry business attributes (promote to entities)?
* Which access patterns dominate (choose store/indexes accordingly)?
* What simplifications are safe today (merge/split/denormalize)?
* What contracts enforce this (constraints, API tests, event schemas)?

If you want, give me a tiny slice of your domain (three entities + the main user task), and I’ll sketch the relationships, invariants, and a storage/API shape you can implement directly.
