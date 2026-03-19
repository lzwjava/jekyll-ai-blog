---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude API Relay Service for China
translated: false
type: note
---

Question: Given the claude-relay-service GitHub repository README, how do people in China obtain the maximum plan or use reverse channels to distribute the Claude API for others to use? If they are Chinese citizens, how can they purchase the max plan? Do they use virtual telephone numbers or emails to register and pay?

Answer: 

The claude-relay-service is a self-hosted proxy/relay tool that lets users forward requests to Anthropic's official Claude API. It supports adding multiple paid Claude accounts (via OAuth), automatic rotation between them, custom API key generation for each user, usage tracking, and cost-sharing. The service itself does **not** provide Claude access or plans — you must already have valid paid Claude accounts (such as the high-tier "Claude Code Max" subscription) to add them. This setup is popular in China for distributing access because it allows one or a few high-limit accounts to be shared among many users (typically 3–5 people splitting costs) while keeping data on your own server.

### How people in China obtain the "max plan" and distribute access
"Max plan" usually refers to Claude Pro (web/chat) or the higher-tier Claude Code Max / Opus-level access needed for advanced models and higher rate limits in the API. Anthropic does not officially support mainland China, so direct sign-up with a Chinese IP, phone, or card is blocked or fails. Chinese users (citizens or residents) bypass this through a combination of tools and services, then use relay services like claude-relay-service (or similar open-source proxies) to resell or share the access.

Common steps to get a max plan account:
1. **VPN / Proxy**: Connect to a clean US or Canadian node (required for registration and OAuth in the relay setup).
2. **Email**: Use a fresh Gmail or other international email (many buy or self-register one).
3. **Virtual phone number**: Almost always required for SMS verification during Claude.ai or console.anthropic.com registration. Popular platforms include PingMe, 5sim.net, or similar temporary number services (cost ~0.5–2 RMB per verification).
4. **Virtual credit card for payment**: Chinese bank cards are usually rejected. Users top up USDT on platforms like WildCard, Coinepay, or bpay.net to get a virtual US Visa/Mastercard. They then bind this card to subscribe to Claude Pro (~$20/month) or the higher Code Max tier. The card must match a US billing address and be used with a consistent US IP.
5. **Fingerprint browser** (optional but common for safety): Tools like AdsPower keep browser fingerprints and IP consistent to reduce ban risk when managing multiple accounts.

Once the account is active:
- For web/Pro: Log into claude.ai and upgrade.
- For API: Go to console.anthropic.com, bind the virtual card, apply for an API key (pay-as-you-go after approval).

To distribute to others (the "reverse channel" or 逆向渠道 method):
- Self-host the claude-relay-service on a server (recommended US-region VPS).
- Add the paid Claude account(s) via OAuth (may need proxy).
- Generate unique API keys for each customer via the web dashboard.
- Share those keys (or sell access) through WeChat groups, Taobao shops, or forums. Customers pay in RMB (Alipay/WeChat) while the relay owner covers the Anthropic bill.
- Multi-account rotation in the relay helps avoid rate limits and 503 errors.

This is how most Chinese relay operators and resellers operate. Buying ready-made accounts or shared subscriptions from domestic platforms is also common for those who want to avoid the setup hassle.

### Risks and notes
All of these methods technically violate Anthropic's terms of service (no support in China, no account sharing). Accounts can be banned if Anthropic detects mismatched IP, repeated verifications, or unusual usage. The relay README explicitly warns users to accept all risks. Many people rotate accounts or use proxies to minimize detection.

In short, Chinese citizens use exactly the virtual phone numbers, international emails, VPNs, and US virtual cards described above — there is no direct legal way to buy the max plan with mainland credentials. The relay service makes distribution easy and profitable once the master account(s) are obtained.

References:  
- [claude-relay-service README_EN.md](https://github.com/Wei-Shaw/claude-relay-service/blob/main/README_EN.md)  
- [2026 Latest Claude Pro Subscription & Registration Tutorial (Chinese methods)](https://github.com/imarvinle/Claude-Pro)  
- [Claude Pro Payment with Virtual Cards Guide](https://sites.google.com/view/coinepaynet/visa_ka/Claude)  
- [YouTube Tutorial on Safe Claude Registration with Virtual Number & WildCard](https://www.youtube.com/watch?v=vvD2jUZYPgI)  
- [How to Use Claude in Unsupported Countries (VPN + alternatives)](https://writingmate.ai/blog/how-to-use-claude-3-in-unsupported-countries)