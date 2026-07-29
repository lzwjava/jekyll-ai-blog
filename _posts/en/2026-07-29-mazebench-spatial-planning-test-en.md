---
audio: false
generated: true
image: false
lang: en
layout: post
title: MazeBench Spatial Planning Test
translated: false
type: note
---

Question: What is MazeBench and what does the MazeBench results page measure?

Answer:

**MazeBench** is an evaluation benchmark designed to test whether multimodal LLMs actually understand **spatial planning** from maze images, rather than just doing pattern matching or converting the image into text and brute-forcing a solution. ([arXiv][1])

The core idea:

```
Image of maze
      |
      v
 Vision model
      |
      v
 Internal representation?
      |
      v
 Planning / navigation
      |
      v
 Correct path
```

Humans see a maze and build a mental map:

```
start
 |
 +---+
     |
     +---- goal
```

But many LLMs appear to do something different:

```
maze image
    |
    v
"convert pixels into grid"
    |
    v
"try paths step by step"
    |
    v
token-level BFS
```

The paper behind MazeBench argues that high accuracy can be misleading because models often solve mazes by **textual enumeration/search**, not by human-like spatial reasoning. ([arXiv][1])

---

## What does it test?

Typical tasks:

1. Give the model a maze image.
2. Ask:

> Find the path from start to finish.

The benchmark varies:

* maze size
* difficulty
* visual complexity
* reasoning budget
* whether the model is allowed to use intermediate representations

The reported benchmark used **110 procedurally generated maze images** and evaluated **16 multimodal model configurations**. ([arXiv][1])

---

## Interesting result

A surprising observation:

A model can score high but still fail at the underlying capability.

Example:

```
Human:
  sees maze
  creates mental graph
  finds shortest path

LLM:
  image -> text grid
  A1 B1 C1...
  enumerate possibilities
  output answer
```

The benchmark found that some models consumed thousands of tokens solving mazes that humans solve almost instantly. ([arXiv][1])

When the correct grid representation is already provided, performance jumps significantly, suggesting part of the problem is **visual grounding**, not pure reasoning. ([arXiv][1])

---

## Why this matters for agents

This connects directly to current agent research.

A coding agent, browser agent, robotics agent, etc. needs:

```
observe
   |
   v
maintain world state
   |
   v
plan
   |
   v
act
   |
   v
observe again
```

MazeBench exposes a weakness:

Current LLMs are excellent at:

```
context -> next token
```

but weaker at:

```
environment -> persistent world model -> action
```

This is similar to the "world model" problem discussed in other maze-agent benchmarks: agents need internal state tracking rather than only responding from the current context window. ([arXiv][2])

---

## Relation to your vLLM / nanoGPT experiments

This is actually a very good benchmark to understand transformer limits.

nanoGPT:

```
tokens
 |
 Transformer
 |
 next token probability
```

MazeBench asks:

```
pixels
 |
 representation
 |
 memory
 |
 planning
 |
 action sequence
```

The missing pieces are not only bigger models:

* external memory
* state representation
* search
* tool usage
* recurrent loops

This is why modern agent systems look like:

```
LLM
 +
memory
 +
tools
 +
planner
 +
environment feedback
```

rather than just:

```
GPT(prompt) -> answer
```

For someone building agents (Hermes-style loops, coding agents, tool-use systems), MazeBench is closer to the real problem than traditional MMLU-style benchmarks. ([arXiv][2])

References:

* ([arXiv][1])
* ([arXiv][2])
* ([Hugging Face][3])

[1]: https://arxiv.org/abs/2603.26839?utm_source=chatgpt.com "From Pixels to BFS: High Maze Accuracy Does Not Imply Visual Planning"
[2]: https://arxiv.org/abs/2607.00627?utm_source=chatgpt.com "AGI Maze as a Benchmark Framework for World-Modeling Agents"
[3]: https://huggingface.co/papers/2603.26839?utm_source=chatgpt.com "Paper page - From Pixels to BFS: High Maze Accuracy Does Not Imply Visual Planning"
