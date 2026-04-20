---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gmail POP IMAP Settings Location
translated: false
type: note
---

Question: Is Gmail forwarding/POP/IMAP settings under “managed labels” in Gmail settings?

Answer:

No — **“Managed labels” is not where Gmail forwarding, POP, or IMAP settings are located.** These are completely different parts of Gmail’s settings system.

Here’s the correct breakdown:

## 1. Where “Managed Labels” actually is

In Gmail, **Labels** are just for organizing emails (like folders, but more flexible).

* Found under: **Settings → Labels**
* Purpose:

  * Create / rename / hide labels
  * Control whether labels appear in sidebar
  * Manage system labels (Inbox, Sent, Drafts, etc.)

👉 This has **nothing to do with syncing or forwarding emails externally**

---

## 2. Where POP / IMAP / Forwarding are

These are under different tabs:

### 📩 POP & IMAP

* Path: **Settings → Forwarding and POP/IMAP**
* Purpose:

  * Enable IMAP (for Gmail sync with Outlook, Apple Mail, etc.)
  * Enable POP download (older method)
  * Configure mail client access

---

### 🔁 Forwarding

* Same tab: **Settings → Forwarding and POP/IMAP**
* Purpose:

  * Automatically forward incoming emails to another address (like QQ, Outlook, etc.)
  * Requires verification email

---

## 3. Why it feels confusing

Gmail groups settings by function, not by “importance”:

* **Labels** = organization inside Gmail UI
* **Forwarding/POP/IMAP** = external access & syncing
* **Filters** = automation rules
* **Accounts and Import** = sending/receiving identity management

So “Managed labels” is just one small category inside Gmail’s internal organization system — not related to mail transfer.

---

## 4. Quick mental model

Think of Gmail like this:

* 📁 Labels → how YOU organize mail inside Gmail
* 🌐 POP/IMAP → how OTHER apps read Gmail
* ↗️ Forwarding → how Gmail sends mail to another inbox
* ⚙️ Filters → automatic rules engine

---

If you want, I can walk you step-by-step to set up **QQ mail → Gmail auto sync/forwarding**, because QQ’s IMAP/forwarding setup is a bit hidden and often confusing.