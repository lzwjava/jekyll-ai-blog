---
audio: false
generated: true
image: false
lang: en
layout: post
title: Load Environment Variables Conditionally
translated: false
type: note
---

Fixed. Here's what I changed in ~/.hermes/plugins/note/init.py:

    python
    Load ww's .env so LLM calls work even without shell-level exports
    try:
        from dotenv import load_dotenv
        load_dotenv(Path.home() / "projects" / "ww" / ".env", override=False)
    except ImportError:
        pass


    Key detail: override=False — if you already have MODEL set in your shell, it won't be overwritten. It only fills in missing vars from ww's .env.

    The try/except ImportError handles the edge case where python-dotenv isn't installed (it almost certainly is, but defensive).

    Try /note again — it should work now.