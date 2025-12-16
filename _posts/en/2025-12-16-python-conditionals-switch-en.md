---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Python Conditional Statements and Switch
translated: false
type: note
---

Question: How do you write conditional code in Python using if, elif, and else? Does Python have a switch statement?

Answer: 

Python uses `if`, `elif`, and `else` statements for conditional execution. Unlike many other languages, Python **does not have a traditional switch statement** until Python 3.10, which introduced the **structural pattern matching** feature (`match` and `case`) that can serve as a more powerful alternative to switch.

### Basic if-elif-else syntax

```python
x = 10

if x > 20:
    print("x is greater than 20")
elif x > 5:
    print("x is greater than 5 but not greater than 20")
else:
    print("x is 5 or less")
```

- `if` checks the first condition.
- `elif` (short for "else if") checks additional conditions if previous ones are false.
- `else` runs if none of the above conditions are true.
- You can have any number of `elif` clauses, and `else` is optional.

### Nested conditions

```python
if x > 0:
    if x % 2 == 0:
        print("Positive even number")
    else:
        print("Positive odd number")
else:
    print("Non-positive number")
```

### Switch-like behavior (Python 3.10+): match-case

Starting with Python 3.10, you can use `match` and `case` for pattern matching, which is often used as a switch replacement:

```python
def http_status(status):
    match status:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500:
            return "Internal Server Error"
        case _ :  # wildcard (default case)
            return "Unknown status"

print(http_status(200))  # Output: OK
```

The `match` statement is more powerful than traditional switch because it supports patterns like lists, dictionaries, guards, and more.

### Older alternatives (before Python 3.10)

Common ways to simulate switch:
- Using a dictionary:

```python
def handle_command(cmd):
    return {
        'start': lambda: print("Starting..."),
        'stop':  lambda: print("Stopping..."),
        'pause': lambda: print("Pausing...")
    }.get(cmd, lambda: print("Unknown command"))()

handle_command('start')
```

- Using if-elif chains (most common and readable for simple cases).

In most cases, `if-elif-else` is preferred for clarity unless you have many cases or need advanced pattern matching.