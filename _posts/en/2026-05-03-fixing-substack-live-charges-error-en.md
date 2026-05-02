---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Substack Live Charges Error
translated: false
type: note
---

Question: How to fix “This Connect account cannot currently make live charges” error on Substack?

Answer:

This error usually comes from **Stripe Connect (which Substack uses for payments)**. It means your creator payout account is **not fully enabled for live transactions**, so subscriptions or payments cannot be processed.

Here are the most common causes and fixes:

---

## 1. Incomplete Stripe / Substack payout setup

Most frequent issue.

Go to your Substack dashboard:

* **Settings → Payments / Payouts**
* Check if there is any “Action required”

Typical missing items:

* Identity verification (KYC not completed)
* Bank account not added or verified
* Tax form not submitted (W-9 / W-8BEN)

👉 Fix: Complete all required onboarding steps until status shows **“Enabled”**

---

## 2. Identity or compliance review failed

Stripe may disable live charges if:

* Name mismatch (bank vs ID)
* Address not verified
* Document rejected or expired

👉 Fix:

* Re-upload ID documents
* Ensure legal name matches bank account exactly
* Update address and tax info

---

## 3. Country or account eligibility restriction

Substack payments depend on Stripe availability. Some regions or account types may be:

* Not fully supported for live charges
* Temporarily restricted during review

👉 Fix:

* Check if your country is supported for Stripe Connect payouts
* Contact Substack support to confirm eligibility

---

## 4. “Disabled reason” inside Stripe Connect

The message explicitly says:

> check `requirements.disabled_reason`

This usually means:

* “requirements.pending_verification”
* “requirements.past_due”
* “rejected.fraud”
* “rejected.other”

👉 Fix:
Substack doesn’t always show the full reason, so you must:

* Open payout settings page
* Look for red warnings or “Verify now” prompts
* Or contact support for the exact Stripe reason

---

## 5. New account cooling / review period

Sometimes Stripe blocks live charges temporarily for:

* New creator accounts
* Sudden payment activity
* Risk review

👉 Fix:

* Wait 24–72 hours
* Ensure all onboarding is complete
* Avoid retrying multiple failed setups

---

## 6. If you are a subscriber (not creator)

If you're just trying to pay:

* The issue is on the creator’s Substack account, not yours
* You cannot fix it directly

👉 Action:
Contact the publication owner and tell them:

> “Your Stripe Connect account is disabled for live charges.”

---

## Practical checklist (fast fix)

Go to Substack → Payments:

* [ ] Identity verified
* [ ] Bank account added & confirmed
* [ ] Tax form completed
* [ ] No “Action required” banner
* [ ] Country supported

---

If you want, paste the **exact Substack payout page status**, and I can tell you precisely which field is blocking activation.