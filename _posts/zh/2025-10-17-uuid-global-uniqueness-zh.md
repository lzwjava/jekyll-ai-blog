---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: UUID确保全局唯一性无需协调
translated: true
type: note
---

UUID能够在无需中央授权的情况下实现全局唯一标识，是因为其设计拥有巨大的地址空间：128位长度可提供约3.4×10^38种可能值。这个数量级远超全球所有系统实际场景中将会生成的UUID总数。对于版本4 UUID（随机生成类型，如您分享的示例），其中122位由高质量随机数据填充，使得重复概率微乎其微。

关于碰撞问题：理论上确实可能存在两个相同UUID，但实际应用中的概率低至可忽略不计。这遵循概率论中的“生日悖论”——随着生成数量增长，碰撞概率会上升，但即便如此：
- 任意两个随机版本4 UUID发生碰撞的概率约为2.71×10^18分之一
- 需要生成约4.8×10^18个UUID（相当于全球每人持有6亿个）才可能出现50%的重复概率
- 即使生成1万亿（10^12）个UUID，碰撞风险也仅约十亿分之一

不同UUID版本还设有额外保障机制：版本1采用时间戳与MAC地址，版本5通过命名空间哈希命名等。但仅凭版本4的随机性，就足以确保分布式系统、数据库或应用程序在无协调机制下的唯一性。

[碰撞概率究竟有多低？](https://jhall.io/archive/2021/05/19/what-are-the-odds/)
[通用唯一识别码 - 维基百科](https://en.wikipedia.org/wiki/Universally_unique_identifier)
[Java UUID.randomUUID 的碰撞概率有多大？](https://stackoverflow.com/questions/24876188/how-big-is-the-chance-to-get-a-java-uuid-randomuuid-collision)
