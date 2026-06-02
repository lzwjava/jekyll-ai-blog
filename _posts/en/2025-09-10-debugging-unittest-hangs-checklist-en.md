---
audio: false
date: 2025-09-10
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Debugging Unittest Hangs Checklist
translated: false
type: note
---

Hangs in `unittest` are usually from deadlocks (threads/async), stuck I/O, subprocess/multiprocessing issues, or a test waiting on a network call. Here’s a tight checklist to *see where it’s stuck* and *unstick it*—works on Python 3.9–3.11.

### 1) Run unittest verbosely (and correctly)

```bash
# If xx.py calls unittest.main()
python xx.py -v

# Or use discovery (recommended)
python -m unittest -v
python -m unittest discover -v -s tests -p "test_*.py"
```

> Note: `python -v` is **interpreter import-verbose**, not test-verbose. Use `-m unittest -v` for test names and progress.

### 2) Turn on faulthandler + dev mode (stack dumps on hang, stricter warnings)

```bash
# One-off
python -X faulthandler -X dev -u -m unittest -v
# Or via env
export PYTHONFAULTHANDLER=1
python -X dev -u -m unittest -v
```

* `-X faulthandler` lets Python print thread stack traces on fatal signals/timeouts.
* `-X dev` makes warnings/errors louder.
* `-u` unbuffers stdout/stderr so you *see* prints in real time.

### 3) Force a traceback when it seems stuck

Option A — from another terminal (Linux/macOS):

```bash
kill -SIGUSR1 <pid>  # with faulthandler enabled, dumps all thread stacks
```

Option B — add to your test bootstrap (top of `xx.py`):

```python
import faulthandler, signal, sys
faulthandler.enable()
# Dump stacks on SIGUSR1:
faulthandler.register(signal.SIGUSR1, all_threads=True)
# Also auto-dump if it hangs > 120s:
faulthandler.dump_traceback_later(120, repeat=True)
```

### 4) Trace execution step-by-step (heavy but decisive)

```bash
python -m trace --trace xx.py
# or
python -m trace --trace -m unittest discover -v
```

You’ll see every line executed; stop when the output “freezes”—that’s your hang site.

### 5) Use the debugger right away

```bash
python -m pdb xx.py         # if xx.py calls unittest.main()
# Break on a suspected line:
# (Pdb) b mymodule.py:123
# (Pdb) c
```

For discovery runs, add `import pdb; pdb.set_trace()` at the suspected spot.

### 6) Common causes & quick fixes

* **Multiprocessing on macOS/Windows**: always guard test entry.

  ```python
  if __name__ == "__main__":
      import unittest
      unittest.main()
  ```

  If you spawn processes in tests on macOS:

  ```python
  import multiprocessing as mp
  if __name__ == "__main__":
      mp.set_start_method("fork")  # sometimes avoids hangs vs default "spawn"
  ```

  (Only do this if you know your code is fork-safe.)

* **Thread deadlocks**: check for `join()` without timeouts, locks not released, or background threads waiting on main thread. Replace:

  ```python
  t.join()
  ```

  with:

  ```python
  t.join(timeout=5); assert not t.is_alive()
  ```

* **Async tests**: ensure you’re using `IsolatedAsyncioTestCase` (3.8+) or `asyncio.run()`. Double event loops or forgotten `await` often hang.

* **Network calls**: add **short timeouts** everywhere:

  ```python
  requests.get(url, timeout=5)
  ```

* **stdin waits**: remove `input()` or guard it in tests; CI/stdin can block forever.

* **Mocking gone wrong**: a mocked method that never resolves a `Future`/promise or a stubbed server not started.

### 7) Extra visibility

* See allocations if leak/spin is suspected:

  ```bash
  python -X tracemalloc=25 -m unittest -v
  ```
* Show import noise (rarely needed for hangs):

  ```bash
  python -v -m unittest -v
  ```

### 8) If it only hangs on one Python version

* Try both:

  ```bash
  pyenv local 3.11.9
  python -X faulthandler -X dev -m unittest -v

  pyenv local 3.9.19
  python -X faulthandler -X dev -m unittest -v
  ```

  Differences usually surface around `multiprocessing`, `asyncio`, or C-extension behavior.

---

If you paste the traceback from `faulthandler` (or the last lines from `trace --trace`), I’ll point to the exact culprit and suggest a targeted fix.
