---
audio: false
generated: true
image: false
lang: en
layout: post
title: Build a High-Income Job and Side Business
translated: false
type: note
---

**Question:** In the current 2026 startup/economic environment, should I build a startup or work for a company—and what is the best way for me to make money in the next stage?

**Answer:**

My view: **don't choose “startup vs job.” Choose a high-income AI engineering position + build a startup-shaped business on the side, and only go full-time startup when revenue proves it.**

For *your particular position*, I would **not** immediately quit and spend 2 years building a speculative startup.

### 1. The macro environment is actually very favorable for you

AI is not in a “wait and see” phase anymore.

Stanford's 2026 AI Index says:

* Organizational AI adoption reached **88%**
* GenAI is used in at least one business function by **79%**
* Global corporate AI investment more than doubled in 2025
* AI company revenue is growing extremely quickly
* But AI infrastructure/compute costs are also exploding. ([Stanford HAI][1])

At the same time, there is a weird bifurcation:

**AI usage is exploding, but generic software engineering is becoming less valuable.**

Stanford reports that employment for software developers aged 22–25 fell nearly 20% from 2024, and one-third of organizations expect AI-related workforce reductions. ([Stanford HAI][1])

So I would not optimize your next stage for:

> “Become a better full-stack engineer.”

I'd optimize for:

> **Become one of the people who can make AI systems actually run.**

That means:

```text
LLM
 ↓
Inference
 ↓
CUDA / Triton
 ↓
GPU systems
 ↓
Training / post-training
 ↓
Distributed systems
 ↓
AI product
 ↓
Revenue
```

That stack is much harder to commoditize.

---

# 2. I would choose the "barbell" strategy

Something like:

```text
                 YOU
                  │
       ┌──────────┴──────────┐
       │                     │
   HIGH-INCOME JOB       YOUR BUSINESS
       │                     │
   $ / month             customers
       │                     │
   AI infra             consulting
   training             agents
   inference             AI systems
   CUDA                  products
       │                     │
       └──────────┬──────────┘
                  │
             capital + skill
                  │
             startup option
```

The job gives you:

**cash + difficult problems + network + credibility + technical growth**

The business gives you:

**customers + distribution + ownership + asymmetric upside**

Eventually, if the business starts doing:

```text
$5k/mo
$10k/mo
$20k/mo
$30k/mo
```

then the decision becomes easy.

You quit when **the business is pulling you out of employment**, rather than quitting and hoping the business works.

---

# 3. Don't start a "startup" yet. Start a cash machine

This distinction is important.

A startup asks:

> “Can I build something worth $100M?”

A small AI business asks:

> **“Can I get one company to pay me $5,000?”**

The second question is dramatically easier.

And in 2026, enterprises clearly have money allocated to AI. Gartner-related research reported that 85% of functional leaders planned to increase AI spending in 2026, while many companies still struggle to measure ROI. ([The Wall Street Journal][2])

That's exactly the opportunity.

Companies don't need another:

```text
AI chatbot
AI wrapper
AI note-taking app
AI agent demo
```

They need:

```text
"We have this expensive business process.
Can you automate it?"
```

That's where I'd hunt.

---

# 4. Your best business opportunity is probably AI engineering services → product

You already have an unusual combination:

```text
backend engineering
        +
Python
        +
LLM
        +
training
        +
GPU
        +
inference
        +
agents
```

Most people have only one or two.

You can sell the combination.

For example:

### AI inference optimization

A company has:

```text
100 GPUs
$300k/month inference bill
```

You improve:

```text
vLLM
KV cache
quantization
Tensor Parallel
CUDA
Triton
batching
speculative decoding
MoE routing
GPU utilization
```

and save them $80k/month.

Charging:

```text
$20k project
```

is completely reasonable.

---

### Private/on-prem LLM deployment

For companies that cannot send data to OpenAI/Anthropic:

```text
customer
   ↓
their servers
   ↓
open-weight model
   ↓
vLLM
   ↓
RAG / agents
   ↓
internal applications
```

You sell:

```text
deployment
+
optimization
+
fine-tuning
+
maintenance
```

This is much more defensible than building another consumer AI app.

