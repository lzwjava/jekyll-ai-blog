---
audio: false
generated: true
image: false
lang: en
layout: post
title: Building an Autonomous Math Research Swarm
translated: false
type: note
---

Question: **How could you build your own OpenAI-style autonomous math/research swarm? Is Karpathy’s `autoresearch` the right starting point?**

Answer: **Yes — but `autoresearch` is the right *pattern*, not the complete framework.** For your goal, I would build a small **ResearchOS** around it rather than immediately adopting a heavyweight agent framework.

Karpathy's `autoresearch` already has the essential loop: an agent modifies a research program, runs a fixed-budget experiment, measures the result, keeps/reverts the change, and repeats. ([GitHub][1])

For mathematical research, change the objective from:

```text
modify train.py
        ↓
5-minute training
        ↓
val_bpb
        ↓
keep / discard
```

to:

```text
conjecture / problem
        ↓
generate idea
        ↓
implement proof / experiment
        ↓
formal checker / numerical checker
        ↓
critic agents
        ↓
score
        ↓
keep promising branch
        ↓
iterate
```

### 1. I would NOT start with LangGraph / CrewAI

For you, I'd use:

```text
Python
  +
asyncio
  +
git worktrees
  +
Claude Code / Codex / Gemini CLI
  +
Lean
  +
SQLite
  +
Docker
```

That's enough.

You don't actually need an "agent framework."

The important abstraction is a **research loop**.

```python
while budget_left():

    problem = db.get_problem()

    ideas = parallel([
        researcher(problem),
        researcher(problem),
        researcher(problem),
        researcher(problem),
    ])

    candidates = parallel([
        solver(problem, idea)
        for idea in ideas
    ])

    verified = parallel([
        verify(candidate)
        for candidate in candidates
    ])

    critiques = parallel([
        critic(candidate)
        for candidate in verified
    ])

    score = evaluate(verified, critiques)

    if score > threshold:
        db.commit(candidate)
```

That's basically the primitive from which the 10,000-agent system can be constructed.

---

## 2. The key is **verification**, not number of agents

This is the biggest lesson from the current OpenAI story.

You don't want:

```text
1000 agents
    ↓
1000 opinions
    ↓
LLM says "looks correct"
```

You want:

```text
             ┌── Agent A ──┐
             ├── Agent B ──┤
Problem ────►├── Agent C ──┤
             └── Agent D ──┘
                    │
                    ▼
             candidate proof
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
      Lean       symbolic     numerical
     checker      checker      checker
        │           │           │
        └───────────┼───────────┘
                    ▼
                 Critic
                    │
                    ▼
              research DB
```

For serious mathematics, **a deterministic verifier is your reward model**.

Lean is especially interesting here because you can make the final criterion:

```text
Does Lean accept the theorem?
```

rather than:

```text
Does GPT think the proof looks convincing?
```

The current OpenAI report itself reportedly includes Lean formalization, which is exactly the direction I'd take. ([The Wall Street Journal][2])

---

# 3. Your first version should be tiny

Don't attempt Navier–Stokes.

Build something like:

```text
research/
├── problem.md
├── program.md
├── agents/
│   ├── researcher.py
│   ├── solver.py
│   ├── critic.py
│   └── verifier.py
├── experiments/
├── proofs/
├── memory/
├── db.sqlite
└── orchestrator.py
```

`problem.md`:

```markdown
# Problem

Prove:

For every n >= 1,
1 + 2 + ... + n = n(n+1)/2.

Requirements:

- produce Lean proof
- no `sorry`
- minimize proof complexity
```

Then:

```bash
python orchestrator.py
```

Agent 1:

```text
try induction
```

Agent 2:

```text
try algebraic identity
```

Agent 3:

```text
search existing lemmas
```

Agent 4:

```text
attempt direct Lean proof
```

Then Lean decides.

---

# 4. Then make the search tree enormous

