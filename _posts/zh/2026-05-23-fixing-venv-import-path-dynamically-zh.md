---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 动态修复venv导入路径
translated: true
type: note
---

以下是修复的完整总结：

## 问题

`/note` 命令执行失败，错误信息为：

```
'ww' package not installed. Install with: pip install -e ~/projects/ww
```

## 根本原因

Hermes Agent 运行在它自己的隔离 Python 虚拟环境中，路径为 `~/.hermes/hermes-agent/venv/`。`ww` 包已安装在系统 Python（`/opt/homebrew/bin/python3.11`）中，但**未**安装在 Hermes 的 venv 中。当插件尝试执行 `from ww.note.create_note_from_clipboard import create_note_from_content` 时，失败的原因有两个：

1. `ww` 不在 venv 的 `site-packages` 中
2. 即使我们用 `pip install -e ~/projects/ww` 安装了它，依赖项 `pyperclip` 也同样缺失

## 解决方案（两部分）

### 第一部分：插件代码修改（`~/.hermes/plugins/note/__init__.py`）

**修改前：**

```python
try:
    from ww.note.create_note_from_clipboard import create_note_from_content
except ImportError:
    return "'ww' package not installed. Install with: pip install -e ~/projects/ww"
```

**修改后：**

```python
try:
    from ww.note.create_note_from_clipboard import create_note_from_content
except ImportError:
    # Add ww project to path if not installed in current venv
    import sys
    ww_path = str(Path.home() / "projects" / "ww")
    if ww_path not in sys.path:
        sys.path.insert(0, ww_path)
    try:
        from ww.note.create_note_from_clipboard import create_note_from_content
    except ImportError:
        return "'ww' package not installed. Install with: pip install -e ~/projects/ww"
```

**为什么这样可行：**

- 不再要求 `ww` 必须在每个 Python 环境中通过 pip 安装，插件现在动态地将源目录添加到 `sys.path`
- 这使得可以直接从 `~/projects/ww/` 的源代码树导入
- 如果源目录不存在，保留原有的错误提示信息

### 第二部分：安装缺失的依赖

```bash
~/.hermes/hermes-agent/venv/bin/python -m ensurepip
~/.hermes/hermes-agent/venv/bin/python -m pip install pyperclip
```

**为什么需要这一步：**

- `ww` 依赖于 `pyperclip` 进行剪贴板操作
- 即使将源目录添加到 `sys.path`，如果依赖项没有安装，导入链也会失败
- `pyperclip` 安装在系统 Python 中，但不在 Hermes 的 venv 中

## 验证

```bash
~/.hermes/hermes-agent/venv/bin/python -c "
import sys
from pathlib import Path
ww_path = str(Path.home() / 'projects' / 'ww')
if ww_path not in sys.path:
    sys.path.insert(0, ww_path)
from ww.note.create_note_from_clipboard import create_note_from_content
print('Import successful!')
"
# 输出: Import successful!
```

## 关键见解

Hermes 插件运行在 Hermes 隔离的 venv 中，而不是系统 Python。当插件依赖于本地包（如 `ww`）时，有两种选择：

1. **在 venv 中安装** — `~/.hermes/hermes-agent/venv/bin/pip install -e ~/projects/ww`（需要所有依赖项）
2. **添加到 sys.path** — 动态注入源目录（我们采用的方式）

选项 2 更稳健，因为它不需要在每个环境中通过 pip 安装该包及其依赖项。
