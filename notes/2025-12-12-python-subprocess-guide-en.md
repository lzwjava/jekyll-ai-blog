---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Using Python Subprocess Module Guide
translated: false
type: note
---

Question: How do I use the `subprocess` module in Python to run a command?

Answer:

The `subprocess` module in Python allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes. The recommended high-level function (introduced in Python 3.5) is `subprocess.run()`, which runs a command and waits for it to complete.

### Basic Usage
Import the module and call `subprocess.run()` with the command as a list of strings (preferred for security) or a single string.

```python
import subprocess

# Simple command: list files (Unix-like systems)
result = subprocess.run(["ls", "-l"])

# On Windows: equivalent to dir
# result = subprocess.run(["dir"])
```

This runs the command and prints output to the console by default. The function returns a `CompletedProcess` object with attributes like `returncode` (0 usually means success).

### Capturing Output
To capture stdout (and optionally stderr):

```python
import subprocess

result = subprocess.run(["ls", "-l"], capture_output=True, text=True)

print(result.stdout)  # Output as string
print(result.stderr)  # Error output if any
print(result.returncode)  # Exit status
```

- `capture_output=True`: Captures both stdout and stderr.
- `text=True`: Returns output as strings (instead of bytes).

### Handling Errors
Use `check=True` to raise an exception if the command fails (non-zero return code):

```python
try:
    subprocess.run(["ls", "nonexistent_file"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Command failed with code {e.returncode}")
```

### Providing Input
Pass data to the command's stdin:

```python
result = subprocess.run(["grep", "search_term"], input="line1\nsearch_term here\nline3", text=True, capture_output=True)
print(result.stdout)
```

### Using Shell Features
For shell built-ins, pipes, or wildcards, set `shell=True` (but be cautious with untrusted input due to security risks):

```python
result = subprocess.run("ls -l | grep .py", shell=True, capture_output=True, text=True)
```

Prefer the list form without `shell=True` when possible for safety.

For more advanced control (e.g., streaming or timeouts), use `subprocess.Popen()`, but `run()` covers most common cases.

References:

- [Python Official Documentation: subprocess — Subprocess management](https://docs.python.org/3/library/subprocess.html)
- [An Introduction to Python Subprocess: Basics and Examples | DataCamp](https://www.datacamp.com/tutorial/python-subprocess)
- [The subprocess Module: Wrapping Programs With Python – Real Python](https://realpython.com/python-subprocess/)
