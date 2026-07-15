---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Crawlers Kill Open Source Revenue
translated: false
type: note
---

Question: What is the news about open-source projects losing revenue because fewer people visit documentation, and how does it connect with Cloudflare saying agent traffic is huge?

Answer:

Yes, this is one of the biggest economic shifts caused by AI agents.

The core problem:

**Before AI agents:**

```
Developer
   |
Google Search
   |
Docs website
   |
Read docs
   |
Maybe click:
- GitHub star
- Sponsor
- Cloud service
- Paid product
```

The website gets:

* page views
* ads
* sponsorship
* conversions
* community growth

---

**After AI coding agents:**

```
Developer
   |
Claude Code / Cursor / ChatGPT
   |
Agent reads docs directly
   |
Answer returned
   |
Developer never opens docs website
```

The documentation is still heavily used, but the **human visit disappears**.

Cloudflare data and related documentation analytics show this shift. For example, Mintlify analyzed documentation traffic and found AI coding agents accounted for about **45% of requests**, almost matching traditional browser traffic. ([Mintlify][1]) Cloudflare also reported that AI-related crawling and non-human traffic are changing the economics of the open web, with AI crawlers consuming content without necessarily sending users back. ([The Cloudflare Blog][2])

---

A simple example:

Old open-source project:

```
100,000 monthly visitors

10% click GitHub Sponsors
1% buy enterprise support

Revenue exists
```

New world:

```
100,000 AI agent requests

0 human page views

$0 sponsor conversion
```

The project becomes:

```
valuable data source
        ↓
used by AI
        ↓
creator receives little value
```

This is similar to what happened to:

* newspapers after search engines
* forums after Stack Overflow
* small blogs after Google snippets

---

The interesting part:

AI agents are actually **more valuable users technically**, but worse economically.

A human:

```
visit 10 pages
read slowly
maybe buy
```

An agent:

```
download entire documentation
extract API details
answer user
leave
```

From the server perspective:

```
requests ↑
bandwidth ↑
value captured ↓
```

Cloudflare explicitly describes this as a broken old exchange: search engines crawled content and returned visitors, while AI systems can consume content and answer users without returning traffic. ([Cloudflare][3])

---

This creates a new business model:

### 1. Docs become machine-readable APIs

Instead of:

```
docs.example.com
```

companies may provide:

```
docs API
MCP server
agent endpoint
```

Example:

```
Human:
"How do I use Stripe webhook?"

Agent:
calls Stripe MCP server

gets structured answer

```

---

### 2. Pay-per-crawl

Cloudflare has been pushing models where content owners can control AI crawler access and potentially require compensation. ([Cloudflare][3])

The future could become:

```
AI agent
    |
    | pay small fee
    ↓
documentation provider
```

Similar to:

```
API call
=
payment
```

---

### 3. Open-source monetization changes

Projects may move from:

```
GitHub stars
+
ads
+
docs traffic
```

to:

```
AI agent adoption
+
enterprise license
+
hosted service
+
usage API
```

For example:

```
Postgres extension

Before:
people read docs

After:
agents recommend it

Winner:
company providing hosted version
```

---

The deeper point:

The internet is moving from:

```
human-readable web
```

to:

```
machine-consumable web
```

The winners may not be websites with the most traffic.

They may be:

```
best structured knowledge
+
best APIs
+
best agent integration
+
strong brand trust
```

For an open-source developer, this is both dangerous and an opportunity:

Danger:

```
AI eats your docs traffic
```

Opportunity:

```
millions of agents know your project
```

The next question is who captures the economic value: the model provider, the infrastructure layer, or the original creator.

References:

* Cloudflare — Content Independence Day / agentic internet economics ([The Cloudflare Blog][2])
* Cloudflare — AI crawlers and broken referral economics ([Cloudflare][3])
* Mintlify — AI agents in documentation traffic analysis ([Mintlify][1])
* Cloudflare — crawl-to-click gap analysis ([The Cloudflare Blog][4])

[1]: https://www.mintlify.com/blog/state-of-ai?utm_source=chatgpt.com "The state of agent traffic in documentation (March 2026)"
[2]: https://blog.cloudflare.com/agentic-internet-bot-report/?utm_source=chatgpt.com "Content Independence Day, one year on: building the business model for the agentic Internet"
[3]: https://www.cloudflare.com/press/press-releases/2025/cloudflare-just-changed-how-ai-crawlers-scrape-the-internet-at-large/?utm_source=chatgpt.com "Cloudflare Just Changed How AI Crawlers Scrape the Internet-at-Large; Permission-Based Approach Makes Way for A New Business Model | Cloudflare"
[4]: https://blog.cloudflare.com/crawlers-click-ai-bots-training/?utm_source=chatgpt.com "The crawl-to-click gap: Cloudflare data on AI bots, training, and referrals"
