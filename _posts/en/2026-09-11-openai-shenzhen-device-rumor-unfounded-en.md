---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenAI Shenzhen Device Rumor Unfounded
translated: false
type: note
---

Question: **Is OpenAI going to Shenzhen to build an AI device?**

Answer: **I don't see credible evidence that OpenAI is setting up an AI-device manufacturing/R&D operation in Shenzhen.**

What *is* happening is more interesting:

* **OpenAI is definitely building an AI device.** It acquired Jony Ive's hardware company and has said its first device is targeted for **2026**. Reports describe it as potentially screenless and designed around ambient AI interaction. ([Axios][1])
* **OpenAI is moving down the hardware stack.** It now has its own inference ASIC, **Jalapeño**, developed with Broadcom. OpenAI says it reached tape-out in only nine months and is intended for deployment in its own infrastructure. ([OpenAI][2])
* OpenAI's current stated strategy explicitly includes **“AI-native devices”** alongside models, chips, data centers, and products. ([OpenAI][3])
* **Shenzhen is a plausible manufacturing ecosystem**, but that's different from OpenAI establishing itself there. Shenzhen has the ODM/EMS/supply-chain density for cameras, microphones, batteries, PCBs, CNC, injection molding, wearables, etc. I found **no reliable current report saying OpenAI is opening a Shenzhen device operation**.

The more likely architecture is:

```text
OpenAI
  │
  ├── models / agents
  │
  ├── device industrial design
  │      └── Jony Ive / io
  │
  ├── custom silicon
  │      └── Broadcom + foundries
  │
  └── manufacturing / supply chain
         └── potentially Asian ODM/EMS ecosystem
              └── Shenzhen/Dongguan/etc. are natural candidates
```

So if you heard **“OpenAI is going to Shenzhen for AI hardware”**, I would currently treat that as **rumor/speculation**, not an established fact.

And strategically, **Shenzhen is exactly the kind of place I'd expect an OpenAI consumer-device supply chain to touch**, even if OpenAI itself doesn't put a large office there. That's where the difference between *designing an AI computer* and *actually shipping millions of physical AI computers* becomes enormous.

I can also trace **who OpenAI's likely hardware manufacturing partners are and whether there are Shenzhen/Dongguan ODM connections**.

[1]: https://www.axios.com/2026/01/19/openai-device-2026-lehane-jony-ive?utm_source=chatgpt.com "OpenAI aims to debut first device in 2026, exec tells Axios"
[2]: https://openai.com/index/openai-broadcom-jalapeno-inference-chip/?utm_source=chatgpt.com "OpenAI and Broadcom unveil LLM-optimized inference chip | OpenAI"
[3]: https://openai.com/index/the-full-stack-behind-abundant-intelligence/?utm_source=chatgpt.com "The full stack behind abundant intelligence | OpenAI"
