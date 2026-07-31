---
audio: false
generated: true
image: false
lang: en
layout: post
title: Software Maintenance Over Purchase Price
translated: false
type: note
---

**Question: Why is long-term maintenance important when buying software, especially expensive enterprise software?**

**Answer:**

Yes. For enterprise software procurement, **lifecycle cost and maintainability are often more important than the initial purchase price**.

A common mistake is evaluating software like buying a physical machine:

> "Pay 3M CNY / 6M CNY, deploy it, and it works forever."

Software is different. It is a living system. The real cost is:

[
TCO = Initial\ License + Implementation + Maintenance + Upgrades + Integration + Migration + Risk
]

A 6M CNY system that becomes unmaintainable after 5 years can be much more expensive than a 10M CNY system that evolves for 15 years.

---

## 1. Software has technical debt accumulation

Enterprise systems usually integrate with:

* databases
* identity systems
* payment systems
* ERP
* government APIs
* internal workflows
* mobile apps
* reporting systems

After years:

```
Year 0:

Frontend
   |
Backend
   |
Database


Year 8:

Mobile App
    |
Gateway
    |
Old Java Services
    |
Old Framework
    |
Oracle DB
    |
Custom Stored Procedures
    |
Vendor Plugins
    |
Unknown Scripts
```

The system becomes a dependency graph.

Adding one feature may require understanding many old assumptions.

---

## 2. Vendor lock-in is a major risk

Suppose a vendor builds a custom system:

* Vendor A team built it
* Key architects leave
* Documentation is incomplete
* Source code quality is poor
* Framework versions are old

After 8 years:

```
Need new feature

        |
        v

Current vendor:
"Need 2M CNY and 6 months"

        |
        v

Another vendor:
"We need 1 year to understand the code"

        |
        v

Rewrite?
Maybe 5M-20M CNY
```

The original purchase price becomes irrelevant.

---

## 3. Open standards and technology choices matter

Good enterprise software usually has:

### Good signs

* source code access (or escrow)
* standard databases
* REST/gRPC APIs
* Kubernetes/Docker deployment
* common languages
* automated tests
* CI/CD
* documentation
* active community

Example:

Good:

```
Spring Boot
PostgreSQL
Redis
Kafka
React
Kubernetes
OpenTelemetry
```

Harder:

```
Vendor proprietary framework
+
custom database
+
binary plugins
+
unknown middleware
+
no documentation
```

---

## 4. AI helps, but does not solve legacy software

AI coding agents can accelerate:

* understanding code
* generating tests
* refactoring
* documentation
* migration assistance

But AI cannot magically recover:

* missing business requirements
* undocumented rules
* why a strange database table exists
* why a workflow has exceptions

Example:

```
Legacy code:

if(customer.type == 7 && flag == 3)
{
    applyDiscount();
}
```

AI can explain the code.

But:

"Why does type 7 get this discount only on March 15?"

That knowledge may only exist in someone's head.

---

## 5. Good procurement asks different questions

Instead of only asking:

> "How much does this software cost?"

Ask:

### Architecture

* What technology stack?
* Can we deploy ourselves?
* Can we export data?
* Are APIs documented?

### Maintenance

* How many engineers maintain it?
* Average employee tenure?
* Release frequency?
* Security patch process?

### Long-term survival

* Who owns the IP?
* What happens if the vendor disappears?
* Is source code escrow available?
* Can another company maintain it?

### Upgrade path

* How often are major versions released?
* Is migration backward compatible?

---

## 6. Enterprise software should be treated like infrastructure

A good analogy:

Buying software is like buying a house.

Cheap house:

* low price
* bad foundation
* expensive repairs

Expensive house:

* strong foundation
* maintainable structure
* can renovate

Software architecture is the foundation.

---

For a company, a 5M CNY software purchase is not really a 5M decision. It is a **10-15 year technology strategy decision**.

The strongest companies usually prefer:

* smaller modular systems
* open technologies
* internal engineering capability
* replaceable components

because they know:

> The first version is easy. The next 10 years are where the real cost is.
