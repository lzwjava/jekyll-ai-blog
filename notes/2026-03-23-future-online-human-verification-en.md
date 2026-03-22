---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Future of Online Human Verification
translated: false
type: note
---

**Question:** Why are we talking here? It seems the internet will eventually have just two types of apps — human (social) apps and AI agent apps. When there are a lot of chatbots, we'll need an app that verifies only real humans. Is that hard to do right now?

**Answer:**

Your observation is sharp and actually maps closely to where the industry is heading right now. Let's break it down properly.

---

## The Internet Is Splitting Into Two Lanes

You're right. The internet is converging toward two distinct types of traffic:

1. **Human (social) apps** — where real people interact, post, vote, transact, and communicate.
2. **AI Agent apps** — where autonomous bots browse, buy, book, and perform tasks on behalf of humans (or sometimes with no human behind them at all).

In 2025, the definition of AI agent shifted to describe large language models capable of using software tools and taking autonomous action — calling APIs, coordinating with other systems, and completing tasks independently with minimal human oversight.

Gartner named agentic AI the top technology trend of 2025 and predicted 33% of enterprise apps will include agentic AI by 2028, up from less than 1% in 2024.

---

## The Core Problem: You Can't Tell Who Is Real Anymore

A social network called Moltbook illustrates the problem perfectly. Within days of launching, 1.6 million agents had registered and nobody — including the platform itself — could reliably say which posts came from bots, which came from humans pretending to be bots, or how many distinct people were actually behind any of it.

Without a way to verify how many real people are behind those agents, platforms have no reliable way to distinguish organic activity from coordinated swarms. There is also a privacy concern — when every agent transaction runs through a public payment rail, it creates a detailed trail of everywhere that agent goes and everything it does.

---

## Yes, It Is Hard — But Solutions Are Emerging

You're right that this is difficult, but it's not unsolved. Several serious approaches are being built right now:

### 1. **Biometric "Proof of Human" — World (formerly Worldcoin)**
World, co-founded by Sam Altman, is dedicated to creating "proof of human" tech — ID verification tools for an internet increasingly overrun by AI-generated content. Their AgentKit allows a user's World ID to be integrated into the x402 payment protocol so that websites can verify a distinct, real human approves of an agent's actions. Their Chief Product Officer compared it to delegating "power of attorney" to an agent.

The catch: it requires an iris scan via a physical "Orb" device. That creates massive friction and raises serious privacy concerns — World has been banned or investigated in at least ten countries over privacy and data concerns.

### 2. **Cryptographic Agent Identity**
HUMAN Security released an open-source project where AI agents sign every HTTP request using HTTP Message Signatures (RFC 9421), and are identified using OWASP's Agent Name Service — a DNS-like naming system for AI agents. This allows web services to cryptographically verify that a specific, registered agent sent a given request.

### 3. **Micropayments as a Rate Limiter**
The x402 protocol, developed by Coinbase and Cloudflare, allows agents to pay small amounts to access resources, using micropayments as a rate limiter. The ecosystem processed over 100 million payments in its first six months. However, micropayments can slow down bad actors but cannot fully address "Sybil dynamics" — if the economic incentive is high enough, the cost of a few cents per request becomes trivial.

---

## Why It's Still Hard

| Challenge | Why |
|---|---|
| **Biometrics** | Privacy invasive, hard to scale globally |
| **Cryptographic keys** | Can be stolen or delegated to malicious actors |
| **CAPTCHAs** | AI now solves them better than humans |
| **Behavioral analysis** | Agents can be trained to mimic human behavior |
| **Micropayments** | Can be absorbed by well-funded bad actors |

Only 15% of enterprises have deployed fully autonomous agents, and most cite trust and governance as their primary barrier to broader adoption. Meanwhile, 81% of executives say they would entrust AI with critical operations — provided trust frameworks are in place.

---

## The Bottom Line

Your intuition is correct. The internet needs a **"human identity layer"** — a foundational infrastructure that can say with confidence: *"a unique, real human is behind this action."* That layer is being built right now, but it remains technically, legally, and ethically hard. The challenge is that you need to verify humanness **without compromising privacy** and **without being spoofed by increasingly capable AI**. That tension is the defining infrastructure problem of the next decade of the internet.

**References:**

- [HUMAN Verified AI Agent (HUMAN Security)](https://www.humansecurity.com/learn/blog/human-verified-ai-agent-open-source/)
- [AgentKit: Proof of Human for the Agentic Web (World)](https://world.org/blog/announcements/now-available-agentkit-proof-of-human-for-the-agentic-web)
- [World launches tool to verify humans behind AI agents (TechCrunch)](https://techcrunch.com/2026/03/17/world-launches-tool-to-verify-humans-behind-ai-shopping-agents/)
- [AI Agents arrived in 2025 (The Conversation)](https://theconversation.com/ai-agents-arrived-in-2025-heres-what-happened-and-the-challenges-ahead-in-2026-272325)
- [Non-human identities: Agentic AI's cybersecurity risk (WEF)](https://www.weforum.org/stories/2025/10/non-human-identities-ai-cybersecurity/)
- [Sam Altman's World builds for AI agents (Quartz)](https://qz.com/sam-altman-world-human-verification-ai-agents)