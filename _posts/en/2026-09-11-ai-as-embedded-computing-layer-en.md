---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI as Embedded Computing Layer
translated: false
type: note
---

**Question: What will AI devices look like in the future?**

**Answer:**

I think the important shift is:

> **AI stops being an app you open, and becomes a computing layer embedded into physical objects.**

The likely evolution looks something like this:

| Era     | AI device              | Core idea                                |
| ------- | ---------------------- | ---------------------------------------- |
| 2020–25 | Phone + cloud LLM      | You talk to an app                       |
| 2025–30 | AI PC / AI phone       | Local inference + cloud                  |
| 2026–32 | AI glasses             | AI sees/hears continuously               |
| 2028–35 | AI earbuds / wearables | Always-on personal agent                 |
| 2030s   | Robots                 | AI acts in physical space                |
| Later   | Ambient computing      | Environment itself becomes the interface |

### 1. AI glasses are probably the biggest near-term form factor

![Image](https://images.openai.com/static-rsc-4/6NNa5X2ILtmX5CTnPcm6B4ySZrjjEiMi5t4bz0v5-IKeWcaKiS7sN62MbGb4GiYieSzwNi1wbEzjz-qcnKXs-pzvxtbHSwC2bPZTBjcmFVdYGo6gZfwuSBDCvvqrYtq0kP0qrIvOt_-AlhM9AJqZeXjXXszMz4UsF9b0BWaN6xNZUO1abMlI1VjQ9AY0wJvG?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Kbrr10DxpJ87ne8aEJaa-3IpaExvTwhq1dGaelH5hFNjE0-0eaTBVOknv4gDTHKeaCQnqcGoSXBqHn1UUPRW0wCXMAB84thLhOf41RVnhL2FTsX_adMzniWo1uBgzyIvf9UODGViRUss0fQx3rU9ZoCyXieW9_xmWD4tIk2MtbgMKqWhcnUL2QCIlb2QR8l0?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/CKessij0HhVxLeSQCgwpU-wIGhTF1VKJsytJGCxfI_zNGCBkdgsI37V3mAZF9jQXcV1klQmExos1SGAr0qyO6yYHQ13eyaixdGbMhMtL7_xSjDSM11iIAf-SfZ1SEpaCf4zAcAsAFO5RgWxSo6emV7EXZnFivfgvb2Y2HZeJdnMXZR7F5DXfMvb6go99RYNa?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/_Ih44136qCVxpKqlEiB4Xf2OTxDEo2ihBiHocxcjQt_IQ7ljm5wEm5ZOnnT7P4o1zYl6SPBmaM4nz2Om2R3KVMfLoRrJG04k5sWLEz3onKGU3VpNJuhpCTDvJrlHf1QySLS5UaiCPmN0qLB4mVQCSnbBAzxoGS2Rd-i-RkHLizIq5tBcWAsYlqBGA7t0U_sR?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/xe6eOFj6wMl07nWTIbJoSUMa4Ex0-mrsydC8bZ7Ts3CB6Fxni6qKLXmFfMPGF-Cyzov2YTuiOfuXn4RbKpNQ-RzCctBP4GuK6U1wfBizlumPp8NIe1LmR82S6YHQw5xQcXs_69SRGleAiFc1FonQFpHYYXRoJ8RyGUs19oKTh7R4uvRXJCEHeNmu1aX74n94?purpose=fullsize)

Imagine walking around with:

```text
camera ─────┐
microphone ─┤
             ↓
        local AI
             ↓
       cloud model
             ↓
      ┌──────┴──────┐
      ↓             ↓
   audio          display
```

You don't ask:

> "What's this building?"

The glasses already see it.

You don't type:

> "Translate this menu."

They see the menu and whisper the translation.

The interaction becomes **context → inference → action**, rather than **keyboard → prompt → answer**.

---

### 2. AI earbuds may become more important than glasses

Earbuds have an enormous advantage:

**They already sit in your ears all day.**

They can provide:

* speech translation
* meeting memory
* personal reminders
* navigation
* contextual Q&A
* real-time conversation assistance
* environmental awareness

For many tasks, you don't need a screen.

```text
World
  ↓
microphones
  ↓
speech / audio encoder
  ↓
LLM
  ↓
TTS
  ↓
your ear
```

This is essentially an **always-available voice agent**.

---

### 3. The phone probably becomes the "compute hub"

Rather than replacing the phone immediately, glasses/earbuds can be thin clients:

```text
             ┌── glasses
             │
sensors ─────┼── earbuds
             │
             └── watch
                  │
                  ↓
             smartphone
                  │
             ├── NPU/GPU
             ├── storage
             └── network
                  │
                  ↓
              cloud AI
```

The phone becomes less about *touching the screen* and more about providing:

**compute + battery + connectivity + storage.**

---

### 4. AI robots are the really interesting endpoint

LLMs currently have:

```text
eyes      → vision model
ears      → speech model
brain     → LLM
hands     → ????
```

Robotics is about closing that final loop:

```text
observe
   ↓
understand
   ↓
reason
   ↓
plan
   ↓
act
   ↓
observe again
```

That's fundamentally different from ChatGPT.

A robot can receive:

> "Clean the desk."

and turn that into hundreds of low-level actions.

This is where **AI + hardware + reinforcement learning + vision + simulation** converge.

---

### 5. The killer device may be something we don't currently call a "device"

Eventually:

```text
              ┌───────────────┐
              │ Personal AI   │
              │     agent     │
              └───────┬───────┘
                      │
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
      glasses       phone         robot
        ↓             ↓             ↓
      camera       sensors       actuators
        └─────────────┼─────────────┘
                      ↓
                 personal model
```

The **agent** becomes the product.

The physical devices become its:

* eyes
* ears
* mouth
* hands
* wheels
* network interfaces.

That's why I think "AI device" is ultimately less about inventing a new gadget and more about giving an AI **persistent perception + memory + agency + actuators**.

### My bet

If I had to rank the important hardware directions:

**2026–28:** AI glasses / earbuds
**2027–30:** local AI PCs and phones
**2028–35:** humanoid / specialized robots
**2030+:** ambient AI + robotics ecosystem

And for someone who likes both **LLMs and hardware repair**, the interesting intersection is probably **edge AI compute**: NPU/GPU modules, cameras, sensors, power electronics, embedded Linux, and small multimodal models. That's much closer to the physical future of AI than simply running another chatbot.

I can also map out what a **$1,000 personal AI device stack in ~2030** might realistically contain—compute, cameras, memory, battery, model size, and bandwidth.
