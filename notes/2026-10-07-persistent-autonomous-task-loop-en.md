---
audio: false
generated: true
image: false
lang: en
layout: post
title: Persistent Autonomous Task Loop
translated: false
type: note
---

Question: What is the `goal` command in Pi Agent, similar to Hermes Agent?

Answer:

`/goal` in Hermes Agent is basically a **persistent autonomous task loop**. It is not just a prompt shortcut; it changes the agent behavior from:

```
User prompt
    ↓
Agent does one response
    ↓
Stop
```

into:

```
User sets goal
    ↓
Agent works
    ↓
Judge checks "is it really done?"
    ↓
If not done:
    Agent continues automatically
    ↓
Repeat until done / paused / budget exhausted
```

Hermes implements `/goal` as a Ralph-loop style mechanism: a separate judge model evaluates completion after each turn, and the agent continues if the goal is not satisfied. ([GitHub][1])

Example:

```
/goal Fix all failing tests in this repository and make CI pass
```

The agent will keep doing:

```
inspect code
→ edit files
→ run tests
→ analyze failures
→ fix
→ rerun
```

without you typing "continue". ([Ryder Freeman Logos][2])

Useful commands:

```text
/goal status     # see current goal
/goal pause      # temporarily stop
/goal resume     # continue
/goal clear      # remove goal
```

Hermes also supports adding extra criteria:

```text
/subgoal Add unit tests for the new API
```

so the agent must satisfy both the original goal and the added condition. ([Hermes Agent][3])

For **Pi Agent**, the equivalent depends on which Pi implementation you mean. If you mean Pi Agent / the `pi` coding agent ecosystem, it historically focuses more on interactive agent sessions, tools, and extensions rather than Hermes-style persistent goals. I don't see a built-in `/goal` command equivalent in Pi from the available information.

You can implement the same idea in Pi with an extension:

```python
goal = """
Build a REST API.
Requirements:
- implement endpoints
- write tests
- run pytest
- fix failures
"""

while True:
    response = agent.run(goal)

    verdict = judge_model(
        goal=goal,
        output=response
    )

    if verdict == "done":
        break
```

The key idea is:

* **normal agent** = "answer this task"
* **goal agent** = "own this objective until completion"

This is one of the important shifts toward agentic software engineering: humans specify the **finish line**, agents handle the iteration loop.

References:

* Hermes Agent Persistent Goals: ([GitHub][1])
* Hermes Slash Commands: ([Hermes Agent][3])

[1]: https://github.com/nousresearch/hermes-agent/blob/main/website/docs/user-guide/features/goals.md?utm_source=chatgpt.com "hermes-agent/website/docs/user-guide/features/goals.md at main · NousResearch/hermes-agent · GitHub"
[2]: https://ryderfreeman4logos.github.io/hermes-agent-docs-i18n/en/website/docs/user-guide/features/goals?utm_source=chatgpt.com "Persistent Goals (/goal) - Hermes Agent Docs i18n"
[3]: https://hermes-agent.nousresearch.com/docs/reference/slash-commands?utm_source=chatgpt.com "Slash Commands Reference | Hermes Agent"
