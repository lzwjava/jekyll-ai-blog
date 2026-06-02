---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Flaws in Engineering Interview Practices
translated: false
type: note
---

Question: What are some unpopular opinions about interviewing for engineering jobs?

Answer:

Here are some genuinely unpopular (but increasingly common among experienced engineers and hiring managers) opinions about the engineering interview process:

- **LeetCode-style algorithmic interviews are mostly theater and correlate poorly with real-world engineering ability.**
  Grinding medium/hard problems for months selects for test-taking stamina and recent prep, not for people who ship reliable systems. Most companies never need you to invert a binary tree on a whiteboard.

- **Take-home projects are usually worse than LeetCode.**
  They consume 10–40 unpaid hours, favor candidates with free time (no kids, no second job), and are often judged superficially by exhausted reviewers. A 4-hour take-home tells you almost nothing compared to a 1-hour pair-programming session.

- **“Culture fit” is responsible for more homogeneity than outright discrimination.**
  People hire clones of themselves and call it culture fit. The result: teams full of 20-30-something extroverted men from the same handful of universities who all listen to the same podcasts.

- **Asking about previous salary or salary expectations early should instantly disqualify the company.**
  It’s a power play designed to anchor low. Good companies pay market rate for the role, not “what you’re willing to settle for.”

- **System-design interviews are cargo-culted nonsense at most non-FAANG companies.**
  Asking a mid-level engineer to design “Twitter at scale” when the company has 200k MAU and runs everything on a single RDS instance is pointless. Real system design is 95% understanding trade-offs in your actual stack, not reciting CDN → load balancer → cache → sharded MySQL.

- **Requiring a degree (or a CS degree) in 2025 is indefensible.**
  The correlation between having a CS degree and being a good engineer approaches zero after ~3 years of experience.

- **Behavioral interviews using STAR format are painful and low-signal.**
  Most candidates rehearse the same three stories. You learn more in ten minutes of casual conversation than in an hour of “Tell me about a time you had a conflict…”

- **Live coding is fine, but whiteboard coding is cruel and unusual punishment.**
  Forcing someone to write bug-free code without autocomplete, documentation, or the ability to run it is artificial. Pair programming on a real IDE (or even a CoderPad/Replit) is vastly superior.

- **Rejecting candidates for one bad interview out of five is lazy.**
  People have off-days. Smart companies use the best signal, not the worst.

- **Most “senior” interview loops are actually testing staff/principal skills.**
  Companies want someone who can already do the job two levels above what they’re hiring for, then pay them as a senior and complain they “lack impact.”

These opinions are unpopular because the current interview industry (bootcamps, LeetCode Premium, coaching, etc.) is a multi-billion-dollar ecosystem that benefits from the status quo. Changing any of this would threaten a lot of business models and egos.

References:

- [The Software Engineering Interview Process Is Broken](https://blog.pragmaticengineer.com/the-software-engineering-interview-process-is-broken/) – Gergely Orosz
- [Why LeetCode-Style Interviews Fail](https://www.honeycomb.io/blog/why-leetcode-style-interviews-fail) – Charity Majors
- [Take-Home Assignments Suck](https://sockpuppet.org/blog/2015/03/06/the-hiring-post/) – Thomas Ptacek
