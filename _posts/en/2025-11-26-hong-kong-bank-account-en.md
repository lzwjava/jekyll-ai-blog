---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Hong Kong Bank Account Required
translated: false
type: note
---

Yes, for **Local Electronic Transfer (HKD via FAST)** from Interactive Brokers (IBKR) to work smoothly and without extra correspondent bank fees, **your receiving bank account must be a Hong Kong bank account** (in your own name.

### Key requirements for this withdrawal method

- **Bank location**: Hong Kong (not mainland China, not offshore accounts)
- **Currency**: HKD account (most HK banks give you a multi-currency account that includes HKD)
- **Account holder name**: Must exactly match your IBKR account name (since you are a Chinese citizen, the name on the HK bank account should be your Chinese name or the exact same English name as on your IBKR account)
- **Supported banks**: Almost all major Hong Kong banks work perfectly with IBKR’s FAST transfer, including:
  - HSBC (including HSBC One)
  - Hang Seng
  - Bank of China (Hong Kong)
  - Standard Chartered
  - Citibank HK
  - DBS Hong Kong
  - ZA Bank, Mox, WeLab Bank, Airstar, etc. (virtual banks also work)
  - Even FPS (Faster Payment System) via mobile number or email works for many virtual banks

### What does NOT work with “Local Electronic Transfer (FAST)”

- Mainland China bank accounts (e.g., ICBC China, Bank of China mainland, Alipay, WeChat Pay, UnionPay cards, etc.) → IBKR will reject or route as international wire with ~USD 20–40 fee and 3–7 days
- Overseas accounts in other countries

### Since you use Tiger Trade (Tiger Brokers)

Many Chinese citizens who use Tiger Brokers also open an IBKR account. The most common and cheapest solution is:

1. Open a Hong Kong bank account remotely or in person (HSBC HK, Standard Chartered HK, ZA Bank, Mox etc. all allow mainland Chinese citizens to open accounts, some fully online with Chinese ID).
2. Add that HK bank as “Local Electronic Transfer” withdrawal method in IBKR → first withdrawal free every month, subsequent ones only HKD 8.
3. Money arrives in 1–3 business days (often same day or next day).

If you don’t have a Hong Kong bank account yet and only have mainland Chinese bank cards, you will be forced to use **international wire transfer (SWIFT)**, which costs around USD 20–40 per withdrawal + possible intermediary bank fees + slower (3–7 days).

Summary: Yes, only Hong Kong bank accounts work for the cheap/fast “Local Electronic Transfer”. Mainland Chinese accounts are not supported for this method.
