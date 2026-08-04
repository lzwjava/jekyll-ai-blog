---
audio: false
generated: true
image: false
lang: en
layout: post
title: Compliance in Guided Decoding
translated: false
type: note
---

**Question: What does "compliance" mean in this SGLang guided decoding context?**

**Answer:**

Here, **compliance means how often the LLM output follows the required format/constraint**, not whether the answer is factually correct.

In the quote:

> without constrained decoding, typical LLM JSON compliance sits at 90-94%; with SGLang's compressed FSM, compliance reaches 96-98.2%.

It means:

* You ask the model:

```text
Generate a JSON object matching this schema:

{
  "name": string,
  "age": integer,
  "email": string
}
```

* The model generates:

✅ Compliant:

```json
{
  "name": "Alice",
  "age": 30,
  "email": "alice@example.com"
}
```

❌ Non-compliant:

```text
Sure! Here is the JSON:

{
  "name": "Alice",
  "age": "thirty"
}
```

or:

```json
{
  "name": "Alice",
  "age": 30,
}
```

(trailing comma)

or:

```json
{
  "name": "Alice",
  "age": 30,
  "extra_field": true
}
```

if extra fields are forbidden.

---

### Why guided decoding improves compliance

Normally LLM generation is:

```
prompt
  |
  v
Transformer forward
  |
  v
logits over vocabulary
  |
  v
sample next token
```

The model can choose any token:

```
{ "age": "thir...
```

because `"thirty"` is a valid token sequence, even though the schema requires an integer.

---

Guided decoding adds a constraint layer:

```
              JSON FSM / grammar
                    |
                    v
prompt --> LLM --> logits --> mask invalid tokens --> sample
```

Example:

Current state:

```
{
 "age":
```

Valid next tokens:

```
0 1 2 3 4 5 6 7 8 9
```

Invalid:

```
"
t
null
true
```

The decoder sets invalid token probabilities to `-inf`:

```python
logits[invalid_tokens] = -inf
```

Then softmax cannot select them.

---

### FSM meaning

SGLang's compressed FSM = finite state machine representing allowed output paths.

For JSON schema:

```
START
 |
 {
 |
 "name"
 |
 :
 |
 STRING
 |
 ,
 |
 "age"
 |
 :
 |
 INTEGER
 |
 }
 |
END
```

The FSM tells the runtime:

> At this exact generation step, only these tokens are legal.

---

### Why only 96-98.2%, not 100%?

Because "compliance" usually measures the whole pipeline, not only token validity.

Failures can still happen:

1. **Schema ambiguity**

Example:

```
age: integer
```

Model outputs:

```json
{"age": 30.5}
```

Depending on implementation.

2. **Stop handling**

Model may stop early:

```json
{
 "name": "Alice"
```

3. **Parser differences**

Generated output may pass one JSON parser but fail another.

4. **External constraints**

Example:

```
email must be a real email address
```

Grammar cannot verify that.

---

For production LLM systems, people usually separate:

| Metric           | Meaning                          |
| ---------------- | -------------------------------- |
| JSON compliance  | Output parses and matches schema |
| Task accuracy    | Answer content is correct        |
| Semantic quality | Human usefulness                 |
| Latency          | Time per request                 |

SGLang's claim is mainly about **syntactic reliability of structured generation**. It is especially important for agent systems where the LLM must emit tool calls:

```json
{
  "tool": "search",
  "arguments": {
    "query": "latest NVIDIA GPU"
  }
}
```

A 98% compliant agent is much easier to run than a 90% compliant one because failures compound over long workflows.
