---
audio: false
generated: true
image: false
lang: en
layout: post
title: Langid Language Codes and Confidence
translated: false
type: note
---

In `langid`, the `classify(text)` function returns a tuple `(lang, confidence)` where:

* **`lang`** is a two-letter ISO 639-1 language code (sometimes extended with region codes like `zh-cn` or `zh-tw`).
* **`confidence`** is a float between 0 and 1 indicating how confident the model is.

The set of possible values for `lang` comes from the languages supported by `langid.py`. Out of the box, it includes **97 languages**. Some common examples:

* `en` → English
* `zh` / `zh-cn` / `zh-tw` → Chinese (generic / Simplified / Traditional)
* `ja` → Japanese
* `ko` → Korean
* `fr` → French
* `de` → German
* `es` → Spanish
* `hi` → Hindi
* `ar` → Arabic
* `ru` → Russian

And many others — the full list covers most major world languages (Afrikaans, Bengali, Greek, Hebrew, Italian, Portuguese, Swahili, Thai, Turkish, Vietnamese, etc.).

👉 If you want, I can give you the **complete list of all 97 codes** supported by `langid`. Would you like me to output that?
