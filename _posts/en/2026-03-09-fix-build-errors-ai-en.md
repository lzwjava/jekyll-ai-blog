---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Build Errors Fast With AI
translated: false
type: note
---

Question: What is the best strategy for using AI coding assistants (like GitHub Copilot or Claude Code) to fix multiple build errors efficiently by providing one example fix as a one-shot learning prompt?

Answer:

## One-Shot Error Fix Strategy for AI Coding Assistants

You've described a very effective prompt engineering technique. Here's a comprehensive breakdown of why it works and how to apply it systematically.

---

### Why This Strategy Works

When you paste all 20 errors at once and ask an AI to "fix them all," the AI must **guess** the pattern. But when you:

1. Fix **one error manually** (or ask AI to fix just one)
2. Show the AI **that one fix as an example**
3. Then paste **all remaining similar errors**

...you've given the AI a **concrete template** — this is called **one-shot prompting**, and it dramatically improves accuracy because the model no longer has to infer intent.

---

### Step-by-Step Workflow

```
Step 1: Run build
  mvn compile  OR  npm run build
  → Get 20 errors

Step 2: Group errors by TYPE/FAMILY
  - Type A: NullPointerException pattern (8 errors)
  - Type B: Missing import (7 errors)
  - Type C: Type mismatch (5 errors)

Step 3: Fix ONE error from Type A manually or with AI help
  → This becomes your "sample"

Step 4: Prompt the AI:
  "Here is ONE example of the error and its fix:
   [ERROR SAMPLE] → [FIXED CODE SAMPLE]
   
   Now here are 8 similar errors from the same build.
   Apply the same fix pattern to each:
   [paste all 8 errors]"

Step 5: Repeat for Type B and Type C families
```

---

### Prompt Template You Can Reuse

```
I have multiple build errors of the same type.

Here is ONE example error and how I fixed it:

--- BEFORE FIX ---
[paste original broken code snippet]

--- ERROR MESSAGE ---
[paste the specific error]

--- AFTER FIX ---
[paste corrected code snippet]

Now here are all similar errors from my build output.
Please apply the same fix pattern to each one:

[paste all similar error messages with file:line references]
```

---

### Why "Error Families" Matter

| Approach | AI Accuracy | Why |
|---|---|---|
| Dump all 20 errors at once | ~50–60% | AI guesses patterns |
| Fix by error family with one-shot | ~85–95% | AI has a concrete reference |
| Fix one error at a time | High but slow | No parallelism |

Grouping by family means errors that **share the same root cause** get the same treatment, avoiding inconsistent fixes.

---

### Tips to Maximize Accuracy

- **Include file name + line number** in your paste so AI can reason about scope
- **Group by error code** (e.g., TS2345, NullPointerException, cannot find symbol) — same code = same family
- After AI generates fixes, **run the build again** immediately — don't batch too many families before verifying
- If a family has **variations**, provide **2 samples** (two-shot) instead of one
- For `mvn` Java errors, the `[ERROR]` prefix lines are the most useful to copy — skip the `[INFO]` noise

---

### Example: TypeScript / npm run build

```
Family: TS2345 - Argument of type 'string' is not assignable to parameter of type 'number'

Sample fix you provide:
  BEFORE: doSomething(userId)   // userId is string
  AFTER:  doSomething(Number(userId))

Then paste all 12 TS2345 errors → AI applies Number() cast consistently
```

---

### Summary

> **Fix 1 → Show AI the fix → Give AI all similar errors → Let it batch-apply the pattern**

This is essentially teaching the AI **by example**, which aligns with how LLMs perform best. The one-shot sample eliminates ambiguity and anchors the model's behavior to your specific codebase style and fix convention.