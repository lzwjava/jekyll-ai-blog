---
audio: false
generated: true
image: false
lang: en
layout: post
title: Duplicate prevention fix call paths
translated: false
type: note
---

You're right to double-check. Let me trace the exact call paths:

**Call Path 1: Hermes `/note` plugin** (`ww/config/hermes/plugins/note/__init__.py`)
```python
# Line 143-152
try:
    file_path = create_note_from_content(text, custom_title=title, directory=note_dir)
except ValueError as e:
    return f"Note rejected: {e}"  # ← catches ValueError
```
✅ Has error handling - will catch duplicate ValueError

**Call Path 2: Research agent** (`ww/agent/research_agent.py`)
```python
# Line 108-114
try:
    file_path = create_note_from_content(content, custom_title=topic)
except Exception as e:
    print(f"Error using create_note_from_content: {str(e)}")  # ← catches Exception
```
✅ Has error handling - will catch duplicate ValueError

**Call Path 3: `create_note()`** (`create_note_from_clipboard.py` line 101-105)
```python
def create_note(date=None):
    if check_duplicate_notes():  # ← first check (clipboard vs notes)
        raise ValueError(...)
    content = get_clipboard_content()
    return create_note_from_content(content, date=date)  # ← second check (my fix)
```
✅ Now has double protection

**Summary:**
- Both callers (Hermes plugin, research agent) have proper exception handling
- They call `create_note_from_content()` **directly** without any prior duplicate check
- My fix adds duplicate checking inside `create_note_from_content()` which is the central function
- The ValueError will be caught by their existing `except` blocks

The fix is correct - it catches the exact gap where duplicates were being created.
