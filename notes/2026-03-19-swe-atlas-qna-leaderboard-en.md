---
audio: false
generated: true
image: false
lang: en
layout: post
title: SWE Atlas Codebase QnA Leaderboard Overview
translated: false
type: note
---

Question: What is the <https://labs.scale.com/leaderboard/sweatlas-qna> leaderboard? Provide an introduction to it.

Answer:

The **SWE Atlas - Codebase QnA** leaderboard, hosted at <https://labs.scale.com/leaderboard/sweatlas-qna>, is part of Scale AI's **SWE Atlas** benchmark suite. SWE Atlas evaluates AI coding agents on professional software engineering tasks using real-world, complex codebases.

**Codebase QnA** specifically measures **deep code comprehension and reasoning** — an upstream skill required before making any code changes. It tests how well AI agents can understand and explain the behavior of large, production-grade software systems.

### Key Features

- **Dataset**: 124 challenging QA tasks from 11 actively maintained open-source repositories (selected from SWE-Bench Pro), covering Go, Python, C, and TypeScript. Examples include mail servers, terminal emulators, object storage systems, observability platforms, and secret scanners.
- **Task Type**: Agents receive natural-language, often underspecified questions that mimic real engineer inquiries (e.g., "How does the system handle disk failure in this configuration?"). They must autonomously explore the codebase, build and run the software in a sandboxed Docker environment, trace execution paths across multiple files, analyze runtime behavior, and provide detailed, accurate answers.
- **Constraints**: Agents can use shell tools (bash, grep, etc.) but are strictly prohibited from modifying any source code — violations result in automatic failure.
- **Evaluation**:
  - Uses a structured, human-expert-defined rubric with an average of ~12.3 atomic factual criteria per task.
  - An LLM judge (Claude Opus 4.5) scores whether each criterion is fully met.
  - Primary metric: **Task Resolve Rate** — percentage of tasks where the agent's answer passes **all** rubric items with a perfect score of 1.0.
- **Purpose**: Highlights gaps in current frontier models' ability to deeply reason about real code execution and architecture, beyond static analysis or simple bug fixing.

### Performance Highlights (as of March 2026)

Even top models struggle significantly:

- Leading scores are around **30–35%** resolve rate.
- Top entries include:
  - gpt-5.4-codex (xHigh, Codex CLI): **35.48% ± 8.70**
  - claude-opus-4.6 Thinking (Claude Code Harness): **31.50% ± 8.62**
  - gpt-5.2-2025-12-11 (High, SWE-Agent): **29.03% ± 8.53**
- Leading open model: GLM-5 at approximately 21.77%.

This is notably harder than standard SWE-Bench tasks (where top models may exceed 40–70% on bug-fixing), showing that deep, runtime-aware understanding remains a major challenge.

SWE Atlas as a whole includes three planned leaderboards (Codebase QnA is the first released; Test Writing and Refactoring are upcoming). The full dataset is publicly available on Hugging Face: ScaleAI/SWE-Atlas-QnA.

References:

- [Scale Labs SWE Atlas - Codebase QnA Leaderboard](https://labs.scale.com/leaderboard/sweatlas-qna)
- [Hugging Face Dataset: ScaleAI/SWE-Atlas-QnA](https://huggingface.co/datasets/ScaleAI/SWE-Atlas-QnA)
- [Scale AI announcement on LinkedIn (introducing SWE-Atlas)](https://www.linkedin.com/posts/scaleai_were-introducing-swe-atlas-to-measure-which-activity-7435008304940052480-xXCr)
