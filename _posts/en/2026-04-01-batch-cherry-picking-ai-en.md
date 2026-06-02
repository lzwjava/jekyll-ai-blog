---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Strategies for Batch Cherry-Picking
translated: false
type: note
---

## Strategies for Batch Cherry-Picking with AI

Yes, your logic is sound. When dealing with a large volume of commits (around 70), breaking them into smaller batches is a highly effective way to manage **context window limits** and ensure the AI remains accurate when resolving conflicts.

While you *could* do this in batches of 10, there is actually a more efficient "Hybrid" approach that uses Git's native power for the bulk work and the AI for the "hard part" (conflicts).

---

### Recommended Workflow: The "Stop-on-Conflict" Method

Instead of manually feeding 10 commits at a time, you can tell Git to do all 70 at once. Git will process them instantly until it hits a conflict. **That is when you call in the AI.**

#### 1. Start the Batch Process in Terminal

Use the inclusive range syntax to start the cherry-pick:

```bash
# A is the commit BEFORE the start of your range
# B is the last commit you want to include
git cherry-pick A^..B
```

#### 2. Let the AI Handle the Conflict

If Git stops because of a conflict:

1. Open your AI assistant (Claude Code, Cursor, or Copilot).
2. **Prompt:** "I am in the middle of a batch cherry-pick. Please resolve the conflicts in the current files, ensuring the logic from the cherry-picked commit is preserved while respecting the target branch's existing code."
3. The AI will fix the files.
4. **You verify** and run:

   ```bash
   git add .
   git cherry-pick --continue
   ```

#### 3. Repeat

Git will automatically move to the next commit in the 70-commit sequence. If it applies cleanly, Git moves on. If there is another conflict, repeat Step 2.

---

### Why this is better than "10 at a time"

* **Efficiency:** Git is faster at applying "clean" commits than an AI agent is at processing them through a chat interface.
* **Context Preservation:** By only using the AI for conflicts, you save your context tokens for the actual code logic rather than wasting them on commits that Git could have handled automatically.
* **Linearity:** It ensures you don't accidentally skip or double-pick commits between your batches of 10.

---

### Comparison of Methods

| Feature | 10-at-a-time (Manual Batch) | Stop-on-Conflict (Hybrid) |
| :--- | :--- | :--- |
| **Speed** | Slow (requires manual intervention every 10) | Fast (only stops when necessary) |
| **Token Usage** | High (AI reads all code for every commit) | Low (AI only reads conflicted files) |
| **Risk of Error** | Moderate (human error in range selection) | Low (Git manages the sequence) |
| **Conflict Quality** | Good (AI has full context of the 10) | **Best** (AI focuses strictly on the diff) |

### Important Tips for 70+ Commits

* **Use a Temporary Branch:** Always create a new "migration" branch before starting. Never cherry-pick 70 commits directly into your main production branch.
* **Verify Mid-way:** Every 20 commits or so, run your test suite. If the AI makes a subtle logic error during a conflict resolution, it's easier to catch it early than after all 70 are done.
* **Check for Dependencies:** If commit #50 depends on a change in commit #5, but you skipped #5, the AI might hallucinate code to make it "work." Ensure your range `A^..B` covers all necessary dependencies.
