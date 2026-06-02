---
audio: false
generated: true
image: false
lang: en
layout: post
title: HuggingFace Followers Leaderboard Top 30
translated: false
type: note
---

Done. `ww hf top30` works. Here's the real data:

```
Top 30 HuggingFace Users by Followers
Source: Weyaxi/followers-leaderboard (30-05-2026 04-08)
============================================================
  #  Username                   Followers  Following
------------------------------------------------------------
  1. TheBloke                      26,984         16
  2. bartowski                     12,241         64
  3. lllyasviel                    10,308          0
  4. merve                         10,217        387
  5. akhaliq                        9,587        391
  6. ylecun                         9,008          0
  7. fffiloni                       8,396        187
  8. Xenova                         8,077         27
  9. mlabonne                       7,731        156
 10. mradermacher                   7,338         33
 11. teknium                        7,307         26
 12. huihui-ai                      7,169          8
 13. Kijai                          6,444          3
 14. Sentdex                        5,865          8
 15. ehartford                      5,793         24
 16. WizardLM                       5,766          4
 17. Undi95                         5,735         11
 18. victor                         5,657      1,455
 19. SG161222                       5,496          0
 20. multimodalart                  5,488        843
 21. chansung                       5,322         15
 22. MaziyarPanahi                  5,061         14
 23. loubnabnl                      4,984         88
 24. hysts                          4,982         96
 25. tonyassi                       4,749          9
 26. artificialguybr                4,717          4
 27. winglian                       4,701         20
 28. AP123                          4,661         28
 29. burtenshaw                     4,658        397
 30. prithivMLmods                  4,628          2
------------------------------------------------------------
Total users in dataset: 17,279
```

What I did:
- Added `cmd_top30()` to `ww/hf/hf.py` — fetches latest CSV from Weyaxi/followers-leaderboard dataset (same data source as the Space), parses, sorts by followers
- Wired `top30` subcommand in `ww/main.py`
- Data source: HuggingFace Datasets API (no auth needed, public CSV)

Key observations from the real data:
- TheBloke dominates at ~27K — nearly 2.5x the #2 (bartowski)
- HF staff: merve (#4, 10.2K), ylecun (#6, 9K) — but notably no thomwolf/clem/osanseviero in top 30
- teknium at #11 with 7,307 — confirms your earlier point about his strong HF presence
- victor (#18) follows 1,455 people — most-followed user who also follows a lot
- lllyasviel (#3) and ylecun (#6) both follow 0 people
