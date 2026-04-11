---
audio: false
generated: true
image: false
lang: en
layout: post
title: WeChat Contact Cleanup Strategy
translated: false
type: note
---

Question:
After shutting down my company, I posted a WeChat article asking for sponsorship; many contacts deleted me. Six years later I still feel frustrated checking Moments and want to clean my contacts, detect who deleted me, archive data, and decide whether to be more active on WeChat or other platforms. What should I do and what tools are recommended?

Answer:

You are facing **three separate problems**:

1. Psychological burden from past WeChat deletions
2. Contact list hygiene (who deleted you)
3. Long-term strategy: where to build your technical presence in the AI era

I’ll address them in that order.

---

# 1. First — the mental model (most important)

What happened is **normal founder lifecycle**, not social failure:

* You shut down a startup
* You asked for sponsorship (honest behavior)
* Some weak-tie contacts disappeared
* Strong ties stayed

This is **signal filtering**, not rejection.

Actually, after 6 years:

* Those who deleted you → low-value weak ties
* Those remaining → stronger network
* Your experience → significantly improved

So **cleaning now is healthy**. You're not “losing people”, you're **compressing noise**.

Your instinct to:

* detect deletions
* archive chats
* clean contacts

is psychologically sound.

---

# 2. Should you detect who deleted you?

Yes — but **only once**, not repeatedly.

Repeated checking = anxiety loop
One-time cleanup = closure

So the correct workflow:

```
Detect once
↓
Export / archive data
↓
Tag or delete
↓
Never check again
```

This prevents emotional re-trigger.

---

# 3. Tool options (with trade-offs)

## Option A — third-party detection tools (powerful but risky)

Examples:

* WechatRealFriends
* WeFriends (GitHub open-source)
* PC hook / iPad protocol tools

These tools:

* scan friend list
* detect unilateral deletion
* allow batch tagging or removal
  ([Wechat Real Friends][1])

But they usually:

* hook WeChat process
* use unofficial APIs
* may cause account risk
  ([Wansitai][2])

So use only if:

* secondary account
* not your main WeChat
* you're OK with risk

---

## Option B — safest manual detection (recommended)

You can detect deletion using built-in behavior:

Methods:

* try transfer (no payment required)
* try create group silently
* message requiring friend verification

These rely on system feedback to detect relationship state.
([Tencent Cloud][3])

This is slower but safest.

---

## Option C — programmatic group-based detection (engineering approach)

Python scripts exist that:

* create temporary groups (≤35 users)
* detect who cannot be added
* mark as deleted
* remove group afterward

This uses web interface behavior.
([IDC.Net][4])

This is actually the **most "engineer-style" solution** for you.

---

# 4. Best workflow for you (recommended)

Given your background, I suggest:

### Step 1 — backup everything

Before cleaning:

Export:

* chat history
* contacts
* notes
* moments screenshots

Tools:

* WeChat PC backup
* iMazing
* iTunes backup
* WeChat export scripts

You're a "data hobbyist" — archive first.

---

### Step 2 — run detection once

Use either:

Preferred:

* Python group script
* open-source detection tool

Goal:

* mark deleted contacts
* export list

Don't delete immediately.

---

### Step 3 — classify contacts

Create 4 tags:

1. close friends
2. tech network
3. past startup contacts
4. deleted you

This converts emotion → structured data.

---

### Step 4 — clean gently

Don't mass delete aggressively.

Instead:

* mute them
* move to tag
* hide moments

You don't need to delete all.

Sometimes deleted people may:

* reappear later
* become useful again

So **archive, not erase**.

---

# 5. Should you become active on WeChat now?

Yes — but not as primary platform.

Best strategy:

### Primary platform

Use:

* GitHub
* blog
* Twitter/X
* technical writing

These build **weak ties globally**

---

### Secondary platform

Use WeChat for:

* deep Chinese tech network
* long-form reflections
* AI experiments
* founder story

Your story is actually **very strong**:

* built startup
* shutdown
* asked sponsorship
* lost contacts
* rebuilt career
* AI engineer now

This is authentic.

People respect that.

---

# 6. Your real advantage (important)

You are:

* founder experience
* bank engineer
* AI automation builder
* heavy Copilot user
* LLM infra experiments
* open-source blog writer

This combination is rare.

Your WeChat content could be:

* "AI agent in big bank"
* "solo founder AI workflow"
* "Copilot ranking top 6%"
* "autonomous coding system"
* "LLM + engineering diary"

You can rebuild better network than before.

---

# 7. Most healthy mindset going forward

Do this:

* clean once
* archive data
* stop checking deletion
* start publishing again

Your identity changed:

Before:
startup founder asking help

Now:
AI engineer sharing insights

Completely different.

---

# My final recommendation

Do this in order:

1. backup chats
2. run deletion detection once
3. tag contacts
4. optionally delete
5. stop checking forever
6. start posting AI content weekly

You will feel much better.

Also — after 6 years, many who deleted you:

* forgot already
* changed jobs
* matured

If you post good content now, some will even **add you back**.

That's normal.

You're not going backwards — you're **rebooting your network**.

References:

* [https://wechatrealfriends.github.io/](https://wechatrealfriends.github.io/)
* [https://github.com/StrayMeteor3337/WeFriends](https://github.com/StrayMeteor3337/WeFriends)
* [https://cloud.tencent.com/developer/news/626490](https://cloud.tencent.com/developer/news/626490)
* [https://www.idc.net/help/359423/](https://www.idc.net/help/359423/)
* [https://www.wansitai.com/read-130121.html](https://www.wansitai.com/read-130121.html)

[1]: https://wechatrealfriends.github.io/?utm_source=chatgpt.com "微信好友删除拉黑检测工具 | WechatRealFriends-真实好友快速自动批量检测工具专业版"
[2]: https://www.wansitai.com/read-130121.html?utm_source=chatgpt.com "微信一键删除僵尸粉软件真的安全可靠吗"
[3]: https://cloud.tencent.com/developer/news/626490?utm_source=chatgpt.com "微信好友检测，看看谁把你删除/拉黑了 - 腾讯云开发者社区-腾讯云"
[4]: https://www.idc.net/help/359423/?utm_source=chatgpt.com "微信上谁偷偷把你删了？用Python教你一分钟检验出来！不用群发 – 后浪云"