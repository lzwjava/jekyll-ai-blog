---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cooking as AI Training Metaphor
translated: false
type: note
---

Question: Is the idea of cooking as a metaphor for data/model training and deep conversations about AI, languages, and science a good analogy?

Answer:

Yes, this analogy is actually very close to how modern AI engineering feels.

Cooking:

* Buy different ingredients:

  * vegetables
  * meat
  * spices
  * fruits

↓

Machine learning:

* Collect different data:

  * books
  * code
  * conversations
  * scientific papers
  * images
  * videos

The quality is not only about having "more ingredients". It is about:

1. **Ingredient diversity = data diversity**

A soup with only potatoes is boring.

A model trained only on one domain becomes narrow:

```
only code -> good coder, weak general reasoning
only math -> good equations, weak world knowledge
only internet text -> broad, but noisy
```

The magic comes from mixing:

```
code + math + science + literature + conversations + multilingual data
```

similar to a good hotpot.

---

2. **Container size = model capacity**

Your analogy:

> 不同容器大小，水量如何，不同做法

is basically:

```
model size
+
dataset size
+
training recipe
```

A small pot:

```
7B model
8GB VRAM
small dataset
```

cannot cook a huge feast.

A giant pot:

```
405B model
H100 cluster
trillions tokens
```

can absorb much more complexity.

But a giant pot with bad ingredients is still bad.

---

3. **Cooking method = training recipe**

Same ingredients:

```
beef + vegetables + water
```

can become:

* soup
* stir fry
* barbecue
* hotpot

Same data:

```
FineWeb
GitHub
books
papers
```

can produce different models:

* GPT-style base model
* coding model
* reasoning model
* chat model

The "chef skill" matters.

This is why Karpathy often emphasizes:

> data + architecture + optimization + evaluation

not just parameter count.

---

4. **"无他，手熟而已" is actually very ML**

A lot of frontier AI work is accumulated craft:

```
train
 ↓
observe loss curve
 ↓
change data
 ↓
change tokenizer
 ↓
change LR schedule
 ↓
change architecture
 ↓
repeat
```

The final recipe looks simple:

```
model.fit(data)
```

but behind it are thousands of small decisions.

Like a chef saying:

"Just cook it."

But the difference between a normal dish and a Michelin dish is 20 years of small adjustments.

---

And your second point:

> 超喜欢和人聊天，只是不讲枯燥车轱辘讲，用日语讲，用英语讲，讲 AI，谈天说地，从王垠讲到牛顿

This is actually the same idea as a good language model.

A good conversation is not:

```
question -> answer -> question -> answer
```

It is:

```
human experience
       +
history
       +
science
       +
language
       +
humor
       +
personal curiosity
```

A person who can jump:

```
王垠
 ↓
programming philosophy
 ↓
AI agents
 ↓
Karpathy
 ↓
Newton
 ↓
physics
 ↓
Japanese culture
```

is doing high-dimensional knowledge navigation.

That is also what we want from models:

not just retrieval, but **connecting distant concepts**.

Your cooking analogy is close to the core idea of intelligence:

> Intelligence is not memorizing ingredients. It is learning how ingredients combine into new dishes.

The interesting future is probably not "bigger pot forever", but better chefs + better ingredients + better recipes.
