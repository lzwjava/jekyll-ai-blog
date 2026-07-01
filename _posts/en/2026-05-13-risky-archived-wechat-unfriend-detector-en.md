---
audio: false
generated: true
image: false
lang: en
layout: post
title: Risky Archived WeChat Unfriend Detector
translated: false
type: note
---

Question: What is the GitHub project "WechatRealFriends" and is it good?

Answer:

## Overview

**WechatRealFriends** is an open-source tool (written in Rust, JavaScript, HTML, and CSS) that lets WeChat users detect **one-sided friendships** — i.e., find out which contacts have quietly deleted or blocked you — with a single click. It is based on the **WeChat iPad protocol** (a reverse-engineered protocol that simulates logging in as an iPad device).

> ⚠️ **Important:** This repository has been **archived and is no longer maintained** as of October 3, 2025. The author has replaced it with a newer project called **WeFriends**.

---

## What It Does

- Scans your entire WeChat friend list and detects **mutual vs. one-sided** friendships
- Automatically **tags** contacts who have deleted or blocked you (so you can bulk-remove them on PC)
- Theoretically supports **tens of thousands of contacts**
- Operates **silently** — your contacts receive no notification
- The tool logs you in as an "iPad" device using the WeChat iPad protocol

---

## Is It Good?

### ✅ Pros

| Feature | Detail |
| --- | --- |
| **Functionality** | Accurately detects unfriended/blocked contacts |
| **Popularity** | 5,300+ GitHub stars, 371 forks — indicating strong community interest |
| **Non-intrusive** | Friends are not notified |
| **Bulk management** | Can tag and batch-remove one-sided contacts |
| **Free & open-source** | MIT licensed |

### ❌ Cons / Risks

| Risk | Detail |
| --- | --- |
| **Archived / Abandoned** | No longer maintained; the author has moved on to WeFriends |
| **Account ban risk** | Using unofficial WeChat protocols violates Tencent's Terms of Service and can result in your WeChat account being **suspended or permanently banned** |
| **Closed-source protocol** | The core WeChat iPad protocol implementation is a **pre-compiled binary** — the author does not have (or share) the source code. This is a security risk since you're running unknown compiled code |
| **Login friction** | Users may encounter verification prompts (numeric captcha), requiring workarounds |
| **Privacy risk** | You are handing your WeChat login credentials to a third-party tool |

---

## Should You Use It?

**For most users: No, not recommended.**

- The repo is **archived** — use the successor **WeFriends** if you still want this functionality
- Running it carries a **real risk of WeChat account suspension**
- The pre-compiled, closed-source backend component is a potential **security/trust concern**
- It only works properly in **China's WeChat ecosystem** (international WeChat has limited support)

If you're just curious whether someone unfriended you, the risk to your WeChat account likely outweighs the benefit.

---

## Successor Project

The author recommends migrating to **WeFriends**: [https://github.com/StrayMeteor3337/WeFriends](https://github.com/StrayMeteor3337/WeFriends), which claims:

- Lower ban probability (uses hook-based approach instead of iPad protocol)
- Supports international WeChat
- No login/verification issues

References:

- [https://github.com/StrayMeteor3337/WechatRealFriends](https://github.com/StrayMeteor3337/WechatRealFriends)
- [https://github.com/StrayMeteor3337/WeFriends](https://github.com/StrayMeteor3337/WeFriends)
