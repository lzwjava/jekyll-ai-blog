---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python Underscore Naming Convention Explained
translated: false
type: note
---

**Question:** Is it good practice in Python to use `_func` (single leading underscore) to indicate a function is not exported, similar to `private`/`protected` in Java?

**Answer:**

Yes, it is absolutely a good and widely accepted practice in Python. However, the mechanism and enforcement differ significantly from Java. Here is a comprehensive breakdown:

---

## The Convention: Single Leading Underscore `_func`

The underscore prefix is meant as a hint to another programmer that a variable or method starting with a single underscore is intended for internal use. This convention is defined in PEP 8, but it is **not enforced by Python**.

Python doesn't enforce public or private names with access restrictions. It relies on naming conventions, where public names have no underscores and non-public names start with a single underscore.

---

## How It Compares to Java `private`/`protected`

| Feature | Java `private` | Java `protected` | Python `_func` |
|---|---|---|---|
| Enforced by language? | ✅ Yes | ✅ Yes | ❌ No |
| Accessible externally? | ❌ No | Subclasses only | ✅ Still accessible |
| Convention-based? | No | No | ✅ Yes |
| Excluded from wildcard import? | N/A | N/A | ✅ Yes |

So in Python, `_func` is a **gentleman's agreement**, not a hard rule.

---

## The Real-World Effect: Wildcard Import Exclusion

One **concrete, enforced** behavior of `_func` is its effect on imports:

Python does not import names that begin with a single underscore if you import all the methods and names from a module using `from module import *`.

Example:
```python
# mymodule.py
def public_func():
    return "I am public"

def _private_func():
    return "I am internal"
```

```python
from mymodule import *
public_func()    # Works fine
_private_func()  # NameError: not imported!
```

This makes `_func` directly analogous to "not exported" — which is exactly what you described.

---

## The Full Underscore System in Python

The following special forms using leading or trailing underscores are recognized in Python:
- `_single_leading_underscore`: weak "internal use" indicator
- `single_trailing_underscore_`: used to avoid conflicts with Python keywords
- `__double_leading_underscore`: when naming a class attribute, invokes name mangling
- `__double_leading_and_trailing_underscore__`: "magic" objects or attributes

### Single Underscore `_func` — "Protected / Internal"
If you want to indicate that an attribute or method is intended for use within the class and its subclasses but not for external use, prefix it with a single underscore (`_`). This signals to other developers that the attribute or method is "protected" and should not be accessed directly.

### Double Underscore `__func` — "Private with Name Mangling"
If you want to make an attribute or method less accessible outside the class to avoid accidental modification or usage, prefix it with a double underscore (`__`). This triggers name mangling and makes it harder (but not impossible) to access the attribute or method from outside the class.

For example, `__method` inside `class Foo` becomes `_Foo__method` internally — it can still be accessed if you know the mangled name, but it prevents accidental collisions in subclasses.

---

## PEP 8 Official Recommendation

Even with `__all__` set appropriately, internal interfaces (packages, modules, classes, functions, attributes or other names) **should still be prefixed with a single leading underscore**.

---

## Summary & Best Practice

- ✅ **Use `_func`** for module-level or class-level functions/methods you consider internal — this is the standard Pythonic convention and is recommended by PEP 8.
- ✅ It effectively acts as "not exported" because `from module import *` will skip it.
- ⚠️ It does **not** prevent direct access — external code can still call `module._func()` if it wants to.
- ✅ **Use `__func`** inside a class only when you need name mangling to prevent subclass attribute collisions (not primarily for privacy).
- 🐍 Python's philosophy is **"we're all consenting adults"** — the community trusts that developers will respect the underscore signal without needing the language to enforce it.

---

**References:**

- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [Single and Double Underscores in Python – Real Python](https://realpython.com/python-double-underscore/)
- [The Meaning of Underscores in Python – dbader.org](https://dbader.org/blog/meaning-of-underscores-in-python)
- [Python Private Methods Explained – DataCamp](https://www.datacamp.com/tutorial/python-private-methods-explained)