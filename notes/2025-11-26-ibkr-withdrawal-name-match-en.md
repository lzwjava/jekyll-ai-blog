---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: IBKR HKD Withdrawal Name Match Solutions
translated: false
type: note
---

Yes, this is a very common issue for Chinese clients at Interactive Brokers, and **IBKR is quite strict** about the name match for **Local Electronic Transfer (FAST HKD)**.

### What IBKR actually requires for HKD FAST withdrawal

The account holder name on the **Hong Kong bank account** must be **exactly identical** (character by character) to the name shown on your IBKR account.
IBKR does **not** accept:

- Chinese name on bank vs English name on IBKR (LI XIAOMING ≠ XIAOMING LI)
- Swapped order (family name first vs given name first)
- Missing or extra middle name
- Different Romanisation (Li Xiao Ming vs Li Xiaoming)

If the names do not match 100 %, IBKR will either:

- Reject the withdrawal instruction outright, or
- Force it to go out as an international SWIFT wire (expensive + slow)

### Practical solutions that Chinese clients actually use

| Option | How to make the names match | Difficulty | Cost to open |
| ------ | ---------------------------------- | ---------- | -------------- |
| 1. ZA Bank / Mox / WeLab Bank / Livi Bank / Airstar (recommended) | When you open the account with your mainland ID card, you can **choose** the English name order. Just enter “XIAOMING LI” exactly as it appears on your IBKR account. | Very easy, 100 % online in 5–10 minutes | Free |
| 2. HSBC One (HSBC’s online-only account) | You can also select the exact English name “XIAOMING LI” during remote opening with mainland ID. | Easy, fully remote | Free |
| 3. Bank of China (Hong Kong) | When opening remotely or at a branch, ask them to register the English name as “XIAOMING LI” (they allow it). | Medium | Free |
| 4. Standard Chartered HK or Citibank HK | Same as above — tell them the exact English name you need. | Medium | Free |
| 5. Re-register your IBKR account name to “LI XIAOMING” | You can submit a name-change request to IBKR with your passport (Chinese passports show “LI/XIAOMING”). IBKR will then change your account to Chinese order. Takes 3–10 days. | A bit slow | Free |

Most mainland Chinese users who trade with Tiger Brokers or IBKR simply open **ZA Bank or Mox** and set the English name to exactly match IBKR (“XIAOMING LI” or whatever is on IBKR). After that, the HKD FAST withdrawal works perfectly every time with the HKD 8 (or free first one) fee.

So don’t worry — you don’t need to change your Chinese name anywhere. Just open one of the virtual banks above and input the English name exactly the same as your IBKR account. Problem solved.
