---
audio: false
generated: true
image: false
lang: en
layout: post
title: Focus on Core Not Tools
translated: false
type: note
---

Question: Why should a Java/Angular engineering team avoid building custom test automation tools (like Selenium wrappers or testing agents) and instead focus on their main application?

Answer:

You've raised very practical and valid points. Let me break this down comprehensively.

---

## The Core Problem: Opportunity Cost

When a focused product team diverts energy into building *tooling around* their main application, they are essentially **starting a second product** — one that competes for the same limited resources.

---

## 1. Your Main Application Still Has Unfinished Work

- A Java/Angular application always has a backlog: new features, performance tuning, security patches, UX improvements, technical debt.
- Every sprint hour spent on a Selenium wrapper is a sprint hour **not spent** closing that backlog.
- The main app is what delivers business value and justifies the team's existence — tooling does not ship to customers.

---

## 2. The "Low User Base" Problem in Large Corporations

- Internal tools built by one team often serve **only that team** — maybe 5–10 people.
- In large orgs, other teams have their own tooling preferences, CI/CD setups, or already-standardized solutions (e.g., company-wide Selenium Grid, Cypress, or cloud testing platforms).
- A tool with no broad adoption is hard to justify maintaining — it becomes **orphaned software** very quickly once the original builder moves on.

---

## 3. Industrial Tools Are the Result of Massive Investment

This is arguably your strongest point:

| Tool | Approximate Age | Backing |
|---|---|---|
| Selenium | 20+ years | Open source, Google, Sauce Labs |
| Playwright | 5+ years | Microsoft, full-time engineers |
| Cypress | 7+ years | Dedicated company, $40M+ funding |
| Jasmine / Jest | 10+ years | Community + Meta (Jest) |

These tools have **hundreds of contributors**, dedicated teams, years of edge-case handling, browser compatibility layers, and documentation ecosystems. A 10-person team cannot realistically replicate even 10% of that quality.

---

## 4. Team Resource Constraints (10 Engineers)

- 10 engineers is enough to deliver a focused product well — it is **not** enough to split attention across two non-trivial codebases.
- Building a robust test tool requires: architecture design, documentation, CI integration, maintenance, bug fixes, onboarding guides, and versioning — essentially a **full product lifecycle**.
- This quietly drains 1–2 engineers who could otherwise be senior contributors to the main app.

---

## 5. Better Alternatives (Use What Exists)

Rather than building, integrate proven tools directly:

- **Selenium / Playwright** — for E2E browser automation in Angular apps
- **JUnit 5 + Mockito** — for Java unit/integration testing
- **Karma + Jasmine / Jest** — for Angular unit tests
- **Cucumber** — for BDD-style acceptance tests
- **Testcontainers** — for Java integration tests with real infrastructure
- **GitHub Actions / Jenkins** — for CI/CD orchestration

These are **production-grade, community-maintained, and free** — combining them covers virtually all testing needs for a Java/Angular stack.

---

## Summary

| Risk of Building Custom Tool | Impact |
|---|---|
| Diverts focus from main product | High |
| Small internal user base | Hard to justify long-term |
| Cannot match industrial tool quality | Technical debt risk |
| Maintenance burden grows over time | Engineer morale + velocity hit |
| Competing with open-source giants | Wasteful and unsustainable |

**The pragmatic decision is clear: use battle-tested open source tools, integrate them well, and keep your 10 engineers laser-focused on shipping a great Java/Angular product.**