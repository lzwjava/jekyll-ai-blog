---
audio: false
generated: true
image: false
lang: en
layout: post
title: WeChat Account Recovery via Contacts
translated: false
type: note
---

**Question:** In WeChat, when logging into an account on a new device (or one that hasn't been used in 5–6 years), does it require two trusted contacts to each send a 6-digit code to verify identity?

**Answer:**

Yes, roughly correct. Here's exactly how WeChat's **account recovery via trusted contacts** works:

## WeChat Login Verification on New/Unfamiliar Device

When WeChat detects a login from an **unrecognized device** or after a **long inactivity period**, it triggers a security challenge. If you don't have access to your registered phone number (or it's been too long), it falls back to **"Verify with Contacts"**:

### The Flow

1. You attempt login on new device
2. WeChat can't verify via SMS (number changed/inaccessible)
3. It offers: **"Verify with WeChat contacts"**
4. You select **3 trusted friends** from your contact list
5. Each of those friends receives a notification in WeChat
6. **Each friend gets a 4-digit code** (not 6 — this is the common misremembering)
7. You need **at least 3 friends to cooperate** and share their codes with you
8. You enter all 3 codes to recover access

### Clarifications on Your Memory

| Your recollection | Actual behavior |
|---|---|
| 2 contacts | Usually **3 contacts** required |
| 6-digit code | Actually **4-digit code** per contact |
| Codes sent to one person | Each contact gets their **own unique code** |

The codes are split intentionally — no single contact has enough to recover your account alone (threshold secret-sharing concept).

### Why This Design

It's a basic **k-of-n secret sharing** UX pattern — Tencent splits the recovery token across N friends, requiring at least k to reconstruct. Prevents a single malicious contact from hijacking your account.

---

The exact numbers (3 contacts, 4 digits) may vary slightly by WeChat version or region — Tencent has tweaked this over the years. But the architecture is: **multiple contacts, each holding a partial code, all required together**.