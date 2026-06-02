---
audio: false
generated: true
image: false
lang: en
layout: post
title: Continuous AI Meeting Context for Coding
translated: false
type: note
---

Question:

Is one way to get a precise and comprehensive Zoom AI companion to have it summarize every 3–5 minutes, store all responses in a single Markdown file, and feed that along with background information (like shared Excel sheets or documents) to Copilot or Claude for code refinement?

Answer:

Yes, that approach is both practical and effective for creating a precise, context-aware AI companion during meetings or coding sessions. Here's a breakdown of how it works and why it’s effective:

1. **Frequent Summarization**

   * Capturing summaries every 3–5 minutes ensures the AI keeps up with the conversation without missing key points.
   * Summaries are easier to store, process, and feed into other AI systems than raw transcript logs.

2. **Centralized Markdown File**

   * Storing all summaries in one Markdown file creates a single, structured source of truth.
   * Markdown supports headings, code blocks, tables, and links, making it ideal for both human review and AI ingestion.

3. **Feeding Background Information**

   * Including external data (Excel sheets, documents, slides) gives the AI relevant context beyond the conversation.
   * You can include links or copy content into the Markdown for Copilot/Claude to reference when generating or refining code.

4. **Code Refinement via AI**

   * By providing up-to-date summaries plus contextual documents, Copilot or Claude can produce code that reflects the latest discussion, decisions, and data.
   * This reduces errors, avoids duplicated work, and keeps outputs aligned with the meeting’s intent.

5. **Implementation Tips**

   * Automate summary capture with Zoom transcription + AI summarization scripts.
   * Use consistent headings/tags in Markdown to make sections easy to parse.
   * Feed the Markdown periodically to Copilot/Claude rather than continuously streaming raw conversation.
   * Optionally, highlight action items or code snippets separately to focus AI refinement.

This method essentially creates a “living document” of the meeting that serves as both a memory and an actionable input for AI code assistants.

It’s a scalable way to get AI companions to not only track discussions but actively improve work outputs in real time.

References:

* [Zoom AI Companion Overview](https://zoom.us/features/ai)
* [Markdown for Knowledge Management](https://www.markdownguide.org/extended-syntax/)
* [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
* [Claude AI for Summarization](https://www.anthropic.com/claude)
