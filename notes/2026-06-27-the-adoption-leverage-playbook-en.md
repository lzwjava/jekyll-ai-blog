---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Adoption Leverage Playbook
translated: false
type: note
---

You've got the core dynamic right, but let me sharpen it.

**Yes — adoption is a sales problem, not a quality problem.** A technically superior tool that introduces a new flow loses to a worse tool that fits the existing flow. The other team's calculus isn't "is this better?" — it's "what's the switching cost vs. my current pain?" If their pain is low or tolerable, your tool's marginal benefit has to clear a high bar, and it rarely does when they have higher-priority work. You're competing against their roadmap, not against the absence of your tool.

**The "desperate" insight is the key one, but refine it.** It's not desperation exactly — it's *acute, owned pain*. Three conditions make adoption easy:

1. **The pain is theirs, not yours.** You think their flow is dumb; they don't care. Adoption happens when *they* already feel the pain and are looking for relief.
2. **Your tool drops into their existing flow** — no new flow to learn. Best case: it's invisible. A wrapper, a CI step, a library call, not a new CLI they have to context-switch into.
3. **You absorb the integration cost.** "I'll set it up for you, here's the PR" beats "here are the docs." Desperate teams will tolerate friction; non-desperate teams won't tolerate any.

**On "people find the easiest path"** — mostly true, with a correction that matters for you: people minimize *perceived effort under their current mental model*, not actual effort. Learning your tool might save them 10 hours/week but costs 2 hours upfront — and the 2 hours is concrete and now, while the 10 is abstract and later. Humans discount that heavily. This is why even strictly-better tools fail to spread. The easiest path is usually "keep doing what I'm doing," because change has an activation energy that the status quo doesn't.

**The strategic takeaway for big-corp tool-building:**

- Don't build tools and hunt for adopters. That's push, and push fails. Find a team already screaming about a problem, then build *for that specific pain*. Pull beats push.
- Make adoption a one-line diff or a Slack-bot they already see, not a migration.
- If you have to *convince* people, you've already lost. The good ones get pulled in.
- Honestly — for your situation, the highest-leverage version is to build the tool for *yourself* first, use it to ship faster than everyone else, and let curiosity pull people in ("how did you do that so fast?"). Your own velocity is the demo. That's also resume/startup-portfolio fuel, unlike internal tools that die when you leave.

One reframe worth sitting with: internal tools rarely compound for *you* unless they're open-sourceable or become public artifacts. A tool that only lives inside the bank evaporates when your contract ends. Build things where the leverage follows you out the door.
