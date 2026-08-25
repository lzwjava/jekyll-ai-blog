---
audio: false
generated: true
image: false
lang: en
layout: post
title: Detecting Illegal Special Characters
translated: false
type: note
---

Question: What illegal characters does the NVIDIA Workday job application form actually detect, and what is the rule behind the error?

Answer: The form is rejecting your "Role Description" text because it contains certain special characters. The error message explicitly lists them:

`< > [ ] " { } \`

Looking at your textarea content, the likely culprits are:

- `"` (straight double quotes) — you used them in phrases like `"AI Full Stack Engineer"` and similar quoted terms
- `<` / `>` — possible if any markdown-style tags slipped in
- `\` — possible in path-style references

The detection rule is a simple **character blocklist** — a server-side or client-side validation that scans the raw text for any occurrence of those eight characters, regardless of context. It is not about HTML injection or SQL injection specifically; it is a broad sanitization filter that Workday applies to free-text fields to prevent potential XSS (cross-site scripting) or template injection attacks. Even one occurrence of any listed character anywhere in the field triggers the error.

**How to fix it:**

Replace the offending characters with safe alternatives:

| Original | Replacement |
|----------|-------------|
| `"quoted term"` | use single quotes `'` or remove quotes |
| `<` / `>` | spell out "less than" / "greater than", or just remove |
| `[link]` or `[text]` | remove brackets |
| `\path\file` | use `/` instead |

Since your description uses `"AI Full Stack Engineer"` and similar double-quoted phrases, simply switching to single quotes or removing the quotes entirely should clear the error.

References:
- [NVIDIA Careers - Job Posting](https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/Senior-Platform-AI-Engineer---Silicon-Co-Design-Group_JR2016323)
