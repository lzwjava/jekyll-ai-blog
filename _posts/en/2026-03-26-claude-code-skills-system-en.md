---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding the Claude Code Skills System
translated: false
type: note
---

Question: How do skills in Claude Code work? Are they markdown files, scripts using the Claude API, or created via tool calls?

Answer:

Claude Code’s skills system is essentially a structured way to extend the AI with custom behavior. Here’s how it works in practice:

1. **Skill Definition Format**

   * Skills are usually stored as **YAML or JSON-like configuration files**, not plain markdown.
   * Each skill defines **triggers**, **inputs**, **actions**, and **responses**.
   * Some documentation or explanation may be provided in markdown, but the skill logic itself is machine-readable data.

2. **Custom Script Integration**

   * Skills can include **custom scripts or prompts** that the Claude model executes.
   * These scripts are often small templates of instructions, allowing dynamic computation or conditional responses.
   * Essentially, the skill is a way to wrap a Claude API call with specific behavior and context.

3. **Tool Calls / Function Hooks**

   * Skills can invoke **tool calls**, which are integrations with external services, APIs, or local functions.
   * For example, a skill could fetch data from a database, perform calculations, or call a third-party API, then feed the result back to Claude for further processing.

4. **Execution Flow**

   * When a user activates a skill, Claude reads the skill definition, determines which part applies, optionally calls any tools/scripts, and then generates a response.
   * This allows skills to combine **static instructions**, **dynamic scripts**, and **external actions** into a seamless experience.

**Summary:**
Skills are not just markdown or plain scripts—they are structured configurations that can include prompt templates, callable scripts, and tool integrations. They act as modular “plugins” for Claude, letting you extend its behavior in specific ways.

References:

* [Claude by Anthropic Documentation](https://www.anthropic.com/)
* [Claude Code GitHub](https://github.com/obra/superpowers) (for community examples and skill structure)
