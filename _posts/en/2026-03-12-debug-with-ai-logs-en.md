---
audio: false
generated: true
image: false
lang: en
layout: post
title: Debug With AI Using Logs
translated: false
type: note
---

Question: What is the golden rule for using AI coding assistants (Copilot/Codex/Claude Code) to fix hard problems?

Answer:

## The Golden Rule: Debug Log-Driven AI Fixing

This is a highly effective and practical strategy for tackling difficult bugs with AI assistance. Here's a comprehensive breakdown:

---

### The Core Loop

```
Hard Problem → Add Debug Logs → Observe Output → Feed Back to AI → Fix
```

---

### Why This Works

AI coding assistants often **lack runtime context**. They can only see your static code, not what's actually happening at execution time. Debug logs bridge that gap by exposing:

- Actual variable values vs. expected values
- Execution flow (which branches/methods are actually reached)
- Timing issues and race conditions
- Null/undefined states that weren't obvious in code review
- Unexpected data shapes from APIs or databases

---

### Step-by-Step Process

**Step 1 — Describe the problem to AI, ask it to add debug logs**
> "I have a bug in this function. Don't fix it yet — add comprehensive debug logs so I can observe the runtime behavior."

**Step 2 — Frontend: Add `console.log` strategically**
```javascript
console.log('[DEBUG] fetchUser called with id:', id);
console.log('[DEBUG] API response:', JSON.stringify(response));
console.log('[DEBUG] Parsed user object:', user);
console.log('[DEBUG] State before update:', this.state);
```

**Step 3 — Backend: Add Log4j / SLF4J logs**
```java
log.debug("[DEBUG] entering processOrder(), orderId={}", orderId);
log.debug("[DEBUG] fetched order: {}", order);
log.debug("[DEBUG] inventory check result: {}", inventoryStatus);
log.error("[ERROR] unexpected state: {}", e.getMessage(), e);
```

**Step 4 — Run the app, reproduce the bug, collect logs**

Copy the relevant log output — this is your **evidence**.

**Step 5 — Feed logs back to the AI**
> "Here is the console output when the bug occurs: [paste logs]. Now identify the root cause and fix it."

**Step 6 — AI fixes with full context**

Now the AI has runtime truth, not just static guesses. The fix quality improves dramatically.

---

### Pro Tips

| Tip | Detail |
|---|---|
| **Tag your logs** | Use prefixes like `[DEBUG]`, `[FLOW]`, `[STATE]` to filter easily |
| **Log before AND after** | Wrap suspicious operations to see input vs. output |
| **Log in catch blocks** | Always log the full exception + context, not just `e.getMessage()` |
| **Remove logs after fix** | Or use proper log levels (`DEBUG`) so they're hidden in production |
| **Be specific in prompt** | Tell AI exactly which log line looks wrong and why |

---

### Example Prompt Template

```
I have this bug: [describe symptom]

Here is the relevant code: [paste code]

Here is the runtime log output when the bug occurs:
[paste logs]

Based on the logs, identify the root cause and provide a fix.
```

---

### Summary

The golden rule is essentially **turning AI from a static code reader into a dynamic debugger** — by giving it the runtime evidence it needs through logs. This is especially powerful for:

- Race conditions
- Wrong data from external APIs
- Complex state management bugs
- Intermittent / hard-to-reproduce issues
