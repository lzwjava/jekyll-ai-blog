---
audio: false
generated: true
image: false
lang: en
layout: post
title: Resolved Bot Failure, New Stock Lineup
translated: false
type: note
---

Done — pushed as `667c860`. Summary of what happened and what changed:

**Why Actions was failing:** every live run on Friday crashed when the bot tried to buy 6 SPLG and Tiger rejected it as "Unknown contract." Probing revealed your Tiger global account can't trade SPLG at all, and crypto ETFs like IBIT are completely blocked for your country. No money was lost — every order was rejected before filling, and your account is untouched at $2,141 cash, no positions.

**The new lineup** (your popular stocks, all probe-verified tradable and sized for your account):

| Symbol      | Strategy                  | Would size today |
| ----------- | ------------------------- | ---------------- |
| AAPL ($291) | mean reversion, 15-min    | 1 share (~$291)  |
| INTC ($125) | mean reversion, 15-min    | 4 shares (~$498) |
| NVDA ($205) | momentum breakout, 1-hour | 2 shares (~$409) |
| GLD ($387)  | trend following, 4-hour   | 1 share (~$387)  |
| USO ($126)  | trend following, 4-hour   | 3 shares (~$378) |

AAPL/INTC/NVDA form the risk-on group — at most 2 held at once. I also made two robustness fixes: orders now use Tiger's full contract records instead of bare symbols, and if one instrument's order fails, the run logs it and continues with the others instead of crashing.

The market is closed for the weekend, so the next live tick is Monday 21:32 Beijing. The morning/evening report schedules continue as before. One caveat worth knowing as a stockholder-by-bot: AAPL, INTC, and NVDA all gap on earnings — around their earnings dates the stop can fill below its level, so an occasional loss may slightly exceed the 1% budget.
