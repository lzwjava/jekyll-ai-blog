---
audio: false
generated: true
image: false
lang: en
layout: post
title: Autonomous Goal Loop Overview
translated: false
type: note
---

Here's the breakdown:

**What `/goal` does differently from a simple prompt:**

1. **Autonomous multi-turn loop ("Ralph loop")** — When you set a goal, Hermes doesn't just answer once. After each response, a **judge LLM** (an auxiliary model) evaluates: "Is this goal fully satisfied?" If the answer is "no", Hermes automatically feeds a continuation prompt back into the same session and keeps working — turn after turn — until the goal is done or the turn budget (default 20 turns) runs out.

2. **Judge-based evaluation** — The judge is a separate LLM call (configurable via `auxiliary.goal_judge` in config). It receives the goal text + the agent's last response and returns a strict JSON verdict: `{"done": true/false, "reason": "..."}`. A simple prompt has no automatic self-evaluation — you decide when it's done manually.

3. **Persistent state** — Goal state is saved in the SessionDB (`state_meta` table). If you `/resume` a session, the goal is still there. A simple prompt is ephemeral — once the conversation moves on, there's no persistent objective.

4. **Turn budget & auto-pause** — There's a configurable `max_turns` (default 20). When exhausted, the goal auto-pauses with a message like "⏸ Goal paused — 20/20 turns used. Use /goal resume to keep going." You can resume to continue or clear to stop.

5. **Subgoals** — You can add mid-loop criteria with `/subgoal <text>`. These get appended to both the continuation prompt (so the agent sees them) and the judge prompt (so the judge requires all criteria to be met, not just the original goal).

6. **User interruption handling** — If you send a new message mid-goal-loop, it preempts the continuation, and the goal pauses for that turn. After your exchange, the goal re-evaluates.

7. **Prompt caching is preserved** — The continuation prompt is a normal user-role message appended to the session. No system prompt mutation, no toolset swap — prompt caching stays intact. This is a hard design invariant.

**In short:** A simple prompt is fire-and-forget — one question, one answer. `/goal` is an autonomous agent loop that keeps working, self-evaluates, and persists across turns until a separate judge model confirms the objective is met. It's like giving Hermes a mission instead of a question.

Source: `hermes_cli/goals.py` (912 lines)
