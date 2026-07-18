---
audio: false
generated: true
image: false
lang: en
layout: post
title: Child's Tab Navigation Learning Failure
translated: false
type: note
---

Question: [Rephrased]
How is this idea: guiding my daughter from global apps (YouTube, YouTube Kids, TikTok) to domestic apps, but she failed to learn the app UI switch between two top buttons: “商城” and “推荐”?

Answer:

This is actually a very interesting **product learning / UX experiment**. The failure is not surprising — it reveals how children learn interfaces.

For adults:

```
顶部按钮:
[商城] [推荐]

mental model:
"These are two tabs. Click to switch content."
```

For a child:

```
screen = a world
button = maybe decoration
```

She may not have formed the concept of **navigation state** yet.

YouTube/TikTok trained her with a very different interaction model:

```
TikTok:
swipe up → next content

YouTube Kids:
tap picture → video

No need to understand tabs.
```

The new app asks for:

```
observe:
"there are two categories"

infer:
"they change the whole page"

remember:
"clicking top area switches mode"
```

This is a higher-level abstraction.

It is similar to AI agents learning UI:

A human sees:

```
[Settings] [Profile] [Home]
```

and understands semantics.

A vision agent sees:

```
pixels + coordinates
```

and needs exploration.

Children are closer to agents during early UI learning. They learn by **action → feedback**.

A better teaching path:

### Stage 1: Make the state obvious

Instead of:

```
商城 | 推荐
```

use:

```
🛒 买东西
⭐ 看视频
```

Icons + meaning.

### Stage 2: Create a task

Don't say:

> "Click 推荐"

Say:

> "我们去找一个小猫视频"

Then guide:

```
Where do you think videos are?
```

Let her discover.

### Stage 3: Build transfer learning

Connect old app:

```
TikTok:
swipe = change video

New app:
推荐 = video area
商城 = shopping area
```

Children learn via analogy.

---

Actually this is also a good reminder for AI product design:

Many apps assume:

```
user knows navigation
```

but onboarding should teach:

```
action → result → mental model
```

The best interfaces are almost like children's toys:

* obvious affordance
* immediate feedback
* low memory requirement

Your daughter's failure is useful data 😄. It is exactly the kind of usability test companies pay for. A 5–7 year old user has zero legacy assumptions, so she exposes hidden UX complexity.
