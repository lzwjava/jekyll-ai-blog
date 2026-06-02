---
audio: false
generated: true
lang: en
layout: post
title: How Modules Work in Python
translated: false
type: note
---

In Python, a **module** is a file containing Python code—such as functions, classes, and variables—that you can import and use in other Python scripts. Modules are a fundamental feature of Python that help you organize your code, promote reuse, and avoid repetition. Let’s explore how they work and how you can use other Python files or modules in your projects.

---

#### What Is a Module?

A module is simply a `.py` file with Python code. When you import a module into another script, Python executes the code in that file and makes its contents (functions, classes, variables, etc.) available for you to use. Python comes with a rich standard library of built-in modules (e.g., `math`, `os`, `sys`), and you can also create your own custom modules.

For example, if you have a file named `greetings.py` with the following code:

```python
def say_hello(name):
    print(f"Hello, {name}!")
```

This file is a module named `greetings`. You can import it into another script to use the `say_hello` function.

---

#### How to Use Other Python Files or Modules

To use code from another Python file (module), you use the `import` statement. Here’s how it works step by step:

1. **Basic Import**
   - If the module is in the same directory as your script, you can import it by its name (without the `.py` extension).
   - Example: In a file named `main.py`, you can write:

     ```python
     import greetings
     greetings.say_hello("Alice")
     ```

   - Running `main.py` will output: `Hello, Alice!`
   - Use dot notation (`module_name.item_name`) to access the module’s contents.

2. **Importing Specific Items**
   - If you only need specific functions or variables from a module, use the `from ... import ...` syntax.
   - Example:

     ```python
     from greetings import say_hello
     say_hello("Bob")
     ```

   - This outputs: `Hello, Bob!`
   - Now you can use `say_hello` directly without prefixing it with the module name.

3. **Importing with Aliases**
   - You can give a module a shorter name (alias) using `as` for convenience.
   - Example:

     ```python
     import greetings as g
     g.say_hello("Charlie")
     ```

   - Output: `Hello, Charlie!`

4. **Importing Everything**
   - You can import all contents of a module using `from module_name import *`, but this is generally discouraged because it can clutter your namespace and cause naming conflicts.
   - Example:

     ```python
     from greetings import *
     say_hello("Dana")
     ```

   - Output: `Hello, Dana!`

---

#### Where Does Python Look for Modules?

Python searches for modules in a list of directories defined in `sys.path`. This includes:

- The directory of the script you’re running (current directory).
- Directories listed in the `PYTHONPATH` environment variable (if set).
- Default locations where Python’s standard library is installed.

If your module is in a different directory, you can:

- Move it to the same directory as your script.
- Add its directory to `sys.path` programmatically:

  ```python
  import sys
  sys.path.append('/path/to/directory')
  import mymodule
  ```

---

#### Built-in Modules

Python’s standard library provides many useful modules you can import without creating them yourself. For example:

- `import math` lets you use `math.sqrt(16)` (returns `4.0`) or `math.pi` (returns `3.14159...`).
- `import os` provides functions for interacting with the operating system.

---

#### Packages

A **package** is a directory containing multiple modules and a special `__init__.py` file (which can be empty). For example, if you have:

```
mypackage/
    __init__.py
    greetings.py
```

You can import the `greetings` module like this:

```python
import mypackage.greetings
mypackage.greetings.say_hello("Eve")
```

Or:

```python
from mypackage.greetings import say_hello
say_hello("Eve")
```

---

#### How Modules Are Executed

When you import a module, Python runs all the code in that module once and caches it. Subsequent imports reuse the cached version. If a module contains top-level code (e.g., a `print` statement), it will execute during import. For example:

```python
# mymodule.py
print("Module is being imported!")
def my_function():
    print("Function called!")
```

```python
# main.py
import mymodule
```

Running `main.py` outputs: `Module is being imported!`

To include code that only runs when the module is executed directly (not imported), use:

```python
if __name__ == "__main__":
    print("This runs only if the module is run directly!")
```

This is useful for testing or defining a main entry point for the module.

---

#### Example

Here’s a complete example:

1. Create `math_utils.py`:

   ```python
   def add(a, b):
       return a + b
   ```

2. Create `main.py` in the same directory:

   ```python
   import math_utils
   result = math_utils.add(3, 4)
   print(result)  # Outputs: 7
   ```

3. Alternatively:

   ```python
   from math_utils import add
   print(add(3, 4))  # Outputs: 7
   ```

---

#### Key Takeaways

- Modules are Python files that you can import to reuse code.
- Use `import module_name` to access contents with dot notation, or `from module_name import item` for direct access.
- Modules can be custom files, built-in library modules, or part of packages.
- Python finds modules using `sys.path`, and you can organize larger projects with packages.

This covers the essentials of how modules work in Python and how to use other Python files or modules in your scripts!
