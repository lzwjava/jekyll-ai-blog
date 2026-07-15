---
audio: false
generated: true
image: false
lang: en
layout: post
title: AdSense Code Deployed, No Ads
translated: false
type: note
---

Here's the full picture:

**Code is deployed correctly** ✅
- `ads.txt` at `https://lzwjava.github.io/ads.txt` — serves the correct content (200)
- `<meta name="google-adsense-account">` — present on the page
- `<script src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js">` — present on the page

**Why no ads show up:**

1. **AdSense account needs to be approved first** — just adding the code doesn't make ads appear. You need to submit your site to Google AdSense for review at `https://adsense.google.com`. The review process can take **1-2 weeks**.
2. **After approval, enable auto ads** — go to the AdSense console → Auto ads → turn on for your site. The script in `<head>` enables this, but it must be activated in the dashboard.
3. **No manual ad units** — what we added is the auto-ads script. If you want ads in specific locations (e.g., after each blog post), you need to create ad units in the console and place their code in the `<body>` of the page.

**AdSense Management API does exist:**
- Endpoint: `https://adsense.googleapis.com` (v2)
- Can query: accounts, ad clients, ad units, earnings reports, payments, policy issues, site status
- Requires OAuth2 credentials — needs to be set up in Google Cloud Console
- API method for site status: `GET /v2/{parent=accounts/*}/sites` — lists approved/rejected sites

Want me to check the AdSense console status or set up a manual ad unit in the body?
