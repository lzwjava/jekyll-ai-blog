---
audio: false
generated: false
image: false
lang: en
layout: post
title: Interview with Zhang Junhong — Founder of ThingsPanel
translated: false
---

**Date:** June 2026
**Location:** Shenzhen, China
**Interviewer:** lzwjava
**AI Translation Tips:** Zhang Junhong(张军宏)

## Overview

Zhang Junhong (born in 1979, age 47) is the founder of ThingsPanel, an open-source IoT platform built with Go. He entered Northwest University in 1998, majoring in Public Administration. During his junior year, he taught himself programming. After graduation, he worked as a programmer for more than a year, then moved into other fields including literary editing and design. At IT companies, he eventually worked in almost every role except front desk and finance, before eventually starting his own company in Beijing.

ThingsPanel was born during the COVID-19 pandemic in 2020. At the time, Junhong was working on an IoT project in Malaysia and was using the overseas software [ThingsBoard](https://thingsboard.io), which was expensive and not particularly pleasant to use. After the pandemic broke out, he returned to China and could no longer meet customers face-to-face. He therefore decided to build software that could be delivered entirely online and would not be constrained by geography.

The name "ThingsPanel" was chosen as a counterpart to ThingsBoard — replacing "Board" with "Panel," both referring to dashboards/panels. Six years later, the platform has more than 50,000 downloads and over 3,000 community users, and has been deployed in infrastructure projects worth hundreds of millions of RMB.

The core themes of the interview are:

1. **The origins of the startup** — The pandemic forced a shift toward remote delivery; ThingsBoard became the benchmark that drove the product ambition.
2. **How to win large customers** — Large state-owned telecom operators and other SOEs often cannot build IoT systems themselves; open source establishes trust, while the enterprise edition monetizes that trust.
3. **AI and agent architecture** — Junhong independently developed a "taskloop" pattern for continuous task execution. At its core, it is essentially *harness engineering* — an agent orchestration loop. He implemented agent orchestration with LangGraph and built an enterprise version of Claw.
4. **"Not knowing how to code" as an advantage** — He claims that because he does not understand implementation details, he can be 3–5× more productive than developers: he defines requirements and standards, while AI handles the implementation.
5. **Business model** — Community edition (AGPLv3 → Apache 2.0, free for commercial use) + enterprise edition (licensed, with proprietary features, license keys, and encrypted binaries). ThingsPanel sells to system integrators, who then sell to end customers.
6. **Pricing philosophy** — Two types of customers: "investment-oriented" customers who care about ROI and are willing to pay a premium, and "consumer-oriented" customers who focus only on cost. The company targets the former. Four infrastructure projects worth a combined RMB 150 million used ThingsPanel as one of their core software components; the integrator reportedly marked up the software to more than RMB 1 million.
7. **Overseas business** — Projects in Malaysia and Singapore around 2020. Junhong prefers doing business overseas ("If you can do business outside, don't do business inside"). He feels Malaysian customers are more meticulous than customers in mainland China.
8. **Personal life** — Divorced, with one child in middle school. Currently lives in Shenzhen after leaving Beijing because of its air quality. He also owns properties purchased years ago in other cities that have remained profitable.

---

# Interview

### Q: Why did you start working on IoT? How did you find those large customers?

**Junhong:** Let me answer the first question first — the original motivation.

Before the pandemic, I happened to be working on an IoT project in Malaysia. We were using overseas software called ThingsBoard. It was relatively expensive and not particularly good to use. It was difficult to learn.

When the pandemic hit, I had just returned to China. Then the Spring Festival came around and suddenly I couldn't meet customers anymore. So I thought: I should build a piece of software that can be sold and delivered without meeting customers in person, entirely online, without being constrained by geography. That's how ThingsPanel came about.

I looked at ThingsBoard and thought their product wasn't very good, so I decided to rebuild it. They had already used "Board," so I used "Panel." Basically the same meaning. I started in 2020, and now it's 2026 — I'm still doing this. The original intention hasn't changed.

But there's something behind those words that you should understand — we've failed many times. It's like raising the temperature of water by 20 degrees every year. We've taken a lot of detours, but if you don't take detours, how would you know which road is straight?

**As for customer acquisition:**

The core reason is that I do things they can't do. The second reason is good publicity. I have an open-source community edition. People discover what we're capable of through the product, and then they come to us. They encounter a problem they can't solve themselves, search for it online, and find us.

For example, a large state-owned telecom operator — I won't say which regional company — told me directly:

> "An organization like ours simply can't build something like this. Nobody is going to do the work. When we encounter this kind of problem, we have no choice but to work with an outside company."

They asked what our core value was. Essentially, we help them reduce risk and save time. The cost of hiring people to modify the software themselves isn't even lower than simply buying the enterprise edition. What they actually want is **compliance, risk transfer, time savings, and guarantees**.

I told them:

> "We think about this almost from the moment we open our eyes in the morning until the last moment before we go to sleep. Do you think about it before and after work? Your company's organizational structure determines that we can continuously focus on one thing and dig deeply into it, while you don't need to. Even Alibaba has this problem, let alone large state-owned enterprises."

---

# Q: What AI technologies does the platform use?

**Junhong:** When AI first appeared, I did some research and saw many possibilities, but we didn't invest much initially.

The first idea was to use AI for visualization — you could ask it a question and have it generate charts and flowcharts. The Mermaid flowchart capability really caught my attention.

But during the first year, I didn't connect AI with actual application scenarios, and I also felt that AI simply wasn't capable enough.

Then in November 2023, I ran some tests and proved that multi-agent conversations and step-by-step reasoning could significantly improve AI's intelligence. But at the time, I didn't turn it into a product innovation.

Later I realized that **the door was already half open**. You just need to believe that AI *can* do something, and then push the door open.

Around the Spring Festival, we were all using Antigravity for development. I had an idea: **Could we make AI continuously generate code without bugs?**

At 9 a.m., I finished a phone call with a colleague and immediately started thinking about it. Around 10:30, while walking to the office, I spent roughly 30–40 minutes working through the whole concept. The core flowchart and functional nodes were all mapped out.

I arrived at the office before 11 and implemented it.

It was that fast.

At 2 p.m., I tested it with my colleagues. We discovered that after adding a system prompt, the AI could keep operating continuously without stopping.

I named it **taskloop**.

Later I learned about **harness engineering**, the well-known approach to agent orchestration. It hadn't become popular yet. I had built something similar several months before it became widely known.

I realized that I was actually pretty good at this.

*[Editor's note: The core concept behind taskloop is a task-decomposition loop: break a large system into modules, then break the modules into subtasks — around 40 tasks per project. Each task file has its own independent context. The loop uses an LLM to determine whether the task is complete; if it isn't, the agent continues. The core logic is roughly six lines of code: determine that the task is incomplete → continue to the next step → check again.]*

The key insight was about the **effective context window**.

Early LLMs had no problem generating short scripts, but once the code became long, errors increased. So if you keep each task within the effective context window, the success rate becomes much higher.

You break the large system into second-level modules, third-level modules, and then multiple tasks. Each task file has its own independent context, so you don't lose context.

After that breakthrough, I didn't go home for the Spring Festival. I stayed in Shenzhen and started using AI to develop all kinds of things — **using AI to manage the company**.

When OpenClaw came out, we developed an enterprise version. What we're working on recently is increasing the concurrency of the enterprise edition so that it can manage **10,000 devices** — large-scale real-time processing, high intelligence, and low cost.

My video account is called **"AI as CEO"**.

That's the direction.

---

# Q: Your professional background is in Public Administration rather than computer science?

**Junhong:** I studied Public Administration at Northwest University. I entered in 1998.

I thought it would be difficult to find a job, so during my junior year I started teaching myself computer science. I studied for about a year and then worked as a programmer for more than a year.

After working as a programmer, I realized it wasn't suitable for me, so I quit and became a literary editor.

Later I did other things as well.

At IT companies, apart from front desk and finance, I've basically done everything. I can do design, and I'm also very familiar with Linux.

### Q: When did you start writing code again?

I discovered that I could actually write code because I optimized Antigravity and made it capable of working continuously without interruption.

That's when I realized I was actually pretty good at this.

I also realized that I'm naturally good at **architecture, methodology, standard processes, and top-level design**.

When you combine those abilities with AI programming tools — optimizing Claude Code, Cursor Composer, and so on — even relatively small optimizations can produce much better results.

I developed what may be a mistaken impression: **my efficiency was several times higher than that of my developer colleagues.**

The reason, as one colleague put it, is that **I don't know how to write code, so I don't even think about looking at the code.**

That dramatically increases my efficiency.

Put simply:

> **If AI can do something and verify it, you don't need to learn it or understand its implementation.**

So when I interview people now, I ask:

> "How long does it take to learn a new programming language?"

Someone who answers **"one week"** is giving the wrong answer.

The correct answer is:

> **"You don't need to learn it anymore."**

---

# Q: What does the workflow look like for long-running agent tasks?

**Junhong:** First, the task has to be large enough.

If it's a 100-line script, the AI will finish it immediately.

The real work needs to be something that can run for several hours.

But there's a critical problem: **if the agent needs an API key and you haven't provided it, it can't simply go to the website and register one by itself.**

If the input conditions aren't complete, the task will stop.

It might happen in the third minute or the tenth minute.

It's like going on a long trip and realizing halfway there that you forgot something, so you have to go back and get it.

Therefore, you have to provide enough information and resources at the beginning.

With our mechanism, if the task is large enough, it can continue working for **ten days or even a month**.

The method is simple:

* Break the large task into around 40 subtasks.
* Give each task its own task file and independent context.
* Use an LLM to determine whether the current task is complete.
* If it isn't complete, continue.
* Check again.

That's basically it.

### Tools

We used Antigravity initially, but it later became unstable.

Now we use **Codex**.

The core logic of multi-agent systems is basically the same across different tools.

LangGraph isn't mandatory, but it saves time and prevents you from stepping into the same traps. It uses graphs and state machines to express agent logic, which is very convenient.

I also wrote an **event gateway** myself.

There are many solutions available on the market, but I didn't know which one to choose. I told AI what I needed, and it said:

> "I'll write one for you."

So it built one using **Redis Streams**.

A lot of things are black boxes to me. **If I can verify that something works, I don't bother figuring out how it works internally.**

---

# Q: What about the business model — enterprise edition versus community edition?

**Junhong:** The community edition is open source and free for commercial use.

Recently, we switched from **AGPLv3 to Apache 2.0**.

The enterprise edition has many proprietary features — that's what we sell.

Why don't customers simply take the community edition and add the features themselves?

Because the cost of hiring people to modify it is often no lower than simply buying the enterprise edition.

What they actually want is:

**compliance, risk transfer, time savings, and guarantees.**

When they buy from our company, the risk is transferred to us. If something goes wrong, we fix it.

They can't become IoT experts in a short period of time.

We've spent several years building this.

They may have spent only a few days comparing the options.

---

## System Integrators

We sell to **system integrators**, and the integrators sell to the end customers.

The license keys are controlled by us.

The integrator handles first-line sales and implementation.

For example, four projects had a combined value of **RMB 150 million**. One of the core software components came from us for around **RMB 160,000**, while the integrator could reportedly sell it for more than **RMB 1 million**.

Why doesn't the end customer bypass the integrator?

1. They don't know us.
2. Their procurement system requires formal channels.
3. They need someone to handle implementation and integration.
4. They operate under budgets — for example, if the budget is RMB 20 million but the actual cost is RMB 10 million, there is room in the middle.

I provide the **flour**.

Someone else has to turn it into **bread**.

---

# Pricing Philosophy

There are two types of customers:

**"Investment-oriented" customers** and **"consumer-oriented" customers**.

Investment-oriented customers care about ROI.

They think:

> "Spend RMB 100,000 and make RMB 1 million."

Consumer-oriented customers only care about cost.

You should avoid consumer-oriented customers because they won't pay a premium.

Pricing needs to be backed by real capability and value.

A gateway can sell for RMB 100, or it can sell for RMB 8,000.

The difference is the value it creates.

For a factory with several thousand employees, the cost of one minute of downtime can be far greater than the price of the software.

I studied Hitachi's **Lumada** platform.

Its IoT business generates around RMB 100 billion in annual revenue.

They deliver city-scale IoT projects as general contractors.

If Hitachi can reach RMB 100 billion, then surely I should at least be able to reach RMB 2 million.

---

# Q: What about overseas business — your experience in Malaysia and Singapore?

**Junhong:** Around 2020, we were doing business in Malaysia and Singapore.

We completed projects worth more than RMB 100,000.

There were many other opportunities, including projects with Malaysian oil companies.

Malaysians are quite similar to people from mainland China in terms of being relationship-oriented societies.

But they are more meticulous in the way they work, and they are friendlier.

There's more light in their eyes.

They don't seem to be under as much pressure.

Singapore is newer, cleaner, and less crowded than Hong Kong.

Singaporeans appear to care more about rules and reputation.

But when interests are at stake, human nature is the same everywhere.

The average level of civilization may be different, but **human nature at the fundamental level is the same**.

My feeling is:

> **If you can do business outside, don't do business inside.**

Doing business domestically means doing the same things you've already done again.

Overseas business opened the door to a whole new world.

---

# Q: What about your personal life?

**Junhong:** I was born in 1979 and I'm 47 years old.

I entered Northwest University in 1998.

Over the past decade, I've lived in various places:

* One year in Northeast China
* Four years in Xi'an
* Sixteen years in Beijing
* Four years in Shenzhen, where I currently live
* Business trips to Malaysia and Singapore

I moved from Beijing to Shenzhen because of the air quality.

I was constantly coughing in Beijing.

And Shenzhen is also a place with good prospects for entrepreneurship.

I'm divorced.

I have one child in middle school who lives with their mother.

This freedom allows me to devote myself fully to entrepreneurship. I'm different from the typical middle-aged person in that respect.

I bought properties in other cities years ago, when prices were around RMB 3,000–3,500 per square meter.

They are still worth more than RMB 8,000 per square meter today.

The market has declined, but I'm still making money on them.

---

# The Real Moat

The real moat of the business is:

1. **The community edition is already open source**, so there isn't much to steal.
2. **Customers want compliance and legal protection, not source code.**
3. **Selling software requires a legal company entity** — an individual can't provide formal licensing and guarantees.
4. **Cognitive differentiation** — I'm one of the few people building this kind of product who comes from a liberal-arts background.

---

# Key Information Summary

| Dimension                  | Details                                                                                                              |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Product**                | ThingsPanel — open-source IoT platform built with Go; supports MQTT/HTTP and multiple languages                      |
| **Origin**                 | Began around 2020 after an IoT project in Malaysia, using ThingsBoard as the benchmark                               |
| **Scale**                  | 50,000+ downloads; 3,000+ community users                                                                            |
| **Revenue model**          | Community edition (free / Apache 2.0) + enterprise edition (licensed, RMB 20,000–2 million+)                         |
| **Channel**                | Sell to system integrators, who then sell to end customers such as SOEs, universities, and infrastructure projects   |
| **AI direction**           | taskloop (task-decomposition loop), event gateway, "AI as CEO" vision, ThingsPanel MCP                               |
| **Founder**                | Zhang Junhong, born 1979; studied Public Administration at Northwest University; self-taught CS; serial entrepreneur |
| **Location**               | Shenzhen; offices in Beijing and Yinchuan                                                                            |
| **International business** | Projects in Malaysia and Singapore; expanding into Southeast Asia, including Thailand and Vietnam                    |

---

# Memorable Quotes

> "We think about this almost from the moment we open our eyes in the morning until the last moment before we go to sleep. Do you think about it before and after work?"

> "We've taken a lot of detours. But if you don't take detours, how would you know which road is straight?"

> "My efficiency is higher than that of my developers — because I don't know how to code, so I don't even think about looking at the code."

> "The door is already half open. You just need to believe AI can do it, and then push the door open."

> "If you can do business outside, don't do business inside. Doing business domestically means doing the same things you've already done again."

> "If Hitachi can reach RMB 100 billion, then surely I should at least be able to reach a few million."
