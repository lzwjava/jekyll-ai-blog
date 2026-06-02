---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Requests Dependency Warning Quickly
translated: false
type: note
---

Question: How do I fix the `RequestsDependencyWarning` about urllib3 or chardet/charset_normalizer not matching a supported version?

Answer:

## Understanding the Warning

This warning means the installed versions of `urllib3`, `chardet`, or `charset_normalizer` are **incompatible with the version of `requests`** installed in your Python environment (`/opt/homebrew/lib/python3.14`). It does **not** break functionality, but it signals a version mismatch.

---

## Fix Options (Best to Try in Order)

### ✅ Option 1 — Upgrade all three packages together (Recommended)

This is the most reliable fix. Upgrade `requests`, `urllib3`, and `charset-normalizer` to mutually compatible versions:

```bash
pip3.14 install --upgrade requests urllib3 charset-normalizer
```

Since you're on macOS with Homebrew Python, you may need:

```bash
pip3 install --upgrade requests urllib3 charset-normalizer
```

---

### ✅ Option 2 — Reinstall `requests` cleanly

Sometimes a fresh reinstall resolves dependency resolution automatically:

```bash
pip3 install --force-reinstall requests
```

---

### ✅ Option 3 — Use a virtual environment (Best Practice)

Since your path is `/opt/homebrew/lib/python3.14`, you're installing packages globally into Homebrew Python. This often causes version conflicts with other tools. Using a virtual environment isolates your project:

```bash
python3.14 -m venv myenv
source myenv/bin/activate
pip install requests urllib3 charset-normalizer
```

---

### ✅ Option 4 — Suppress the warning (Quick workaround)

If you just want to silence it without fixing the root cause, add this to the top of your Python script:

```python
import warnings
from requests import packages
warnings.filterwarnings('ignore', category=packages.urllib3.exceptions.RequestsDependencyWarning)
```

Or run your script with:

```bash
python3 -W ignore::Warning your_script.py
```

---

### ✅ Option 5 — Check current versions and pinpoint the conflict

Run the following to see exactly what's installed:

```bash
pip3 show requests urllib3 chardet charset-normalizer
```

Then check [requests' PyPI page](https://pypi.org/project/requests/) to see what versions of `urllib3` and `charset-normalizer` it requires for your installed `requests` version, and adjust accordingly.

---

## Root Cause Summary

| Package | Role |
|---|---|
| `requests` | HTTP library — depends on urllib3 and charset detection |
| `urllib3` | Low-level HTTP client used by requests |
| `chardet` / `charset-normalizer` | Character encoding detection (requests uses one of these) |

The warning is triggered when `requests` detects that the installed versions of these dependencies are **outside the version ranges it was built to support**. The fix is to align all versions together — **Option 1** above usually solves it completely.

References:

- [requests changelog – supported chardet/charset_normalizer versions](https://requests.readthedocs.io/en/latest/community/updates/)
- [urllib3/urllib3 GitHub Issue #1571](https://github.com/urllib3/urllib3/issues/1571)
