---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Pi Agent 插件开发指南
translated: true
type: note
---

问题：如何为 Pi Agent 编写这样的插件？

答案：

您展示的插件具有非常常见的架构：

```
用户输入:
/note --title "..."

        │
        ▼
插件加载器
        │
        ▼
register(ctx)
        │
        ▼
ctx.register_command(...)
        │
        ▼
处理函数(raw_args)
        │
        ▼
访问对话历史
        │
        ▼
处理数据
        │
        ▼
返回字符串到 CLI
```

核心概念包括：

* 插件发现
* 注册
* 上下文对象
* 命令处理函数
* 可选的生命周期钩子

---

## 最小插件 API

假设 Pi Agent 暴露类似以下内容：

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

那么每个插件只需要

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

然后

```
/hello OpenAI
```

变成

```
Hello OpenAI
```

---

## plugin.yaml

```yaml
name: hello
version: 1.0
entry: __init__.py
description: 示例插件
```

加载器读取

```
~/.pi/plugins/
    hello/
        plugin.yaml
        __init__.py
```

并导入

```python
plugin.register(ctx)
```

---

# 访问历史记录

与 Hermes 完全相同。

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

现在你的插件可以总结

```python
def summary(args):
    text = last_assistant()

    return text[:300]
```

---

# 调用 Agent API

无需直接操作文件

```python
_ctx.agent.add_note(...)
```

或

```python
_ctx.agent.memory.save(...)
```

或

```python
_ctx.agent.vector_store.insert(...)
```

例如

```python
def remember(args):
    _ctx.agent.memory.save(args)
    return "已保存。"
```

---

# 注册多个命令

```python
def register(ctx):

    ctx.register_command(
        "note",
        note_handler,
        description="保存笔记"
    )

    ctx.register_command(
        "summary",
        summary_handler,
        description="总结"
    )

    ctx.register_command(
        "clip",
        clip_handler,
        description="复制回复"
    )
```

---

# 事件钩子（推荐）

除了仅有的斜杠命令，还可以暴露生命周期钩子。

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

这样，插件可以自动存档每一条回答，而无需使用 `/note`。

示例：

```python
def on_after_llm(response):

    if len(response) > 500:
        save(response)
```

---

# 建议的 Pi Agent 插件接口

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

这大致是成熟 Agent 框架所使用的抽象层次。

---

# 示例笔记插件

```python
def note(args):

    text = _ctx.history.last_assistant()

    _ctx.storage.enqueue(
        queue="notes",
        content=text,
        title=args
    )

    return "已加入队列。"
```

请注意，它避免访问像

```python
_ctx._manager._cli_ref
```

这样的私有字段，因为这会使得插件与内部实现细节紧密耦合。暴露稳定的 API，如 `ctx.history.last_assistant()` 和 `ctx.storage.enqueue()`，可以使插件更易于编写、测试，并在不同 Pi Agent 版本间保持兼容。

参考资料：

* Hermes 插件示例（你的代码）
* Pluggy（pytest 插件系统）：[https://pluggy.readthedocs.io/](https://pluggy.readthedocs.io/)
* Stevedore（OpenStack 插件管理器）：[https://docs.openstack.org/stevedore/latest/](https://docs.openstack.org/stevedore/latest/)