---
audio: false
generated: true
image: false
lang: en
layout: post
title: Langdetect Mistook Text as Nepali
translated: false
type: note
---

Ah, I see — thanks for clarifying.

In the log you pasted:

```
Debug: raw langdetect output: [('ne', 0.9999953270916105)]
Debug: normalized langdetect output: [('ne', 0.9999953270916105)]
Debug: Detected languages: [('ne', 0.9999953270916105)]
```

Here **`ne` is not the French word** — it’s actually a **language code** emitted by `langdetect`.

The `langdetect` library sometimes returns `"ne"` as the ISO 639-1 code for **Nepali**.

* `"en"` = English
* `"fr"` = French
* `"hi"` = Hindi
* `"ne"` = Nepali

So in this case, `langdetect` thought your text was Nepali with probability `~0.99999`.

That’s why your validation failed with:

```
Translated text does not contain the target language 'hi' (detected: [('ne', 0.9999953270916105)])
```

👉 To summarize:

* `ne` here = ISO language code **Nepali**, not the French negation word `"ne"`.
* It shows up when `langdetect` decides your input looks like Nepali.

Do you want me to show you how to **normalize or remap** `ne` (Nepali) in your `_map_target_code` so your validator doesn’t choke when unexpected languages pop up?