The interesting architecture becomes:

```text
                         PROBLEM
                            │
                 ┌──────────┼──────────┐
                 ▼          ▼          ▼
              strategy   strategy   strategy
                 │          │          │
             ┌───┴───┐  ┌──┴───┐  ┌───┴───┐
             ▼       ▼  ▼      ▼  ▼       ▼
            proof   proof    proof      proof
             │       │        │           │
             └───────┴────────┴───────────┘
                         │
                         ▼
                      verifier
                         │
                  ┌──────┴──────┐
                  ▼             ▼
                 FAIL          PASS
                  │             │
                  ▼             ▼
               critic       formalize
                  │             │
                  └──────┬──────┘
                         ▼
                       memory
```

Now you have **Monte-Carlo-tree-search-like exploration over mathematical ideas**.

That's much more interesting than a conventional multi-agent framework.

---

# 5. Where `autoresearch` fits

I would literally steal Karpathy's design philosophy.

The original project has an extremely small interface:

```text
prepare.py
train.py
program.md
```

The agent modifies the experiment, runs it, measures it, and learns from the result. ([GitHub][1])

For your math version:

```text
problem.md
research.py
program.md
verify.py
```

where:

```text
problem.md
    ↓
program.md
    ↓
agent
    ↓
research.py
    ↓
Lean / Python / Mathematica
    ↓
score
```

The beautiful part is that **`program.md` becomes your research organization**.

You can tell the agent:

```markdown
You are the lead mathematician.

Do not merely generate proofs.

For every failed attempt:

1. identify the exact obstruction
2. record it in memory
3. generate 3 alternative strategies
4. avoid repeating failed strategies
5. prioritize ideas with independent mathematical justification

A proof is accepted only when Lean verifies it.
```

That is essentially an executable research methodology.

---

# 6. Then add specialized agents

Don't make every agent identical.

I'd create:

```text
                    ORCHESTRATOR
                         │
       ┌─────────────────┼──────────────────┐
       │                 │                  │
       ▼                 ▼                  ▼
   Explorer          Mathematician       Librarian
       │                 │                  │
       ▼                 ▼                  ▼
 generate ideas     construct proof     search papers
       │                 │                  │
       └─────────────────┼──────────────────┘
                         ▼
                      Critic
                         │
                         ▼
                    Formalizer
                         │
                         ▼
                      Lean
```

Later:

```text
Explorer
Solver
Counterexample Hunter
Literature Agent
Formalization Agent
Proof Critic
Numerical Experimenter
Meta-Researcher
```

The **Counterexample Hunter** is particularly important.

Instead of asking:

> "Can you prove this?"

ask another model:

> "Assume this theorem is false. Find the smallest counterexample."

That's an extremely powerful adversarial loop.

---

# 7. Memory becomes critical

Don't just dump conversations into a vector DB.

I'd maintain structured research state:

```sql
CREATE TABLE experiments (
    id INTEGER PRIMARY KEY,
    parent_id INTEGER,
    strategy TEXT,
    hypothesis TEXT,
    result TEXT,
    score REAL,
    status TEXT
);

CREATE TABLE failures (
    strategy TEXT,
    obstruction TEXT,
    evidence TEXT
);

CREATE TABLE discoveries (
    statement TEXT,
    proof TEXT,
    confidence REAL
);
```

Then agents can query:

```python
failures = db.search_failures(
    current_strategy
)
```

This prevents:

```text
Agent #37:
"I have a brilliant idea!"

Agent #12 already tried it 400 iterations ago.
```

---

# 8. Scaling to 1000 agents

Once the single-agent loop works, **don't rewrite the architecture**.

Just make:

```python
tasks = [
    ResearchTask(problem, seed=i)
    for i in range(1000)
]

await asyncio.gather(
    *(run_agent(t) for t in tasks)
)
```

But use different search distributions:

