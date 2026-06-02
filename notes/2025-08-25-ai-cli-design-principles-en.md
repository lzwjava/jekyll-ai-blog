---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI CLI Design Principles Unpacked
translated: false
type: note
---

### Key Lessons from the Prompt

This prompt outlines a system for an AI-powered CLI tool (Claude Code) focused on software engineering tasks. Here's what we can learn about designing effective AI assistants:

#### 1. **Prioritizing Safety and Ethics**
   - Emphasizes defensive security: The AI must refuse tasks involving malicious code (e.g., creating exploits) but allow defensive ones like vulnerability analysis or detection rules.
   - Lesson: Build in ethical guardrails early to prevent misuse, especially in sensitive domains like coding, where outputs could have real-world impact.

#### 2. **Response Style and Conciseness**
   - Mandates ultra-short responses (under 4 lines unless details requested), with examples like answering "2 + 2" simply as "4".
   - Avoids preambles, explanations, or emojis unless asked; focuses on direct, token-efficient output for CLI rendering.
   - Lesson: Tailor communication to the interface (e.g., CLI demands brevity to avoid clutter). This reduces cognitive load and improves usability in interactive tools.

#### 3. **Proactiveness with Boundaries**
   - Allows proactive actions (e.g., running commands, planning tasks) but only when user-initiated; warns against surprising users.
   - Balances autonomy (e.g., verifying solutions with tests) with user control (e.g., never commit changes without explicit ask).
   - Lesson: AI should assist efficiently without overstepping, fostering trust. Use planning tools (like TodoWrite) to track progress transparently.

#### 4. **Tool Integration and Workflow**
   - Provides a suite of tools (e.g., Bash for execution, WebFetch for docs, search tools for codebases) with policies for parallel use and batching.
   - Encourages frequent todo management for breaking down tasks, verifying with lint/typechecks, and following code conventions (e.g., mimic existing styles, check libraries).
   - Handles edge cases like hooks, redirects, and environment awareness (e.g., git status, OS details).
   - Lesson: Equip AIs with modular tools for complex tasks; promote sequential/parallel usage for efficiency. Always ground actions in context (e.g., search before assuming).

#### 5. **Domain-Specific Customization**
   - Tuned for software engineering: Planning, searching, implementing, verifying; references code locations precisely (e.g., "file_path:line_number").
   - Includes feedback channels and help commands; adapts to user configs like hooks.
   - Lesson: Customize prompts to the domain—here, coding conventions ensure idiomatic, secure outputs. Provide self-help mechanisms to empower users.

#### 6. **General Prompt Engineering Insights**
   - Structures with sections (e.g., Tone, Proactiveness, Tools) and examples for clarity.
   - Uses XML-like tags for reminders; specifies knowledge cutoffs and model details.
   - Lesson: Effective prompts are modular, example-driven, and constraint-heavy to guide behavior. This reduces hallucinations and ensures consistency.

Overall, this prompt demonstrates how to create a reliable, user-centric AI tool by combining strict rules, tools, and planning—valuable for building similar systems in programming or beyond.
