---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Python Regular Expressions Guide
translated: false
type: note
---

### Importing the `re` Module

The `re` module (short for regular expressions) is part of Python's standard library. It's not a separate "regex package" but a built-in module. Import it at the top of your script:

```python
import re
```

### Basic Concepts

Regular expressions (regex) are patterns used to match, search, and manipulate strings. They use special characters like:

- `.` (any character)
- `*` (zero or more occurrences)
- `+` (one or more occurrences)
- `[]` (character classes, e.g., `[a-z]` for lowercase letters)
- `^` (start of string), `$` (end of string)

Examples are based on Python's `re` documentation. Always compile complex patterns for efficiency with `re.compile()`.

### Key Functions and Usage

#### 1. **Matching a Pattern at the Start**

- `re.match(pattern, string)`: Checks if the pattern matches from the beginning of the string.
- Returns a match object or `None`.

   Example:

   ```python
   import re
   result = re.match(r"Hello", "Hello world")
   print(result.group())  # Output: Hello
   ```

#### 2. **Searching Anywhere in the String**

- `re.search(pattern, string)`: Finds the first occurrence of the pattern anywhere.
- Returns a match object or `None`.

   Example:

   ```python
   result = re.search(r"world", "Hello world")
   print(result.group())  # Output: world
   ```

#### 3. **Finding All Matches**

- `re.findall(pattern, string)`: Returns a list of all non-overlapping matches.

   Example:

   ```python
   matches = re.findall(r"\d+", "I have 3 cats and 42 dogs")
   print(matches)  # Output: ['3', '42']
   ```

#### 4. **Splitting Strings**

- `re.split(pattern, string)`: Splits the string at occurrences of the pattern.

   Example:

   ```python
   parts = re.split(r"\s+", "Hello    world   example")
   print(parts)  # Output: ['Hello', 'world', 'example']
   ```

#### 5. **Replacing Matches**

- `re.sub(pattern, replacement, string)`: Replaces matches with the replacement string.

   Example:

   ```python
   new_string = re.sub(r"bad", "good", "This is bad")
   print(new_string)  # Output: This is good
   ```

#### 6. **Compiling Patterns for Reuse**

- For repeated use, compile the regex to a pattern object for better performance.

   Example:

   ```python
   pattern = re.compile(r"\d+")
   matches = pattern.findall("Room 101 and 102")
   print(matches)  # Output: ['101', '102']
   ```

### Best Practices

- Use raw strings (`r""`) for regex patterns to avoid backslash escaping issues.
- Handle match objects: Use `.group()` to get the match, `.span()` for indices.
- For complex tasks, test patterns with online tools or Python's interactive shell.
- Reference Python's official docs: <https://docs.python.org/3/library/re.html> for more examples and flags (e.g., `re.IGNORECASE`).

If you have a specific use case or error, provide more details!
