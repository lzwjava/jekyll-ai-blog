---
audio: false
generated: true
image: false
lang: en
layout: post
title: Codifying AI for Frontend Design
translated: false
type: note
---

Question: As a frontend developer with ~2 years of Vue/Angular experience, is it correct that good UI/UX design is harder to "codify" into AI skills than code quality, because design is subjective — and should we look at what great frontend looked like 5 years ago before trying to find the right AI skill?Answer:

**Your insight is sharp and largely correct.** Let me break it down systematically.

---

## Your Core Thesis: Why Design Is Harder to Codify Than Code

You're right. Here's why, with precision:

**Code has objective quality signals:**

- Cyclomatic complexity (measurable)
- Coupling/cohesion (measurable)
- Test coverage (measurable)
- Runtime performance (measurable)

**Design quality signals are semi-subjective or context-dependent:**

- While interfaces, devices and interaction models are constantly evolving, the core principles of UX design remain the same — but applying them correctly depends heavily on who your users are and what context they're in.
- Even objective-sounding laws like Fitts's Law (target acquisition time is a function of distance and size) or Hick's Law (decision time increases with number of choices) require judgment about *which* tradeoff to make in a specific situation.

This is exactly why AI skills struggle here — a skill can teach Claude *what* the principle is, but not *which* principle to prioritize in your specific product context.

---

## The "Look Back 5 Years" Approach: Valid, But Incomplete

Your instinct to look at what worked before AI is good, but the real anchor is **timeless principles, not a specific era**. These principles predate AI tools entirely and remain the gold standard:

**Nielsen's 10 Heuristics (NN/g — foundational since 1994, still cited today):**
These include: keeping users informed of system status through feedback, matching the system to the real world, giving users control and freedom, maintaining consistency and standards, preventing errors, and minimizing cognitive load by keeping interfaces free of irrelevant information.

**Laws of UX (the psychological layer):**
Key laws include: Jakob's Law (users prefer your site to work the same way as sites they already know), the Peak-End Rule (people judge an experience based on how they felt at its peak and at its end), and Tesler's Law (for any system there is a certain amount of complexity which cannot be reduced — it can only be shifted).

These are what "good frontend 5 years ago" was built on. They haven't changed.

---

## Why AI Frontend Tools Produce Bad Output

The real problem is **how you prompt**, not just which skill you use:

1. **AI doesn't know your users.** Interaction design requires knowing who uses your product, in what context, with what goals. A generic prompt gets a generic UI.

2. **AI optimizes for visual novelty, not interaction quality.** It will produce a "good-looking" layout that violates Hick's Law (too many choices), Fitts's Law (tiny touch targets), or fails progressive disclosure.

3. **Skills encode patterns, not judgment.** UI principles like clarity, hierarchy, feedback, accessibility, and progressive disclosure are heuristics — tested patterns that, when applied thoughtfully, consistently produce better outcomes. But applying them thoughtfully is exactly what AI struggles to do without explicit guidance.

---

## Practical Improvements: How to Get Better AI Frontend Output

Given your Vue/Angular background, here's what actually works:

### 1. Give AI a Design System Constraint

Instead of: *"build me a dashboard"*
Say: *"build me a dashboard using these constraints: 4px spacing unit, max 3 actions visible at once, all interactive elements min 44px touch target, primary action always bottom-right, error states always red-bordered with inline message"*

AI performs much better when you reduce its design freedom to match real constraints.

### 2. Feed It the Laws of UX Explicitly

Paste specific heuristics into your prompt:

- "Apply Fitts's Law — primary CTA must be large and close to where the user's eye is likely to be"
- "Apply Miller's Law — show no more than 7 items in any list without pagination"
- "Apply Jakob's Law — follow standard e-commerce conventions, don't invent new patterns"

### 3. Use Tailwind + shadcn/ui as Your Baseline

You mentioned Tailwind — it's worth trying. The real power comes from **shadcn/ui** (component library built on Radix UI + Tailwind). It gives AI a constrained, accessible, well-structured component vocabulary. AI that "knows" shadcn/ui generates far more consistent, interaction-correct output than AI designing from scratch.

### 4. Separate Design Phase from Build Phase

Don't ask AI to design and build simultaneously. Instead:

- Step 1: Ask AI to describe the interaction model in words (what happens on hover, click, error, empty state, loading)
- Step 2: Review and correct that description
- Step 3: Ask AI to implement *that specific description*

### 5. Reference Real Products in Prompts

*"The interaction should feel like Notion's sidebar — collapsible, drag-reorderable, keyboard navigable"* gives AI a concrete behavioral target instead of making it guess.

---

## Your Diagnosis Is Correct

To directly validate your conclusion: yes, the reason skills for design are underdeveloped compared to code skills is exactly what you identified — good interfaces feel invisible, but making them invisible requires judgment calls about consistency, visual feedback, and progressive disclosure that are hard to specify as rules. Code has universal standards (DRY, SOLID, O(n) complexity); design's "standards" are contextual and user-dependent, making them harder to encode into a reusable AI skill.

The most productive path: **learn the timeless principles yourself** (Nielsen's heuristics, Laws of UX), then use that knowledge to *constrain and correct AI output* rather than expecting AI to produce good design autonomously.

References:

- [Nielsen's 10 Usability Heuristics — NN/g](https://www.nngroup.com/articles/ten-usability-heuristics/)
- [Laws of UX](https://lawsofux.com/)
- [7 Fundamental UX Design Principles (2026 updated)](https://www.uxdesigninstitute.com/blog/ux-design-principles-2026/)
- [14 Essential UI Design Principles — UXPin](https://www.uxpin.com/studio/blog/ui-design-principles/)
- [Effective UI/UX Design Principles for Front-End Developers — Keitaro](https://www.keitaro.com/insights/2024/06/11/effective-ui-ux-design-principles-for-front-end-developers/)
