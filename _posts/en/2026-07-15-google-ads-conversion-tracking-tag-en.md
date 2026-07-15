---
audio: false
generated: true
image: false
lang: en
layout: post
title: Google Ads Conversion Tracking Tag
translated: false
type: note
---

**Question:** What is this `gtag.js` snippet with `AW-18324816389` used for?

**Answer:**

That `AW-` prefix means this is a **Google Ads tag**, not Google Analytics (which uses `G-` or `UA-`). Specifically:

- `AW-18324816389` = your **Google Ads Conversion ID**, tied to a specific Google Ads account.
- This snippet loads the base tracking library and initializes it — but on its own **it does nothing except identify which Ads account is talking**. It's the plumbing, not the measurement.

**What it's actually for:** conversion tracking. To measure "did this ad spend turn into revenue," you need a second piece — an **event snippet** fired on the action you care about (form submit, purchase, signup), like:

```html
<script>
  gtag('event', 'conversion', {
    'send_to': 'AW-18324816389/AbC-D_efGHij123',  // conversion label, from Ads UI
    'value': 100.0,
    'currency': 'USD'
  });
</script>
```

That runs on your "thank you" / success page, or on a button click. Without this second piece, the base tag you pasted is just sitting there loading a library with nobody calling it.

**How this ties back to campaigns:** when you create a campaign (previous question) and set a conversion goal, Google Ads generates this exact `AW-...` tag + event snippet for you to paste into your site. It's how Google knows "user clicked ad → landed on lzwjava's site → filled out contact form → that's a conversion → optimize bidding toward more of these."

So the presence of this tag tells me: **you (or someone) already started creating a Google Ads campaign**, and this is step 2 of setup (install tracking) before step 3 (define what a "conversion" event is on your site).

**Next concrete step:** go to Google Ads → Tools → Conversions → find/create the conversion action → copy the event snippet with the actual `send_to` label → tell me what page/action on your site should count as a conversion (contact form? Calendly booking? WeChat/email click?) and I'll write the exact JS to fire it.
