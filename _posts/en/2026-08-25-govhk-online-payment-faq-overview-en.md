---
audio: false
generated: true
image: false
lang: en
layout: post
title: GovHK Online Payment FAQ Overview
translated: false
type: note
---

Question: Read and explain the GovHK online payment FAQ.

Answer:

This page explains how Hong Kong government online services handle payments. The key points: ([Government of Hong Kong][1])

### 1. Supported payment methods

For most GovHK online services, payment can be made by:

* Credit cards

  * Visa
  * MasterCard
  * JCB
  * UnionPay
* PPS (Payment by Phone Service)
* Faster Payment System (FPS) is being added progressively. ([Government of Hong Kong][1])

For immigration services (for example visa/e-Visa related fees), newer systems may also support FPS and mainland e-wallets such as Alipay, WeChat Pay, and UnionPay App. ([Immigration Department Web Application][2])

---

### 2. Security model

When you enter credit card or PPS information:

```
Your browser
      |
      v
Payment provider / acquiring bank
      |
      v
Hong Kong Government service
```

The government department itself does **not** receive your card number or PPS password. The payment provider handles that information. ([Government of Hong Kong][1])

---

### 3. If payment fails

Important practical points:

* The payment page provides a **Transaction Reference Number (TRN)**.
* Keep the TRN if something goes wrong.
* Before trying again, check whether the first payment actually succeeded, otherwise you might accidentally pay twice. ([Government of Hong Kong][1])

---

### 4. Browser / network issues

Common causes:

* Session timeout
* Internet interruption
* Antivirus/security software blocking payment pages

The FAQ specifically mentions some security software (for example Kaspersky) may interfere with payment pages. ([Government of Hong Kong][1])

Also:

* GovHK online payment currently does **not support IPv6** for PPS and credit card payments.
* Use IPv4 if payment does not work. ([Government of Hong Kong][1])

---

### 5. Refunds

Refund rules:

* PPS payment → normally refund by cheque.
* Credit card payment → normally refunded back to the same credit card account. ([Government of Hong Kong][1])

---

### For your QMAS / Immigration application case

For the Hong Kong Quality Migrant Admission Scheme:

* You submit the application first.
* If approved, you receive payment instructions.
* Payment is made online through the provided payment page. ([Immigration Department Web Application][2])

Practical preparation:

```
Prepare:
✓ Visa/Mastercard/JCB/UnionPay card
✓ Stable IPv4 internet
✓ Disable aggressive browser security extensions
✓ Save payment receipt / acknowledgement
✓ Keep transaction reference number
```

A mainland Chinese applicant should generally prepare an internationally enabled UnionPay/Visa/MasterCard card or use supported e-payment options if offered by that specific ImmD payment page. ([Immigration Department Web Application][2])

References:

* ([Government of Hong Kong][1])
* ([Immigration Department Web Application][2])

[1]: https://www.gov.hk/en/about/helpdesk/faq/payment/?utm_source=chatgpt.com "GovHK: Online Payment"
[2]: https://webapp.es2.immd.gov.hk/applies2-client/static/faq/pnv-train/en-US/entry_faq.html?utm_source=chatgpt.com "ESERVICES2"
