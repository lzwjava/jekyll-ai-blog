---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 囚徒困境简介
translated: true
type: note
---

Question: What is the Prisoner's Dilemma?

Answer:

**Prisoner's Dilemma** 是 game theory 中的一个核心概念，它描述了一种情境：两个理性的个体在追求自身利益最大化时，即使合作会带来更好的集体结果，也往往会选择不合作。

### Classic Scenario

两名嫌疑人（Prisoner A 和 Prisoner B）因涉嫌犯罪被捕，并被分开审讯。检察官向每人提供了一份方案：

- 如果**两人都保持沉默**（互相合作），则各判处较轻的刑期：**1 年**。
- 如果**一人认罪**（背叛），而另一人保持沉默，则认罪者将**获释**（0 年），而沉默者将面临重刑：**3 年**。
- 如果**两人都认罪**（互相背叛），则各判处中等刑期：**2 年**。

这种设定产生了如下的收益矩阵（数字越小越好，代表服刑年数）：

|                  | B 保持沉默 (Cooperate) | B 认罪 (Defect) |
|------------------|----------------------------|----------------------|
| **A 保持沉默 (Cooperate)** | A: 1 年<br>B: 1 年    | A: 3 年<br>B: 0 年 |
| **A 认罪 (Defect)**       | A: 0 年<br>B: 3 年  | A: 2 年<br>B: 2 年 |

### Key Insight

- 对于每个囚犯个体而言，**认罪（背叛）是 dominant strategy**：无论对方做什么，认罪都能带来更好的个人结果（0 年或 2 年，优于 1 年或 3 年）。
- 然而，如果双方都遵循这种理性自利，他们都会认罪并各获刑 **2 年**——这一结果比双方都合作（各获刑 1 年）要糟糕。
- 因此，共同合作在集体层面上更好，但个体的理性却导致了共同背叛。

### Broader Implications

Prisoner's Dilemma 模拟了许多现实世界的冲突，例如：

- 国家间的军备竞赛
- 环境问题（如过度捕捞或污染）
- 商业价格战
- 社会困境，如疫苗接种或纳税合规性

它解释了为什么即使合作对所有人都有利，合作也很难达成。该理论对 economics、political science、evolutionary biology 和 ethics 等领域产生了深远影响。

在博弈的重复版本（iterated Prisoner's Dilemma）中，像 "Tit for Tat"（首轮合作，之后模仿对手前一步的行动）这样的策略可以促进持续的合作。
