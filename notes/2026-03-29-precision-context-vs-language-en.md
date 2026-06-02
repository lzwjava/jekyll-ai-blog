---
audio: false
generated: true
image: false
lang: en
layout: post
title: Precision Context Over Natural Language Only
translated: false
type: note
---

Question:
Is it incorrect to call it the “LLM's language”? Is the more accurate idea that prompts should include concrete context (like CSS selectors, HTML, or code) rather than just natural English?

Answer:

Yes — saying **“LLM’s language”** is not accurate. Your corrected understanding is better.

LLMs **do not have a special language**. They accept **any text**:

* English
* Chinese
* code
* HTML
* CSS selectors
* logs
* stack traces
* JSON
* mixed content

What actually matters is **context precision**, not “LLM language”.

Your idea can be expressed more precisely like this:

### Core Idea

LLMs work best when the **prompt contains concrete, machine-level context**, not vague natural language.

Bad prompt (vague):

```
Click that button and extract the text
```

Good prompt (precise context):

```
Click this element:
<button class="btn-primary submit-order" data-testid="checkout-submit">

CSS selector:
button[data-testid="checkout-submit"]

Then extract text from:
<div id="order-confirmation">
```

The second works better because:

* removes ambiguity
* reduces hallucination
* gives exact DOM structure
* matches what the model sees in code

---

### Why English-only prompts are weaker

Natural language:

```
click the blue button on the right
```

Problems:

* multiple blue buttons
* layout may change
* model must guess

But this is deterministic:

```
document.querySelector('#checkout > button.primary')
```

LLM doesn't guess — it executes reasoning directly.

---

### So the real principle

Not “LLM language”, but:

**LLMs prefer structured context over descriptive language**

Best prompt = mix of:

* natural language (intent)
* code (precision)
* selectors (location)
* logs (state)
* errors (feedback)

Example ideal prompt:

```
Goal: click checkout button

HTML:
<button id="checkout-btn" class="primary">

Selector:
#checkout-btn

Error:
Element not clickable at point (532, 410)

What's wrong?
```

This is extremely strong.

---

### Why Copilot / Claude Code work better with copied code

Because they are **context-driven**, not language-driven.

When you paste:

* VSCode code
* DOM HTML
* CSS selectors
* stack trace

You reduce **search space** for the model.

Less guessing → better output.

---

### Your corrected statement (most accurate)

Your improved understanding is correct:

* LLMs don't need special language
* any text works
* but **prompt + context must be self-consistent**
* copying real code/HTML/selectors improves results

This is exactly right.

---

### One-sentence summary

LLMs don't require a special language — they perform best when prompts include **precise, real context (code, selectors, logs)** instead of vague natural language.
