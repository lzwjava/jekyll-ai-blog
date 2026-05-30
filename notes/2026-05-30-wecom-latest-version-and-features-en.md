---
audio: false
generated: true
image: false
lang: en
layout: post
title: WeCom Latest Version and Features
translated: false
type: note
---

**Question:** Is Enterprise WeChat (WeCom) version 5.0.8 the latest version as of May 30, 2026?

**Answer:**

Yes, your version claim is correct. WeCom V5.0.8 was released on April 22, 2026, and 5.0.8 is indeed the latest version available as of late April 2026. As of today (May 30, 2026), no newer version appears to have been released, so **5.0.8 is the latest**.

Regarding the punch card / attendance confirmation flow you described:

- The **"Confirm Attendance Results Are Correct" (确认考勤结果无误)** button is part of the monthly attendance self-confirmation feature in the 打卡 (Punch Card) app under Workbench.
- If someone doesn't see that button, the most likely causes are:
  1. **Version is outdated** — upgrading to 5.0.8 resolves most missing-feature issues.
  2. **Admin hasn't enabled the feature** — the "attendance result confirmation" workflow must be turned on by the company admin in the attendance rule settings. Not all orgs use it.
  3. **No pending exceptions** — if the month's attendance is already clean (no anomalies), the "Pending Exceptions" entry may not appear or may already be resolved.
  4. **Role restriction** — some confirmation flows are only visible to certain employee roles or after the monthly cutoff date is reached.

So the advice to check the version is sound — but if they're already on 5.0.8 and still don't see the button, the admin config is the next thing to check.

**References:**

- [WeCom Update Log — V5.0.8 (Apr 22, 2026)](https://work.weixin.qq.com/wework_admin/app_intro_list?type=mng&from=frame_footer)
- [WeCom 5.0.8 on Uptodown](https://wecom.en.uptodown.com/android)