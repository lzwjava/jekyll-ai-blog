---
audio: false
generated: true
image: false
lang: en
layout: post
title: Symantec Proxy Block at Bank
translated: false
type: note
---

**Question:** What is this message about?

**Answer:**

This is a **Symantec Web Filter block page** — you're hitting a corporate internet proxy that's blocking a website you're trying to visit.

Your bank employer's network is running **Symantec ProxySG** (a Broadcom/Symantec product), which categorizes web traffic and enforces an internet access policy. When you hit a blocked URL, instead of the actual site, you get this page.

**What's happening technically:**

- Your HTTP/HTTPS traffic is routed through a ProxySG appliance (transparent or explicit proxy)
- Symantec maintains a URL categorization database (e.g., "Social Media", "Hacking Tools", "Personal Storage", etc.)
- Your IT team configured which categories are blocked
- The site you tried to reach falls into a blocked category

**What you can do:**

- Ask IT/Helpdesk to whitelist the specific URL if it's work-relevant
- Use your phone's hotspot for personal browsing (standard contractor practice)
- VPN through your own endpoint if allowed (check your contract — bank networks often prohibit this)

Given you're a contractor at a global bank, this is completely normal. Banks block aggressively — dev tools, GitHub sometimes, AI APIs, even documentation sites. The path of least resistance is mobile hotspot for anything personal or unblocked-but-needed.
