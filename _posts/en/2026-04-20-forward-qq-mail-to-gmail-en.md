---
audio: false
generated: true
image: false
lang: en
layout: post
title: Forwarding QQ Mail to Gmail
translated: false
type: note
---

Question: How can I automatically sync or forward emails from QQ Mail to Gmail so that new emails are sent to Gmail automatically?

Answer:

To automatically forward emails from **QQ Mail** to **Gmail**, you don’t need “sync” in the strict sense—you can simply set up **auto-forwarding** or let Gmail fetch your QQ emails via **POP3/IMAP**. Here are the two main approaches:

---

# ✅ Method 1: Set up Auto Forwarding in QQ Mail (Recommended)

This makes every incoming email automatically sent to your Gmail inbox.

### Steps

1. Log in to QQ Mail: [https://mail.qq.com](https://mail.qq.com)
2. Click **Settings (设置)** → **Accounts (账户)**
3. Find **Auto Forwarding (自动转发)**
4. Enable it and enter your Gmail address
5. Confirm via verification email sent to Gmail
6. (Optional) Choose whether to:

   * Keep a copy in QQ Mail
   * Delete after forwarding

### Result

* Every new email received in QQ Mail → instantly forwarded to Gmail

---

# ✅ Method 2: Use Gmail to Fetch QQ Mail (POP3)

Instead of pushing emails, Gmail will periodically pull emails from QQ.

### Step 1: Enable POP3 in QQ Mail

1. Go to QQ Mail → Settings → Accounts
2. Enable:

   * **POP3/SMTP service**
3. Generate an **authorization code** (important: not your QQ password)

---

### Step 2: Add QQ Mail in Gmail

1. Open Gmail
2. Click **Settings → See all settings → Accounts and Import**
3. Under **Check mail from other accounts**, click **Add a mail account**
4. Enter your QQ email (e.g. [xxx@qq.com](mailto:xxx@qq.com))
5. Choose **Import emails from my other account (POP3)**
6. Use these settings:

   * Username: your QQ email
   * Password: authorization code from QQ
   * POP server: `pop.qq.com`
   * Port: `995` (SSL enabled)

---

### Result

* Gmail will **periodically fetch emails** from QQ (not instant, usually every few minutes)

---

# ⚖️ Which one should you choose?

| Method           | Speed   | Setup Difficulty | Reliability |
| ---------------- | ------- | ---------------- | ----------- |
| Auto Forwarding  | Instant | Easy             | High        |
| Gmail POP3 Fetch | Delayed | Medium           | Good        |

👉 If you want **real-time delivery → use forwarding**
👉 If you want **centralized control inside Gmail → use POP3**

---

# ⚠️ Important Notes

* QQ Mail may occasionally flag forwarding as suspicious → ensure your account is verified
* Gmail might classify forwarded emails as spam → check spam folder initially
* For business use, consider using filters in Gmail to label QQ emails automatically

---

If you want, I can also show you how to:

* Send emails *from Gmail using your QQ address* (SMTP setup)
* Or sync both ways (more advanced setup)

Just tell me 👍
