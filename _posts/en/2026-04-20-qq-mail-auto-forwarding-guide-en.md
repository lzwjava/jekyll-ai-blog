---
audio: false
generated: true
image: false
lang: en
layout: post
title: QQ Mail Auto Forwarding Guide
translated: false
type: note
---

Question: Why can’t I find the “Auto Forwarding” option in QQ Mail, and how do I enable automatic forwarding to Gmail?

Answer:

You’re **not wrong** — the reason you can’t find “Auto Forwarding (自动转发)” is that:

👉 In newer versions of QQ Mail,
this option is often **hidden, moved, or only visible in the web desktop version** (not mobile / simplified UI).

---

# 🔍 Where “Auto Forwarding” actually is (exact location)

You need to use **desktop web version**, not app.

### Steps (important details)

1. Open: [https://mail.qq.com](https://mail.qq.com)
2. Login
3. Click **Settings (设置)** — top right
4. Click **“General (常规)” tab** (NOT Accounts)

👉 Now scroll **WAY DOWN (this is key)**

You are looking for:

> **邮件自动转发 / 自动转发 (Mail Auto Forwarding)**

✔ It is **NOT inside POP3/IMAP section**
✔ It is usually near:

* Spam settings
* Auto reply

Then:

* Enable (启用)
* Enter your Gmail
* Verify
* Save

📌 This feature exists but is easy to miss because it’s far down the page ([bkqs.com.cn][1])

---

# ⚠️ Why you currently don’t see it

Based on what you pasted:

> “POP3/IMAP/SMTP/Exchange/CardDAV 服务（已开启）”

This means you are inside:

👉 **“Accounts (账户)” tab**

❌ That tab only shows:

* POP3 / IMAP
* SMTP
* Authorization codes

👉 It does NOT contain forwarding

---

# 🚫 Important reality (this is the catch)

In recent years, Tencent sometimes:

* Removes or hides auto-forwarding for some accounts
* Restricts it due to spam/security
* Only shows it for:

  * older accounts
  * certain regions
  * desktop full UI

👉 So if you **still don’t see it after scrolling**, then:

👉 **Your account likely does NOT have this feature enabled**

---

# ✅ Best workaround (what actually works reliably)

Use Gmail to fetch instead:

## Use Gmail POP3 fetch

Since you already enabled:

> POP3/IMAP/SMTP ✔

You can do this:

### In Gmail

1. Settings
2. Accounts & Import
3. Add mail account
4. Use:

   * server: `pop.qq.com`
   * port: 995
   * SSL: yes
   * password: QQ authorization code

👉 Result:

* Gmail pulls your QQ mail automatically
* Not instant, but works 100%

---

# 🧠 Practical recommendation

* If you **find auto-forwarding → use it (best, real-time)**
* If you **can’t find it → don’t waste time**
  → just use POP3 fetch

Because:

👉 Many people simply **don’t have forwarding anymore**

---

# ⚡ Quick diagnosis for you

Based on your screenshot text:

✔ POP3 enabled
❌ Forwarding missing

👉 Conclusion:

> Your QQ Mail likely **does NOT expose auto-forwarding** → use Gmail fetch

---

If you want, I can guide you step-by-step to:

* make Gmail send as QQ (so you fully replace QQ Mail)
* or build a near “real-time” sync workaround

Just tell me 👍

[1]: https://www.bkqs.com.cn/content/opylwzo1n.html?utm_source=chatgpt.com "QQ邮箱怎么设置自动转发功能 〖百科全说〗"
