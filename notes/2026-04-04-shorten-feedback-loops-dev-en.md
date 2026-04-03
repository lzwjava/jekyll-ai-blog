---
audio: false
generated: true
image: false
lang: en
layout: post
title: Shortening Feedback Loops in Development
translated: false
type: note
---

Question: Is shortening the feedback loop in software development by preferring local tests over server tests, simple logs over full debugging, unit tests over integration tests, verifying small pieces incrementally, and using UAT/SIT tests over finding bugs in production the right approach? Also, are production bugs often simple cases rather than complex issues like deadlocks?

Answer:

Yes, you are largely right. Shortening the feedback loop is one of the most effective ways to speed up software development and improve overall quality. The principles you listed align well with modern best practices in agile, DevOps, and test-driven development (TDD). Here's a clear breakdown:

### Why shorter feedback loops matter
The faster you can write code → run it → see the result → fix issues, the quicker you learn and iterate. Long loops (waiting for Jenkins builds, deploying to test environments, or discovering bugs only in production) waste time and mental energy. Each extra hour of delay compounds across a project.

### Your specific preferences explained

- **Prefer local instead of Jenkins/server tests**  
  Correct. Running tests locally is almost always faster and more reliable for quick iteration. You avoid network latency, queue times, and environment differences. Use CI/CD (like Jenkins) for validation and gatekeeping, not for daily development feedback.

- **Prefer simple logs instead of full debugging**  
  Often true for initial investigation. Printing key values with logs is quick and low-overhead. It helps you understand flow without pausing execution. However, use a proper debugger when logs aren't enough (e.g., complex state, multi-threaded code, or when you need to step through logic). The key is starting simple and escalating only when needed.

- **Prefer unit tests instead of integration tests**  
  Yes, for speed. Unit tests are fast, isolated, and easy to run frequently (often in milliseconds). They give immediate feedback on individual components. Integration tests are slower and flakier due to external dependencies, so run them less often (e.g., in CI). A good test pyramid has many unit tests at the base and fewer, broader integration/E2E tests higher up.

- **Verify small, verify a bit and a bit (incremental verification)**  
  This is excellent advice. Breaking work into tiny, verifiable pieces follows the "make it work, make it right, make it fast" mindset. It reduces cognitive load and catches issues early before they compound.

- **Prefer UAT/SIT tests instead of prod bugs**  
  Absolutely. User Acceptance Testing (UAT) and System Integration Testing (SIT) are designed to catch problems in a controlled environment before they reach real users. Finding bugs in production is the most expensive and painful feedback loop — it affects customers, requires hotfixes, and damages trust. Shift-left testing (testing earlier in the cycle) is a core principle for this reason.

### Production bugs: often simple, not complex?
Yes, you're right in many cases. A surprisingly large percentage of production incidents are caused by simple bugs:
- Off-by-one errors
- Null pointer/reference issues
- Wrong configuration values
- Missing edge cases that seemed "unlikely"
- Typos or copy-paste mistakes
- Incorrect assumptions about data formats or business rules

Complex issues like deadlocks, race conditions, or memory leaks do happen, but they are usually less frequent than basic logic or integration mistakes. Simple bugs often slip through because developers assume "it will be fine" or skip thorough local verification. Production exposes the gaps between what we thought would happen and reality (different data volumes, user behaviors, timing, etc.).

That said, production can still reveal truly hard problems (scalability, distributed system failures, third-party service quirks). The goal is to minimize the simple ones so your team has bandwidth to handle the complex ones properly.

### Practical tips to shorten the loop even more
- Write code in very small increments (e.g., 5-15 minutes of changes) and test immediately.
- Use hot-reload / live-reload features in your IDE/framework.
- Automate as much local validation as possible (pre-commit hooks, linting, fast test suites).
- Keep your local environment as close as possible to production (containers, Docker, etc.).
- When a bug reaches prod, treat it as a process failure: ask "why didn't our local/unit/UAT catches this?" and improve the earlier loops.

Overall, your approach promotes faster learning, higher quality, and less stress. Teams that master short feedback loops ship better software more quickly. The key is balance — use the right tool for the situation rather than dogmatically avoiding debugging or integration tests entirely.

References:  
- None