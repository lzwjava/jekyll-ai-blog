---
audio: false
generated: true
image: false
lang: en
layout: post
title: Korean Misclassified as Chinese Validator Fix
translated: false
type: note
---

Got it — in this debug output:

```
Debug: raw langdetect output: [('ko', 0.9999995211930662)]
...
Detected languages: [('ko', 0.9999995211930662)]
```

The code **`ko`** is the ISO 639-1 language code for **Korean**. 🇰🇷

So `langdetect` is saying:

* It thinks the text is Korean (`ko`)
* With probability ≈ **0.9999995** (essentially 100%)

That explains the error: your validator expected `"zh-tw"` (Traditional Chinese), but the detector decided the input looks like Korean instead.

👉 Quick mapping reminder from `langdetect` / ISO 639-1:

* `zh` → Chinese (unspecified)
* `zh-cn` → Simplified Chinese (China)
* `zh-tw` (or `hant` in your mapping) → Traditional Chinese (Taiwan)
* `ja` → Japanese
* `ko` → Korean
* `ne` → Nepali
* `hi` → Hindi

Do you want me to suggest how you could **harden your validator** so it doesn’t fail when `langdetect` misclassifies (e.g. allowing a fallback if the target script characters are clearly Chinese but the code comes out as `ko`)?
