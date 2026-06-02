---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Fixing Python 3.13 Regex Error
translated: false
type: note
---

The error you're seeing is caused by **Python 3.13** being stricter about regular expression syntax than previous versions.

Specifically, this line in `wikiextractor/extract.py` (around line 378) is now invalid in Python 3.13:

```python
ExtLinkBracketedRegex = re.compile(
    '\\[(((?i)' + '|'.join(wgUrlProtocols) + ')' + EXT_LINK_URL_CLASS + r'+)\s*([^\\]\x00-\x08\x0a-\x1F]*?)\\]',
    re.S | re.U)
```

The problem is the inline `(?i)` flag placed in the middle of the string after string concatenation. Starting with Python 3.12/3.13, **inline flags like `(?i)` are no longer allowed anywhere except at the very beginning of the regex pattern**.

### Quick Fix (works on Python 3.13)

Edit the file:

```bash
~/.local/lib/python3.13/site-packages/wikiextractor/extract.py
```

Go to line ~378 and replace the broken block with this corrected version:

```python
# Old broken way (fails on Python 3.13)
# ExtLinkBracketedRegex = re.compile(
#     '\\[(((?i)' + '|'.join(wgUrlProtocols) + ')' + EXT_LINK_URL_CLASS + r'+)\s*([^\\]\x00-\x08\x0a-\x1F]*?)\\]',
#     re.S | re.U)

# Fixed version – move the case-insensitivity flag to the re.compile flags
protocol_pattern = '|'.join(wgUrlProtocols)
ExtLinkBracketedRegex = re.compile(
    r'\\['
    r'(((' + protocol_pattern + r')' + EXT_LINK_URL_CLASS + r'+)'
    r'\s*([^\\]\x00-\x08\x0a-\x1F]*?)\\])',
    re.IGNORECASE | re.DOTALL | re.UNICODE
)
```

Or even cleaner (recommended):

```python
ExtLinkBracketedRegex = re.compile(
    r'\\['
    r'(((' + '|'.join(wgUrlProtocols) + r')' + EXT_LINK_URL_CLASS + r'+)'
    r'\s*([^\\]\x00-\x08\x0a-\x1F]*?)\\])',
    re.I | re.S | re.U
)
```

`re.I` is the same as `re.IGNORECASE`, and it can be passed as a flag instead of embedding `(?i)` inside the pattern.

### Alternative solutions

1. Use Python 3.11 or 3.12 (easiest if you don’t want to patch)
   ```bash
   python3.11 -m pip install wikiextractor
   # then run with python3.11 wikiextractor ...
   ```

2. Use the maintained fork that already fixes Python 3.13 compatibility:
   ```bash
   pip uninstall wikiextractor
   pip install git+https://github.com/attardi/wikiextractor.git
   ```

   Giuseppe Attardi’s fork has been updated for Python 3.12+ and works perfectly on 3.13.

3. Use the very fast modern alternative (highly recommended for large dumps):
   ```bash
   pip install wikiextractor-ng   # or "wiki-dump-tools", "wikitextprocessor", etc.
   ```

After applying the patch or switching to the fixed fork, your command will work again:

```bash
wikiextractor *.bz2
```

Let me know if you want a one-liner patch or the exact `sed` command to fix it automatically.
