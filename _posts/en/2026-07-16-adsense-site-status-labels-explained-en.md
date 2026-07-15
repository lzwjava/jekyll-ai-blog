---
audio: false
generated: true
image: false
lang: en
layout: post
title: AdSense Site Status Labels Explained
translated: false
type: note
---

Question: What do the AdSense site status labels (Getting ready / Ready / Requires review / Needs attention) mean?

Answer: This is Google AdSense's site-review pipeline — every domain you add goes through this state machine before it can serve ads.

- **Getting ready** — Google's crawler + policy checks are running. Normal wait is a few days, worst case 2-4 weeks. Nothing to do, just wait.
- **Ready** — Site passed review, ads are live/eligible. You're not done though — ongoing policy compliance is checked continuously (this isn't a one-time gate).
- **Requires review** — Either never submitted for review, or was previously ready/active but went inactive (no traffic, site down, etc.) long enough that Google pulled it back to unreviewed. You manually click "Request review" to re-trigger the check.
- **Needs attention** — Failed policy check. Something concrete is wrong (thin content, prohibited content, insufficient original content, navigation issues, etc.) — check Policy Center on that site for the specific violation, fix it, it auto-rechecks.

Typical flow: `Requires review → Getting ready → Ready`, with `Needs attention` as the branch when something's flagged, and sites can fall back to `Requires review` if traffic drops to zero for too long.

References:

- [Site status and getting ready](https://support.google.com/adsense/answer/12176698)
- [Request review for inactive site](https://support.google.com/adsense/answer/12171038#request_review)
