---
audio: false
generated: true
image: false
lang: en
layout: post
title: Small Code Model Inference Results
translated: false
type: note
---

## Inference Results Summary

**Model tested: `out-github-code-124m`** — 124M param GPT-2, trained on GitHub code (14B tokens)

Here's what each prompt produced:

---

### 1. `prompt_hashmap.txt` — Java HashMap (incomplete `put` method)

```
public void put(K key, V value) {
    return this).Size;
         assertEquals("test for required ` + object)
  ...
```

**Verdict:** Garbage. It knows it's in Java (braces, `assertEquals`, `+` string concat) but produces semantically meaningless code. The `HashTable` concept is there — it emitted `getNext_files` and size checks — but nothing compilable.

---

### 2. `prompt_java.txt` — Java BST (incomplete `search` method)

```
boolean search(int key) {
    return this;
              }
                *handle = newkey;
             if ( str.key)) {
                         return;
  ...
```

**Verdict:** Garbage with Java-ish shape. Recognises it should return something and recurse into nodes, but syntax and logic are broken.

---

### 3. `prompt_python.txt` — Complete MiniGPT (151 lines)

The model **perfectly reproduced** the entire prompt verbatim (as expected — it's the longest prompt and the model has seen similar PyTorch code in training), then added:

```python
        return parse_s.array_or_id
           expect = self.current_index_c('und' ) * time_size_t'
                          self.send_dict_text_by_model(self).'=self.size)
  ...
```

**Verdict:** After the prompt ends, garbage. It recognises Python but produces incoherent method bodies.

---

### 4. `prompt_quicksort.txt` — Just `def quicksort(arr):`

```
def quicksort(arr):
                                     class     *                 (                               .
```

**Verdict:** Complete garbage. Too short a prompt — the model has no context to latch onto, so it produces whitespace + random tokens.

---

### 5. `prompt_webapp.txt` — Complete Flask app (258 lines)

Perfectly reproduced the full Flask app, then appended:

```python
        return 'Eailed', )
         end
  assert_backend = self._config_description_1('status'=True,
```

**Verdict:** Clean reproduction of prompt, then garbage continuation.

---

### Comparison with other models

| Model | Java HashMap | Notes |
|-------|-------------|-------|
| `out-github-code-124m` | Garbage (Java-shaped) | Best of the 3 — at least knows Java syntax |
| `out-fineweb-gpt3` (124M) | Garbage (symbols) | Worse — doesn't know Java at all |
| `out-gpt2-200m` (200M) | `string type` × 200 | Web text model, no code knowledge |

### Why this happens

**Root cause:** 124M parameters is far too small for coherent code generation. At this scale, the model:

1. **Learns code syntax well** — correct indentation, braces, keywords, method structure
2. **Learns token-level statistics** — `return` follows `{`, `}` ends blocks, `assertEquals` appears in test code
3. **Has no capacity for semantic understanding** — it can't maintain a coherent plan across >50 tokens because the hidden state (768-dim) is too compressed

For reference, Codex (the model powering early GitHub Copilot) was 12B parameters. Even CodeGen-350M (350M params) starts producing half-reasonable completions. 124M is just too small.

**Vibe-coding these prompts would require a model like CodeLlama-7B or GPT-2 XL (1.5B)** to get semantically meaningful completions on partial Java/Python code.