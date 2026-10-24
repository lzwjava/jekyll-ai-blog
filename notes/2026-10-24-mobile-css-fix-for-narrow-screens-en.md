---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mobile CSS Fix for Narrow Screens
translated: false
type: note
---

Done ✅ — deployed and live on https://truthlab.cc/ (run `40089370394` success).

What changed in the mobile CSS (≤620px):
- **Removed** `flex-wrap: wrap` from the header and `order: 3; width: 100%` from the nav (that's what forced it onto a full second line).
- Nav now sits **inline on the top row**: `⟡ Research Services About Contact [EN|中文 ☾]` all on one line.
- Compacted sizing so it fits: nav links `12.5px / 5px 8px` padding, tighter gaps.

Plus a new **≤400px breakpoint** for narrow phones (nav `12px`, tighter padding/gaps) so the single line holds even on small screens.

If it still feels tight on your specific phone, easy knobs: drop the nav font to `11.5px` or hide the wordmark lamp below 340px — happy to tweak.
