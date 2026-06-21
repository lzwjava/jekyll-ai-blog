---
audio: false
generated: true
image: false
lang: en
layout: post
title: Generator-Verifier Hallucination Reduction
translated: false
type: note
---

**Question:** What is Probably Company, and how do they use a verifier to reduce hallucination?**Answer:**

I couldn't find a specific company named exactly "Probably" in the AI hallucination space — it's likely you're thinking of one of these candidates, or the name was slightly off:

- **Probably.ai** — a personal research blog on probabilistic AI by Tárik S. Salem, not a product company
- The pattern you're describing ("use a verifier to reduce hallucination") maps to several real, well-known techniques and companies

Let me give you the full picture of what that pattern actually is, since it's genuinely important for your AI engineering work:

---

## The Verifier Pattern for Hallucination Reduction

This is the **generator → verifier** architecture. The core idea: don't trust one model's output. Run a second model (the verifier) to check factual consistency before returning to the user.

### Architecture

```
User prompt
     │
     ▼
┌──────────┐      response      ┌──────────────┐
│ Generator│ ────────────────►  │   Verifier   │
│  (LLM)   │                   │  (judge LLM) │
└──────────┘                   └──────┬───────┘
                                      │
                              ✓ pass / ✗ fail
                                      │
                              ┌───────▼────────┐
                              │ Re-prompt or   │
                              │ Return result  │
                              └────────────────┘
```

This is widely called **LLM-as-judge** or **verification agent**.

### How It Works Mechanically

The verifier receives:

1. The original user query
2. The generator's response
3. (Optional) retrieved context from RAG

It then outputs a structured verdict: `{verdict: "hallucinated" | "faithful", reason: "..."}`.

A typical production stack uses GPT-4o as the primary generator and Claude as the verifier — different model families to avoid correlated failure modes. The tradeoff is roughly 30-50% hallucination reduction at the cost of 2x token spend and 1-3s extra latency.

### Real Companies Doing This

- **AIMon** — dedicated hallucination detection model (HDM-1). HDM-1 is a specialized hallucination detection model that can be used in real-time or offline, available in on-premise or hosted configurations, with fast enough latency to support re-prompting and multi-sampling workflows.

- **Galileo** — uses multiple evaluation methods including embedding-based similarity, Chain-of-Thought analysis, and a proprietary G-Eval metric measuring context alignment and reasoning quality.

- **Datadog LLM Observability** — uses LLM-as-judge approaches with optimized judgment prompts and structured output enforcement via finite state machines to ensure the verifier's verdict is always parseable JSON.

### Verifier Implementation (Minimal)

{% raw %}

```python
import anthropic

client = anthropic.Anthropic()

def generate(prompt: str) -> str:
    r = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return r.content[0].text

def verify(query: str, response: str, context: str = "") -> dict:
    judge_prompt = f"""You are a factual verifier. Given:
QUERY: {query}
CONTEXT: {context}
RESPONSE: {response}

Is the response faithful to the context and factually accurate?
Respond ONLY as JSON: {{"verdict": "faithful"|"hallucinated", "reason": "..."}}"""

    r = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        messages=[{"role": "user", "content": judge_prompt}]
    )
    import json
    return json.loads(r.content[0].text)

def generate_with_verification(prompt: str, context: str = "", retries: int = 2) -> str:
    for _ in range(retries):
        response = generate(prompt if not context else f"Context: {context}\n\n{prompt}")
        verdict = verify(prompt, response, context)
        if verdict["verdict"] == "faithful":
            return response
        prompt += f"\n\nPrevious attempt was wrong: {verdict['reason']}. Try again carefully."
    return response  # return best effort after retries
```

{% endraw %}

### Why Verifiers Work

Hallucination is an "inevitable" byproduct of the current approach to LLM training: maximizing predictive performance on large text corpora without a built-in verifier. The verifier adds the missing truth-checking constraint as a post-hoc layer rather than baking it into training.

Research published at ICML 2025 (VeriFY) teaches models to assess factual uncertainty *during* generation rather than relying on post-hoc checking — models that learn to verify their own claims as they produce them, with hallucination reduction of 9.7–53.3% across model families and only modest recall loss. That's the next evolution: internalizing the verifier into the generator itself (think process reward models, RLHF on factuality).

---

If you can give me more context on where you heard "Probably company" — a podcast, tweet, paper, video — I can track down the exact reference. The name might be slightly different (e.g., "Proba", "ProbAI", "Probably Good", etc.).
