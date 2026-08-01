---
audio: false
generated: true
image: false
lang: en
layout: post
title: Value in Hardware and Execution
translated: false
type: note
---

**Question: As AI becomes abundant and open-source models commoditize intelligence, what kind of value will still matter? Is hardware + software a better position?**

**Answer:**

Yes, your intuition is pointing toward one of the biggest shifts in the AI economy.

The pattern is similar to previous technology waves:

* Internet → information became cheap → distribution, trust, community became valuable.
* Cloud → servers became cheap → products, data, workflows became valuable.
* Open-source software → code became cheap → deployment, integration, support became valuable.
* AI → intelligence generation becomes cheap → **execution, ownership, physical systems, proprietary data, and trust become valuable.**

A simple way to think:

```
Raw intelligence
        ↓
       cheap
        ↓
What remains scarce?
        ↓
+ Data
+ Distribution
+ Hardware
+ Real-world integration
+ Brand/trust
+ Workflow ownership
+ Unique feedback loops
```

---

### 1. Open-source AI will reduce "model advantage"

Today:

```
OpenAI / Anthropic / Google
        |
        |  frontier models
        |
        ↓
developers build apps
```

But over time:

```
Qwen
Llama
DeepSeek
Mistral
etc.

        ↓

everyone has similar intelligence
```

The model itself becomes like Linux:

Nobody pays you because you know Linux exists.

People pay because you can build:

* Kubernetes platforms
* cloud services
* enterprise solutions
* devices
* products

The model becomes infrastructure.

---

### 2. Closed-source creates temporary gaps, but not permanent moats

Your thought:

> 闭源造成一个 GAP 信息差，会是一个比较舒服的

Correct in the short term.

Examples:

* knowing GPT-5 capabilities earlier
* knowing unpublished APIs
* having private datasets
* having internal engineering experience

This creates an advantage.

But information gaps disappear.

A stronger moat is:

```
You know something
        +
You built something
        +
Users depend on it
        +
Data feedback improves it
```

That is much harder to copy.

---

### 3. Taalas is interesting because it attacks inference economics

Taalas is an example of a hardware/software co-design approach.

Traditional:

```
LLM weights
    |
    v
GPU
    |
    v
CUDA kernels
    |
    v
Inference
```

GPU is general purpose.

Taalas idea:

```
LLM weights
    |
    v
custom silicon
    |
    v
faster cheaper inference
```

Basically:

"Can we turn the model into hardware?"

Similar ideas existed before:

* Google TPU
* Cerebras wafer-scale engines
* Graphcore IPU
* Tesla Dojo

The key insight:

The future AI stack may not only be:

```
software eats hardware
```

but:

```
AI models reshape hardware
```

---

### 4. Hardware has a psychological advantage: people pay for objects

You mentioned:

> 买一个东西这种人们愿意给钱

Yes.

Humans are comfortable paying for:

* iPhone
* Tesla
* GPU
* robot
* smart glasses
* home AI server

Because the value is visible.

Compare:

```
$999 AI device
```

versus

```
$20/month AI subscription
```

Many consumers understand the first more easily.

Physical products create:

* ownership
* identity
* status
* trust

---

### 5. The strongest future position: AI + physical world

The future may look like:

```
                 AI model
                    |
          ----------------------
          |                    |
      Software             Hardware
          |                    |
    digital workers       robots/devices
          |                    |
          -------- humans -----
```

Examples:

* AI coding agent + private server
* AI security appliance
* AI education robot
* AI factory controller
* AI medical assistant
* AI home assistant

---

### 6. For an individual engineer, where is the opportunity?

The dangerous position:

```
"I know how to call GPT API"
```

Many people can do this.

Better:

```
"I understand transformers"
"I trained models"
"I optimize inference"
"I build vLLM-like systems"
"I deploy AI on hardware"
```

Even better:

```
I own a small AI system used by real people.
```

The progression:

```
User of AI
   ↓
Developer with AI
   ↓
AI infrastructure engineer
   ↓
AI product builder
   ↓
AI company
```

---

Your recent direction (nanoGPT → nano-vLLM → CUDA → GPU → inference optimization) is actually aligned with this deeper layer.

Many developers will stay at:

```
prompt → API → app
```

The people who understand:

```
attention
KV cache
CUDA kernel
GPU memory
quantization
distributed inference
ASIC architecture
```

are closer to the "picks and shovels" layer.

The key is not only knowing technology. The final step is:

```
deep technology
        +
real user pain
        +
distribution
        =
economic value
```

The future probably has millions of small AI companies: one person or a small team operating AI systems that previously required hundreds of employees. The winners are not necessarily those with the biggest models; they are those who combine models with unique workflows, hardware, data, and users.
