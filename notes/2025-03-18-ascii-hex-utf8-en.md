---
audio: false
generated: true
image: false
lang: en
layout: post
title: ASCII Hex UTF-8 Explained Simply
translated: false
type: note
---

Let’s break them down clearly:

---

### ASCII

* **Definition**: ASCII (American Standard Code for Information Interchange) is one of the earliest character encodings.
* **Range**: Uses **7 bits** (values 0–127).
* **Meaning**: Each number corresponds to a character.
  For example:

  * `65` → `"A"`
  * `97` → `"a"`
  * `48` → `"0"`
* **Limitation**: Only covers English letters, digits, punctuation, and control codes (like newline).

---

### Hex (Hexadecimal Representation)

* **Definition**: Hex is not a character set by itself, but a **numerical representation** (base-16) of data.
* **Usage**: Commonly used to display bytes in a compact and human-readable way.
* **Example**:

  * ASCII `"A"` = decimal `65` = hex `41`.
  * ASCII `"B"` = decimal `66` = hex `42`.
  * So the text `"AB"` looks like `41 42` in hex.

---

### UTF-8

* **Definition**: UTF-8 is a **Unicode encoding** standard.
* **Features**:

  * Variable length: encodes each character in **1 to 4 bytes**.
  * Backward compatible with ASCII: characters `0–127` are the same as ASCII (1 byte).
  * Can represent all Unicode characters (letters, symbols, emojis, Chinese characters, etc.).
* **Examples**:

  * `"A"` → `41` (same as ASCII).
  * `"中"` → `E4 B8 AD` (three bytes in hex).
  * `"😊"` → `F0 9F 98 8A` (four bytes in hex).

---

✅ **In short**:

* ASCII = old 7-bit code for English characters.
* Hex = a way of writing numbers/bytes (base-16).
* UTF-8 = modern encoding that includes ASCII but also supports every language and symbol.

---

Would you like me to also show you a **side-by-side example of the same text** (`"Hello 世界😊"`) in ASCII (where possible), hex, and UTF-8 so you can see the difference directly?
