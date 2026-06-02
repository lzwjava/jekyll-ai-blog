---
audio: false
generated: true
image: false
lang: en
layout: post
title: Unittest vs Pytest Key Differences
translated: false
type: note
---

Here’s a crisp, no-table comparison focused on what actually changes in your day-to-day testing.

# Philosophy & Style

* **unittest**: xUnit style (Java/JUnit vibe). Class-based tests, lifecycle hooks like `setUp/tearDown`, method names must start with `test_`.
* **pytest**: Pythonic and minimal. Test **functions** or classes, rich fixtures, plain `assert` with assertion rewriting.

# Test Discovery

* **unittest**: `python -m unittest discover` (or load suites). Looks for `test*.py`, `TestCase` subclasses.
* **pytest**: `pytest` auto-discovers `test_*.py` and `*_test.py`; functions `test_*` and methods on `Test*` classes.

# Assertions

* **unittest**: Many specific methods (`assertEqual`, `assertTrue`, `assertRaises`, …).
* **pytest**: Use plain `assert` and it prints expressive diffs (“left vs right”), supports `pytest.raises`.

# Fixtures & Setup

* **unittest**: `setUp()/tearDown()`, `setUpClass/tearDownClass`, `setUpModule/tearDownModule`.
* **pytest**: **Fixtures** with scopes (function/class/module/session), dependency injection, autouse, finalizers. Encourages small, reusable setup.

# Parametrization

* **unittest**: No built-in; use loops/subTests or 3rd-party libs.
* **pytest**: `@pytest.mark.parametrize` is first-class (matrix of inputs, clean reporting).

# Skips, Expected Failures, Markers

* **unittest**: `@skip`, `@skipIf`, `@expectedFailure`.
* **pytest**: Same ideas plus powerful **markers** (`@pytest.mark.slow`, `xfail`, `filterwarnings`, custom marks) and command-line selection (`-m slow`).

# Plugins & Ecosystem

* **unittest**: Batteries-included but lean; relies on external runners/tools for advanced features.
* **pytest**: Huge plugin ecosystem (`pytest-xdist` for parallel, `pytest-randomly`, `pytest-cov`, `pytest-mock`, `pytest-asyncio`, `pytest-django`, etc.).

# Mocks

* **unittest**: `unittest.mock` is standard; works everywhere.
* **pytest**: Use `unittest.mock` or `pytest-mock`’s `mocker` fixture (cleaner patching & auto-teardown).

# Async Testing

* **unittest**: Since 3.8, has `IsolatedAsyncioTestCase` (ok but verbose).
* **pytest**: With `pytest-asyncio` (or trio’s plugin) you get `@pytest.mark.asyncio` and fixture support for event loops.

# Performance & Parallel

* **unittest**: No built-in parallel; use `unittest-parallel`/CI tricks.
* **pytest**: `pytest-xdist -n auto` is the go-to.

# IDE/CI/Coverage

* Both integrate with IDEs and CI. Coverage via `coverage.py`:

  * **unittest**: `coverage run -m unittest` → `coverage report`.
  * **pytest**: `pytest --cov=your_pkg` with `pytest-cov`.

# When to choose which

* **Choose unittest** if:

  * You need only the stdlib (no external deps).
  * You’re plugging into legacy/xUnit codebases or strict org policies.
* **Choose pytest** if:

  * You want faster authoring, clearer failures, and powerful fixtures/parametrization.
  * You’ll benefit from its plugin ecosystem and parallelization.

# Interop & Migration

You can run **unittest** suites under **pytest** (pytest finds `unittest.TestCase`s). This lets you migrate gradually:

1. Start invoking `pytest` as the runner.
2. Add pytest tests alongside existing ones.
3. Introduce fixtures/parametrize where they help.
4. Optionally refactor old `TestCase`s to functions later.

# Tiny side-by-side examples

## The same test

**unittest**

```python
import unittest

class TestMath(unittest.TestCase):
    def setUp(self):
        self.data = [1, 2, 3]

    def test_sum(self):
        self.assertEqual(sum(self.data), 6)

    def test_raises(self):
        with self.assertRaises(ZeroDivisionError):
            1 / 0

if __name__ == "__main__":
    unittest.main()
```

**pytest**

```python
import pytest

@pytest.fixture
def data():
    return [1, 2, 3]

def test_sum(data):
    assert sum(data) == 6

def test_raises():
    with pytest.raises(ZeroDivisionError):
        1 / 0
```

## Parametrization

**unittest (subTest)**

```python
import unittest

class TestParity(unittest.TestCase):
    def test_even(self):
        for n in [0, 2, 4]:
            with self.subTest(n=n):
                self.assertEqual(n % 2, 0)
```

**pytest**

```python
import pytest

@pytest.mark.parametrize("n", [0, 2, 4])
def test_even(n):
    assert n % 2 == 0
```

## Mocking

**unittest.mock**

```python
from unittest.mock import patch

@patch("pkg.api.fetch_user", return_value={"id": 1})
def test_uses_api(mock_fetch):
    from pkg.service import get_user
    assert get_user(1)["id"] == 1
    mock_fetch.assert_called_once_with(1)
```

**pytest-mock**

```python
def test_uses_api(mocker):
    mock_fetch = mocker.patch("pkg.api.fetch_user", return_value={"id": 1})
    from pkg.service import get_user
    assert get_user(1)["id"] == 1
    mock_fetch.assert_called_once_with(1)
```

# Practical recommendations

* New projects: default to **pytest** for speed, readability, and ecosystem.
* Legacy/stdlib-only environments: stick with **unittest**, but consider running it via **pytest** to unlock better output and plugins without rewriting tests.
* Add `pytest-xdist` early for faster CI, and `pytest-cov` for coverage.
* Use fixtures over large class setups; keep them small and composable.
* Use markers to organize suites (`slow`, `integration`, `db`) and run subsets in CI stages.

If you want, tell me your project layout and constraints (stdlib-only? need parallel? async? Django/Flask/FastAPI?) and I’ll sketch a minimal, opinionated test setup for you.
