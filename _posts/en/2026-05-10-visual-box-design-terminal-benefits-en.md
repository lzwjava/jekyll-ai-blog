---
audio: false
generated: true
image: false
lang: en
layout: post
title: Visual Box Design Benefits in Terminals
translated: false
type: note
---

Question: What is Hermes, and is its use of colorful rectangles/boxes to visually separate parts of messages a good UI design approach?

Answer:

## What is Hermes?

**Hermes** is an AI-powered terminal/CLI assistant (similar to Claude Code) that uses a rich terminal UI to display its responses and actions. It appears to be a coding/devops agent that can execute shell commands, clone repos, manage files, etc.

---

## The Colorful Box/Panel Design — Is It Good?

Yes, this is generally considered **good terminal UI design**. Here's why:

### ✅ Benefits of Visual Separation with Boxes

**1. Cognitive chunking**

- Boxes group related content together, making it easier for your brain to process each "unit" of information separately.
- e.g., the agent's *reasoning* is clearly separated from *command output*.

**2. Scanability**

- Users can quickly scan and find the part they care about (the error, the command, the explanation) without reading everything linearly.

**3. Role clarity**

- Different box styles (e.g., `⚕ Hermes` vs `💻 $`) instantly signal *who is speaking* — the AI, the shell, or the system.

**4. Error/status visibility**

- Errors like `[error]` stand out clearly in their own visual block rather than being buried in a wall of text.

**5. Aesthetic professionalism**

- Rich terminal UIs using boxes (like those from libraries such as `rich`, `blessed`, `bubbletea`) feel polished and modern compared to plain stdout text.

---

### ⚠️ Potential Downsides

| Issue | Detail |
| --- | --- |
| **Log noise** | If you pipe or log output, box characters become ugly unicode garbage |
| **Narrow terminals** | Boxes can wrap badly on small terminal widths |
| **Screen reader unfriendly** | ASCII box-drawing chars can be inaccessible |
| **Over-separation** | Too many boxes for tiny pieces of info can feel cluttered |

---

### 🔧 Libraries That Power This Style

Tools like Hermes likely use one of:

- **Python**: `rich` (most popular), `textual`
- **Go**: `bubbletea` + `lipgloss`
- **Node.js**: `ink`, `blessed`
- **Rust**: `ratatui`

---

## Verdict

For an **interactive terminal agent**, colorful boxed panels are an excellent design choice — they make the tool feel intentional, legible, and professional. The key is **restraint**: not every line needs a box, only logical sections that benefit from visual grouping.
