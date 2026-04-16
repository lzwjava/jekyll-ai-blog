---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python Logging Formatting Best Practices
translated: false
type: note
---

Question: How does Python logging work, and is `{0}` formatting needed or better than using `,` or `+` string concatenation?

Answer:

Python’s built-in **`logging`** module is designed for **flexible, efficient, and configurable logging**, especially in production systems.

---

## 1. How Python logging works (core idea)

At a high level:

* You create a **logger**
* You send messages with levels (`DEBUG`, `INFO`, `WARNING`, etc.)
* Messages are handled by **handlers** (console, file, etc.)
* Output format is controlled by **formatters**

Example:

```python
import logging

logging.basicConfig(level=logging.INFO)

logging.info("Hello world")
```

---

## 2. The key point: string formatting in logging

This is where your question matters.

### ✅ Recommended way (lazy formatting)

```python
logging.info("User %s logged in", username)
```

### ❌ Not recommended

```python
logging.info(f"User {username} logged in")
logging.info("User " + username + " logged in")
logging.info("User {} logged in".format(username))
```

---

## 3. Why `%s` (comma style) is better

### 🔥 Reason 1: **Lazy evaluation (performance)**

Logging only formats the string **if the log level is enabled**.

```python
logging.debug("Expensive: %s", compute_heavy())
```

If level is `INFO`, this will NOT call formatting → saves CPU.

But this:

```python
logging.debug(f"Expensive: {compute_heavy()}")
```

👉 `compute_heavy()` is executed **every time**, even if not logged.

---

### 🔥 Reason 2: cleaner separation

```python
logging.info("User %s has %d points", user, points)
```

* Template is fixed
* Data is separate
* Easier for structured logging / parsing

---

## 4. What about `{0}` or `{}`?

That comes from `str.format()`:

```python
"User {0}".format(username)
```

or

```python
"User {}".format(username)
```

### ❗ In logging, this is NOT special

Logging **does NOT use `{}` formatting by default**.

So this:

```python
logging.info("User {}", username)   # ❌ WRONG
```

Will NOT work.

---

## 5. Comparison summary

| Style               | Example                      | Recommended?       | Reason           |
| ------------------- | ---------------------------- | ------------------ | ---------------- |
| `%` (logging style) | `"User %s", username`        | ✅ YES              | Lazy, efficient  |
| f-string            | `f"User {username}"`         | ❌ NO (for logging) | Always evaluates |
| `+` concat          | `"User " + username`         | ❌ NO               | Ugly + eager     |
| `.format()`         | `"User {}".format(username)` | ❌ NO               | Eager            |

---

## 6. Advanced: if you really want `{}` style

You *can* configure logging to use `{}` formatting:

```python
logging.basicConfig(
    format="{asctime} - {message}",
    style="{"
)
```

But even then:

```python
logging.info("User {}", username)  # still ❌
```

Because argument substitution still uses `%` internally.

---

## 7. Best practice (production-level)

Always write logs like this:

```python
logging.debug("Processing file %s size=%d", filename, size)
```

NOT:

```python
logging.debug(f"Processing file {filename} size={size}")
```

---

## 8. Simple mental model

Think of logging like:

> “I give you a template + data, you decide later whether to build the string.”

That’s why `%s` + `,` is the correct design.

---

## Final takeaway

* `{0}` / `{}` → **not needed, not used by logging**
* `+` or f-string → **works but inefficient**
* ✅ Best practice → **use `%s` with comma arguments**

---

If you want, I can show how this affects performance in a real benchmark (it’s surprisingly significant in high-throughput systems).