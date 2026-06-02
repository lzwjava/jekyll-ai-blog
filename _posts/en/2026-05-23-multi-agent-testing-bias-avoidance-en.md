---
audio: false
generated: true
image: false
lang: en
layout: post
title: Multi-Agent Testing Bias Avoidance
translated: false
type: note
---

Yeah, this is a very natural pattern. It maps to several well-established software engineering principles:

1. TDD Red-Green cycle — one "writes code", the other "verifies it passes"
2. Author vs reviewer separation — same reason humans do code review with someone who didn't write the code
3. Defense in depth — the coding agent has blind spots that a separate testing agent can catch

The key insight: when the same agent writes both code AND tests, it unconsciously designs tests that pass. Separate agents break that bias.

Practical workflow:

```
Agent A (coder):  "Implement feature X in module Y"
Agent B (tester): "Review the implementation of X, write comprehensive tests,
                    run them, report failures back"
Agent A (coder):  "Fix the failures Agent B found"
```

In Hermes you can actually orchestrate this with delegate_task:

```
# Stage 1: code
delegate_task(goal="Implement user auth module with JWT", toolsets=["terminal","file"])

# Stage 2: test (separate agent, no context from stage 1)
delegate_task(goal="Review and test /src/auth.py — write pytest tests,
                    run them, identify edge cases, report failures",
              toolsets=["terminal","file"])
```

The separation is especially powerful for:

- Catching overfitting to happy paths
- Finding unhandled edge cases the coder didn't think of
- Security review (tester agent focused on attack vectors)
- API contract verification (tester checks from the consumer's perspective)

This is essentially what Anthropic does internally with Constitutional AI — one model generates, another critiques. And it's what Devin/OpenHands style agents do with plan-then-verify loops.

Want me to set up a concrete workflow or skill for this two-agent pattern in your Hermes setup?
