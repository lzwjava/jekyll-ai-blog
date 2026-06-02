---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Using Python -c Command Flag
translated: false
type: note
---

Question: How do I use `python -c` to execute Python code directly from the command line?

Answer:

The `-c` flag allows you to pass a string containing Python code that will be executed immediately, without creating a script file.

### Basic syntax
```bash
python -c "code_here"
# or with python3 explicitly
python3 -c "code_here"
```

### Simple examples
```bash
# Print something
python -c "print('Hello, world!')"

# Do some math
python -c "print(2 + 2 * 10)"

# Import and use modules
python -c "import math; print(math.sqrt(16))"

# Multiple statements (use semicolons or explicit line breaks)
python -c "import sys; print(sys.version); print('Platform:', sys.platform)"
```

### Handling quotes and complex code
When your code contains quotes or spans multiple lines, you need to escape properly depending on your shell.

#### Single-line with single quotes inside
```bash
python -c "print('Single quotes are fine inside double-quoted string')"
python -c 'import os; print("User home:", os.path.expanduser("~"))'
```

#### Multi-line code (recommended way)
Use a heredoc or quote the entire block:
```bash
python -c "
import json
data = {'name': 'Alice', 'age': 30}
print(json.dumps(data, indent=2))
"
```

Or with single quotes and escaped newlines:
```bash
python -c 'import antigravity
print("Flying to xkcd...")
'
```

#### Alternative: Use `\` for line continuation (bash/zsh)
```bash
python -c 'import sys, json; \
data = [line.strip() for line in sys.stdin]; \
print(json.dumps(data))'
```

### Common one-liners you’ll actually use
```bash
# List all files in current directory (alternative to ls)
python -c "import os; print('\n'.join(os.listdir('.')))"

# Get your public IP
python -c "import urllib.request; print(urllib.request.urlopen('https://api.ipify.org').read().decode())"

# Quick HTTP server (Python 3)
python -c "import http.server, socketserver; http.server.test(HandlerClass=http.server.SimpleHTTPRequestHandler, Port=8000)"

# Generate a range and sum it
python -c "print(sum(range(1, 101)))"  # prints 5050
```

### Tips
- Always wrap the code in quotes to prevent shell interpretation.
- Use `python3` instead of `python` on systems where `python` points to Python 2.
- For very long scripts, consider writing a proper `.py` file instead.

That’s it! `python -c` is perfect for quick calculations, testing snippets, or automation in shell scripts.
