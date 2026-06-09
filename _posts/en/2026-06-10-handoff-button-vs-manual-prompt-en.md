---
audio: false
generated: true
image: false
lang: en
layout: post
title: Handoff Button vs Manual Prompt
translated: false
type: note
---

Now I have the full picture. Here's the difference:

== "Start Implementation" Button vs Manual Prompt ==

THE HANDOFF BUTTON (planAgentProvider.ts:225-231):

```
startImplementationHandoff = {
    label: 'Start Implementation',
    agent: 'agent',          // switches to main coding agent
    prompt: 'Start implementation',
    send: true,              // auto-sends the prompt
    model: implementAgentModelOverride  // optional model switch
}
```

When you click "Start Implementation":

1. MODE SWITCH — It calls `workbench.action.chat.toggleAgentMode` to
   switch from the Plan agent to the main Agent (coding) mode.

2. AUTO-SEND — It sends "Start implementation" as the user message
   automatically (`send: true`). You don't type anything.

3. FULL CONVERSATION HISTORY CARRIES OVER — This is the critical
   difference. The implementation agent receives the ENTIRE planning
   conversation: all the Discovery research, Alignment Q&A, Design
   iterations, and Refinement rounds. The agent has context of:
   - What the Explore/Search subagents found
   - What questions were asked and answered
   - What alternatives were considered and rejected
   - The final approved plan

4. MODEL OVERRIDE — Can use a different model for implementation via
   `ConfigKey.ImplementAgentModel` setting. Plan might use a cheaper
   model for research, implementation uses a stronger one.

MANUALLY ADDING plan.md + PROMPTING "do it":

1. NO MODE SWITCH — You stay in whatever mode you're already in.
   If you're still in Plan agent mode, it will refuse to implement
   ("Your SOLE responsibility is planning. NEVER start implementation.")

2. YOU MUST BE IN AGENT MODE — You need to manually switch to Agent
   mode first, then attach plan.md and type your prompt.

3. PLAN.md ONLY — The agent only sees the plan document itself.
   It does NOT see:
   - The research Discovery phase findings
   - The Q&A Alignment discussion
   - What was explored and rejected
   - The reasoning behind decisions

   The plan.md is a summary; the conversation is the full context.

4. YOUR OWN PROMPT — You write whatever you want. Could be
   "implement step 1 only" or "do this but skip the tests".
   More control, but less automatic.

5. NO MODEL OVERRIDE — Uses whatever model the Agent mode is
   configured with.

== PRACTICAL IMPACT ==

The handoff is richer because the implementation agent gets the full
planning transcript as conversation history. With manual prompt, it
only gets the plan.md file — a compressed artifact. For complex plans
where the "why" matters (edge cases discovered during research,
tradeoffs discussed), the handoff preserves that context. For simple
plans where the plan.md is self-contained, the difference is minimal.

The handoff also has a second option: "Open in Editor" which creates
an untitled file with the plan for further editing before you commit
to implementation.
