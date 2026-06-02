---
audio: false
generated: true
image: false
lang: en
layout: post
title: QQ Mail Auto-Forwarding Feature Explained
translated: false
type: note
---

Question: In QQ Mail forwarding settings, what does the “auto forward emails” option mean, and is it part of the sending settings?

Answer:

Yes, you are looking at the **QQ Mail “email forwarding (自动转发)” feature**, but it is not part of “sending settings”—it belongs to **mail receiving / forwarding rules**.

### 1. What this setting does
When you enable:

> **邮件自动转发（Auto email forwarding）**

It means:
- Any incoming email to your QQ mailbox
- Will be automatically sent (“forwarded”) to another email address you specify (e.g. Gmail: `lzwjava@gmail.com`)

So QQ Mail acts like a **relay mailbox**.

---

### 2. Meaning of each option

#### ✔️ Forward to email
This is the destination email address (e.g. Gmail).

#### ✔️ Original email handling (原邮件操作)

After forwarding, QQ Mail lets you choose what happens to the original message:

- **保留在本邮箱中 (Keep in this mailbox)**
  → QQ Mail keeps a copy, nothing changes

- **保留并标为已读 (Keep and mark as read)**
  → Still stored, but marked as read (helps avoid duplicate attention)

- **自动删除 (Auto delete)**
  → After forwarding, QQ Mail deletes it (acts like full transfer, not backup)

---

### 3. Is this “sending settings”?
No.

This is:
- **Incoming mail rule / forwarding rule**
- Not related to sending emails (SMTP or outgoing mail settings)

Sending settings would be things like:
- SMTP configuration
- signature
- sending identity

---

### 4. Practical advice (important for your case)

Since you mentioned:
- QQ Mail missing important emails (notification muted on iPhone)
- Using Gmail as main inbox

A good setup is:

#### Recommended configuration
- Forward all QQ mail → Gmail
- Choose: **“保留在本邮箱中” (keep copy)**

Why?
- Gmail becomes your main inbox (no missed emails)
- QQ still keeps backup (safe if forwarding fails)

---

### 5. Small warning (important)
Forwarding is not always perfect:
- Some emails may delay
- Some services block auto-forwarded emails (rare but possible)
- Filters in QQ may affect forwarding order

So best practice is:
👉 Treat Gmail as “primary inbox view”
👉 QQ as “storage + backup system”

---

If you want, I can help you design a cleaner setup like:
- QQ + Gmail + iPhone notifications unified flow
- or even remove QQ dependency completely
