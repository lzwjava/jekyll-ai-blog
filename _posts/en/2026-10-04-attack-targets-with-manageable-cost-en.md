---
audio: false
generated: true
image: false
lang: en
layout: post
title: Attack Targets with Manageable Cost
translated: false
type: note
---

Question: Is the world basically a situation where weaker people attack each other, while people avoid attacking genuinely powerful actors because they lack the courage or incentives?

Answer: **There is a real phenomenon here, but “weak people attack weak people” is too simple.** A better model is:

> **People attack targets where the expected payoff is high and the expected cost is manageable.**

The 方舟子–唐骏 case is actually a good example. In 2010, 方舟子 attacked claims about 唐骏's academic credentials, patents, and résumé, and the controversy eventually led 唐骏 to acknowledge that his 西太平洋大学 doctorate was purchased for about $3,000. ([Sina News][1])

But notice the power structure:

```text
方舟子
   │
   │ public evidence + media + reputation
   ▼
唐骏
   │
   │ corporate executive / celebrity
   ▼
large companies / institutions
```

方舟子 wasn't necessarily attacking someone *weak*. 唐骏 was quite powerful in the commercial/media sphere. The interesting thing is that **his vulnerability was unusually high**: credentials and factual claims are things that can be checked.

### The deeper mechanism

Think in expected-value terms:

$$
U(\text{attack}) =
P(\text{win}) \cdot R
-
P(\text{retaliation}) \cdot C
+
S
$$

where:

* \\(R\\) = reward/status gained from exposing the target
* \\(C\\) = cost of retaliation
* \\(S\\) = intrinsic satisfaction / moral motivation
* \\(P(\text{win})\\) = probability your evidence survives scrutiny

People preferentially attack when:

$$
P(\text{win})R \gg P(\text{retaliation})C
$$

That's why **credentials, scientific claims, plagiarism, fraud, public statements, etc. are attractive targets**. The attacker can bring evidence.

But attacking a genuinely powerful institution can have:

```text
small additional reward
+
huge asymmetric retaliation
+
uncertain probability of winning
```

So rational actors become much more cautious.

### And this is not unique to China

You can see the same structure in universities, corporations, politics, open-source communities, and even technical organizations.

A junior engineer may aggressively criticize another junior engineer's PR:

```text
cost = almost zero
reward = reputation
```

But criticizing the VP's favorite project:

```text
cost = potentially losing promotion
reward = small
```

So the engineer becomes much more diplomatic.

This produces what you might call **local courage**:

> People are brave where the power differential is small enough that retaliation is survivable.

There is another important distinction, though.

### “Not attacking” does not necessarily mean cowardice

Sometimes the stronger target simply has **legitimate power**.

If I discover that an unknown engineer's résumé contains a false PhD:

```text
easy target
high evidentiary confidence
little downside
```

If I discover that a government agency has done something questionable:

```text
much harder fact pattern
institutional complexity
possible retaliation
potentially enormous consequences
```

Not speaking publicly could be rational risk management rather than lack of moral courage.

And sometimes people *do* attack powerful actors—but usually through mechanisms that reduce personal exposure:

```text
anonymous whistleblower
journalist
lawsuit
independent institution
collective action
leaked documents
academic publication
```

That's a very important pattern.

**Power doesn't eliminate criticism. It changes the cost structure of criticism.**

### Your intuition becomes stronger if you replace “weak vs strong” with “low-risk vs high-risk”

I'd formulate your observation this way:

> **Human beings disproportionately confront people who are both vulnerable and socially valuable to confront, while avoiding targets whose retaliation capacity greatly exceeds the expected benefit of confrontation.**

That explains much more than “the weak attack the weak.”

And there is an interesting second-order effect:

**The people who repeatedly attack relatively safe targets can acquire a reputation for courage without necessarily demonstrating courage against the most powerful targets.**

That's where your observation about 方舟子 becomes philosophically interesting. Whether one agrees with his specific political positions or not, you can separate two questions:

1. **Is his factual criticism correct?**
2. **What classes of targets is he willing to confront?**

Those are independent variables.

A person can be extremely courageous in one dimension and extremely conservative in another.

([People's Daily Paper][2])

References:

* [方舟子：唐骏自传80%造假](https://news.sina.com.cn/o/2010-07-11/142217788313s.shtml?utm_source=chatgpt.com)
* [唐骏学历争议概述](https://zh.wikipedia.org/wiki/%E5%94%90%E9%AA%8F?utm_source=chatgpt.com)
* [方舟子与“打假”争议报道](https://paper.people.com.cn/hqrw/html/2012-04/06/content_1037045.htm?utm_source=chatgpt.com)

[1]: https://news.sina.com.cn/o/2010-07-11/142217788313s.shtml?utm_source=chatgpt.com "方舟子：唐骏自传80%造假_新闻中心_新浪网"
[2]: https://paper.people.com.cn/hqrw/html/2012-04/06/content_1037045.htm?utm_source=chatgpt.com "环球人物"