Open-weight models are becoming increasingly viable because of lower cost and customization, while enterprises are increasingly evaluating AI based on economics rather than just benchmark scores. ([Business Insider][3])

---

# 5. Your GPU obsession is actually potentially useful

Your recent work with:

* RTX cards
* GPU repair
* VRAM
* CUDA
* inference
* Triton
* FreeToken
* MoE
* MXFP4
* KV cache
* multi-GPU
* training

looks somewhat scattered.

But I see a potential underlying direction:

> **AI compute engineering**

That's a real industry.

AI infrastructure spending is enormous. Nvidia, for example, is still forecasting extremely strong growth, while HPE and CoreWeave are seeing massive AI infrastructure demand. ([Reuters][4])

You don't need to become Nvidia.

You can sit one layer above/below:

```text
NVIDIA
   ↓
GPU / hardware
   ↓
cloud / servers
   ↓
AI infrastructure
   ↓
YOU
   ↓
customers
```

Potential businesses:

```text
GPU optimization consultancy
AI inference optimization
private LLM deployment
GPU cluster setup
model quantization
training optimization
AI agent infrastructure
AI migration consulting
```

---

# 6. But I would still get a better AI job

If you can get a job paying substantially more than your current role, I would take it **provided the technical density is high**.

Don't optimize only for salary.

I'd rank opportunities approximately:

| Opportunity                           | Value to you |
| ------------------------------------- | -----------: |
| Frontier AI / AI infra engineer       |        ⭐⭐⭐⭐⭐ |
| LLM inference/training engineer       |        ⭐⭐⭐⭐⭐ |
| GPU/CUDA systems engineer             |        ⭐⭐⭐⭐⭐ |
| AI startup with strong technical team |        ⭐⭐⭐⭐⭐ |
| Enterprise AI engineer                |         ⭐⭐⭐⭐ |
| Generic backend engineer              |           ⭐⭐ |
| Generic full-stack                    |            ⭐ |
| Traditional CRUD outsourcing          |            ⭐ |

Your goal isn't merely:

> “make 40k RMB/month.”

It is:

> **Become capable of generating $10k–$100k/month from AI expertise.**

Employment is one way to monetize that capability.

Ownership is another.

---

# 7. I would use the next 2 years deliberately

My proposed trajectory:

### Phase 1 — next 6 months

**Job + aggressive AI specialization**

Learn deeply:

```text
PyTorch
CUDA
Triton
vLLM
DeepSpeed
Megatron
FSDP
MoE
quantization
KV cache
speculative decoding
distributed training
inference optimization
```

But don't learn them academically.

Build things.

For example:

```bash
git clone your-own-llm-runtime

# implement
attention
kv-cache
paged-attention
moe
tp
quantization
speculative-decoding
```

Your GitHub becomes your portfolio.

---

### Phase 2 — simultaneously

Start selling engineering.

Not:

> “I run an AI company.”

Instead:

> “I can reduce your LLM inference cost / deploy your private model / optimize your GPU workload.”

Find 20 companies.

Talk to them.

Your first objective:

```text
$1,000
```

Then:

```text
$5,000
```

Then:

```text
$10,000/mo
```

---

### Phase 3 — 6–18 months

Look for repetition.

Suppose you discover:

```text
Customer A:
GPU inference optimization

Customer B:
GPU inference optimization

Customer C:
GPU inference optimization

Customer D:
GPU inference optimization
```

Now you have something.

Turn:

```text
consulting
```

into:

```text
service
```

then:

```text
productized service
```

then:

```text
software
```

That's much safer than inventing a SaaS product from zero.

---

# 8. Your biggest mistake would be building too early

You have enough technical ability to disappear into engineering for 12 months.

That's dangerous.

You could spend:

```text
3 months → CUDA
2 months → inference
3 months → model training
2 months → agent
2 months → product
```

and have:

```text
$0 revenue
```

The market doesn't reward technical complexity.

It rewards:

```text
pain × willingness to pay × distribution
```

So I'd force yourself into this loop:

```text
Talk to customer
      ↓
find painful problem
      ↓
sell solution
      ↓
build minimum solution
      ↓
deliver
      ↓
get paid
      ↓
repeat
      ↓
automate
      ↓
productize
```

---

