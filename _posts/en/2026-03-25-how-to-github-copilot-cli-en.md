---
audio: false
generated: true
image: false
lang: en
layout: post
title: How to Use GitHub Copilot CLI
translated: false
type: note
---

Question: How do I use the `% copilot` CLI interface shown to perform tasks and get answers?

Answer:

The `% copilot` CLI you’re seeing is an interactive interface for **GitHub Copilot CLI**. Here’s how it works and how to use it effectively:

---

### 1. Starting the CLI

* You launch it with `% copilot` (or `copilot` if installed globally).
* You will see the welcome screen, like in your screenshot.

---

### 2. Basic Workflow

* The CLI works **like a prompt-based AI assistant**.
* You type a **task or question** in natural language.
* Copilot will generate suggestions, code snippets, or answers.

**Example:**

```bash
% copilot
> Create a Python function to reverse a string
```

Copilot will generate a code snippet for you.

---

### 3. Commands and Tips

* `/usage` — shows your current session usage metrics and statistics.
* `/exit` — exits the CLI.
* You can also try commands like `/help` to see other built-in options.

---

### 4. How to Search for Answers

Since it’s a text-based interface:

1. Type a **clear, concise question** or task description.

   * Example: `Search how to read a JSON file in Python`
2. Copilot will generate either:

   * A code snippet
   * Instructions
   * Relevant examples

---

### 5. Safety and Verification

* Copilot suggestions **may contain mistakes**, so always verify generated code or instructions.
* It’s best used as a **starter for tasks**, not final production code.

---

### 6. Example Session

```bash
% copilot
> Create a bash script to backup a folder
# Copilot will suggest a script

> /usage
# Shows session metrics

> /exit
# Exits the CLI
```

---

If you want, I can make a **short cheat sheet for the Copilot CLI**, showing all commands and practical examples for coding, search, and task automation.

Do you want me to do that?
