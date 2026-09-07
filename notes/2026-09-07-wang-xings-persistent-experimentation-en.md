---
audio: false
generated: true
image: false
lang: en
layout: post
title: Wang Xing’s Persistent Experimentation
translated: false
type: note
---

Question: **Why does Meituan’s Wang Xing keep going after failing so many times?**

Answer: The key is that **Wang Xing doesn't seem to interpret failure as “I am a failed entrepreneur.” He treats each company as an experiment in a much longer game.**

His history is unusually clear:

* **Xiaonei (校内网)** — successful product, but he ran out of money and sold it for about $2M.
* **Fanfou (饭否)** — strong product, but was shut down for regulatory reasons.
* **Hainei (海内网)** — failed to become a major network.
* **Meituan** — entered the brutal “thousand Groupon war,” then eventually won.
* **Dianping merger** — instead of insisting Meituan had to win alone, he merged with a major competitor.
* Then Meituan expanded from group buying → food delivery → hotels → travel → local services → instant retail. ([Sina Finance][1])

So I think there are **five important mechanisms** behind his persistence.

### 1. He separates *self* from *project*

This is probably the biggest one.

A normal psychological loop is:

```text
project fails
    ↓
"I failed"
    ↓
identity damage
    ↓
avoid another attempt
```

Wang Xing's loop appears closer to:

```text
hypothesis
    ↓
build
    ↓
market feedback
    ↓
failure
    ↓
update model of reality
    ↓
new hypothesis
    ↓
build again
```

That is much closer to **scientific experimentation** than conventional career thinking.

His first major company didn't work out, but the founder didn't disappear. His second company was killed by external circumstances. He still continued. ([China Story][2])

---

### 2. His failures were not actually “zero”

This is important.

Suppose:

```text
Xiaonei → failure
Fanfou  → failure
Hainei  → failure
Meituan → success
```

You might calculate:

```text
success rate = 1 / 4 = 25%
```

But that's the wrong model.

Each iteration gave him:

```text
engineering experience
+ recruiting experience
+ fundraising experience
+ product intuition
+ understanding of users
+ understanding of competition
+ understanding of capital
+ understanding of regulation
```

So the real state is more like:

```text
S0
 ↓
failure → S1
 ↓
failure → S2
 ↓
failure → S3
 ↓
success
```

The failures **changed the state of the entrepreneur**.

That is why experienced founders can look irrationally persistent from the outside. You're counting failed companies; they're counting accumulated information.

---

### 3. He learned to change the *game*, not merely try harder

This is where Wang Xing becomes particularly interesting.

He didn't keep making Facebook clones forever.

Eventually he recognized:

> Social networking was extremely powerful, but also heavily dependent on network effects, capital, and regulation.

Then he moved toward local services.

Meituan started as a Groupon-style group-buying company. But when the “thousand Groupon war” became insanely competitive, Wang Xing gradually concentrated on food and dining, where transactions could happen repeatedly rather than being one-off coupon purchases. ([Irish Examiner][3])

That's a crucial distinction:

```text
stubbornness:
    "I will keep doing the same thing until I win."

persistence:
    "I will keep playing, but I will change my strategy."
```

Wang Xing appears much closer to the second.

---

### 4. He has unusually long time horizons

There's a famous idea associated with Wang Xing:

> **无限游戏 — infinite game**

In a finite game:

```text
Win this competition.
Beat this competitor.
Make this quarter's profit.
```

In an infinite game:

```text
Stay alive.
Keep learning.
Keep accumulating capability.
Keep finding new games worth playing.
```

This explains some otherwise strange Meituan decisions.

For example, Meituan recently spent enormous amounts fighting Alibaba and JD.com in food delivery. It suffered major losses during the subsidy war, including a ¥6.82B loss in Q1 2026. But by Q2 it returned to ¥2.155B net profit as competition eased. ([The Wall Street Journal][4])

From a short-term perspective:

> “Why burn billions?”

From the infinite-game perspective:

> “What strategic asset are we buying?”

Potential answers:

```text
users
merchant relationships
rider network
logistics density
delivery infrastructure
consumer habits
instant-retail infrastructure
```

And that's exactly where the company is moving now: food delivery → instant retail → increasingly general local fulfillment. Reuters reported that Meituan held about **45.3% of instant retail** in Q2 2026, very close to Alibaba's 45.7%. ([Reuters][5])

So the “failure” of one battle doesn't necessarily mean failure of the overall strategy.

---

### 5. He seems to have very high tolerance for uncertainty

This is underrated.

Most people optimize:

```text
risk ↓
certainty ↑
income stability ↑
```

An entrepreneur like Wang Xing appears to optimize more like:

```text
optionality ↑
learning rate ↑
upside ↑
survival ↑
```

That's a different utility function.

Imagine two people:

**Person A**

```text
Job
→ salary
→ promotion
→ stable career
```

**Person B**

```text
attempt
→ failure
→ attempt
→ failure
→ new information
→ attempt
→ massive upside
```

For Person B, several failures can be rational **if the downside is survivable and the upside is enormous**.

That's basically venture capital logic applied to one's own life.

---

## The deeper lesson

I wouldn't summarize Wang Xing as:

> **“Never give up.”**

That's too shallow.

The much more interesting principle is:

> **Don't confuse failure of an implementation with failure of the underlying objective.**

For example:

```text
Goal:
build something valuable

Implementation #1:
Xiaonei       → failed/sold

Implementation #2:
Fanfou        → shut down

Implementation #3:
Hainei        → failed

Implementation #4:
Meituan       → worked
```

The objective remained relatively stable:

```text
internet
→ large-scale products
→ massive user networks
→ real-world services
```

But the implementation kept changing.

That's very similar to training an AI system:

```python
while not_solved:
    trajectory = run(policy)
    error = evaluate(trajectory)
    policy = update(policy, error)
```

A failed rollout isn't an existential crisis for the model.

It is **training data**.

And honestly, this may be one reason Wang Xing is such an interesting entrepreneur for someone building AI products: **the useful question after failure isn't “am I good enough?” but “what did reality just tell me?”**

One caveat: the popular “nine failures, one success” narrative is partly a retrospective framing; the exact count and characterization of his early ventures varies by source. The underlying pattern of repeated attempts is well documented. ([Sina Finance][1])

I can also break down **Wang Xing vs. Elon Musk vs. Liang Wenfeng/Karpathy** as three very different ways of dealing with failure and long-term uncertainty.

[1]: https://finance.sina.com.cn/wm/2026-05-15/doc-inhxytzf3300439.shtml?utm_source=chatgpt.com "王兴：九败一胜，美团的无限游戏 从连续创业失败到外卖帝国掌舵人丨〖商业人物档案〗|美团_新浪财经_新浪网"
[2]: https://www.chinastory.cn/PCywdbk/english/v1/detail/20190906/1012700000042741567733471315808045_1.html?utm_source=chatgpt.com "Wang Xing: The 'poet entrepreneur' behind Meituan Dianping-China Story"
[3]: https://www.irishexaminer.com/opinion/commentanalysis/arid-30915780.html?utm_source=chatgpt.com "Dishing out big changes: China's market leaders"
[4]: https://www.wsj.com/business/earnings/meituan-returns-to-profit-as-food-delivery-competition-eases-1026a0e9?utm_source=chatgpt.com "Meituan Returns to Profit as Food-Delivery Competition Eases"
[5]: https://www.reuters.com/business/retail-consumer/chinese-e-commerce-moves-next-phase-after-delivery-price-war-changes-shopping-2026-09-03/?utm_source=chatgpt.com "Chinese e-commerce moves to next phase after delivery price war changes shopping habits"
