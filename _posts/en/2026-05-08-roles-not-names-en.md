---
audio: false
generated: true
image: false
lang: en
layout: post
title: Use Roles Instead of Real Names
translated: false
type: note
---

Question: In a Whisper meeting transcription article, is it better to use “the senior” instead of real names like “Zhiwei Li” or “Ruixiu Zhang,” especially because Chinese names and proper nouns are harder to translate correctly?

Answer:

Yes — in many cases, using role-based descriptions such as “the senior engineer,” “the researcher,” “the student,” or “the interviewer” is better than repeatedly using personal names, especially for AI-transcribed meeting summaries.

There are several practical reasons:

### 1. Better readability after translation

Chinese names transliterated into English are often ambiguous when translated back into Chinese or into other languages.

For example:

* “Ruixiu Zhang”
* “Rui Xiu Zhang”
* “Ray Hsu Chang”
* “Zhang Ruixiu”

These may all refer to the same person depending on:

* pinyin spacing
* accent
* ASR recognition
* translation model behavior
* human interpretation

So when the document later gets translated into Chinese, Japanese, or another language, the mapping becomes unstable.

This is not really an AI failure — it is fundamentally a **one-to-many mapping problem** between:

* sound
* romanization
* characters
* cultural naming conventions

Chinese names especially have:

* multiple valid pinyin segmentations
* homophones
* surname/given-name ambiguity
* optional tone information loss

So role-based references are often safer.

---

### 2. More natural for edited meeting articles

Once a transcript becomes an “article,” readers usually care more about:

* the ideas
* the interaction
* the experience level
* the discussion structure

rather than exact identity repetition.

So writing:

> The senior engineer explained that repeated communication becomes inefficient over time.

often reads cleaner than:

> Zhiwei Li explained that repeated communication becomes inefficient over time.

especially if the article is not primarily about the individual person.

---

### 3. Easier speaker recovery from imperfect transcripts

Whisper transcripts often lose:

* speaker diarization
* punctuation
* boundaries
* names
* pronouns

Using abstract roles lets you avoid overclaiming speaker identity.

For example:

* “the senior”
* “the student researcher”
* “the participant”
* “they”

is safer than incorrectly attributing statements.

That is particularly important in long meetings.

---

### 4. Better multilingual portability

Role labels translate very cleanly:

| English                | Chinese |
| ---------------------- | ------- |
| the senior engineer    | 资深工程师   |
| the student researcher | 学生研究者   |
| the interviewer        | 面试官     |
| the participant        | 参与者     |

But names may:

* transliterate inconsistently
* lose meaning
* become awkward in machine translation
* confuse readers unfamiliar with Chinese naming order

---

### 5. More timeless and reusable

If the document is intended as:

* educational material
* blog content
* internal notes
* AI-generated article
* podcast summary

then generalized references age better and feel more professional.

It also reduces unnecessary personal exposure.

---

A good hybrid style is:

> The meeting involved a senior programmer and a high-school AI researcher (Ruixiu Zhang).

Then afterward:

* “the senior”
* “the researcher”
* “they”

This introduces identity once while keeping the rest readable.

Your instinct here is correct: this is largely a language-mapping and document-structure issue, not simply an AI weakness.