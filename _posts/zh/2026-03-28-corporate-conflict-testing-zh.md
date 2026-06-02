---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过循证测试解决企业冲突
translated: true
type: note
---

Question:
在大型公司中，解决冲突的一种有效方法是让双方都尝试彼此的方法（A 与 B），这样在 implementation 之后差异变得清晰，争论也会减少，这种说法对吗？

Answer:

是的 —— 这实际上是 **大型组织中最有效的 conflict-resolution 策略之一**，特别是针对技术或架构上的分歧。它用 **evidence-based decision making** 取代了 **opinion-based debate**。

这种方法通常被称为：

* **Spike solution**
* **Proof of Concept (PoC)**
* **A/B implementation**
* **Parallel experiment**
* **Bake-off**
* **Prototype comparison**

---

## 为什么这种方法有效

当两个人在争论时：

* A 捍卫 **Approach A**
* B 捍卫 **Approach B**
* 双方都依赖于假设
* 讨论变得情绪化或政治化

但当双方都进行 **implement and test** 时：

* 假设变得可衡量
* tradeoffs 变得可见
* 误解消失
* 尊重增加

对话从：

> “我的想法更好”

转变为：

> “Approach A 在 X 方面表现更好，但在 Y 方面较差”

这极大地提高了 decision quality。

---

## 双方尝试后哪些情况会变得清晰

在并行尝试之后，团队可以比较：

* Performance
* Complexity
* Maintainability
* Dev speed
* Failure cases
* Operational cost
* Team understanding
* Debug difficulty
* Scalability

现在决策是 **显而易见** 的，而不是政治化的。

---

## 示例（现实的工程场景）

Conflict：

* Engineer A：“使用 microservices”
* Engineer B：“使用 modular monolith”

与其争论 2 周：

团队决定：

* A 构建 microservice prototype
* B 构建 modular monolith prototype
* 双方解决相同的功能

2 天后：

结果：

* Microservices → complex infra，slower dev
* Monolith → simpler，faster

决策变得容易。

无需争论。

---

## 更强大的版本

大型技术公司中的最佳实践：

* **同一个人同时 implement A 和 B**

为什么？

因为：

* 消除了自我（ego）
* 消除了 bias
* 确保公平比较
* 深入理解

这非常有效。

---

## 这种方法减少了

* 无休止的会议
* 政治斗争
* 基于资历的决策（Seniority-based decisions）
* “舆论战”
* 架构教条（Architecture dogma）

它增加了：

* Engineering culture
* Empirical thinking
* Trust
* Learning
* Team alignment

---

## 什么时候最适合使用这种方法

在以下情况使用：

* Architecture 分歧
* Tool 选择冲突
* Framework 争论
* Performance 争论
* API design 分歧
* Data model 冲突

不适用的情况：

* 决策微不足道
* 成本过高
* 截止日期紧急
* 不可测试

---

## 为什么仅靠争论会失败

因为在大型企业中：

* 人们捍卫名誉
* 人们捍卫所有权（ownership）
* 人们捍卫过去的决定
* 人们害怕出错

但实验消除了 **丢面子（face loss）** 的风险。

没有人是“错误”的 —— 只有数据说话。

---

## 这实际上是 senior engineering mindset

优秀的工程师会说：

> “让我们两种都试一下，然后测量结果。”

平庸的工程师会说：

> “相信我，我的更好。”

经理们喜欢第一种人。

---

## 最终结论

是的 —— 让双方 **implement and compare** 是大型组织中解决冲突最务实、最成熟的方法之一。它实现了：

* debate → experiment
* opinion → evidence
* ego → learning
* conflict → alignment
