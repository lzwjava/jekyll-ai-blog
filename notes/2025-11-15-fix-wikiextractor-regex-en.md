---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Fix wikiextractor Python 3.13 Regex Error
translated: false
type: note
---

The error you're encountering is due to a compatibility issue in the `wikiextractor` package with Python 3.13's stricter handling of regular expression inline flags. Specifically, the `(?i)` flag in the regex pattern is being interpreted as a global flag, but it's not positioned at the very start of the expression, leading to the `re.PatternError`.

To fix this, edit the file `/home/lzw/.local/lib/python3.13/site-packages/wikiextractor/extract.py` and modify line 378 (or the nearby `ExtLinkBracketedRegex` definition) as follows:

- Original: `'\\[(((?i)' + '|'.join(wgUrlProtocols) + ')' + EXT_LINK_URL_CLASS + r'+)\s*([^\\]\x00-\x08\x0a-\x1F]*?)\\]',`
- Updated: `'\\[(((?i:' + '|'.join(wgUrlProtocols) + ')' + EXT_LINK_URL_CLASS + r'+)\s*([^\\]\x00-\x08\x0a-\x1F]*?)\\]',`

This adds a `:` after `(?i`, changing it to a local inline flag `(?i:...)` that applies only to the protocol matching group, which resolves the parsing error.

Additionally, the `SyntaxWarning: invalid escape sequence '\\['` warnings are from non-raw strings containing escapes that Python 3.13 treats more strictly (though they don't cause the main failure). You can ignore them for now, or update those strings to raw strings (e.g., `r'\\['`) in the same file if they bother you.

After editing, rerun `wikiextractor *.bz2`. If the package is outdated, consider checking for updates via `pip install --upgrade wikiextractor` or using a virtual environment with an older Python version (e.g., 3.10) as a workaround.
