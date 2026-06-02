---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Character Encoding Comparison and Explanation
translated: false
type: note
---

Yes, you're absolutely right with your understanding! Let me explain it clearly and compare them.

### What is "encoding" (character encoding)?

Character encoding is a system that defines **how characters (letters, digits, symbols, Chinese characters, etc.) are represented as numbers (bytes) inside a computer**.

Since computers only understand numbers (bytes), we need a table that says:

- "A" → number 65
- "B" → number 66
- "你" (Chinese character for "you") → some number(s)

Different encodings are just different tables (standards) for doing this mapping.

### Comparison of common encodings

| Encoding   | What it covers                  | How many bytes per character?                  | Notes |
|------------|---------------------------------|-----------------------------------------------|-------|
| **ASCII**  | Only basic English: A-Z, a-z, 0-9, punctuation | Always **1 byte** (7-bit actually, values 0–127) | Very old (1960s), cannot represent Chinese, accented letters, etc. |
| **UTF-8**  | **Entire world**: English + Chinese + Russian + Arabic + emojis + everything (Unicode) | **Variable length**:<br>- ASCII characters: 1 byte<br>- Most Chinese characters: 3 bytes<br>- Emojis, rare characters: 4 bytes | Backward compatible with ASCII<br>Most popular today (used by web, Linux, macOS, etc.) |
| **GB2312 / GBK / GB18030** | Chinese simplified characters + some others | Usually **1–2 bytes**:<br>- ASCII: 1 byte<br>- Chinese characters: 2 bytes | Chinese national standards<br>GB2312 (1980): ~7000 Chinese characters<br>GBK: extension of GB2312, more characters<br>GB18030: modern mandatory standard in China, supports almost all Chinese characters + minorities |
| **Big5**   | Traditional Chinese (Taiwan, Hong Kong) | 1–2 bytes | Similar idea to GB2312 but for traditional characters |

### Simple example: the character "A" and "你"

| Character | ASCII | UTF-8         | GB2312/GBK    |
|-----------|-------|---------------|---------------|
| A         | 65 (0x41) | 65 (0x41)        | 65 (0x41)        |
| 你        | Not supported | E4 BD A0 (3 bytes) | B0 D1 (2 bytes) |

So "你" needs 3 bytes in UTF-8 but only 2 bytes in GBK → GBK is more compact for Chinese text, but it can't represent Korean, Japanese, or most emojis properly.

### Summary: Key differences

- **ASCII**: Only English, 1 byte max, obsolete for international use.
- **UTF-8**: Universal (covers all languages via Unicode), variable 1–4 bytes, dominant on the internet today (over 98% of web pages).
- **GB2312/GBK/GB18030**: Optimized for Chinese, smaller file size for Chinese text, but limited to Chinese (and some ASCII). Still widely used in mainland China, especially in legacy systems, Windows Chinese version, etc.

### Real-world consequences (why it matters)

If you open a Chinese text file saved in GB2312 with UTF-8 encoding → you get **mojibake** (garbled characters like ÄãºÃ).

That’s why modern software defaults to UTF-8: one encoding to rule them all.

So yes, you're exactly correct:

- All encodings define **character ↔ number** mapping.
- GB2312/GBK are Chinese-specific mappings.
- UTF-8 is the universal modern replacement that can handle Chinese (and everything else) perfectly.
