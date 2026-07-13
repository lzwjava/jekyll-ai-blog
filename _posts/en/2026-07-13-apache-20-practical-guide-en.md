---
audio: false
generated: true
image: false
lang: en
layout: post
title: Apache 2.0 Practical Guide
translated: false
type: note
---

Question: What does the Apache License 2.0 mean in practice?

Answer: Standard permissive OSS license. Key mechanics:

**You can:**

- Use, modify, distribute, sublicense — commercially or privately, no restrictions on your own code that merely links to it.
- Keep your own license on your modifications (dual-licensing your changes is fine).

**You must:**

- Include a copy of the license with any distribution.
- Mark changed files as modified (a comment header noting you changed it is enough).
- Preserve existing copyright/attribution notices from the original source.
- If a `NOTICE` file exists in the original, carry its contents forward in your distribution (file, docs, or UI credits — your choice where).

**Patent grant (the part that differs from MIT):**
Each contributor grants you a patent license covering their contributions. But if you sue anyone claiming the Work infringes your patent, your patent license from this project terminates immediately. This is the defensive clause — protects the project from patent trolls emerging from within the contributor base.

**No warranty, no liability** — standard AS-IS, no support obligation on the licensor.

**What it does NOT require:**

- No requirement to open-source your own derivative work (unlike GPL) — you can build closed-source products on top of Apache-2.0 code.
- No "copyleft" — you don't have to release your changes to the public, just mark that you changed the files if you redistribute them.

For your stack (ww/iclaw/zz, model training scripts): if you pull in an Apache-2.0 dependency and ship a binary/CLI, you just need to bundle the LICENSE file and preserve NOTICE if one exists. No obligation to open your own agent code.

References:

- [Apache License 2.0 full text](https://www.apache.org/licenses/LICENSE-2.0)
- [Apache 2.0 vs MIT vs GPL comparison](https://choosealicense.com/licenses/apache-2.0/)