# 9. What about VC-backed startup?

**Not yet, unless you discover an unusually strong opportunity.**

The startup funding environment is still very strong for AI. Cognition, for example, just raised $2B at a $48B valuation. ([Reuters][5])

But that doesn't mean **you** should raise VC.

VC is appropriate when:

```text
market is enormous
+
product has strong pull
+
growth is extremely fast
+
capital accelerates the business
```

It is not appropriate merely because:

```text
"I want to be a founder."
```

If you can make:

```text
$20k/month
```

with 2–3 people and high margins, that's already an excellent business.

You don't need a $100M valuation.

---

# 10. The real game: increase your "earning surface area"

I think this is the most important concept for you.

Don't think:

> job OR startup.

Think:

```text
                 earning surface
                       │
       ┌───────────────┼────────────────┐
       │               │                │
     salary        consulting        equity
       │               │                │
   $40k/mo         $10k/mo          startup
       │               │                │
       └───────────────┼────────────────┘
                       │
                  AI expertise
```

Over time:

```text
2026
salary        ██████████
consulting    ██
equity        ▏

2027
salary        ████████
consulting    █████
equity        ██

2028
salary        ████
consulting    ███████
equity        ███████████
```

You gradually move from **selling your time** to **selling systems** to **owning assets**.

---

# My recommendation for you

If I were making the decision with your current profile, I'd do:

```text
2026–2027

        HIGH-END AI JOB
             +
       AI consulting
             +
      public technical work
             +
        small products
```

Target:

```text
Job:             $60k–100k+/year
Consulting:      $30k–100k+/year
Products:        optional
Equity:          upside
```

Then reassess.

If consulting/product revenue reaches:

```text
$10k/mo → serious
$20k/mo → very serious
$30k+/mo → consider leaving job
```

At that point, **you don't need to ask whether you should start a company. You already have one.**

The current AI economy is giving you a particularly good wedge because capital is flowing heavily into AI infrastructure and enterprise deployment, while organizations are struggling to convert AI spending into measurable ROI. ([Stanford HAI][1])

So my one-line answer is:

> **Don't gamble your cash flow on a startup. Become an unusually strong AI systems engineer, get paid well for it, sell the same expertise directly to companies, and let customer revenue tell you when to become a full-time founder.**

And I'd specifically position you around **LLM inference/training + GPU systems + AI agents**, rather than generic “AI application development.”

### References

* [Stanford AI Index 2026 — Economy](https://hai.stanford.edu/ai-index/2026-ai-index-report/economy?utm_source=chatgpt.com)
* [Stanford AI Index 2026](https://hai.stanford.edu/ai-index/2026-ai-index-report?utm_source=chatgpt.com)
* [Reuters — Cognition raises $2B at $48B valuation](https://www.reuters.com/technology/cognition-ai-raises-2-billion-48-billion-valuation-2026-09-08/?utm_source=chatgpt.com)
* [Reuters — Nvidia forecasts continued AI growth](https://www.reuters.com/business/media-telecom/nvidia-forecasts-quarterly-revenue-above-estimates-2026-08-26/?utm_source=chatgpt.com)

[1]: https://hai.stanford.edu/ai-index/2026-ai-index-report/economy?utm_source=chatgpt.com "Economy | The 2026 AI Index Report | Stanford HAI"
[2]: https://www.wsj.com/tech/ai/ai-spending-is-up-so-is-the-guesswork-93cf1f36?utm_source=chatgpt.com "AI Spending Is Up. So Is the Guesswork."
[3]: https://www.businessinsider.com/nea-partner-aaron-jacobson-weighs-in-on-open-versus-closed-2026-9?utm_source=chatgpt.com "An NEA partner says not every AI task needs frontier intelligence"
[4]: https://www.reuters.com/business/media-telecom/nvidia-forecasts-quarterly-revenue-above-estimates-2026-08-26/?utm_source=chatgpt.com "Nvidia forecasts 70% sales growth next year, signals AI spending boom has years left to run"
[5]: https://www.reuters.com/technology/cognition-ai-raises-2-billion-48-billion-valuation-2026-09-08/?utm_source=chatgpt.com "Cognition AI raises $2 billion at $48 billion valuation"
