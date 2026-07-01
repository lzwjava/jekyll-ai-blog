---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes /goal Command Ralph Loop
translated: false
type: note
---

Here's how the `/goal` command works in hermes-agent:

## Overview

`/goal` implements a **"Ralph loop"** — a persistent, autonomous goal that keeps Hermes working across multiple turns until the goal is achieved, the user stops it, or a turn budget is exhausted. It's described in `hermes_cli/goals.py`.

## Core Flow

```
User sets /goal <text>
        |
        v
   Goal becomes "active" (persisted in SessionDB)
        |
        v
   Hermes processes the goal as a normal user message
        |
        v
   After each turn, _maybe_continue_goal_after_turn() fires
        |
        v
   Judge model evaluates: "Is the goal done?"
        |
      / \
    done  continue
    |       |
    v       v
  Mark   Push continuation prompt
  done   back into _pending_input queue
            |
            v
         Next turn starts automatically
```

## Key Components

### 1. GoalState (dataclass, line 130)

Stores per-session goal state: `goal` text, `status` (active/paused/done/cleared), `turns_used`, `max_turns` (default 20), `subgoals` list, `consecutive_parse_failures`, etc. Persisted in SessionDB's `state_meta` table keyed by `goal:<session_id>`.

### 2. The Judge (`judge_goal()`, line 334)

After every turn, an auxiliary model is called with a strict prompt asking: "Is the goal satisfied based on the agent's last response?" The judge must reply with a JSON verdict: `{"done": true/false, "reason": "..."}`. The judge is **fail-open** — any error defaults to "continue" so a broken judge doesn't stall progress. The turn budget is the backstop.

### 3. GoalManager (line 431)

Orchestrates state. Key methods:

- `set(goal)` — create new active goal, persisted to DB
- `pause(reason)` / `resume()` — user controls
- `clear()` — remove the goal
- `evaluate_after_turn(last_response)` — the main entry point called after each turn. Calls the judge, updates state, and returns a decision dict with `should_continue` and `continuation_prompt`
- `next_continuation_prompt()` — builds the prompt fed back as a user message

### 4. CLI Handler (`_handle_goal_command`, cli.py line 8263)

Dispatches subcommands:

- `/goal <text>` — set a new goal (also immediately queues the goal text into `_pending_input` to kick off the loop)
- `/goal status` — show current state
- `/goal pause` / `/goal resume` — manual control
- `/goal clear|stop|done` — remove the goal

### 5. The Loop Hook (`_maybe_continue_goal_after_turn`, cli.py line 8404)

Called after every CLI turn. It:

1. Skips if no active goal or a real user message is already queued (preemption)
2. Auto-pauses if the turn was Ctrl+C interrupted
3. Extracts the last assistant response from conversation history
4. Calls `mgr.evaluate_after_turn()` which runs the judge
5. If `should_continue`, pushes the continuation prompt onto `_pending_input` — triggering another turn automatically

### 6. Continuation Prompts (line 60-81)

Two templates: one plain, one with subgoals. Example:

```
[Continuing toward your standing goal]
Goal: Refactor the auth module

Continue working toward this goal. Take the next concrete step.
If you believe the goal is complete, state so explicitly and stop.
```

## Stopping Conditions

| Condition | What happens |
| ----------- | ------------- |
| Judge says "done" | Goal marked done, user notified |
| Turn budget exhausted (default 20) | Auto-paused, `/goal resume` resets budget |
| User sends real message mid-loop | Preempts continuation, goal pauses for that turn |
| User presses Ctrl+C | Auto-paused (recoverable via `/goal resume`) |
| 3 consecutive judge parse failures | Auto-paused with config hint for a better judge model |
| `/goal pause` or `/goal clear` | Manual stop |

## Subgoals (`/subgoal`)

Users can add extra criteria mid-loop via `/subgoal <text>`. These are appended to both the judge prompt (verdict must consider them) and the continuation prompt (agent sees them). Supports `remove <n>` and `clear` subcommands.

## Design Invariants

- **No system prompt mutation** — continuation prompts are just user messages, so prompt caching stays intact
- **Fail-open judge** — errors default to "continue"; turn budget is the real backstop
- **User preemption** — real user messages always take priority over continuation prompts
- **Session persistence** — goal state survives `/resume` across sessions
