---
audio: false
generated: true
image: false
lang: en
layout: post
title: WeChat Remark Persists Over Nickname Changes
translated: false
type: note
---

Question: If I set a WeChat alias (remark/备注) for a contact, does it keep showing my alias even after they change their WeChat username/nickname? And if I don't set one, does their display name update live?

Answer: Yes, that's exactly how it works.

- **Remark set** → WeChat stores it locally in your contact list, keyed to their `wxid` (immutable internal ID), not their nickname. Their nickname change is irrelevant to what you see — your remark persists until you manually edit/clear it.
- **No remark set** → you're just rendering their live `NickName` field pulled from their profile, so any rename propagates to your contact list and chat header immediately.

Mental model:
```
display_name = remark_map[wxid] if remark_map.get(wxid) else contact.nickname
```
Same pattern shows up in Telegram (contact name vs. "First/Last name"), Slack (custom display name vs. profile name pulled via SCIM/directory sync), etc. — local override wins, otherwise you inherit the upstream mutable field.

One gotcha: group chat display has its own layer — group nickname (群昵称) > remark > nickname, in that priority order, if the person set a nickname specific to that group.
