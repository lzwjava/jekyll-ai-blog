---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Telegram iOS 作者与竞赛编程背景
translated: true
type: note
---

根据我的调查，以下是关于Telegram-iOS主要作者及其OI/IOI背景的发现：

---

## Telegram-iOS 主要贡献者

| 排名 | GitHub | 姓名 | Commits |
|------|--------|------|---------|
| 1 | laktyushin | Ilya Laktyushin | 7,952 |
| 2 | petertechstories | Peter Iakovlev | 1,502 |
| 3 | appleguy | Scott Goodson | 915 |
| 4 | DerAndereAndi | - | 891 |
| 5 | overtake | - | 890 |
| 6 | maicki | - | 572 |
| 7 | lumaxis | - | 453 |
| 8 | smohantty | - | 452 |
| 9 | Adlai-Holler | - | 414 |
| 10 | nguyenhuy | - | 302 |

---

## 确认的 OI/IOI/算法竞赛优胜者

**Nikolai Durov**（Telegram 联合创始人，VK 联合创始人，Pavel Durov 的兄弟，MTProto 协议作者）：

- **3 枚**国际数学奥林匹克（IMO）金牌（1996、1997、1998）
- **3 银 + 1 金**国际信息学奥林匹克（IOI，1995-1998）
- **2 次** ACM ICPC 世界总决赛金牌（2000、2001），代表圣彼得堡国立大学
- 数学博士（圣彼得堡国立大学 + 波恩大学，师从 Gerd Faltings）

这绝对是精英级别的竞技编程背景——全球前 0.001%。

---

## 针对 iOS 代码库

具体到 iOS 代码库——Ilya Laktyushin（7,952 次提交，主要 iOS 作者）和 Peter Iakovlev（1,502 次提交）——我未能找到公开可验证的 OI/IOI 记录。他们未出现在 Codeforces（Cloudflare 阻拦了我）或我能访问的任何公开竞赛数据库中。他们的 GitHub 个人资料内容稀少，没有关于竞技编程背景的个人简介。

尽管如此，该仓库的代码质量非常卓越——架构（Postbox → TelegramEngine 重构、AsyncDisplayKit 的使用、Bazel 构建系统）体现了深厚的系统思维。这种能力是来自竞技编程训练还是单纯的天才工程才能，仅凭公开数据很难判断。

**可验证的结论在于最顶端：** Telegram 的技术联合创始人 Nikolai Durov 是历史上成就最高的竞技程序员之一——IMO 金牌、IOI 金牌、ACM ICPC 金牌。这就是 Pavel Durov 在谈论 Telegram 工程文化时所提到的“算法竞赛优胜者”。
