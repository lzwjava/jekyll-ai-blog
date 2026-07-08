---
audio: false
generated: true
image: false
lang: en
layout: post
title: Building Goal-Mode Agent Loops
translated: false
type: note
---

Question: In agent frameworks like Hermes (Nous Research), how do you actually use "goal mode" / long-horizon task execution — and how do you build the same pattern into your own CLI agents (ww, iclaw, zz)?

Answer:

## 1. What Hermes actually does (mechanism, not hype)

Nous Research's Hermes Agent is an open-source AI agent framework released under the MIT license that runs a five-stage learning loop: execute, evaluate, extract reusable reasoning patterns as named skills, refine those skills, and retrieve relevant skills for new tasks, with five sandbox backends — local, Docker, SSH, Singularity, and Modal. The differentiator vs. something like OpenClaw is that Hermes treats skill formation as part of the agent's own operating loop rather than depending on an external skill marketplace — after a complex task it writes a structured skill document capturing procedure, pitfalls, and verification steps, then improves that skill on future runs.

The "goal mode" long-horizon mechanism specifically works like this:

- `/goal <text>` sets a standing objective, `/goal status` checks progress, `/goal pause`/`/goal resume` halt and restart without losing state.
- After every turn, an **auxiliary judge model** is called to decide if the goal is done. The judge is deliberately conservative — it only marks a goal done when the response explicitly confirms completion, the deliverable is clearly produced, or the goal is genuinely blocked (treated as done with a block reason so budget isn't burned on impossible tasks). Critically it uses fail-open semantics: if the judge errors, Hermes treats the verdict as continue, so a broken judge never wedges progress.
- Turn budget is capped — default is 20 continuation turns (goals.max_turns in ~/.hermes/config.yaml), and when the budget hits, Hermes auto-pauses and reports how many turns were used.
- Composability: goals combined with skills work well when the goal triggers and orchestrates specific skills that handle individual steps, and goals combined with memory persistence keep long-running goals coherent across days; goals combined with multi-agent setups let a manager agent set sub-goals for worker agents.

⚠️ Caveat: several of the sources describing this (aiprofitboardroom.com, juliangoldieaiautomation.com, aisuccesslabjuliangoldie.com) are the same SEO content-mill author repeating near-identical templates — treat specific numbers (ROI claims, £/month savings) as marketing, not verified facts. The mechanism itself (judge-based turn-budgeted loop, `/goal` commands, config path) is corroborated across independent write-ups (i-scoop.eu, openhosst.com) so I'd trust the *architecture* description more than the *case-study numbers*.

The two failure modes worth internalizing before you copy this pattern: vague goals where the judge can't determine completion — be specific about what "done" means — and using the default turn budget for big goals, since 20 turns won't finish a 50-step task.

## 2. This is a general pattern — build it yourself in ~80 lines

You don't need Hermes to get this. The core primitive is: **actor loop + judge/critic + turn budget + persisted state**. Academic work formalizes this as a planner-actor split — a planner receives the task instruction, decomposes it into a reference sub-goal graph before execution, then tracks progress by comparing the actor's trajectory against that graph, intervening with corrective feedback when the actor deviates or stalls. This is directly usable in your CLI agents.

```python
# goal_loop.py — minimal Hermes-style goal harness for ww/iclaw/zz
import json, os, time
from anthropic import Anthropic

client = Anthropic()
STATE_PATH = ".goal_state.json"

def load_state():
    if os.path.exists(STATE_PATH):
        return json.load(open(STATE_PATH))
    return None

def save_state(s):
    json.dump(s, open(STATE_PATH, "w"), indent=2)

def judge(goal: str, transcript: str) -> dict:
    """Conservative judge — fail-open on error (per Hermes semantics)."""
    try:
        resp = client.messages.create(
            model="claude-opus-4-8",  # use a stronger model as judge than the actor
            max_tokens=300,
            system=(
                "You are a strict completion judge. Given a GOAL and a TRANSCRIPT of "
                "an agent's work, respond ONLY with JSON: "
                '{"done": bool, "blocked": bool, "reason": str}. '
                "Mark done=true only if the deliverable is explicitly produced, or "
                "blocked=true if further progress is genuinely impossible."
            ),
            messages=[{"role": "user", "content": f"GOAL:\n{goal}\n\nTRANSCRIPT:\n{transcript}"}],
        )
        return json.loads(resp.content[0].text)
    except Exception:
        return {"done": False, "blocked": False, "reason": "judge_error_fail_open"}

def actor_step(goal: str, history: list, tools: list) -> str:
    resp = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=2000,
        system=f"Standing goal: {goal}\nWork one concrete step closer to completion. "
                f"State clearly if you believe the goal is now complete.",
        messages=history,
        tools=tools,
    )
    # ... handle tool_use blocks, append tool_result, etc. (omitted for brevity)
    text = "".join(b.text for b in resp.content if b.type == "text")
    history.append({"role": "assistant", "content": resp.content})
    return text

def run_goal(goal: str, tools: list, max_turns: int = 20, resume: bool = False):
    state = load_state() if resume else None
    history = state["history"] if state else []
    turn = state["turn"] if state else 0

    while turn < max_turns:
        turn += 1
        out = actor_step(goal, history, tools)
        transcript = "\n".join(m.get("content", "") if isinstance(m.get("content"), str) else str(m) for m in history)

        verdict = judge(goal, transcript)
        print(f"[turn {turn}/{max_turns}] judge={verdict}")

        if verdict["done"] or verdict["blocked"]:
            save_state({"history": history, "turn": turn, "status": "finished", "reason": verdict["reason"]})
            return verdict

        save_state({"history": history, "turn": turn, "status": "running"})
        time.sleep(1)  # backoff / rate-limit hygiene

    save_state({"history": history, "turn": turn, "status": "paused"})
    print(f"⏸ Goal paused — {turn}/{max_turns} turns used. Call run_goal(..., resume=True) to continue.")
    return {"done": False, "blocked": False, "reason": "turn_budget_exhausted"}
```

Notes on why each piece matters for your context:

- **Judge model ≠ actor model.** Use a stronger/cheaper model as judge than as actor (Sonnet actor + Opus judge, or a cheap fast model as judge if cost matters — this is literally what the Hermes docs recommend when they say "Sonnet 4.8 Review — the judge model I recommend").
- **Fail-open is non-negotiable.** A judge exception should never silently kill a long-running job. That's the single biggest bug people hit rolling their own version.
- **Turn budget forces you to write a "done" spec up front** — this is the discipline part, not the code part. If you can't articulate what "done" looks like in one sentence, your goal is too vague for any of this to work regardless of framework.
- **Persisted state (JSON on disk here, Redis/SQLite in prod) is what makes it "long time task"** rather than a single long context window — you're trading context length for checkpointed iteration, which also sidesteps context-rot on 100+ turn tasks.

## 3. Where to go deeper (matches your MoE/agent-architecture direction)

- Sub-goal decomposition with explicit graphs instead of implicit judge calls: agents lose track as new information arrives during online execution, lacking a clear adaptive path to the final goal — and this is compounded during RL fine-tuning where sparse, delayed rewards make it hard to identify which actions lead to success. If you're going to train/RL your own agent (which fits your GRPO interest), read this before building a reward model around your judge.
- If you want the judge itself to be a *trained* planner rather than a prompted one: EAGLET introduces a plug-and-play, task-specific planner model whose sole responsibility is generating a global plan, in a plan-and-execute framework where the global planner and executor are cleanly separated — this is the natural next step once your prompted judge/actor split above stabilizes and you want to distill it into something cheaper to run at scale (fits your nanochat/DeepSeek MoE trajectory better than staying API-only).

For your CLI tools specifically: I'd wire the `judge()` fail-open pattern and turn-budget pause/resume into `zz` or `ww` first since it's ~80 lines and framework-agnostic, before adopting Hermes wholesale — you get the same long-horizon capability without taking on a dependency whose ecosystem is, per the comparison piece, smaller and younger than OpenClaw's, with security posture not yet proven at scale.

References:

- [Hermes Agent from Nous Research](https://www.i-scoop.eu/hermes-agent-from-nous-research/)
- [Hermes Agent: What It Is, How It Works (2026)](https://openhosst.com/blog/hermes-agent)
- [Hermes Goal Mode — Set The Target. Walk Away.](https://agentos.guide/hermes-goals)
- [A Goal Without a Plan Is Just a Wish: EAGLET (arXiv)](https://arxiv.org/pdf/2510.05608)
- [A Subgoal-driven Framework for Improving Long-Horizon LLM Agents (Google DeepMind, arXiv)](https://arxiv.org/pdf/2603.19685)
- [C-World: A Computer Use Agent Environment Creator (arXiv)](https://arxiv.org/pdf/2601.06328)
