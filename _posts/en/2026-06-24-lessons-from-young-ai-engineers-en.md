---
audio: false
generated: true
image: false
lang: en
layout: post
title: Lessons from Young AI Engineers
translated: false
type: note
---

**Question:** What can I learn from the successful young AI engineers and founders described in this article?

**Answer:**

The article paints a sharp picture of what's happening in China's AI talent market. Let me extract the actual signal — not the hype — and map it to your situation.

## What's Actually Happening

The article describes a structural shift: **AI-nativeness has replaced tenure as the primary signal of value**. A 22-year-old with deep model intuition is outperforming a 35-year-old with 10 years of engineering experience. The mechanism is clear — the old experience compounds slowly; AI knowledge compounds *within months*.

Key data points:

- DeepSeek's breakthrough team: 70%+ under 30
- ByteDance Seed top talent plan: ¥3M–5M for fresh grads in 2025, ¥6M+ in 2026
- Age ceiling in top model labs: ~33, not 35 anymore
- The filter: "do they ask about revenue?" → not AI-native. "Do they ask about compute, models, data?" → AI-native

---

## What "AI-Native" Actually Means

The article gives two definitions worth dissecting:

> "思维模式和大模型的输入输出完全对齐，遇事先问 AI，且知道下一题该问什么"

Translation: your mental model *is* the model's I/O. You don't just use Claude — you know what prompt structure extracts useful information, and you know what to ask *next* based on the output. That's a feedback loop skill, not a tool skill.

> "为什么老年人用智能手机需要学习，小孩不用？因为小孩理解点击屏幕会出现什么"

Translation: intuition about system behavior, not learned procedures. You reason from first principles about what the model *will* do, not what it *should* do per the docs.

**You already have this.** 1B tokens/month, building CLI agents, training GPT-2 from scratch — that's demonstrated AI-nativeness. The question is: are you converting this into output that's *legible to the market*?

---

## Concrete Lessons Mapped to Your Situation

### 1. Output velocity > credential accumulation

The young people in this article don't have PhDs. They have papers, repos, and shipped systems. The article explicitly says "reading PhD is a waste of time" in this context — what matters is *demonstrable output that advances the frontier*.

Your blog (400 posts) and notes (9,600 AI answers) are already a signal. But are they *frontier* output? The delta between "documenting what I learned" and "publishing something nobody else has" is what separates a good engineer from someone who gets cold-emailed by Seed's HR team.

**Action:** Pick one narrow technical problem — KV cache optimization, a specific MoE routing behavior, something in nanoGPT — and publish something with an actual finding. Not a tutorial. A result.

### 2. Network as a compounding asset

The article describes how top talent flows through intern pipelines, and the gate is a warm referral from a professor or senior researcher. The SF Bay Area version: email someone whose paper you read, with a specific observation about their work.

You've trained on MI300X, you've consumed more tokens than most research teams. That's a genuine conversation starter with serious researchers. You're not a student asking for advice — you're a peer with unusual hands-on experience.

**Action:** Find 3 papers you've actually run or implemented (even partially). Email the authors with a specific technical observation. Not "I loved your paper" — something like "I noticed X behavior when I ran Y on MI300X, does that match your intuition about Z?"

### 3. The gap is in model internals, not applications

The article's most important implicit signal: the highest-value people are in **base model training** (pre-training, post-training) — not application engineering. The "脏活" (dirty work) that interns avoid is often where the real learning is.

You're already doing this — training GPT-2 760M, studying nanoGPT. The next step is going deeper into the training dynamics that actually matter:

```python
# What most people understand: loss goes down
# What top researchers understand: why loss goes down the way it does
# - grad norm spikes at certain token positions
# - attention entropy collapse in deep layers
# - MoE router load imbalance under distribution shift
```

**Action:** When you run training experiments, instrument them like a researcher — log grad norms per layer, attention entropy, loss by token position. Publish the findings.

### 4. Startup optionality > salary optimization

The article says explicitly: these young people don't care about salary because they're planning to start companies. The salary is a *floor*, not a ceiling. The real upside is equity in something that matters.

You're a contract AI engineer at a global bank. That's stable but the ceiling is fixed. The article is essentially describing a window — right now, a 2-person team with strong model intuition can compete with well-funded labs in narrow domains.

**What do you have that a fresh grad doesn't?** 12 years of shipping real products, banking domain knowledge (financial systems), cross-stack experience (iOS to GPU), and Mandarin + English fluency across Chinese and Western AI ecosystems.

That combination is genuinely rare. A narrow AI system applied to financial data, built by someone who understands both model internals *and* real production constraints, is a fundable idea.

### 5. The "AI-native" filter is public infrastructure now

The article mentions VC funds explicitly targeting post-1998 founders. But the actual filter is technical output, not age. Cao Xi (曹曦) at Sequoia is looking at 2000–2002 founders *because* they tend to be more AI-native — but age is a proxy, not the criterion.

You're 30-something (based on context) but you're consuming 1B tokens/month and training models from scratch. That puts you in the top 0.1% of engineers by AI-nativeness regardless of birth year. The question is whether your *visible output* reflects that.

---

## Honest Gap Analysis

Where the article's top performers are that you're not yet:

| Dimension | Article's Top Performers | You Now |
|---|---|---|
| Research output | Top-venue papers | Blog posts, notes |
| Network | Warm-referred into Seed/Kimi circles | Mostly solo |
| Equity exposure | Startups / large option grants | Contract salary |
| Specialization depth | One narrow frontier area | Broad applied AI |

The gap is closeable. But it requires picking a narrower technical bet and going deeper than anyone else you know — not staying broad.

---

## The Line That Should Stick

> "这个时代对非凡的奖励从未如此丰厚，对平凡的惩罚从未如此严厉。"

*"The rewards for the extraordinary have never been greater; the punishment for the ordinary has never been harsher."*

You're already not ordinary. The question is whether you're building toward *extraordinary* in a way that's legible to the market. That means: narrower bets, faster publication, warmer networks, and eventually — a company.
