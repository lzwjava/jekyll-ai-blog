---
audio: false
generated: true
image: false
lang: en
layout: post
title: Data as Representation of Facts
translated: false
type: note
---

Question: Is this definition of **data** correct?

> 数据：对客观事物的性质、状态以及相互关系等进行记载的符号及其组合，通常是数字、文字、图像等，也可以是其他抽象的符号。

Answer:

Yes, this is basically correct. It is a classic definition from **information science / database theory**.

A more precise understanding:

**Data = representation of facts.**

The key points:

1. **Data describes things**

   The "things" can be:

   * objects: a person, a car, a product
   * events: a transaction, a click, a temperature reading
   * relationships: "Alice bought Product A"

2. **Data itself is symbols, not meaning**

Example:

```
2026-08-01
```

This is data.

Its meaning depends on context:

```
2026-08-01 = date
2026-08-01 = product ID
2026-08-01 = version number
```

The raw symbols become information after interpretation.

A common hierarchy:

```
Data
  |
  | interpretation
  v
Information
  |
  | analysis + experience
  v
Knowledge
  |
  | decision
  v
Wisdom
```

Example:

Raw data:

```
{
  "user_id": 123,
  "temperature": 39.2,
  "time": "08:00"
}
```

Information:

```
User 123 had a high temperature at 08:00.
```

Knowledge:

```
A temperature above 39°C may indicate fever.
```

Decision:

```
Recommend medical attention.
```

---

In computer science, we usually generalize data into:

### 1. Structured data

Fixed schema:

```sql
User(
    id INT,
    name VARCHAR,
    age INT
)
```

Examples:

* databases
* CSV
* JSON with fixed fields

### 2. Semi-structured data

Has structure but flexible:

```json
{
  "name": "Alice",
  "skills": ["Python", "AI"]
}
```

Examples:

* JSON
* XML
* logs

### 3. Unstructured data

No fixed schema:

* images
* audio
* video
* documents
* natural language

Modern AI is largely about learning representations from unstructured data:

```
text
 |
Tokenizer
 |
tokens
 |
embeddings
 |
vectors
 |
model learns patterns
```

For an LLM:

```
"The cat sits on the mat"
```

is converted into:

```
tokens:
[464, 3797, 286, 262, 2603]

↓

embedding vectors:

[0.12, -0.54, ...]
```

The model never directly sees "meaning"; it learns statistical patterns over numerical representations.

So your definition is correct. A more modern AI-oriented version would be:

> Data is a symbolic representation of objects, events, attributes, and relationships that can be stored, transmitted, processed, and interpreted by humans or machines.

References:

* Database System Concepts
* Artificial Intelligence: A Modern Approach
