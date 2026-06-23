---
audio: false
generated: true
image: false
lang: en
layout: post
title: Inference Cost Collapse Fuels AI Debate
translated: false
type: note
---

**Question:** In the future, inference will be cheap and fast — text-to-image, translation, all of it. Whisper is fast, Sesame is fast. Can AIs argue with each other?

**Answer:**

Yes, and this is already happening. The trajectory is clear:

**Inference cost collapse is real.** GPT-4-level capability now costs ~100x less than 2 years ago. Groq on LPU does 800+ tokens/sec. Cerebras does 2000+ tokens/sec. Text-to-image went from 30s (SD 1.x) to <1s (SDXL Turbo, FLUX schnell). Whisper runs real-time on CPU. The trend doesn't slow down.

**AI debate / multi-agent argument is already a research direction.** A few concrete forms:

- **Society of Mind / multi-agent debate** — multiple LLMs argue positions, a judge model picks the best answer. Shown to improve reasoning on hard problems (Du et al., 2023 — "Improving Factuality and Reasoning in Language Models through Multiagent Debate")
- **Constitutional AI** — Claude's own training uses AI-vs-AI critique loops (red-teaming, revision)
- **LLM-as-judge** — one model scores another's output; now standard in RLHF pipelines
- **AutoGen / CrewAI** — agents with opposing roles (devil's advocate, critic, optimizer) literally argue in a message loop until convergence

**What "AI arguing" looks like in code (50 lines):**

```python
import anthropic

client = anthropic.Anthropic()

def agent_turn(role: str, position: str, history: list[dict]) -> str:
    system = f"You are {role}. Argue {position} forcefully. Be concise, technical, sharp."
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=system,
        messages=history,
    )
    return response.content[0].text

def debate(topic: str, rounds: int = 3):
    history_a, history_b = [], []
    last_b = f"Let's debate: {topic}"

    for i in range(rounds):
        # Agent A responds to B
        history_a.append({"role": "user", "content": last_b})
        reply_a = agent_turn("Agent A", "FOR", history_a)
        history_a.append({"role": "assistant", "content": reply_a})
        print(f"[A] {reply_a}\n")

        # Agent B responds to A
        history_b.append({"role": "user", "content": reply_a})
        reply_b = agent_turn("Agent B", "AGAINST", history_b)
        history_b.append({"role": "assistant", "content": reply_b})
        print(f"[B] {reply_b}\n")
        last_b = reply_b

debate("MoE is better than dense transformers for frontier models")
```

**The interesting implication:** when inference is near-free, you can run 100 agents arguing in parallel, distill the consensus, and get better answers than any single model. This is basically ensemble learning but with language. DeepSeek R1's chain-of-thought is a single model arguing with itself — multi-agent debate is the distributed version.

**Sesame specifically** (the conversational voice AI) — fast enough to feel real-time, emotional enough to feel like a person. When two of those argue, it's indistinguishable from humans debating on a podcast. That's the near future.

The bottleneck shifts from *can we do this* to *what's worth arguing about* — curation and orchestration become the real engineering problems.

**References:**

- [Improving Factuality via Multiagent Debate — Du et al. 2023](https://arxiv.org/abs/2305.14325)
- [AutoGen: Multi-agent conversation framework](https://github.com/microsoft/autogen)
