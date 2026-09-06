---
audio: false
generated: true
image: false
lang: en
layout: post
title: Display Banner vs Direct Link
translated: false
type: note
---

Question: Is a **normal display banner** basically a direct link?

Answer: **No. They are different.**

```text
Normal Display Banner
your page
   ↓
[ visual advertisement ]
   ↓ user intentionally clicks
advertiser (e.g. Trip.com)
```

The banner is an **ad unit**. Monetag handles the advertiser, tracking, and destination URL.

A **Direct Link** is different:

```text
your page/button
   ↓
directly opens Monetag link
   ↓
advertiser
```

There is **no visible banner**. You have to decide where to put the link yourself.

### In short

| Format               | Visible ad? | User clicks ad?              | UX           |
| -------------------- | ----------- | ---------------------------- | ------------ |
| **Display Banner**   | ✅ Yes       | ✅ Yes                        | 👍 Good      |
| **Vignette**         | ✅ Overlay   | ✅ Yes                        | 😐 Intrusive |
| **Direct Link**      | ❌ No        | User clicks your link/button | 😐 Depends   |
| **OnClick/Popunder** | ❌ Usually   | ⚠️ Unexpected redirect       | 👎 Bad       |

So if you want:

> **"Show an ordinary rectangular advertisement on my blog, and don't redirect users unexpectedly."**

→ **Display Banner** is what you want.
