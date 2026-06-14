---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why My AI Hallucinated About Zhiwei Li
translated: false
type: note
---

Now I see the full picture. Here's the analysis:

---

**Why the model got it completely wrong:**

**1. The REAL data about 李智维 exists in your blog — but it's NOT a biography.**

Your blog posts about Zhiwei Li are:

- "AI Engineer Titles for Zhiwei Li" — bio line polishing
- "李智维的未来生活路线图" — career roadmap advice
- "打造更佳个人简介" — bio writing tips
- "为新加坡人脉添加客家话至领英" — LinkedIn Hakka strategy

These are all Q&A-style career coaching posts. The actual facts scattered across them:

- AI engineer, exploring code/life/LLMs
- Works at TEKsystems/HSBC
- ~13/18 courses done for associate degree
- IELTS 6.5, Hakka speaker
- GitHub: lzwjava, blog: lzwjava.github.io
- Used ~1B tokens of Claude Code, trained nanoGPT on H200

**2. The model never learned "Who is Zhiwei Li?" as a question.**

Your training format is title→body:

```
user: "AI Engineer Titles for Zhiwei Li"
assistant: <the full blog post about polishing bio lines>
```

The model learned: given a blog TITLE, generate the blog BODY. It never learned to answer direct biographical questions like "李智维是谁?".

**3. So it hallucinated from base model knowledge.**

Qwen3-4B's pre-training data contains lots of Chinese internet content. "李智维" is a real name that maps to multiple people. The model confidently confabulated a completely fictional biography (编程教育公司创始人, born 1992, 营口市) by pattern-matching on the name from its base knowledge — none of which came from your fine-tuning data.

**4. The hallucinated references are also fake.**

The URLs it cited (知乎, 王垠's blog, 36kr, Wikipedia) look plausible but the model invented the connection. This is classic LLM hallucination behavior when the fine-tuned data doesn't cover the question format.

---

**Root cause:** SFT on title→body pairs teaches the model to generate blog content from titles. It does NOT teach it to answer factual questions about people mentioned in the blog. The model falls back to base model knowledge when the question format doesn't match training distribution.

**Possible fixes:**

- Add actual Q&A pairs about biographical facts to the training data
- Use chat-format SFT with system prompts like "You are Zhiwei Li's personal AI assistant"
- Add a "Who is X?" → factual answer training format alongside the title→body format
