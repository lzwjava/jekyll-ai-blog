---
audio: false
generated: true
image: false
lang: en
layout: post
title: Blocked After Grok-CLI Setup
translated: false
type: note
---

Question: How do you think about a Chinese user being blocked from grok.com right after getting the grok-cli tool setup?

Answer: It is incredibly frustrating to hit a sudden block right after getting a tool like `grok-build` configured and integrated into your workflow.

The "Sorry, you have been blocked" message on grok.com usually comes down to automated network security systems (like Cloudflare) triggering on specific traffic patterns. When accessing the service from China, routing changes, VPN server switches, or high-frequency API/CLI requests can easily trip these security protocols, causing a temporary or permanent IP block.

If you want to try and get around the block, you can adjust your proxy rules to use a cleaner, less crowded residential IP, clear your browser cookies, or switch to an alternative platform that offers stable access to the Grok API models through regional developer platforms.
