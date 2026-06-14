---
audio: false
generated: true
image: false
lang: en
layout: post
title: CTExcel China UK MVNO Guide
translated: false
type: note
---

The page renders entirely client-side JS — no static content came through. Let me search for what's on that page.**Question:** Intro to CTExcel UK (ctexcel.com/uk/home) — what is it, how does it work, key plans and features?

**Answer:**

The page is a client-side JS app that doesn't render statically, but between the official docs and the NodeLoc community thread, here's a solid picture:

---

## CTExcel UK — China Telecom's UK MVNO

**What it is:** CTExcel is China Telecom International's (CTG) brand launched in the UK in 2012, targeted specifically at Chinese students, tourists, and business visitors, aiming to provide affordable communications between China and the UK. It operates on EE, one of the UK's main networks.

It's an MVNO (Mobile Virtual Network Operator) — CTExcel doesn't own towers, it leases from EE in the UK and hands off to China Telecom's domestic network when you're in China.

---

## The Core Value Proposition

**China + UK shared data pool.** The data allowance is shared between China and the UK — UK plan data can be used in mainland China. This is the key differentiator. Most SIMs charge heavy roaming fees when crossing the border. CTExcel treats both countries as part of the same data bucket.

This also means: when you're in China using CTExcel data, your traffic egresses through the UK carrier — bypassing the GFW. Google, GitHub, HuggingFace, etc. work without a VPN.

---

## Key Features

- Roams on China Telecom 4G/5G in mainland China
- Supports WiFi Calling
- Supports iMessage
- UK +44 number (10 digits)
- eSIM supported: first physical→eSIM conversion is free; subsequent eSIM→eSIM swaps cost £3 each

---

## Costs

**Account fees:**

- Activation fee: £9.9 (one-time)
- Monthly fee: £0 (zero monthly charge)
- Number retention: just trigger a balance change within 180 days — e.g. top up, or send one SMS (£0.1)

**Mainland China roaming rates (pay-as-you-go, no plan):**

- Outgoing calls: £0.2/min (~¥1.90)
- Incoming calls: £0.05/min (~¥0.47)
- Outgoing SMS: £0.1/message (~¥0.95)
- Incoming SMS: free
- Data: £0.005/MB (~¥0.047) — roughly £5/GB

The PAYG data rate in China is expensive (£5/GB), so you'd want to buy a bundled plan (like the 50GB annual plan) rather than use raw roaming rates.

---

## Activation Constraint

Activation cannot be done in mainland China — you must activate it in the UK or Europe first, before it can be used in mainland China. This is the main friction: you either activate it yourself when traveling to the UK/EU, or buy a pre-activated SIM from a reseller (common on Telegram/NodeLoc, typically ~35 USDT with £5 credit).

---

## Who It's For (for you specifically)

If you're in Guangzhou and want clean international internet access without running a VPN server:

- Get a pre-activated CTExcel SIM/eSIM from a reseller
- Install on your iPhone (eSIM, no physical card needed)
- When in China, your data routes through EE UK → exits GFW cleanly
- 50GB annual plan covers reasonable usage for API calls, GitHub, docs, etc.

**References:**

- [NodeLoc: CTExcel UK eSIM detailed breakdown](https://www.nodeloc.com/t/topic/65188)
- [CTExcel Global About](https://www.ctexcel.com/global/globalBusiness-en.html)
