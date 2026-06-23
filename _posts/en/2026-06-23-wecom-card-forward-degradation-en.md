---
audio: false
generated: true
image: false
lang: en
layout: post
title: WeCom Card Forward Degradation
translated: false
type: note
---

**Question:** When sharing an Enterprise WeChat (WeCom) contact to a group, it shows as a rich contact card. But when *forwarding* a WeCom business card, does it degrade to plain text like `[WeCom Business Card] name`?

**Answer:**

Yes, that's correct behavior. Here's what's happening:

**Share vs Forward — two different paths:**

| Action | Result |
|--------|--------|
| Share contact directly from contact profile | Renders as interactive card UI in chat |
| Forward an existing business card message | Degrades to text: `[WeCom Business Card] 姓名` |

**Why the degradation happens:**

When you share a contact directly, WeCom sends a structured message type (specifically a `contact` message type in the WeCom message protocol). The client renders it natively.

When you *forward* that message, WeChat/WeCom's forward mechanism doesn't always preserve the original structured message type — it serializes it into a text fallback representation. This is a known limitation across both personal WeChat and WeCom: certain rich message types (mini-programs, contact cards, location shares) lose fidelity when forwarded rather than reshared from source.

**The pattern in WeCom's message types:**

```
msgtype: "contact"    →  forwarded as plain text fallback
msgtype: "text"       →  forwarded as-is
msgtype: "image"      →  forwarded as-is
msgtype: "video"      →  forwarded as-is
```

Rich structured types (contact, location, voip) tend to fall back to text on forward.

**Workaround:**

If you need the recipient to get a proper interactive card, go to the contact's profile and re-share from there directly — don't forward the forwarded message.
