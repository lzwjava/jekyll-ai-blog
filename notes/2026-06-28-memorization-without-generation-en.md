---
audio: false
generated: true
image: false
lang: en
layout: post
title: Memorization Without Generation
translated: false
type: note
---

Here's the summary of all 5 tests:

== Test 1: Java BST (long prompt, continuation of search method) ==
RESULT: Mixed. The prompt was replayed verbatim (good), but once it hit
the continuation point, it generated nonsensical Java: `return;`, garbled
method signatures like `public String get(String source)`, random tokens
like `Property.TrveradataValue`. The structure (indentation, braces) was
loosely maintained but the logic is garbage.

== Test 2: Python MiniGPT (long prompt, continuation after training loop) ==
RESULT: Best of the bunch. The entire prompt was reproduced nearly
verbatim including the full training loop, checkpoint save, and model
load. The continuation after "Model loaded successfully!" degraded into
garbage (`data_size(t.last, self.get_size())`). For a 124M model this is
respectable memorization of Python patterns.

== Test 3: Flask webapp (long prompt, continuation after error handlers) ==
RESULT: Good memorization of the prompt (user routes, error handlers,
main block all replayed correctly). The continuation after
`app.run(debug=True, port=5000)` was pure nonsense:
`def = assert_user_text): data = get_action.get_to_get_get_string(...)`.

== Test 4: Short prompt "def quicksort(arr):" (3 samples) ==
RESULT: Complete failure. All 3 samples produced whitespace and random
punctuation only. The model cannot generate meaningful Python from a
short prompt.

== Test 5: Java HashMap (long prompt, continuation after put method) ==
RESULT: Prompt replayed verbatim, continuation was garbage:
`return self.copy(J,);` — mixing Python syntax into Java. Then random
tokens.

== VERDICT ==
The model has learned to MEMORIZE long code blocks it has seen in
training (replay is near-perfect), but has almost ZERO generative
ability for new code. Short prompts produce gibberish. Even with long
context, the moment it passes the memorized region, output degrades
immediately into random tokens and cross-language contamination.

This is expected for a 124M model on 14B tokens of code — it's more
of a code-memorization model than a code-generation model. The val
loss of 3.466 confirms it hasn't learned the distribution well enough
to generate novel coherent code.
