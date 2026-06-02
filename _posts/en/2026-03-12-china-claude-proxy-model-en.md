---
audio: false
generated: true
image: false
lang: en
layout: post
title: China Claude Proxy Sharing Model
translated: false
type: note
---

Question: What is a "Claude Code mirror" service, especially in China? Specifically, the distribution model where it acts like a proxy/relay server — where one person buys a Max plan and shares it with many others?

Answer:

## What Is a "Claude Code Mirror" in China?

### Background: Why It Exists

Claude (and Claude Code) is **officially blocked in mainland China**. Anthropic does not support Chinese payment methods, Chinese IP addresses are often rejected, and starting from September 5, 2025, Anthropic officially announced a policy banning all "Chinese-controlled companies" from using Claude services, including API and Web products. This created a large grey market of workaround services.

---

### What Is a "Claude Code Mirror"?

A **Claude Code mirror** (also called "CC mirror", 镜像服务, or relay service) is a **third-party proxy/relay platform** that sits between Chinese users and Anthropic's official servers. These are third-party platforms providing Claude Code mirror access for developers in China, offering an API-compatible service layer for stable access — with no official authorization from Anthropic.

The key mechanism: the mirror service **intercepts your API requests** and forwards them to Anthropic on your behalf, using servers hosted in compliant regions (outside China). Users simply change their `ANTHROPIC_BASE_URL` environment variable to point to the mirror instead of Anthropic's servers directly.

---

### The "Bus" / Shared Pool Model (拼车 / 合租)

Your "bus" analogy is spot-on. This is colloquially called **拼车 (carpooling)** or **合租 (shared rental)** in Chinese developer communities. Here's how the business model works:

**The operator's side:**
- Someone purchases a Claude Max plan ($100–$200/month) or an Anthropic API key
- They deploy a reverse proxy / relay server (tools like `claude-relay-service` or custom API gateways)
- They resell access to many users, charging per-token or via a subscription fee in RMB
- The operator collects revenue from many people and uses it to cover the official plan cost, keeping profit on top

**The user's side:**
- Users pay in RMB (Chinese yuan) — often around 200–300 RMB/month
- These mirror sites often allow registration with a regular email address, bypassing the need for foreign phone numbers or addresses, and pricing is usually presented in RMB. For instance, plans around 359 RMB/month for standard use may be offered, which can be more cost-effective than direct conversion and fees.
- Users get an API endpoint + API key, and just set `ANTHROPIC_BASE_URL` to the mirror's URL

**The relay service infrastructure:**
Open-source tools like `claude-relay-service` act as a middleware layer that forwards requests while managing authentication, routing, and cost-sharing scenarios. The system is particularly useful for teams or communities that want to pool access or simplify integration with different AI backends.

---

### Types of Services in This Ecosystem

There are several distinct models:

| Type | How It Works | Risk Level |
|---|---|---|
| **Official API reseller** | Buys Anthropic API credits, resells at markup | Medium |
| **Subscription sharing (Max pooling)** | One Max plan shared among many users | High — violates ToS |
| **Third-party reverse-engineered** | Uses technical exploits/unofficial endpoints | Very High |
| **VPN + direct access** | User configures VPN proxy themselves | Lower, but still restricted |

---

### Legal & Risk Issues

This is the critical part:

1. **Violates Anthropic's Terms of Service** — Sharing a subscription account or reselling API access without authorization is explicitly against the ToS. In the second half of 2025, multiple Claude reseller services shut down due to Anthropic's strengthened risk control, causing significant losses for prepaid users.

2. **Account bans** — Anthropic has multi-layer detection mechanisms checking IP addresses, DNS leak locations, browser fingerprints, and device fingerprints. Mainland China IP ranges are rejected, and data center IPs or shared VPN IPs are flagged as high risk.

3. **Operator disappearance risk** — Over 60% of third-party Claude reverse engineering services that emerged in 2025 shut down or disappeared within 3 months of operation. Users who prepaid lose their money.

4. **Security risk** — When you route all your code and prompts through a third-party relay, that operator can potentially log your code, API calls, and data.

5. **China policy** — Third-party reverse-engineered services use technical loopholes to provide unofficial services, violating Anthropic's terms of service, and can be banned at any time.

---

### Legitimate Alternatives for Chinese Developers

- **VPN + direct official account** — Use a residential IP VPN (not data center), pay with a virtual international card like WildCard. Tools like Clash with a proxy server outside China work; you just need to configure `HTTPS_PROXY` environment variables in your shell so the Claude Code CLI and terminal correctly route through the proxy.
- **Pay-as-you-go API via compliant platforms** — Some platforms like apiyi.com deploy servers in compliant regions and provide Claude API access legally at pay-per-use rates, which can be cheaper for light users.
- **Anthropic official Team/Enterprise plans** — These offer more flexibility for organizations.

---

### Summary

A "Claude Code mirror" in China is essentially a **paid relay proxy service** that solves access and payment barriers. The "bus/pooling" model specifically refers to operators pooling many users onto one or a few accounts/API keys, billing users in RMB at a markup. While popular and practically useful, these services carry **real risks**: ToS violations, account bans, operator fraud, data security issues, and instability.

References:

- [How I Got Claude Code Working in China](https://gist.github.com/docularxu/aa321d6bc4cfe3abde3c098ee42f9908)
- [Lumecoder: Claude Code Mirror (China Direct)](https://lumecoder.com/claude-code-mirror)
- [Claude Code Subscription Purchase Guide for China (apiyi.com)](https://help.apiyi.com/en/claude-code-subscription-purchase-guide-en.html)
- [Claude Account Ban Solutions for China Users 2025 (apiyi.com)](https://help.apiyi.com/claude-account-ban-solutions-china-users-2025-en.html)
- [Navigating Claude's Payment Maze from China (Oreate AI)](https://www.oreateai.com/blog/navigating-claudes-payment-maze-your-guide-to-subscribing-from-china/36e37a9f66d4f611b269f61d2c8e836d)
- [Claude Relay Service (SourceForge mirror)](https://sourceforge.net/projects/claude-relay-service.mirror/)
- [Fix: Claude Code 403 in China (GitHub Issue)](https://github.com/anthropics/claude-code/issues/30318)
