---
audio: false
generated: true
image: false
lang: en
layout: post
title: How to Find Your Hugging Face Registration Date
translated: false
type: note
---

The public profile page doesn't display registration date directly. Here are your options:

**1. Account Settings (easiest)**
Log into HF, go to Settings → Account. Registration/join date should be listed there.

**2. From what we can see publicly:**
Your activity page shows earliest recorded action is "liked 12 models over 1 year ago"—so you registered **at least 1+ year ago** (sometime before May 2025). But that's a lower bound, not exact.

**3. HF API (if you want to script it)**
```bash
curl https://huggingface.co/api/users/lzwjava
```
This returns JSON with account metadata including `createdAt` timestamp.

**4. Check model timestamps**
If you had any older models, their creation dates would give clues. But you only have `zz` which is brand new.

The Settings page is fastest—just click your avatar → Settings on HF directly.