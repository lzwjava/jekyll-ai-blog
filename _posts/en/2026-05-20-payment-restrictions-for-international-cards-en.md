---
audio: false
generated: true
image: false
lang: en
layout: post
title: Payment Restrictions for International Cards
translated: false
type: note
---

Question: Why can I add Alipay as a payment method to AMD Developer Cloud for GPU droplets, but my HSBC Hong Kong Mastercard debit card with a China address does not work?

Answer:

This is likely due to regional and banking restrictions rather than an issue with AMD Developer Cloud itself:

1. **Card Issuer Restrictions:** Some banks, especially foreign ones, may block cross-border transactions for cloud services. Your HSBC HK card might be considered an international transaction if AMD’s billing system detects your account is in China.

2. **Billing Address Mismatch:** Many payment gateways require the card’s billing address to match the account’s country. Since your card is HK-based but your AMD account shows a China address, the system may reject it.

3. **Payment Gateway Limitations:** Some services use Stripe or other processors that have rules about which cards from which countries are accepted. Alipay is domestic in China, so it passes easily, whereas international cards may be restricted.

4. **Type of Card:** Debit cards can sometimes have more restrictions than credit cards for online international payments, especially recurring or pre-paid subscriptions.

**Workarounds:**

* Use Alipay, which is fully supported.
* Use a card issued in China (credit card preferred) with a matching billing address.
* If you want to use HK cards, you may need to contact AMD support to see if they allow exceptions for cross-border billing.

References:

* [AMD Developer Cloud Payment Methods](https://developer.amd.com/amd-developer-cloud/)
* [Stripe Card Restrictions](https://stripe.com/docs/payments/cards/payment-methods)
* [Alipay International Acceptance](https://intl.alipay.com/)
