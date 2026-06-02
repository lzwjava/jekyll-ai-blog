---
audio: false
generated: true
image: false
lang: en
layout: post
title: Code Changes People Resist
translated: false
type: note
---

**Question:** In large corporations and teams, is it true that code is easier to change than people are to persuade — and does this echo von Neumann's idea that mathematics is simple but humans are complicated?

**Answer:**

## Yes — and It's One of the Most Profound Truths in Engineering Culture

### The Von Neumann Quote — What He Actually Said

Von Neumann made this remark as keynote speaker at the first national meeting of the Association for Computing Machinery in 1947. He had argued that computers would need only a small number of instruction types to express all of mathematics — and when the audience laughed skeptically, he responded: *"If people do not believe that mathematics is simple, it is only because they do not realize how complicated life is."*

The point was sharp: math operates by clean, deterministic rules. Human beings — their emotions, politics, habits, and incentives — are far messier systems.

---

### Code vs. People: The Asymmetry in Big Teams

This insight maps perfectly onto the reality of engineering in large organizations:

**Changing code** is a deterministic, reversible, and auditable process. You write a diff, open a pull request, run tests, merge, deploy. The system either accepts the change or it doesn't. There is no ego, no turf war, no loss of face. Code doesn't have a career to protect.

**Changing people** is a completely different problem. Computers don't care if they're running new software. Apps don't mind new code. Assembly lines have no sentimental longings when reconfigured. But humans are different — our routines give us comfort, confidence, and consistency, and significant changes threaten those things. That's why change management is much more about the people than the changing technology or processes.

This asymmetry gets *worse* at scale:

- **Seniority creates calcification.** Senior engineers or managers have often built the very systems you want to change. Changing the code can feel like a personal attack on their judgment.
- **Consensus overhead compounds.** In a small startup, you convince 3 people. In a big corp, you may need sign-off from dozens across different teams, time zones, and incentive structures.
- **Political capital is finite.** Every persuasion attempt costs social capital. Code changes cost compute time and review cycles — far cheaper currencies.

---

### Why Persuasion Fails More Than Pull Requests Do

Studies show that in most organizations, two out of three transformation initiatives fail. Research on change initiatives at 225 companies found consistent correlations between change program outcomes and four hard factors: project duration, integrity of performance (team capability), level of commitment from senior executives, and the additional effort required of employees.

Notice that *none* of these failure factors are about technical correctness — they are all human factors.

The "soft" side of change is actually the harder side. Getting people on board and participating can make the difference between success and failure, because individuals will need to perform their jobs differently — and the degree to which they change their behaviors and adopt new processes has a significant impact on the initiative.

---

### The Deeper Echo of Von Neumann's Insight

Von Neumann's observation was really about **complexity classes**. Mathematics has axioms, rules, and proofs. You can be definitively right or wrong. Human social systems have no such luxury — they are shaped by:

- **Loss aversion**: people fear what they lose more than they value what they gain
- **Status dynamics**: changing a process can implicitly signal that someone's prior work was suboptimal
- **Ambiguity tolerance**: different people have wildly different thresholds for uncertainty
- **Tribal identity**: teams, codebases, and methodologies become identity markers

Code is a formal system. Humans are not. And as von Neumann understood from his work in game theory and automata — *"It is just as foolish to complain that people are selfish and treacherous as it is to complain that the magnetic field does not increase unless the electric field has a curl. Both are laws of nature."*

---

### Practical Implication for Engineering Leaders

This asymmetry is why experienced engineers learn to:

1. **Change the system before changing the culture** — make the right thing the easy thing (e.g., automate code formatting so no one debates it)
2. **Invest in narrative, not just correctness** — being technically right is necessary but not sufficient
3. **Build coalitions first, propose changes second** — the PR comes last, not first
4. **Frame changes as additive, not corrective** — avoid signaling that past decisions were wrong

The best engineers in big orgs are not just good at writing code. They are good at the far harder problem: making other humans want to accept the code.

---

**References:**

- [Von Neumann Quotes — Wikiquote](https://en.wikiquote.org/wiki/John_von_Neumann)
- [The Hard Side of Change Management — HBR](https://hbr.org/2005/10/the-hard-side-of-change-management)
- [Managing Organizational Change — ProductPlan](https://www.productplan.com/learn/managing-organizational-change-change-management-models/)
- [What is Change Management — Prosci](https://www.prosci.com/blog/what-is-change-management-and-how-does-it-work)
