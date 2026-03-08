---
audio: false
generated: true
image: false
lang: en
layout: post
title: Avoid Over-Engineering With Simple Rules
translated: false
type: note
---

Question: What does the "防止过度工程" (Preventing Over-Engineering) section of Wang Yin's "The Wisdom of Programming" say?

Answer:

## Preventing Over-Engineering

Wang Yin opens by acknowledging something ironic: even though everyone knows over-engineering is bad, engineers still fall into it repeatedly — himself included. So he analyzes the early warning signs so you can catch and avoid it before it takes hold.

---

### Warning Sign #1: Obsessing Over the Future

The first major signal is when you start thinking too much about things that haven't happened yet. Examples he gives:

- "If we someday have millions of lines of code and thousands of engineers, this tool won't scale."
- "I might need this feature in the future, so I'll write the code for it now and leave it there."
- "Many people will extend this code later, so I should make it reusable right now."

This is precisely why so many software projects become so complex. In reality, not much has actually been accomplished, but the codebase is bloated with unnecessary complexity added in the name of "the future." The immediate problem hasn't even been solved yet, yet the project has already been crushed under the weight of hypothetical future concerns.

His point: sometimes in real engineering, you need to focus close — solve the problem in front of you first, then talk about future extensibility.

---

### Warning Sign #2: Obsessing Over Code Reuse

The second source of over-engineering is excessive concern about reusability — before you've even written working code. Trying to make code reusable too early leads to building elaborate frameworks that tie your own hands, and you end up failing to write even a basic working version. If you can't write working code in the first place, what's the point of making it "reusable"?

He notes that many projects built around reusability from day one end up completely abandoned — because other developers find the code too hard to understand, and find it easier to just rewrite from scratch.

---

### Warning Sign #3: Obsessing Over Testing

Excessive focus on testing can also cause over-engineering. Some developers contort otherwise simple code into "test-friendly" shapes, introducing so much complexity that the code — which could have been written correctly in one pass — ends up riddled with bugs.

He makes a memorable distinction between two kinds of "bug-free" code:

- **"Code with no obvious bugs"** — complex, heavily tested, lots of coverage metrics, and we *assume* it's correct because the tests pass.
- **"Code that is obviously bug-free"** — so simple and direct that even without many tests, you can look at it and immediately know it can't be wrong.

He clearly prefers the second kind.

---

### His Three Principles to Prevent Over-Engineering

He summarizes everything into three concise rules:

1. **Solve the problem at hand first, and solve it well — then think about future extensibility.**
2. **Write working code first, refine it repeatedly — then consider whether reuse is even necessary.**
3. **Write working, simple, obviously-bug-free code first — then consider testing.**

---

The underlying philosophy throughout this section is consistent with the rest of the article: **simplicity is a virtue, and premature complexity — regardless of how forward-thinking it sounds — is still a form of failure.**

References:

- [稀土掘金 mirror of 编程的智慧](https://juejin.cn/post/6844903424572538887)