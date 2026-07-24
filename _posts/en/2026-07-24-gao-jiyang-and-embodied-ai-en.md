---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gao Jiyang and Embodied AI
translated: false
type: note
---

Question: Who is 高继扬 (Gao Jiyang), founder of 星海图 (Galaxea AI)?

Answer:

高继扬 is a Chinese AI entrepreneur working on **embodied intelligence (具身智能)** — the intersection of robotics, foundation models, computer vision, and real-world AI systems. He is the founder and CEO of 星海图. ([China Daily][1])

His background is unusually aligned with the current "robotics + foundation model" wave:

* **Education**

  * Graduated from Tsinghua University Electronic Engineering.
  * Completed a PhD in computer vision at University of Southern California.
  * Reports say he completed the USC computer vision PhD in about 3.5 years, which was considered very fast. ([The Paper][2])

* **Industry experience**

  * Worked at Waymo.
  * Worked at Momenta.
  * His experience was not only research; it involved autonomous driving systems moving toward real-world deployment. ([Talksai][3])

* **Founded 星海图**

  * 星海图 was founded around 2023.
  * The company focuses on **general embodied intelligence**, aiming to build a "robot brain" rather than only a specific robot body.
  * Their philosophy is often summarized as:

    1. **Model** — embodied foundation models (VLA, world models, etc.)
    2. **Body** — robot hardware platforms
    3. **Data** — large-scale real-world interaction data. ([China Daily][1])

A key idea from Gao's talks:

> Robots will likely not be won by making the best humanoid body alone. The core competition is building the intelligence layer that can operate across different robot forms.

This is similar to the AI stack evolution:

```
Traditional robotics:
        Robot body
            |
     hand-written control
            |
       limited tasks


Future embodied AI:
        Foundation model
              |
        perception + reasoning
              |
        action generation
              |
      many robot embodiments
```

This is why 星海图 talks about **"一脑多形" (one brain, multiple bodies)** — one general intelligence system controlling different robot forms. ([The Paper][2])

From an AI industry perspective, Gao Jiyang belongs to the same generation of founders trying to bring the **LLM scaling paradigm into physical agents**:

| Person     | Area              | Core bet                                     |
| ---------- | ----------------- | -------------------------------------------- |
| 梁文锋        | LLM               | Scaling intelligence in software             |
| 杨植麟        | LLM               | Foundation models                            |
| Gao Jiyang | Embodied AI       | Scaling intelligence into the physical world |
| 王兴兴        | Robotics hardware | Low-cost robot platforms                     |

The interesting part is his **Waymo + Momenta background**. Autonomous driving is basically the closest previous example of "AI agent in the real world":

```
camera / lidar
       ↓
 perception model
       ↓
 world understanding
       ↓
 planning
       ↓
 action
       ↓
 physical environment feedback
```

Embodied AI extends this loop from cars to general robots:

```
vision + language + action model (VLA)
                ↓
        robot manipulation
                ↓
        real-world data
                ↓
        better model
                ↓
             scaling law
```

So his bet is essentially:

**"The next GPT moment may happen not inside a chatbot, but inside machines that can act in the physical world."**

References:

* ([China Daily][1])
* ([The Paper][2])
* ([Talksai][3])
* ([21 Economic Network][4])

[1]: https://cnews.chinadaily.com.cn/a/202606/18/WS6a33d433a310d709c2fb903a.html?utm_source=chatgpt.com "星海图创始人高继扬：具身智能企业要做好模型、本体、数据三张答卷 - 中国日报网"
[2]: https://www.thepaper.cn/newsDetail_forward_27109535?utm_source=chatgpt.com "星海图高继扬：人形机器人不是具身智能的唯一答案_澎湃号·湃客_澎湃新闻-The Paper"
[3]: https://www.talksai.cn/19566/?utm_source=chatgpt.com "清华系操盘手高继扬：92年通用机器人专家，顶级自动驾驶交付经历，风投巨头青睐"
[4]: https://www.21jingji.com/article/20260212/herald/749ec7e87213e59bb51f18545108c713.html?utm_source=chatgpt.com "34岁清华毕业生，28个月制造百亿独角兽 - 21经济网"
