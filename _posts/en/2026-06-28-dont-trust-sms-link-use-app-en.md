---
audio: false
generated: true
image: false
lang: en
layout: post
title: Don't trust SMS link, use app
translated: false
type: note
---

Question: For this JD (京东) delivery SMS with a survey link, can the photo of the delivered package actually be checked quickly?

Answer:

Short version: not by me, and not reliably by that link either.

A few things going on here:

**1. I can't fetch it.** The URL is truncated — it ends at `waybillCode=` with no actual waybill code. Even with the full code, `h5-ql.jdl.com` is a JD logistics H5 page that almost certainly requires a logged-in JD session (cookies/token) to render the signed-delivery photo. My `web_fetch` can't carry your auth, so it'd just hit a login wall or empty state.

**2. Treat the SMS link as suspicious by default.** Delivery-notification SMS with embedded links are one of the most common phishing vectors in China (伪基站 / 钓鱼). The legit way to see the proof-of-delivery photo:

- Open the **京东 app** → 我的 → 我的快递 / 订单 → find the order → 物流详情. The "已放在家门口" signed photo shows there natively.
- Or **京东物流 (JD Logistics) official mini-program** in WeChat, search by waybill tail `93941`.

Don't tap the SMS link directly. The real JD delivery photo is always reachable from inside the authenticated app, which makes the SMS link redundant.

**3. The phone number** `<​IP_ADDRESS>`— I mean the courier number `139xxxx2377` — if you genuinely need to confirm, call through the number listed in the app's 物流详情, not the one in the SMS.

So: yes, the photo exists and is quick to check — but check it inside the JD app, not via that link, and not via me.
