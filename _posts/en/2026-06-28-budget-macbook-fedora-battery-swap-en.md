---
audio: false
generated: true
image: false
lang: en
layout: post
title: Budget MacBook Fedora battery swap
translated: false
type: note
---

At 100-200 CNY ($14-28), it's a no-brainer — do it. That's basically the cost of a nice lunch.

**What you'd get:**

- 59% → ~90-100% battery health
- 2-3 hrs → 6-8 hrs of portable use
- A perfectly usable portable Fedora machine with 16 GB RAM

**What to buy on Taobao:**
Search `MacBook Pro 2017 A1706 电池` or `MacBookPro14,1 battery`. Look for:

- Rated 54.5 Wh or 4770-4790 mAh (matches original)
- Reviews with actual capacity test results
- 1-year warranty minimum
- Brands like 绿巨能 (Lvneng), 品胜 (Pisen), or 基胜 (Jisheng) are decent

**How to replace it:**

```
Tools needed: P5 Pentalobe screwdriver + T3 Torx screwdriver
Time: ~20 minutes
Difficulty: Easy (MacBook Pro 2017 non-Touch Bar is one of the easiest)

Steps:
1. Remove 10x P5 pentalobe screws from bottom case
2. Lift bottom cover off
3. Disconnect battery connector (gently pry up)
4. Remove 5x T3 Torx screws holding battery
5. Peel out old battery (adhesive strips, pull slowly)
6. Insert new battery, reverse steps
7. Done
```

**After replacement**, check health from Fedora:

```bash
upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep capacity
```

At that price, you'd have a portable 16 GB Linux machine for under 200 CNY total. Worth it even just as a travel/backup box.