```python
temperature = {
    "conservative": 0.2,
    "normal":       0.7,
    "creative":     1.2,
    "crazy":        1.8,
}
```

Then perhaps:

```text
700 exploitation agents
200 exploration agents
50 critics
50 formalizers
```

The exact numbers aren't important initially.

**Diversity of search trajectories is.**

---

# 9. Your GPU is actually useful here

You don't necessarily need frontier API models for every role.

For example:

```text
                         orchestrator
                              │
                    frontier model API
                              │
          ┌───────────────────┼──────────────────┐
          ▼                   ▼                  ▼
       planning            critique          synthesis
          │                   │                  │
          └───────────────────┼──────────────────┘
                              ▼
                       local models
                              │
                    RTX 4070 / cloud GPU
                              │
                    cheap parallel agents
```

Use expensive models for:

```text
research direction
proof strategy
final synthesis
```

Use cheap/local models for:

```text
proof mutation
lemma search
counterexample generation
code editing
routine critique
```

That's much closer to how you'd economically build a real research swarm.

---

# 10. And yes: start with Karpathy `autoresearch`

I'd do this in stages:

```text
Stage 1
-------
karpathy/autoresearch
        ↓
understand autonomous experiment loop


Stage 2
-------
autoresearch
        +
Lean
        ↓
autonomous theorem proving


Stage 3
-------
multiple agents
        ↓
parallel hypothesis search


Stage 4
-------
persistent research DB
        ↓
agents learn from previous failures


Stage 5
-------
agent specialization
        ↓
research organization


Stage 6
-------
100s/1000s agents
        ↓
distributed research swarm
```

There are already community extensions moving in this direction; for example, `autoresearch-agents` adds orchestrator/researcher/implementer roles while preserving the basic autoresearch loop. ([GitHub][3])

And the original `autoresearch` repo itself is intentionally minimal: **one GPU, one training script, one program specification, autonomous iteration**. ([GitHub][1])

### What I would build in your case

Given that you're already doing **LLM training + CUDA + agents**, I'd make a project like:

```text
        ┌───────────────────────────┐
        │       ResearchOS          │
        │                           │
        │  problem → hypothesis     │
        │          ↓                │
        │      agent swarm          │
        │          ↓                │
        │    experiment/proof       │
        │          ↓                │
        │       verifier            │
        │          ↓                │
        │       score + memory      │
        │          ↓                │
        │      next generation      │
        └───────────────────────────┘
```

**Start with 4 agents, not 10,000.**

If you can make **4 agents autonomously discover something nontrivial overnight**, scaling to 100 or 1,000 is an engineering problem.

If 4 agents can't produce useful research, **10,000 agents will mostly produce 10,000 piles of garbage**.

That is exactly why `autoresearch` is such a good starting point: it forces you to solve the **evaluation loop** before throwing compute at the problem. ([GitHub][1])

References:

* [Karpathy — autoresearch](https://github.com/karpathy/autoresearch?utm_source=chatgpt.com)
* [autoresearch-agents multi-agent fork](https://github.com/artificialguybr/autoresearch-agents?utm_source=chatgpt.com)
* [OpenAI Navier–Stokes coverage](https://www.theverge.com/ai-artificial-intelligence/991710/openai-navier-stokes-solution?utm_source=chatgpt.com)

[1]: https://github.com/karpathy/autoresearch?ref=stdy.blog&utm_source=chatgpt.com "GitHub - karpathy/autoresearch at stdy.blog · GitHub"
[2]: https://www.wsj.com/tech/ai/openai-millennium-prize-navier-stokes-math-2bf240f8?utm_source=chatgpt.com "OpenAI Says It Has Solved a Millennium Prize Problem-a Holy Grail of Math"
[3]: https://github.com/artificialguybr/autoresearch-agents?utm_source=chatgpt.com "GitHub - artificialguybr/autoresearch-agents: AI agents running research on single-GPU nanochat training automatically · GitHub"