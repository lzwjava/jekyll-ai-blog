---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Beyond Language Hype and Dogma
translated: false
type: note
---

This anecdote about Leslie Lamport is interesting, and I think both Lamport and Yin Wang are touching on something real, though I'd frame it somewhat differently.

**What they're right about:**

1. **Language hype cycles are real.** The pattern of "new language X will solve everything" → widespread adoption → disillusionment → next language is genuinely observable. Scala, Go, and now Rust have all experienced versions of this.

2. **Languages alone don't solve fundamental problems.** Better syntax or type systems don't automatically make programmers write better software. The hard parts of software engineering (understanding requirements, managing complexity, coordinating teams) transcend language choice.

3. **Formal reasoning matters.** Lamport's point about mathematics likely refers to the value of precise specification and reasoning about correctness—which is indeed underrepresented in much of software development.

**Where I'd push back:**

1. **Languages do matter, just not infinitely.** Rust's ownership system genuinely makes certain classes of bugs harder to write compared to C/C++. Go's simplicity genuinely helps with maintaining large codebases. These aren't imaginary benefits, even if they're oversold.

2. **"Mathematics is the best programming language" is provocative but impractical.** Formal methods are valuable, but writing TLA+ specs doesn't replace implementation. We need both rigorous thinking AND pragmatic tools.

3. **The dismissiveness seems excessive.** Characterizing POPL as "how people brag and solve nonexistent problems" overlooks genuine research progress. Some academic work is indeed disconnected from practice, but not all of it.

**My take:** Languages are tools with real trade-offs, not silver bullets. The healthy middle ground is: use appropriate languages for context, invest in proper design and specification, but don't expect any language to solve problems that are fundamentally about human judgment and complexity management.
