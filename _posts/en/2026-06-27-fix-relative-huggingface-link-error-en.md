---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Relative HuggingFace Link Error
translated: false
type: note
---

I need to see the actual code to figure this out. The 404 is coming from your Cloudflare Worker, not HuggingFace, so the issue is in how the HuggingFace button's link/route is constructed or handled.

Let me check what's actually live.The button itself points to `https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf` — that link is fine and external. The 404 isn't from the button's `href`; it's from HuggingFace returning 404 because **that repo doesn't exist** (or is private/misnamed). Let me confirm.The HuggingFace repo exists and resolves fine (200, full model card). So the 404 is **not** the destination — it's how the link is being rendered/clicked on your page.

Most likely cause: the HuggingFace link in your Worker's HTML is **relative, not absolute**. In the fetched markdown the links render as `[HuggingFace]` with no visible scheme, and your Worker serves everything from the root domain. If the `href` is written as `huggingface.co/lzwjava/...` (missing `https://`), the browser treats it as a **relative path** and resolves it to:

```
https://sec-edgar-gpt.lzwjava.workers.dev/huggingface.co/lzwjava/sec-edgar-gpt-124m-hf
```

— which your Worker has no route for → its own 404 page (the exact "Sorry, we can't find the page" you're seeing).

Fix: make the href absolute. Check your source (HTML or markdown):

```bash
# find the offending link
grep -rn "huggingface" .

# look for href missing the scheme
grep -rn 'href="huggingface' .
grep -rn '](huggingface' .   # markdown form
```

The bad pattern and the fix:

```html
<!-- BAD: relative → resolves under your worker domain → 404 -->
<a href="huggingface.co/lzwjava/sec-edgar-gpt-124m-hf">HuggingFace</a>

<!-- GOOD -->
<a href="https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf">HuggingFace</a>
```

Markdown equivalent:

```markdown
<!-- BAD -->  [HuggingFace](huggingface.co/lzwjava/sec-edgar-gpt-124m-hf)
<!-- GOOD --> [HuggingFace](https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf)
```

Note your GitHub and Paper buttons probably work because they were written with `https://`, and only the HuggingFace one was written bare. To confirm the diagnosis in one shot, open the page and inspect the resolved URL:

```bash
curl -s https://sec-edgar-gpt.lzwjava.workers.dev/ | grep -i huggingface
```

If the `href` comes out without `https://`, that's it. Add the scheme and redeploy (`wrangler deploy`).
