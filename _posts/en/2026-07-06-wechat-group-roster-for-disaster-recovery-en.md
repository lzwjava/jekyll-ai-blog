---
audio: false
generated: true
image: false
lang: en
layout: post
title: WeChat Group Roster for Disaster Recovery
translated: false
type: note
---

**Question:** Should I maintain a member roster document (WeChat ID, name, intro) for my 400–500 person WeChat group, so that if the group gets banned due to GFW / sensitive-content triggers, we can rebuild a new group? How do I do this well and securely?

**Answer:**

Yes — this is standard disaster-recovery practice for large WeChat groups, because a banned/dissolved group leaves you with no member list at all. But a roster alone isn't enough; the mechanics of rebuilding a 500-person group matter more than the document itself.

## What to collect (minimal schema)

Keep it lean — every extra field is extra liability if the doc leaks:

```csv
wechat_id,display_name,intro,backup_contact,row_added
lzwjava,Zhiwei,AI engineer / model training,<EMAIL or TG handle>,2026-07-06
```

- **wechat_id (微信号)** is the critical field — it's searchable and stable. Nicknames change; phone numbers are over-collection.
- **backup_contact** (email or Telegram handle) is your real insurance. If the *group* is banned, WeChat IDs work. If key members' *accounts* get banned, WeChat IDs are useless — you need an out-of-band channel.
- Skip phone numbers, real names, employers unless the group genuinely needs them.

## Where to host it

Tencent Docs (腾讯文档) or Shimo work inside China and support a collection form (收集表) so members self-fill — you don't manually enter 500 rows. Tradeoff: Tencent-hosted content is itself subject to review, so if your group discusses sensitive topics, the roster on Tencent Docs is not where I'd keep the master copy. Practical setup: collect via Tencent Docs form, then periodically export CSV and keep the master offline (encrypted local file, e.g. `age` or a password-protected archive), held by 2–3 admins.

## Rebuild mechanics — the part people underestimate

- WeChat groups cap at 500; **QR-code join only works up to 200 members**. Beyond 200, every person must be invited by an existing member *and* confirm the invite. So rebuilding a 450-person group is a fan-out operation, not one admin clicking 450 times.
- Adding strangers by 微信号 requires them to accept a friend request first, and WeChat rate-limits friend adds (roughly a few dozen/day before you risk restrictions). One admin cannot re-add 400 people.
- Therefore: designate **5–10 "seed" members** who each hold the roster and each re-invite their slice. This turns a multi-week rebuild into a day or two.
- Better still: pre-create a small **lifeboat group** (just the seeds) or a mirror channel (Telegram group / mailing list) that exists *before* anything goes wrong. Announce its existence in the main group once, so members know where to look.

## Security hygiene for the roster itself

- A 500-person roster with IDs + intros is a doxxing target. Access-control the live doc (link + password, edit-by-form-only), and redact anything identifying in copies you share — same discipline as redacting `<IP_ADDRESS>` / `<API_KEY>` in logs.
- Don't put the roster link in the group description permanently; share it periodically and rotate the link.
- Prevention beats recovery: pin group rules about what topics trigger bans, and have admins delete risky content fast. Bans are usually triggered by reports + keyword hits on specific messages, so moderation lowers the probability you ever need the roster.

## Announcement template you can post (Chinese, since your group is)

> 【群备份登记】为防止群意外解散无法找回大家，请花30秒填写：微信号 + 昵称 + 一句话介绍 + 备用联系方式（邮箱/TG）。仅管理员可见，只用于重建群聊。链接：…

One thing worth doing beyond the doc: a simple dedup/validation pass before you rely on it — `python -c "import csv,collections; ..."` style check that wechat_ids are unique and non-empty — because self-filled forms always have ~5% garbage rows, and you'll discover it at the worst possible moment otherwise.

Want me to generate the full CSV template + a small Python script that validates/dedupes the exported roster and splits it into per-seed-member invite lists?
