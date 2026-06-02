---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Optimizing Grok Custom Instructions for GitHub
translated: false
type: note
---

### Prompt

how about I add this in grok custom instruction? is it smart trick? I want to review it back , and copy to my git hub repo save answer

Do not return Grok render tags. Markdown is fine. If have references, just place at the end with [title](url) format. Don't have [1] [2] in the main text.

### Answer

Yes, it’s a very smart and practical trick!

Putting those exact lines (or an expanded version of them) into your Grok custom instructions is one of the best ways to make Grok’s answers consistently clean, readable, and easy to archive. Here’s why it works so well:

- It forces every single response to follow the format you want without you having to remind Grok each time.
- No more annoying tags or [1][2][3] footnotes that break when you paste into Markdown files, Obsidian, Notion, or GitHub repos.
- References stay neatly at the end in clean Markdown link style, perfect for version control.
- You keep full control over output style even when Grok updates or changes default rendering.

Many power users (including people who maintain big knowledge bases or second-brain repos on GitHub) already do exactly this. It saves a ton of post-processing time.

Recommended full version you can copy-paste into your custom instructions right now:

```
Always use clean Markdown formatting. Never use Grok render tags like <grok:render ...>. For citations/references, only use inline-style Markdown links or place them at the very end in [title](url) format. Never use [1], [2], footnote superscripts, or numbered reference lists in the body. When the user asks to show the prompt, use this exact header format:

### Prompt
[repeater the original user message]

### Answer
[your response]
```

This way every answer you get is instantly ready to commit to your GitHub repo without any cleanup. Totally worth it!
