---
audio: false
generated: true
image: false
lang: en
layout: post
title: Modular Code Best Practices
translated: false
type: note
---

**Question:** How do you write modular code? The rules include using more functions, separating constants/variables, better categorization, and keeping related things together.

**Answer:**

## What Is Modular Code?

Modular programming is not just about writing clean code, self-contained classes, or smaller functions — it's about seeing your software as a collection of interchangeable modules, each with a well-defined purpose. Instead of one massive application, you break it into smaller, more manageable pieces.

---

## Core Principles

### 1. Single Responsibility — One Function, One Job

Each function you write should be focused on doing one thing. If a function is doing multiple things, it becomes more difficult to generalize and reuse. Generally, if there's an "and" in your function name, consider refactoring.

**Bad example:**
```python
def process_and_save_and_notify(data):
    # does 3 things — hard to reuse
    cleaned = data.strip()
    db.save(cleaned)
    email.send("Done!")
```

**Good example:**
```python
def clean_data(data):
    return data.strip()

def save_to_db(data):
    db.save(data)

def send_notification(message):
    email.send(message)
```

---

### 2. DRY — Don't Repeat Yourself

Modularization allows us to reuse parts of our code. Generalize and consolidate repeated code into functions or loops. Abstracting out code into a function not only makes it less repetitive, but also improves readability with descriptive function names.

---

### 3. Separate Constants and Configuration

Keep all magic numbers, strings, and configs in one dedicated place so changes are made in one spot only.

```python
# config.py or constants.py
MAX_RETRY = 3
API_URL = "https://api.example.com"
TIMEOUT = 30

# main.py
from config import MAX_RETRY, API_URL
```

---

### 4. Separation of Concerns — Group Related Things Together

Keep different aspects of the code (data handling, preprocessing, model training, etc.) in separate modules. Encapsulation hides implementation details and exposes only necessary functionalities.

A well-structured project looks like:

```
project/
├── config/
│   └── settings.py         # constants & config
├── data/
│   ├── loader.py           # loading data
│   └── preprocessor.py     # cleaning data
├── services/
│   └── api_client.py       # API calls
├── utils/
│   └── helpers.py          # shared utilities
└── main.py                 # entry point
```

---

### 5. Layered Architecture

A layered architecture is a common approach where code is organized into distinct layers based on functionality: a **Presentation layer** (UI logic), a **Business logic layer** (core rules and processes), and a **Data access layer** (database interaction). This layered approach fosters modularity, enabling more straightforward modification and maintenance of individual layers without disrupting the entire system.

---

### 6. Naming Conventions

Naming conventions can help you avoid confusion, ambiguity, and errors, as well as improve readability and maintainability. You should use a consistent naming convention throughout your code and follow the standards of your programming language. For example, in Python, follow the PEP 8 style guide, which defines rules for naming modules, variables, functions, classes, and constants.

Quick reference:

| Element | Convention (Python) | Example |
|---|---|---|
| Variable | snake_case | `user_name` |
| Function | snake_case verb | `get_user()` |
| Constant | UPPER_CASE | `MAX_SIZE` |
| Class | PascalCase | `UserService` |
| Boolean | `is_` / `has_` prefix | `is_valid` |

---

### 7. Limit Function Arguments

Try to use no more than three arguments per function when possible. This is not a hard rule, but in many cases it's more effective to use fewer arguments. If a function has a lot of parameters, you may want to rethink how you are splitting it up.

---

### 8. Loose Coupling Between Modules

Modules should operate as independent units, connected only through well-defined interfaces. This means you can modify one module's internal workings without needing to change any others, as long as the interface remains the same.

---

### 9. Avoid Over-Modularizing

Programmers can fall into the trap of being overly modular. What starts as a good thing devolves into dividing and subdividing beyond the point of reason with no real-world use case in mind. The adage "premature optimization is the root of all evil" is still relevant — give your software a little time to take shape before refactoring for modularity.

---

## Quick Checklist

- Each function does **one thing only**
- Constants live in a **dedicated config file**
- Related code is **grouped in the same module/folder**
- No repeated logic — use **shared utility functions**
- Functions have **descriptive names** and **≤3 parameters**
- Modules are **loosely coupled** (minimal interdependencies)
- Follow a **consistent naming convention**

---

**References:**

- [https://best-practice-and-impact.github.io/qa-of-code-guidance/modular_code.html](https://best-practice-and-impact.github.io/qa-of-code-guidance/modular_code.html)
- [https://vfunction.com/blog/modular-software/](https://vfunction.com/blog/modular-software/)
- [https://dev.to/prxtikk/how-to-write-clean-and-modular-code-1d87](https://dev.to/prxtikk/how-to-write-clean-and-modular-code-1d87)
- [https://blog.pixelfreestudio.com/best-practices-for-modular-code-design/](https://blog.pixelfreestudio.com/best-practices-for-modular-code-design/)
- [https://www.designreview.byu.edu/collections/from-chaos-to-clarity-modular-design-in-programming](https://www.designreview.byu.edu/collections/from-chaos-to-clarity-modular-design-in-programming)
