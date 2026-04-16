---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python String Formatting Methods Compared
translated: false
type: note
---

Question: When formatting a string in Python, which method is better?

Answer:

It depends on **what you care about** (readability, performance, logging, compatibility). There is no single “best” universally, but in modern Python, there *is* a clear default choice.

---

# 1. The modern best choice: **f-strings (✅ recommended)**

```python
name = "Alice"
age = 25
msg = f"{name} is {age} years old"
```

### Why this is best:

* ✅ Most **readable**
* ✅ Fast (often fastest in CPython)
* ✅ Direct and expressive
* ✅ Supports inline expressions

```python
f"{name.upper()} is {age + 1} next year"
```

👉 This is the **default choice in Python 3.6+**

---

# 2. `.format()` (older, flexible, but less used now)

```python
msg = "{} is {} years old".format(name, age)
```

or:

```python
msg = "{name} is {age}".format(name=name, age=age)
```

### Pros:

* Works in older Python (<3.6)
* Flexible formatting system

### Cons:

* ❌ More verbose
* ❌ Slower than f-strings
* ❌ Less readable

👉 Today: mostly **legacy / compatibility use**

---

# 3. `%` formatting (old style)

```python
msg = "%s is %d years old" % (name, age)
```

### Pros:

* Still useful in **logging** (special case)

### Cons:

* ❌ Outdated
* ❌ Less flexible
* ❌ Type issues (`%d`, `%s` etc.)

👉 Use it **only for logging**, not general string formatting.

---

# 4. String concatenation (`+`)

```python
msg = name + " is " + str(age) + " years old"
```

### Cons:

* ❌ Hard to read
* ❌ Easy to make mistakes
* ❌ Manual type conversion needed
* ❌ Not scalable

👉 Avoid in almost all cases.

---

# 5. Performance comparison (rough intuition)

Fastest → Slowest (usually):

```
f-string  ≥  % formatting  >  .format()  >  concatenation
```

But differences are small unless in tight loops.

---

# 6. Important exception: **logging**

Even though f-strings are best generally:

```python
logging.info(f"User {name}")   # ❌ not ideal
```

Use:

```python
logging.info("User %s", name)  # ✅ correct
```

Because logging uses **lazy formatting**.

---

# 7. Final recommendation

### Use this rule:

* ✅ **General string formatting → f-strings**
* ✅ **Logging → `%s` with comma**
* ❌ Avoid `.format()` unless needed
* ❌ Avoid `+` concatenation

---

# 8. Simple intuition

* f-string = **"just write what you mean"**
* `.format()` = **old flexible system**
* `%` = **special-purpose (logging)**
* `+` = **primitive, avoid**

---

If you want, I can show **edge cases where `.format()` is still better than f-strings** (there are a few subtle ones).