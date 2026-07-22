---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pi Agent Plugin Development Guide
translated: false
type: note
---

Question: How do I write a plugin like this for the Pi Agent?

Answer:

The plugin you showed has a very common architecture:

```
User types:
/note --title "..."

        │
        ▼
Plugin loader
        │
        ▼
register(ctx)
        │
        ▼
ctx.register_command(...)
        │
        ▼
handler(raw_args)
        │
        ▼
access conversation history
        │
        ▼
process data
        │
        ▼
return string to CLI
```

The key ideas are:

* plugin discovery
* registration
* context object
* command handler
* optional lifecycle hooks

---

## Minimal plugin API

Suppose Pi Agent exposes something like

```python
class PluginContext:
    agent
    cli

    def register_command(
        self,
        name,
        handler,
        description="",
        args_hint=""
    ):
        ...
```

Then every plugin only needs

```
my_plugin/
    __init__.py
    plugin.yaml
```

---

## **init**.py

```python
from pathlib import Path

_ctx = None

def hello(args):
    return f"Hello {args}"

def register(ctx):
    global _ctx
    _ctx = ctx

    ctx.register_command(
        "hello",
        handler=hello,
        description="Say hello",
        args_hint="<name>"
    )
```

Then

```
/hello OpenAI
```

becomes

```
Hello OpenAI
```

---

## plugin.yaml

```yaml
name: hello
version: 1.0
entry: __init__.py
description: Example plugin
```

The loader reads

```
~/.pi/plugins/
    hello/
        plugin.yaml
        __init__.py
```

and imports

```python
plugin.register(ctx)
```

---

# Accessing history

Exactly like Hermes.

```python
def last_assistant():
    history = _ctx.cli.history

    assistants = [
        m
        for m in history
        if m["role"] == "assistant"
    ]

    return assistants[-1]["content"]
```

Now your plugin can summarize

```python
def summary(args):
    text = last_assistant()

    return text[:300]
```

---

# Calling agent APIs

Instead of touching files directly

```python
_ctx.agent.add_note(...)
```

or

```python
_ctx.agent.memory.save(...)
```

or

```python
_ctx.agent.vector_store.insert(...)
```

For example

```python
def remember(args):
    _ctx.agent.memory.save(args)
    return "Saved."
```

---

# Register multiple commands

```python
def register(ctx):

    ctx.register_command(
        "note",
        note_handler,
        description="Save note"
    )

    ctx.register_command(
        "summary",
        summary_handler,
        description="Summarize"
    )

    ctx.register_command(
        "clip",
        clip_handler,
        description="Copy response"
    )
```

---

# Event hooks (recommended)

Rather than only slash commands, expose lifecycle hooks.

```python
def on_start(ctx):
    ...

def on_before_llm(prompt):
    ...

def on_after_llm(response):
    ...

def on_exit():
    ...
```

Then a plugin can automatically archive every answer without requiring `/note`.

Example:

```python
def on_after_llm(response):

    if len(response) > 500:
        save(response)
```

---

# Suggested Pi Agent plugin interface

```python
class PluginContext:

    config

    logger

    history

    workspace

    cache_dir

    register_command(...)

    register_hook(...)

    run_shell(...)

    ask_llm(...)

    current_model

    conversation

    clipboard

    notify()

    storage
```

This is roughly the level of abstraction used by mature agent frameworks.

---

# Example note plugin

```python
def note(args):

    text = _ctx.history.last_assistant()

    _ctx.storage.enqueue(
        queue="notes",
        content=text,
        title=args
    )

    return "Queued."
```

Notice how it avoids reaching into private fields like:

```python
_ctx._manager._cli_ref
```

which tightly couples the plugin to internal implementation details. Exposing stable APIs such as `ctx.history.last_assistant()` and `ctx.storage.enqueue()` makes plugins easier to write, test, and keep compatible across Pi Agent versions.

References:

* Hermes plugin example (your code)
* Pluggy (pytest plugin system): [https://pluggy.readthedocs.io/](https://pluggy.readthedocs.io/)
* Stevedore (OpenStack plugin manager): [https://docs.openstack.org/stevedore/latest/](https://docs.openstack.org/stevedore/latest/)
