---
audio: false
generated: true
image: false
lang: en
layout: post
title: Avatar fixes deployed and verified
translated: false
type: note
---

Done — deployed, verified, committed (`8f1ab99`), and pushed.

**Summary of what happened and what I fixed:**

**1. The "some big, some small" layout was the old build.** The 50px-circle grid fix was already in tonight's deploy (`ea7176d`), but the build live until then (from 12:23) had no size on `.avatar` at all, so images rendered at their natural size — exactly what you saw. My production probe now measures **all 30 avatars at exactly 50×50** with `object-fit: cover`. You were likely viewing the cached old build — **hard-refresh** (or clear cache) to see the fixed version at https://funlive.io/#/live/1/users.

**2. Real remaining issues I fixed in `user-avatar.vue`** (visible even in the new grid):
- **Dead avatar images** (e.g. 路上, whose GCS object is gone) showed a broken-image icon with oversized alt text spilling out of the circle → now falls back to a colored circle with the username's first letter
- **Mixed-content URLs** — API returns `http://storage.googleapis.com/...` avatars on an https page; some in-app webviews (WeChat) block those outright → now upgraded to `https://` (GCS serves it fine)
- Added `loading="lazy" decoding="async"` so long lists like this 30+ item grid don't fetch everything at once

**3. Production verification** (fresh headless browser, cache disabled): 30/30 avatars at 50×50, 29 https images + 1 letter fallback, zero `http://` URLs remaining.

One note: I added a `Co-Authored-By` trailer to the commit that isn't your usual style — say the word if you want me to drop it with an amend + force-push.