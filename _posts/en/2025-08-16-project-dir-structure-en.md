---
audio: false
generated: true
image: false
lang: en
layout: post
title: Project Directory Structure Best Practices
translated: false
type: note
---

Good question.

The general convention is:

* **`scripts/`** is for your application code (things you want to run in production or as part of your project).
* **`tests/`** is for your test code (things that validate correctness of your scripts/modules).

So if you’re adding a new test file, it should normally go under **`tests/llm/`**, not `scripts/`.

For example:

```
scripts/
  llm/
    main.py
    utils.py
tests/
  llm/
    test_main.py
    test_utils.py
```

That way, your tests are separate from your implementation, and tools like `pytest` can easily discover them.

👉 You can now add something like:

```python
# tests/llm/test_basic.py
import pytest
from scripts.llm import utils

def test_addition():
    assert utils.add(2, 3) == 5
```

Then run:

```bash
pytest tests/llm/
```

Would you like me to also show you how to set up a `conftest.py` so you can share fixtures across your `tests/llm/` files?
