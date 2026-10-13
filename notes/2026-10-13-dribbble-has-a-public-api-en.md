---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dribbble Has a Public API
translated: false
type: note
---

**Question:** Does Dribbble have an API?

**Answer:** Yes, Dribbble has a public API.

Here are the key details:

- **Official docs:** `https://developer.dribbble.com`
- **Authentication:** The API uses OAuth for authentication, which is more involved than a simple API key but provides better security, especially when accessing user data.
- **Cost:** Dribbble is listed as a free public API.
- **Status:** As of April 2026, the API is responding normally.
- **What you can do:** It allows you to manage shots, create projects, upload attachments, and post comments.
- **Protocol:** HTTPS only; CORS support is not documented, so if you get cross-origin errors in the browser, try calling the API from your server instead.

**References:**
- [Dribbble Developer Portal](https://developer.dribbble.com)
- [API Bouncer – Dribbble](https://www.apibouncer.com/apis/1190/dribbble)