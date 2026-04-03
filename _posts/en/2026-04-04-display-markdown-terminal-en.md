---
audio: false
generated: true
image: false
lang: en
layout: post
title: Display Markdown in Terminal
translated: false
type: note
---

Question: How do I properly display Markdown-formatted AI responses (e.g., `**bold**`, `- list`) in a terminal CLI tool? Can I also use a system prompt to tell the LLM to stop using Markdown syntax?

Answer:

You have **two main approaches** — render the Markdown beautifully in the terminal, or suppress it at the source via a system prompt. Here's a full breakdown of both.

---

## Approach 1: Render Markdown in the Terminal

The best Python library for this is **Rich**. Rich can render Markdown and does a reasonable job of translating formatting to the terminal — including headings, bold, italic, lists, and code blocks with full syntax highlighting.

### Install Rich

```bash
pip install rich
```

### Render an LLM response as Markdown

```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()

# Suppose this is your LLM response string
llm_response = """
# Summary

Here are the key points:

- **Point one**: Very important
- **Point two**: Also important

```python
print("Hello World")
```
"""

md = Markdown(llm_response)
console.print(md)
```

You can also use the Markdown class directly from the command line — for example: `python -m rich.markdown README.md`

### Pipe LLM output into `rich-cli`

If you are using a CLI tool that pipes output, you can pipe output from another process: `cat response.md | rich - --markdown --force-terminal`

---

## Approach 2: Strip Markdown via a System Prompt

Yes, you absolutely can instruct the LLM to respond in plain text without any Markdown syntax. This is a very common and effective solution.

### Effective system prompt wording

```
You are a helpful assistant running inside a terminal CLI tool.
Do NOT use any Markdown formatting in your responses.
No bold (**text**), no italics (*text*), no headers (# text),
no bullet dashes, no backtick code fences.
Respond in plain text only.
```

### Why this approach works (with caveats)

Many developers face this exact issue — LLMs tend to default to Markdown formatting. Techniques like placing "deliver the response in plain text with no formatting" at the beginning of the system prompt can help, but results vary.

Recently, in the "o" series models, OpenAI introduced a default setting that prevents generating responses with Markdown formatting, explicitly requiring a "Formatting re-enabled" instruction to re-enable this behavior.

A strong, explicit system prompt example that works well in practice (from real-world usage):

```
You will be given questions by the user.
Respond in plain text only — no markdown, no fenced code blocks, no bullet dashes, no bold or italic syntax.
Your output will be printed directly to a terminal.
```

---

## Approach 3: Strip Markdown Programmatically (Fallback)

If the LLM still occasionally leaks Markdown syntax, you can strip it using a library like `markdownify` or a simple regex cleaner:

```python
import re

def strip_markdown(text: str) -> str:
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)   # bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)         # italic
    text = re.sub(r'#{1,6}\s?', '', text)            # headers
    text = re.sub(r'`{1,3}.*?`{1,3}', '', text, flags=re.DOTALL)  # code
    text = re.sub(r'^\s*[-*]\s+', '', text, flags=re.MULTILINE)    # bullets
    return text.strip()
```

---

## Summary — Which Approach to Use?

| Approach | Best For |
|---|---|
| **Rich (render Markdown)** | You want nicely formatted terminal output with colors and structure |
| **System prompt (suppress Markdown)** | You want raw plain text, no decoration |
| **Programmatic stripping** | As a safety fallback if system prompt isn't 100% reliable |

The most robust solution for a CLI tool is to **combine both**: use a system prompt to minimize Markdown output, and use `rich` to render whatever structured text still comes through.

References:

- [Rich Markdown Docs](https://rich.readthedocs.io/en/latest/markdown.html)
- [Rich on GitHub](https://github.com/Textualize/rich)
- [Rich-CLI on GitHub](https://github.com/Textualize/rich-cli)
- [OpenAI Community — Preventing Markdown Output](https://community.openai.com/t/how-to-prevent-gpt-from-outputting-responses-in-markdown-format/961314)