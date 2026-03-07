---
audio: false
generated: true
image: false
lang: en
layout: post
title: X Translation Skips Quoted Posts
translated: false
type: note
---

**Question:** On Twitter/X, I have automatic translation set from Chinese to English. When someone reposts a Chinese post, the repost's added words are shown in English — that's fine — but the original quoted/embedded post still appears in Chinese. Why does this happen, and how can I fix it?

---

**Answer:**

This is a **known limitation** of how X (Twitter) handles translation in the context of reposts and quote posts. Here's a clear breakdown of what's happening and what you can do about it.

---

## Why This Happens

When someone reposts (or quote-tweets) a Chinese post, there are actually **two separate text blocks** rendered on screen:

1. **The reposter's own comment** — this is a "new" post written by the person reposting, so X's auto-translation engine processes it normally and translates it into English.
2. **The embedded original post** — this is a separate, nested post object. X's translation system **does not always automatically translate embedded/quoted posts**, even if auto-translation is enabled. The original post is treated as a referenced card, not a fresh piece of content in your feed.

This is essentially a **design gap** in X's translation feature — the auto-translation applies to top-level feed posts, but the embedded quoted content can slip through untranslated.

---

## What You Can Do

### Option 1: Manually Translate the Original Post
Click on the original post's date/time link to jump directly to it. Because you're now viewing it as a standalone post, X will show a **"Translate post"** link directly on it — click that to get the translation.

### Option 2: Use Grok Auto-Translation (if available to you)
X has rolled out a feature using Grok AI to automatically translate posts in your feed. When a post is translated, you'll see the text "Translated by Grok – Show original" at the top of the tweet. If this is active on your account, it may also translate embedded posts more reliably than the older system.

### Option 3: Use Your Browser's Built-in Translation
If you use Microsoft Edge or Chrome, you can drag to select the Chinese text, right-click, and choose "Translate Selection to English" — the browser's built-in translation (powered by Google Gemini or similar) can handle text that X's own system misses.

### Option 4: Use a Browser Extension
Extensions like "Post Translator for Twitter X" can automatically detect the original language and translate text directly below it without disrupting the page layout, covering content that X's native translation might skip — including embedded quoted posts.

---

## Summary

| Content Type | Auto-Translated? |
|---|---|
| Reposter's own comment | ✅ Yes (usually) |
| Embedded original Chinese post | ❌ Often skipped |

This is a platform-level limitation. Until X improves translation coverage for nested/quoted posts, **clicking through to the original post** or **using a browser extension** are your most reliable solutions.

---

**References:**

- [Ask Dave Taylor – How to Translate Posts on X](https://www.askdavetaylor.com/how-to-translate-foreign-language-posts-on-twitter-x/)
- [Croma – How to Turn Off X's Grok Auto-Translations](https://www.croma.com/unboxed/how-to-turn-off-x-grok-translations)
- [Chrome Web Store – Post Translator for Twitter X](https://chromewebstore.google.com/detail/post-translator-for-twitt/pbmchlbpmommkfpafninfdcjheapdkfi)