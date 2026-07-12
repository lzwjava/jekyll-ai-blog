---
audio: false
generated: true
image: false
lang: en
layout: post
title: WeChat Channels Daily Upload Limit
translated: false
type: note
---

Question: What's the daily video upload limit on WeChat Channels (视频号) — is it 10 or more?

Answer: Depends on video type — there's one official hard rule, and no official hard rule for everything else.

**Official, documented limit — product/commerce-linked videos only:**
Tencent's own support page states the rule explicitly, based on follower count: accounts with fewer than 100,000 followers can publish at most 5 product-sharing videos per natural day, and accounts with 100,000+ followers can publish at most 10 per natural day, with the day counted in Beijing time and deleted videos still counting toward the quota. This only applies to videos that use the short-video product-link feature — not regular content.

**Regular (non-commerce) videos — no documented official cap:**
There's no published Tencent policy setting a fixed daily post count for ordinary videos. Community reports are inconsistent:

- Some creators report hitting an upload cap around **10/day** for personal accounts, though this isn't in any official doc I could find.
- Other community posts claim there's effectively no hard number, but posting too aggressively (e.g. >5-10 low-quality videos in a burst) triggers **algorithmic throttling** (限流) rather than a hard block.
- Practical operator consensus (from creator-economy blogs, not Tencent) is 1-3/day for established accounts, 3-5/day during a new account's testing phase — this is a growth-strategy recommendation, not a platform-enforced limit.

**Bottom line for you:** if you're building an agent (`ww`/`zz`-style) to auto-post to 视频号, don't hardcode "10" as a technical ceiling unless you've hit it empirically on your own account — it isn't in Tencent's public docs except for the commerce-video case above. If you're testing automated posting, I'd rate-limit conservatively (≤5/day) and watch for a 频次达到上限-style error response, since that's the only reliable signal of where your specific account's real ceiling is.

References:

- [视频号短视频商品视频发布频次管理规定 (Tencent official)](https://support.weixin.qq.com/cgi-bin/mmsupportacctnodeweb-bin/pages/bHwUU86V3aZ43Dzm)
- [公众号上传视频每日限制 - 微信开放社区](https://developers.weixin.qq.com/community/minihome/doc/0000c0d576c320d8aefbde2785b000)
- [视频号一天可以发布多少条视频？是否有数量上限 - 微信开放社区](https://developers.weixin.qq.com/community/develop/doc/000048305fc788225750b2baa6f400)
