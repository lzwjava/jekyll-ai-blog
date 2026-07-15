---
audio: false
generated: true
image: false
lang: en
layout: post
title: Choose Google's 3-Button CMP
translated: false
type: note
---

Question: Which consent-message setup should I actually pick — Google's 2-button, Google's 3-button, or a third-party certified CMP — for my site now and future sites?

Answer: Go with **3-button (Consent / Do not consent / Manage options)**, using Google's own CMP. Skip third-party for now.

**Why 3-button over 2-button:**

The 2-button version ("Consent" + "Manage options", no direct reject) is Google nudging you toward higher consent rates — burying "reject" inside a sub-menu is a mild dark pattern. That's exactly the design EU regulators have been going after:

- Belgian DPA ruled the IAB TCF framework itself non-compliant in 2022 partly over consent-quality issues.
- CNIL (France) and EDPB guidance both establish that declining must be as easy as accepting — one click to reject, not one click to accept + N clicks to reject.
- Google's own CMP explicitly frames this as a **revenue vs. compliance-risk tradeoff** in its docs, not a neutral choice — the 2-button option is there because it converts better, not because it's safer.

Since you're running an AI consulting company with (likely) EU clients/traffic, and this decision propagates to "future sites" too, default to the compliant version. Fixing 10 sites' consent banners later because one got flagged costs more than the marginal ad revenue you'd gain now.

**Setup (Google CMP, no third party):**

```
AdSense → Privacy & messaging → Consent messages → Create message
  → Regions: EEA, UK, Switzerland
  → Message type: 3 buttons (Consent, Do not consent, Manage options)
  → Legitimate interest: leave ON unless you have a specific reason to disable
  → Apply to: select "apply to all sites" if your AdSense account covers multiple properties
```

For **future sites**: if they're under the same AdSense/Ad Manager account, the message and its settings can be applied account-wide rather than recreated per-site — check "Apply message to all sites" instead of building a new one each time.

**On the third-party CMP question:** only bother if you need functionality Google's CMP doesn't have — e.g., non-ad-related cookie categorization (analytics, functional cookies unrelated to Google ads), multi-network vendor management beyond Google's ATP list, or white-labeling for client sites you don't control the AdSense account on. If you do need that, Secure Privacy, Cookiebot, and CookieYes are all Google-certified and have decent free/cheap tiers for low-traffic sites. But for your own properties monetized straight through AdSense, Google's native CMP does the job with zero extra JS and zero extra vendor to manage.

References:
- [Consent management requirements (for publishers)](https://support.google.com/adsense/answer/13554116?hl=en)
- [Choose 2 vs 3 buttons - Google Ad Manager Help](https://support.google.com/admanager/answer/16918505?hl=en)
- [About consent optimization - AdSense Help](https://support.google.com/adsense/answer/16878447?hl=en)
