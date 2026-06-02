---
audio: false
generated: true
image: false
lang: zh
layout: post
title: HuggingFace 关注者排行榜前30名
translated: true
type: note
---

已完成。`ww hf top30` 已生效。以下是真实数据：

```
HuggingFace 用户关注数 TOP30
来源：Weyaxi/followers-leaderboard（2026-05-30 04-08）
============================================================
  #  用户名                    关注者数量    关注人数
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
数据集中总用户数：17,279
```

我做了以下操作：

- 在 `ww/hf/hf.py` 中添加了 `cmd_top30()` 函数——从 Weyaxi/followers-leaderboard 数据集（与 Space 相同的数据源）获取最新 CSV，解析后按关注者数量排序
- 在 `ww/main.py` 中注册了 `top30` 子命令
- 数据来源：HuggingFace Datasets API（无需认证，公开 CSV）

从真实数据中得出的关键观察：

- TheBloke 以约 27K 关注者遥遥领先——几乎是第二名 bartowski 的 2.5 倍
- HuggingFace 员工：merve（第 4 名，10.2K）、ylecun（第 6 名，9K）——但值得注意的是 thomwolf/clem/osanseviero 均未进入前 30
- teknium 以 7,307 名关注者位列第 11——证实了你之前关于他在 HuggingFace 上影响力强大的观点
- victor（第 18 名）关注了 1,455 人——是关注人数最多的关注者
- lllyasviel（第 3 名）和 ylecun（第 6 名）均未关注任何人
