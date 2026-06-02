---
audio: false
generated: true
image: false
lang: en
layout: post
title: Analytics for GitHub Pages Without Domain
translated: false
type: note
---

**Question:** What if I didn't add a domain, I just use Web Analytics / logs for my blog that is hosted on GitHub Pages with the GitHub domain?

**Answer:**

You **can** use **Cloudflare Web Analytics** for a blog hosted on GitHub Pages (using either the default `username.github.io` or a project subdomain like `username.github.io/repo`) **without adding any domain to Cloudflare** and **without changing your DNS or nameservers**.

Cloudflare Web Analytics is specifically designed for this exact scenario: it is a **privacy-first, lightweight JavaScript-based tracker** that works completely independently of Cloudflare's proxy, DNS, or domain setup. It does **not** require a Zone ID (because no zone/domain is added to your account), and it collects data client-side via a small beacon script.

### How to set it up for your GitHub Pages blog
1. Log in to your Cloudflare dashboard (free account is fine).
2. Go to **Analytics & Logs** → **Web Analytics** (or directly search for "Web Analytics" in the dashboard).
3. Click **Add a site** (or "Create" / "Add site").
4. Enter your GitHub Pages hostname exactly as visitors see it:
   - For user/organization site: `username.github.io`
   - For project site: `username.github.io/repo-name`
5. Cloudflare will generate a small JavaScript snippet (usually ~1 KB) that looks something like this:
   ```html
   <script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "YOUR_UNIQUE_TOKEN_HERE"}'></script>
   ```
6. Add this snippet to the `<head>` section of your site's HTML files (or in your Jekyll/Hugo/etc. layout template if using a static site generator).
   - For plain HTML: edit `index.html` and other pages.
   - For Jekyll: add it to `_includes/head.html` or equivalent.
   - Push the change → GitHub Pages will rebuild and deploy automatically.
7. After a few hours/days of traffic, view your stats in the same Web Analytics section of the dashboard.

### Key points and limitations
- **No Zone ID needed** — You never see or use a Zone ID here because you're not adding a zone/domain.
- **No proxy / performance features** — You won't get Cloudflare's caching, DDoS protection, image optimization, etc. (those require proxying traffic, which means using Cloudflare DNS + adding the domain).
- **Data is privacy-friendly** — No cookies, no personal IPs stored, GDPR-friendly.
- **Works on any hostname** — Including `*.github.io`, custom domains not pointed to Cloudflare, localhost during dev, etc.
- **Alternative for Pages projects** — If you ever migrate your blog from GitHub Pages to **Cloudflare Pages** (highly recommended for better speed, free analytics integration, and custom domains), you can enable Web Analytics with **one click** in the project settings (Metrics → Enable), and Cloudflare auto-injects the snippet on deploy — no manual code edit needed.

This is the simplest and most common way people add free, decent analytics to pure GitHub Pages sites without touching DNS.

**References:**

- [Enabling Cloudflare Web Analytics - Get started](https://developers.cloudflare.com/web-analytics/get-started)
- [Enable Web Analytics for Pages projects](https://developers.cloudflare.com/pages/how-to/web-analytics)
- [FAQs - Cloudflare Web Analytics](https://developers.cloudflare.com/web-analytics/faq)
- [Cloudflare Web Analytics for sites not proxied through Cloudflare](https://developers.cloudflare.com/web-analytics/get-started/#sites-not-proxied-through-cloudflare)
