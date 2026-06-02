---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 批量精选樱桃的AI策略
translated: true
type: note
---

## Strategies for Batch Cherry-Picking with AI

是的，你的逻辑是合理的。在处理大量 Commits（大约 70 个）时，将它们拆分为较小的 Batch 是管理 **Context Window Limits** 并确保 AI 在解决 Conflict 时保持准确性的高效方法。

虽然你*可以*按每组 10 个进行操作，但实际上有一种更高效的 "Hybrid" 方法，它利用 Git 原生的能力处理大部分工作，而将 AI 用于“困难部分”（Conflict）。

---

### Recommended Workflow: The "Stop-on-Conflict" Method

与其手动分次输入 10 个 Commits，你可以让 Git 一次性处理所有 70 个。Git 会立即处理它们，直到遇到 Conflict。**这时你再动用 AI。**

#### 1. Start the Batch Process in Terminal

使用包含起始范围的语法开始 Cherry-pick：

```bash
# A 是你范围开始之前的那个 Commit
# B 是你想要包含的最后一个 Commit
git cherry-pick A^..B
```

#### 2. Let the AI Handle the Conflict

如果 Git 因为 Conflict 停止：

1. 打开你的 AI Assistant（Claude Code, Cursor, 或 Copilot）。
2. **Prompt:** "I am in the middle of a batch cherry-pick. Please resolve the conflicts in the current files, ensuring the logic from the cherry-picked commit is preserved while respecting the target branch's existing code."
3. AI 会修复文件。
4. **你进行验证**并运行：

   ```bash
   git add .
   git cherry-pick --continue
   ```

#### 3. Repeat

Git 会自动移动到 70 个 Commit 序列中的下一个。如果它能干净利落地 Apply，Git 就会继续。如果出现另一个 Conflict，重复步骤 2。

---

### Why this is better than "10 at a time"

* **Efficiency:** Git 处理 "Clean" Commits 的速度比 AI Agent 通过聊天界面处理它们要快。
* **Context Preservation:** 通过仅将 AI 用于 Conflict，你可以为实际的代码逻辑节省 Context Tokens，而不是浪费在 Git 能够自动处理的 Commits 上。
* **Linearity:** 它确保你不会在每组 10 个的 Batch 之间意外跳过或重复 Pick Commits。

---

### Comparison of Methods

| Feature | 10-at-a-time (Manual Batch) | Stop-on-Conflict (Hybrid) |
| :--- | :--- | :--- |
| **Speed** | Slow (requires manual intervention every 10) | Fast (only stops when necessary) |
| **Token Usage** | High (AI reads all code for every commit) | Low (AI only reads conflicted files) |
| **Risk of Error** | Moderate (human error in range selection) | Low (Git manages the sequence) |
| **Conflict Quality** | Good (AI has full context of the 10) | **Best** (AI focuses strictly on the diff) |

### Important Tips for 70+ Commits

* **Use a Temporary Branch:** 在开始之前始终创建一个新的 "Migration" Branch。永远不要将 70 个 Commits 直接 Cherry-pick 到你的 Main Production Branch 中。
* **Verify Mid-way:** 每隔 20 个 Commits 左右，运行一次你的 Test Suite。如果 AI 在解决 Conflict 时犯了微妙的逻辑错误，早发现比完成所有 70 个后再发现要容易。
* **Check for Dependencies:** 如果 Commit #50 依赖于 Commit #5 中的更改，但你跳过了 #5，AI 可能会自行生成代码（Hallucinate）来使其“工作”。确保你的范围 `A^..B` 涵盖了所有必要的 Dependencies。
