---
audio: false
generated: true
image: false
lang: en
layout: post
title: Selling Claude VPN Service Breaks Laws
translated: false
type: note
---

**Question:** Is selling a Claude/OpenClaw deployment service on Xianyu (闲鱼) to individual users in China — where you also help users install a VPN/proxy tool like Clash or Hysteria — a violation of the law?

**Answer:**

## Short Answer: Yes — This Business Model Violates Multiple Laws Simultaneously

This scenario stacks **at least three separate legal risks** on top of each other. Let's break them down one by one.

---

## Risk Layer 1: Selling the VPN/Proxy Setup (Clash / Hysteria)

This is the most serious and most directly prosecutable layer.

Under current law, VPN providers can be prosecuted in China under Supreme Court Guidelines on computer crimes. Providing a type of VPN in a way that severely disrupts the telecommunications market constitutes the offense of unlawful business operations.

Even helping individual users install unauthorized proxy software for a fee counts as "providing" VPN services — which is illegal. Real prosecutions have happened at exactly this scale:

- Wu Xiangyang was fined 500,000 yuan (US$76,000) and jailed for 5½ years for running a VPN service without the proper licence, after providing software and modified routers to help people access foreign websites restricted in China. He sold to roughly 8,000–13,000 users — but the law doesn't set a minimum user threshold.
- A Shanghai developer received a suspended jail term for selling VPN services to hundreds of people, found guilty of hacking-related offenses.
- A separate individual was sentenced to nine months in prison specifically for selling VPN apps.

**500 users in one month is not a small scale — this is clearly commercial activity**, and Chinese courts have prosecuted people at far smaller scales.

---

## Risk Layer 2: Reselling Claude/AI API Access on Xianyu

This is a grey-market activity that is already widespread but also increasingly targeted:

Mirror sites (中转站) procure model access from Anthropic's official API platform using phone numbers and payment methods from a supported region, then resell access to users in China. A "direct connection" Claude Pro account from a mirror site can be found for as low as 65 RMB per month, while transferred API is usually sold at a 70–90% discount compared to official prices.

From Anthropic's side, this is a clear **Terms of Service violation**. Anthropic's Terms of Service prohibit use of their services in certain regions due to legal, regulatory, and security risks, and companies subject to control from authoritarian regions like China face legal requirements that can compel them to share data, cooperate with intelligence services, or take other actions that create national security risks.

Anthropic has identified that actors bypass geofencing and business restrictions that limit Claude's commercial availability in China by routing traffic through proxy services that resell access to major Western AI models. Anthropic actively detects and bans these operations, and has been escalating enforcement.

From China's domestic side, there is also a growing risk: In China, AI applications for the domestic market rely almost exclusively on local models, as the government has not approved any foreign large language models for Chinese users. This means distributing access to unapproved foreign AI models to the public could itself attract regulatory attention from the Cyberspace Administration of China (CAC).

---

## Risk Layer 3: Platform Risk — Xianyu (闲鱼) Itself

Xianyu is operated by Alibaba. Selling VPN tools, proxy setups, or access to blocked foreign services on Xianyu is against the platform's own rules and is monitored. Wu Xiangyang originally set up his VPN business on Taobao (Xianyu's parent ecosystem) — and was still prosecuted. Selling on these platforms does not provide cover — it actually creates a documented, traceable commercial record that authorities can use as evidence.

---

## Summary of Legal Exposure

| Activity | Legal Risk | Severity |
| --- | --- | --- |
| Installing Clash/Hysteria for users for a fee | Selling unauthorized VPN service — Criminal Law §225 | **Very High — Prison + Fines** |
| Reselling Claude API access | Unauthorized telecom operations + Anthropic ToS violation | **High — Account bans + potential prosecution** |
| Distributing unapproved foreign AI to Chinese users | CAC foreign AI content regulations | **Medium-High — Fines, platform shutdown** |
| Selling on Xianyu publicly | Creates evidence trail; violates platform rules | **Amplifies all above risks** |

---

## Practical Reality

This type of business is common in China's grey market — sellers use a range of strategies to appeal to consumers with different priorities: cost, convenience, privacy, and technical needs. Many operate for months or years without prosecution. However, enforcement is **unpredictable and selective** — when authorities do act, penalties are severe and retroactive. The more users you have, the more revenue you generate, and the more visible you become — all of which increase the chance of being targeted.

In short: **this business model is illegal on multiple fronts in China**, and 500 users/month is substantial enough to be treated as a serious commercial operation rather than a personal-use grey area.

**References:**

- [How US Models Are Sold in China's Grey Market — ChinaTalk](https://www.chinatalk.media/p/the-grey-market-for-american-llms)
- [Anthropic Updating Regional Restrictions](https://www.anthropic.com/news/updating-restrictions-of-sales-to-unsupported-regions)
- [Man Jailed 5½ Years for Selling VPN — SCMP](https://www.scmp.com/news/china/policies-politics/article/2125326/man-jailed-51/2-years-fined-us76000-selling-vpn)
- [Chinese Programmer Punished for Selling VPN — CNN](https://www.cnn.com/2018/10/10/asia/china-vpn-censorship-intl)
- [Internet Censorship in China — Wikipedia](https://en.wikipedia.org/wiki/Internet_censorship_in_China)
- [Anthropic's Impact on Chinese Claude Users — Yahoo/SCMP](https://www.yahoo.com/news/articles/impact-anthropics-china-ban-unlikely-093000589.html)
