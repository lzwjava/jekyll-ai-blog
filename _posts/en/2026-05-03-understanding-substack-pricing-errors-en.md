---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding Substack Founding Plan Pricing Errors
translated: false
type: note
---

Question: Why does Substack show “Suggested price must be greater than other plans, and cannot be less than the minimum price” when setting a Founding plan price (e.g., 20 USD)?

Answer:

This error in Substack usually comes from **pricing hierarchy rules**, not from the number itself being invalid.

### What Substack is enforcing

For Founding Plans, Substack applies **two constraints at the same time**:

#### 1. Founding plan must be higher than other paid plans

Your Founding tier is treated as a *premium tier above everything else*.

So it must be:

* **> Monthly plan price**
* **> Annual plan price (or annual equivalent per month)**

If your:

* Monthly = (blank or 0 or lower than expected)
* Annual = empty or lower than 20

→ Substack still may interpret it as invalid and block saving.

---

#### 2. Must be above the platform minimum threshold

Substack also enforces a **minimum allowed subscription price**, which can vary by:

* currency (USD vs others)
* billing type (monthly vs annual)
* Stripe region rules

So even if 20 USD *looks fine*, it may still be below the **effective minimum for founding tier logic** in your configuration.

---

### Why you see this even with “20 USD”

Most common real causes:

#### A. Annual plan is not set or too low

Example:

* Monthly: not set
* Annual: not set or 0

→ Substack cannot compare properly, so it fails validation.

---

#### B. Founding plan is expected to be a “top tier”

In many setups, Substack expects:

* Monthly: lowest
* Annual: discounted
* Founding: **highest (premium supporter tier)**

So if Founding = 20 USD/year, but annual is also 20 or higher → error triggers.

---

#### C. Hidden rule: Founding is often expected to be significantly higher

Even though not always documented, Substack often behaves like:

* Founding must feel like a *supporter tier*
* Typically higher than annual (sometimes 2× or more)

---

### How to fix it (practical steps)

1. Set your **Monthly plan first**

   * e.g. $5/month

2. Set your **Annual plan next**

   * e.g. $50/year (or ~$4/month equivalent)

3. Then set Founding plan:

   * Must be **greater than annual total value**
   * e.g. $80/year or $100/year

4. Save again

---

### If it still fails

Try these quick checks:

* Ensure no plan is blank
* Ensure annual is not accidentally higher than founding
* Try increasing Founding to something clearly higher (e.g. 99, 120)
* Refresh Stripe connection if pricing logic feels stuck

---

If you want, paste your current monthly/annual values and I can tell you exactly what Founding price Substack will accept.