---
audio: false
generated: true
image: false
lang: en
layout: post
title: US Work via Engineering Experience
translated: false
type: note
---

Question: **How can I use my current resume/background to get to the U.S. and legally work there?**

Answer:

I read your current resume. [Your resume](https://lzwjava.com/resume-en?utm_source=chatgpt.com)

My honest assessment: **you have a much stronger engineering profile than your formal education profile.** Your main immigration problem is not "can you do the job?" — it's **which visa category can legally convert your experience into U.S. work authorization.**

Your strongest assets are:

* ~11 years professional engineering experience.
* Backend/full-stack + increasingly serious AI/LLM work.
* HSBC/DBS experience.
* You founded a company and generated meaningful revenue.
* 30K-user product + ~3M RMB consulting revenue.
* 10 open-source projects with substantial commit history.
* Technical blog with ~75K monthly page views.
* IELTS 6.5.
* Hands-on LLM training/inference rather than just "prompt engineering."
* Experience with H200/MI300X/RTX 4070, nanoGPT/GPT-2, PyTorch, ROCm, etc.
* You're already operating at something closer to **AI engineer / ML systems engineer** than ordinary full-stack engineer. ([Zhiwei Li][1])

The big weakness is:

> **No conventional bachelor's degree.**

That makes the normal U.S. software-engineer immigration path considerably harder, but **not impossible**.

## My ranking for you

| Route                               | Fit for you | My view                                                    |
| ----------------------------------- | ----------: | ---------------------------------------------------------- |
| **O-1A**                            |        ⭐⭐⭐⭐ | Potentially very interesting                               |
| **H-1B via experience equivalency** |         ⭐⭐⭐ | Possible, but difficult                                    |
| **L-1B/L-1A**                       |        ⭐⭐⭐⭐ | Excellent if you structure the right employer relationship |
| **F-1 → OPT → H-1B**                |         ⭐⭐⭐ | Expensive but straightforward                              |
| **EB-2 NIW**                        |         ⭐⭐⭐ | Long-term immigration strategy                             |
| **EB-1A**                           |          ⭐⭐ | Possible eventually, not yet my first choice               |
| B1/B2 → find job                    |           ❌ | Not a work route                                           |

---

# 1. I would seriously investigate O-1A

This is probably the most interesting route given what you've built.

O-1A is for people with extraordinary ability in science, education, business, or athletics. USCIS specifically has guidance discussing O-1A evidence for STEM professionals. ([USCIS][2])

The important thing is that **O-1A is not simply "have a PhD."**

Evidence can include things such as:

* major original contributions
* judging other people's work
* authorship
* critical/essential roles
* high compensation
* significant recognition
* media coverage
* awards
* distinguished organizations
* etc.

USCIS evaluates the evidence as a whole rather than simply looking at your resume title. ([USCIS][3])

And this is where your profile becomes interesting.

### Your existing evidence

You already have things like:

```text
Founder
  ↓
30,000-user product
  ↓
~RMB 3M consulting revenue
  ↓
11 years engineering
  ↓
HSBC / DBS
  ↓
10 open-source projects
  ↓
~75K monthly blog views
  ↓
AI / LLM experimentation
  ↓
model training on H200 / MI300X / RTX
  ↓
public technical writing
```

That's much more interesting for O-1 than:

> "I'm a Java developer with 11 years experience."

But there is a critical distinction:

**Having impressive things on your resume ≠ having O-1 evidence.**

For example:

> "I trained GPT-2 760M."

is weak by itself.

But:

> "My open-source implementation was used by X people, cited by Y projects, covered by Z publication, and I was invited to judge/teach/review work in this field."

is much stronger.

So I would start **building an O-1 evidence portfolio now**, even if you don't apply immediately.

---

# 2. H-1B is still worth pursuing

H-1B is the traditional route for a foreign software/AI engineer.

The State Department describes H-1B as the category for specialty occupations and says the applicant generally needs at least a bachelor's degree or equivalent experience in the specialty. ([U.S. Department of State Travel][4])

Your lack of bachelor's degree therefore matters.

But there is an important point:

USCIS guidance recognizes certain combinations of education/training/experience for degree equivalency. Its H-1B guidance describes the traditional **3 years of specialized professional experience per year of college-level education** framework, while emphasizing that the experience must actually represent specialized professional knowledge. ([USCIS][5])

So your:

```text
11 years professional engineering
```

is not automatically useless.

However, this is **not**:

```text
11 years experience = bachelor's degree
```

automatically.

The employer's immigration lawyer needs to establish that your experience and training satisfy the requirements for the particular specialty occupation.

### Therefore

When applying for U.S. jobs, don't only search:

```text
Software Engineer
```

Search:

```text
AI Engineer
ML Engineer
Machine Learning Engineer
LLM Engineer
Inference Engineer
AI Infrastructure Engineer
ML Systems Engineer
Research Engineer
Software Engineer, AI
Distributed Training Engineer
```

Your resume should be heavily biased toward the AI side.

---

# 3. L-1 could actually be a very good strategy

This one is underappreciated.

L-1 is an intracompany transfer visa.

The basic architecture is:

```text
Foreign company
      │
      │ you work there
      ▼
  ≥ 1 year qualifying employment
      │
      │ transfer
      ▼
US parent / subsidiary / affiliate
      │
      ▼
     L-1
```

USCIS says L-1 can transfer someone with specialized knowledge, or a manager/executive, from a qualifying foreign organization to a related U.S. organization. The general foreign-employment requirement is one continuous year in the relevant period. ([USCIS][6])

This could become interesting if you build your AI company into a genuine international company:

```text
Your China company
       │
       ├── AI consulting
       ├── model training
       ├── agent development
       └── open-source products
                │
                ▼
        US subsidiary
                │
                ▼
             L-1
```

But it needs to be a **real qualifying corporate relationship and real employment**, not a paper company created solely for immigration.

For you, this route becomes especially attractive if you actually want to build a U.S. business.

---

# 4. F-1 → U.S. school → OPT is the expensive fallback

You've already been researching U.S. master's programs.

This route is conceptually:

```text
China
  ↓
F-1
  ↓
U.S. master's
  ↓
OPT
  ↓
AI/ML job
  ↓
H-1B
  ↓
potential green card
```

The huge advantage is that you physically enter the U.S. as a student and then get a legal mechanism to work after completing the program.

USCIS explicitly describes the F-1 → OPT → H-1B transition and the cap-gap mechanism. ([USCIS][7])

The downside for you is obvious:

**money + time + your existing experience.**

You don't really need a master's degree to learn:

```text
Transformer
RoPE
GEMM
FlashAttention
MoE
distributed training
inference
PyTorch
CUDA/ROCm
```

You're already doing these things.

So I would **not automatically spend $60k–$100k+ simply because it's the easiest immigration route.**

I'd first test O-1/H-1B/L-1.

---

# 5. Your biggest opportunity: turn "AI enthusiast" into "recognized AI engineer"

This is the part I'd work on aggressively.

Your resume currently contains a lot of:

> "I experimented with..."

That's good for learning.

It's weaker for immigration and high-end U.S. hiring.

You want to transform it into:

```text
I built X
→ people used X
→ measurable impact Y
→ recognized by Z
```

For example:

### Current

```text
Experimented with nanoGPT.
```

### Much stronger

```text
Trained a 760M-parameter GPT-2 model from scratch on
15B+ tokens using consumer and datacenter GPUs.
Published the training code and technical analysis.
```

Then ideally:

```text
GitHub stars
forks
contributors
downstream projects
citations
technical articles
conference talks
podcasts
media
```

Those are much more valuable.

---

# 6. I'd build a public AI research/engineering track

You already have the raw ingredients.

I'd make the next 12 months look like:

```text
             Zhiwei
                │
        AI / ML Systems
                │
       ┌────────┼────────┐
       │        │        │
    Training  Inference  Agents
       │        │        │
     PyTorch   vLLM     agents
     ROCm      CUDA     CLI
     MoE       KV       tools
     FlashAttn quant    coding
       │        │        │
       └────────┼────────┘
                │
        open-source work
                │
        technical writing
                │
       external recognition
                │
          O-1 / H-1B
```

This is much more powerful than trying to become:

> "another generic full-stack developer applying to 500 U.S. companies."

---

# 7. Don't use B1/B2 as a work strategy

This is important because you've recently been looking at the U.S. visitor visa.

A visitor visa is **not a backdoor employment visa**.

The State Department explicitly separates visitor travel from employment categories and says foreign nationals wishing to work in the U.S. need the appropriate employment visa/status. ([U.S. Department of State Travel][8])

So:

```text
B1/B2
  ↓
visit Silicon Valley
  ↓
interview/network
  ↓
return / obtain proper status
  ↓
work
```

is fundamentally different from:

```text
B1/B2
  ↓
enter USA
  ↓
start working
```

Don't do the second one.

---

# 8. What I would do if I were you

I'd run **three tracks simultaneously**.

### Track A — U.S. AI jobs

Start applying from outside the U.S.

Target:

```text
AI Engineer
ML Engineer
Research Engineer
LLM Engineer
Inference Engineer
ML Infrastructure Engineer
AI Agent Engineer
```

Focus on companies that are comfortable sponsoring immigration.

Don't make "degree required" an automatic stop if the job otherwise matches you.

---

### Track B — O-1 preparation

Start collecting evidence:

```text
GitHub
├── stars
├── forks
├── contributors
├── external users
└── downstream projects

Blog
├── traffic
├── citations
├── external references
└── notable readers

AI work
├── models trained
├── benchmarks
├── open-source implementations
└── technical contributions

Recognition
├── talks
├── podcasts
├── interviews
├── awards
├── judging
└── publications
```

Then have a U.S. immigration attorney specializing in **O-1A for engineers/AI researchers** evaluate it.

---

### Track C — build an international company

Your existing entrepreneurial history makes this particularly interesting.

Build:

```text
China / international AI company
             │
             ├── consulting
             ├── agents
             ├── model training
             ├── open source
             └── SaaS
                    │
                    ▼
              U.S. subsidiary
                    │
                    ▼
                 L-1
```

That gives you another immigration architecture independent of winning a random U.S. job.

---

# My actual recommendation for you

If your goal is:

> **"I want to physically live and work in America within the next 1–3 years."**

I'd rank your strategy:

```text
                 ┌──────────────┐
                 │  Build AI CV │
                 └──────┬───────┘
                        │
            ┌───────────┼───────────┐
            ▼           ▼           ▼
         O-1A         H-1B        L-1
            │           │           │
            └───────────┼───────────┘
                        │
                   U.S. work
                        │
                        ▼
                  EB-2 NIW / EB-1
```

And keep:

```text
F-1 → master's → OPT → H-1B
```

as your **fallback**, not necessarily Plan A.

### One particularly important thing

Your **lack of a bachelor's degree is the biggest structural weakness in your current profile**.

If you finish your current associate degree, that's useful, but it doesn't magically solve every H-1B requirement.

If you can eventually obtain a **bachelor's-equivalent credential**, your U.S. employment options become dramatically cleaner.

But I would **not wait years before trying the U.S. market**.

You already have enough engineering experience to start testing the market now.

Your profile is unusual:

> **strong engineering + entrepreneurship + public technical work + emerging AI expertise + weak formal education.**

That means the optimal strategy is **not** to hide the unusual part.

It's to make the AI/technical achievements strong enough that your lack of conventional education becomes a secondary issue.

References:

* [U.S. Department of State — Employment Visas](https://travel.state.gov/content/travel/en/us-visas/employment.html?utm_source=chatgpt.com)
* [U.S. Department of State — Temporary Worker Visas](https://travel.state.gov/content/travel/en/us-visas/employment/temporary-worker-visas.html?utm_source=chatgpt.com)
* [USCIS — O-1A STEM guidance](https://www.uscis.gov/sites/default/files/document/policy-manual-updates/20220722-ExtraordinaryAbility.pdf?utm_source=chatgpt.com)
* [USCIS — L-1 classification](https://www.uscis.gov/i-9-central/form-i-9-resources/handbook-for-employers-m-274/70-evidence-of-employment-authorization-for-certain-categories/79-other-temporary-workers/792-l-nonimmigrant-status?utm_source=chatgpt.com)
* [USCIS — Practical Training / OPT](https://www.uscis.gov/policy-manual/volume-2-part-f-chapter-5?utm_source=chatgpt.com)

[1]: https://lzwjava.com/resume-en "Resume"
[2]: https://www.uscis.gov/sites/default/files/document/policy-manual-updates/20220722-ExtraordinaryAbility.pdf?utm_source=chatgpt.com "U.S. Department of Homeland Security"
[3]: https://www.uscis.gov/sites/default/files/err/D8%20-%20Aliens%20of%20Extraordinary%20Ability%20or%20Achievement%20%28O-1%2C%20O-2%2C%20and%20O-3%29/Decisions_Issued_in_2011/Apr152011_02D8101.pdf?utm_source=chatgpt.com "U.S. Department of Homeland Security"
[4]: https://travel.state.gov/content/travel/en/us-visas/employment/temporary-worker-visas.html?colooo=yes&utm_source=chatgpt.com "Temporary Worker Visas"
[5]: https://www.uscis.gov/sites/default/files/document/foia/H1-B_Training_Material_and_Guidance.pdf?utm_source=chatgpt.com "Specialty Occupation as Described ~ VSC H -lB"
[6]: https://www.uscis.gov/sites/default/files/document/presentations/Additional_%20Employment-Based_Visas.pdf?utm_source=chatgpt.com "Topics of Discussion"
[7]: https://www.uscis.gov/node/92821?utm_source=chatgpt.com "Chapter 5 - Practical Training | USCIS"
[8]: https://travel.state.gov/content/travel/en/us-visas/employment.html?utm_source=chatgpt.com "Employment"
