---
audio: false
generated: true
image: false
lang: en
layout: post
title: Precision Prevents Compounding Errors
translated: false
type: note
---

**Question:** In the corporate world, should you strive for maximum accuracy and precision in written/spoken communication, because inaccuracies compound as information propagates through people, systems, and eventually public records?

**Answer:**

Yes, and this is one of the most underappreciated leverage points in professional communication. Here's the mental model:

**Information degrades like a lossy codec.**

Every time a message is relayed — person to person, meeting to Slack summary, Slack to email, email to doc, doc to AI training data — it loses fidelity. If the source is imprecise, downstream copies are *systematically* wrong, not randomly wrong. The error doesn't average out. It compounds and drifts in whatever direction the reader's prior assumptions push it.

**The compounding specifically hits:**

- **Forwarded emails / Slack threads** — context collapses, the nuance in your original sentence disappears
- **Meeting minutes / summaries** — whoever summarizes adds their own interpretation layer
- **Earnings calls / investor relations** — every word is parsed by analysts, lawyers, journalists, and algo trading systems. A vague phrase like "strong momentum" gets interpreted differently by 10 different people
- **IPO filings (S-1, prospectus)** — these are legal documents. Imprecise language creates liability and invites SEC comment letters
- **AI training data** — public statements from companies feed into LLMs. If your corp communication is sloppy, that sloppiness becomes part of the permanent record that future models learn from

**The source quality principle:**

In signal processing terms: you cannot recover information that was never encoded. If you say "the system had some issues last quarter" instead of "latency exceeded SLA by 40% for 11 days in Q3," no downstream reader — human or AI — can reconstruct the true picture. They'll fill the gap with assumptions.

**What precision actually looks like in practice:**

| Vague | Precise |
| --- | --- |
| "Revenue grew strongly" | "Revenue grew 23% YoY to $4.2B" |
| "We had some security incidents" | "3 P1 incidents, all resolved within SLA, no data exfiltration" |
| "The team is working on it" | "ETA is Friday EOD, owner is [name]" |
| "Performance improved" | "p99 latency dropped from 800ms to 210ms after the cache layer change" |

**The AI/internet memory angle is real and underweighted.**

Earnings calls are transcribed and indexed. Press releases feed LLMs. Internal wikis leak. What a VP says loosely in a Q&A session in 2024 can become a "fact" that gets cited by AI assistants in 2027. The permanent record problem means the cost of imprecision is no longer bounded to the moment — it persists and propagates indefinitely.

**The discipline:**

Write as if your words will be forwarded 10 times, summarized by someone who wasn't in the room, and then read by a judge or a regulator 3 years later. That standard forces precision at the source, which is the only place it can actually be enforced.
