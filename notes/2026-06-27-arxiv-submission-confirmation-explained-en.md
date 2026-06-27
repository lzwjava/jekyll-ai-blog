---
audio: false
generated: true
image: false
lang: en
layout: post
title: arXiv Submission Confirmation Explained
translated: false
type: note
---

Question: How do I understand this arXiv submission confirmation? How long until announcement, and will it be rejected?

Answer:

This is a standard automated acknowledgment. Nothing has gone wrong — it just means arXiv received your submission and queued it for screening.

**What's happening now**

Your paper is in the moderation/screening pipeline. arXiv runs both automated checks (TeX compiles, no overlap/plagiarism flags, formatting sanity) and human moderation (a moderator confirms the paper fits the claimed category and meets basic scholarly standards). The `submit/xxx` is a temporary ID; once announced you get a permanent `arXiv:YYMM.NNNNN` identifier.

**Timeline**

- Typically **~2 business days** to screen.
- Announcements happen at **20:00 ET, Sunday–Thursday**.
- The key cutoff: submissions finalized before **14:00 ET on a business day** are queued for that night's announcement cycle. Miss the cutoff and you roll to the next cycle. Weekends and US holidays don't count, so a Friday submission often won't announce until Monday night.

So concretely: if you finalized today and it clears screening, expect it live within 1–3 calendar days, landing on a Sun–Thu evening.

**Will it be rejected?**

Most submissions are *not* rejected — they're announced. The realistic outcomes ranked by likelihood:

1. **Announced as-is** — most common.
2. **Reclassified** — moderator moves it to a more appropriate category (e.g. `cs.LG` → `cs.CL`). Minor, automatic.
3. **Put on hold** — moderator wants clarification, or it's flagged for endorsement/overlap review. Adds days. You'd get an email.
4. **Returned/removed** — rare, and usually for: missing endorsement (first-time submitters in some categories need an endorser), content that reads as non-research, heavy text overlap with prior work, or wrong-venue material.

The most common *actual* friction for a first submission is the **endorsement requirement** — if you hit that, it usually surfaces before or right at submission, not silently later.

There's no action to take right now. Watch your email and the dashboard status field. If it sits on "on hold" more than a few days with no email, that's when to investigate. Otherwise just wait for the announcement mail with your permanent ID.

If you tell me the category you submitted to (e.g. `cs.AI`, `cs.LG`) and whether this is your first arXiv paper, I can tell you whether endorsement is a likely snag.
