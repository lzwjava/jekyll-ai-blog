---
audio: false
generated: true
image: false
lang: en
layout: post
title: Substack Payment Account Disabled
translated: false
type: note
---

Question: Why does my Substack page show “This Connect account cannot currently make live charges” and what happened?

Answer:

From the screenshot, the key error message is:

> “This Connect account cannot currently make live charges… ‘requirements.disabled_reason’… Your transaction has not been processed.”

This points to an issue with **Substack’s payment processor (Stripe Connect)**, not just a simple UI error. Here’s what’s likely going on:

---

## 🔴 What the error actually means

Substack uses **Stripe Connect** to handle subscriptions. This error means:

👉 The **payment account linked to this Substack publication is currently disabled**
👉 Therefore, **no one can successfully pay or subscribe**

---

## 🧠 Common reasons this happens

### 1. Account suspended due to policy violation

This is the most likely cause, especially since you mentioned earlier:

> “Your account is currently suspended… violation of Spam & Phishing policy”

If Substack suspends your publication:

* They **disable Stripe payments immediately**
* This prevents collecting money during investigation

---

### 2. Stripe verification not completed

Stripe requires:

* Identity verification (ID, name, address)
* Bank account verification
* Possibly tax info

If incomplete or expired:

* Payments are blocked
* You’ll see a “disabled_reason” error like this

---

### 3. High-risk or suspicious activity

Stripe may disable accounts if:

* Sudden spikes in subscriptions
* Unusual payment patterns
* Content flagged as risky (spam, scams, etc.)

---

### 4. Country / compliance restrictions

If your account details or location conflict with Stripe rules:

* Payments can be disabled
* Especially common with cross-region setups

---

### 5. CAPTCHA expired (minor issue)

You also see:

> “Verification expired. Check the checkbox again.”

This is just a UI issue and **not the main problem**. Even if you fix it, payment will still fail because the account is disabled.

---

## 🧩 What happened in your specific case

Based on your earlier message + this screen:

👉 Your **Substack account was suspended**
👉 Substack **disabled your Stripe Connect account**
👉 That’s why payments now fail

---

## ✅ What you should do next

### Step 1: Appeal the suspension

Go to Substack Appeals Center and:

* Explain your intent clearly
* Say if this was a misunderstanding
* Show your content is legitimate

---

### Step 2: Check Stripe requirements

If you regain access:

* Go to Substack → Settings → Payments
* Complete all identity + bank verification

---

### Step 3: Avoid triggering flags again

Be careful with:

* Bulk messaging / growth hacks
* External links that look like phishing
* Aggressive monetization early

---

## ⚠️ Important reality check

Even if you fix Stripe:
👉 If Substack considers your content “spam/phishing”, they may **permanently block monetization**

---

## 💡 Strategic advice (based on your situation)

You’re trying to monetize (courses, etc.):

Substack is **strict and fragile** for this use case.

Better alternatives:

* WeChat Store (you already mentioned)
* Gumroad / Stripe directly
* Personal website + payment link

Substack works best for:
👉 long-term trust + writing
👉 not fast monetization experiments

---

If you want, I can help you:

* Diagnose why Substack flagged you specifically
* Or design a safer monetization setup (WeChat + Stripe + content funnel)