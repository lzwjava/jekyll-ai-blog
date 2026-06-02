---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Coding Requires Human Iteration Always
translated: false
type: note
---

Question:
Why do people still need to manually intervene when using tools like Copilot or Claude Code, especially when they often do not know the exact desired result beforehand and only discover acceptable outcomes during the building process?

Answer:

Yes, your observation is fundamentally correct. One major reason manual intervention is still necessary when using AI coding assistants such as GitHub Copilot or Claude Code is that **software development frequently involves discovering the requirements during the process rather than defining them perfectly in advance**.

This phenomenon appears in several important aspects of software engineering.

### 1. Requirements Are Often Unknown or Incomplete

In many real-world projects, developers cannot fully describe what they want at the beginning. Instead, they only have a **rough intention**.

For example:

* “Build a search feature”
* “Make the UI feel smoother”
* “Improve performance”

These goals are **ambiguous and evolving**. The precise implementation only becomes clear after experimentation.

This is sometimes called **emergent design**, where the final design emerges gradually through iteration.

### 2. Acceptance Criteria Are Discovered Through Building

When developers build a feature, they often discover constraints that were not obvious before:

* Performance limitations
* Unexpected edge cases
* Integration issues
* Usability problems

For instance, you might initially want a complex architecture, but after implementing it you realize:

* It is too slow
* It is too complex
* It is difficult to maintain

At that point, you refine the requirements. This is why **coding and thinking are tightly coupled activities**.

### 3. Many Qualities Are Hard to Describe in Natural Language

Certain aspects of software quality are difficult to specify beforehand, such as:

* Code elegance
* Simplicity
* Maintainability
* Architectural clarity

These qualities are often recognized **only when developers see the code or run the system**.

So even if AI generates code, humans still need to evaluate:

* Does this design feel right?
* Is it maintainable?
* Does it match the mental model of the system?

### 4. Software Development Is an Iterative Exploration

Modern development methodologies like Agile assume that **knowledge emerges during development**.

Typical workflow:

1. Idea
2. Prototype
3. Observe limitations
4. Refine design
5. Rebuild
6. Repeat

AI tools accelerate steps 2–5, but **they do not eliminate the exploration process**.

### 5. Humans Provide Judgment and Context

AI can generate solutions, but humans still provide:

* Product intuition
* Architectural judgment
* Trade-off decisions
* Domain understanding

For example, AI might generate working code, but a developer might decide:

* This abstraction is wrong
* This dependency should not exist
* This feature should be simplified

These judgments require **experience and contextual awareness**, which AI currently cannot fully replicate.

### 6. Programming Is Often a Process of Discovering the Problem

A famous idea in software engineering is:

> “We don't really understand the problem until we try to solve it.”

Developers often only understand:

* the real requirements
* the system limits
* the correct architecture

**after writing and testing code**.

### Conclusion

Manual intervention remains essential with AI coding tools because:

1. Requirements are often unclear at the start.
2. Acceptable results are discovered through experimentation.
3. Many software qualities are hard to describe explicitly.
4. Development is an iterative exploration process.
5. Human judgment and system understanding are still necessary.

AI assistants such as GitHub Copilot and Claude Code significantly speed up coding, but they **do not replace the exploratory nature of software design**. Instead, they function more like extremely fast collaborators that still require human guidance and evaluation.
