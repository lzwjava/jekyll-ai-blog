---
audio: false
generated: true
image: false
lang: en
layout: post
title: Re-check Prompt Effectiveness
translated: false
type: note
---

I think you may have meant to paste more context, or this is a continuation of something I don't have. Let me make sure I'm tracking what you mean before responding.

From what I can parse: you're saying that in **hermes-agent**, you use a re-check prompt (like literally asking the AI "really?" or "check again") as a verification step, and you've found it genuinely effective.

If that's the gist, I agree, and there's a real mechanism behind why it works. A short re-check prompt like "really? verify this" forces a second forward pass conditioned on the agent's own prior output now sitting in context. That second pass isn't bound by the commitment the model made in the first pass — it can attend to the earlier tokens as *claims to evaluate* rather than *a direction to continue*. This is the same reason self-consistency, reflexion, and verifier-style loops work: you're decoupling generation from verification, and the verification step has strictly more information (the candidate answer) than the generation step did.

A few things that make it more reliable in an agent loop:

- **Make the re-check adversarial, not polite.** "Find the bug in the above" beats "is this correct?" The latter has a yes-bias; models tend to agree with themselves. Framing it as "assume this is wrong — where?" flips the prior.
- **Give it a concrete check target.** "Re-verify the IP ranges and the team ID handling specifically" outperforms a generic "check again," because you're directing attention rather than hoping it re-reads everything.
- **Separate the verifier's context if you can.** A fresh sub-agent that only sees the artifact (not the reasoning that produced it) catches more, since it isn't anchored to the original chain of thought.

That said — and this is where I'd push back if you're leaning on it as a primary correctness guarantee — a single "really?" can also flip a *correct* answer to a wrong one, because the model reads the implied skepticism as a signal it erred. If you measure it, you'll sometimes see regression on already-correct items. The clean fix is to ask for a *justification or a diff*, not a verdict: "list what's wrong, or output UNCHANGED if nothing is." That makes the no-op path explicit and cheap.

Is hermes-agent yours? If you tell me how the re-check is wired in (single prompt vs. sub-agent, what it's checking, whether you parse a structured verdict), I can suggest something concrete to harden it.
