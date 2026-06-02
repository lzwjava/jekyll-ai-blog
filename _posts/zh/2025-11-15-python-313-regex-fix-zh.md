---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 修复Python 3.13正则表达式错误
translated: true
type: note
---

您遇到的错误是因为 **Python 3.13** 对正则表达式语法比之前的版本更加严格。

具体来说，`wikiextractor/extract.py` 中（大约第 378 行）的这行代码在 Python 3.13 中现已无效：

```python
ExtLinkBracketedRegex = re.compile(
    '\\[(((?i)' + '|'.join(wgUrlProtocols) + ')' + EXT_LINK_URL_CLASS + r'+)\s*([^\\]\x00-\x08\x0a-\x1F]*?)\\]',
    re.S | re.U)
```

问题在于内联的 `(?i)` 标志被放在了字符串连接之后的字符串中间。从 Python 3.12/3.13 开始，**像 `(?i)` 这样的内联标志只允许出现在正则表达式模式的最开头，其他地方不再允许**。

### 快速修复（适用于 Python 3.13）

编辑文件：

```bash
~/.local/lib/python3.13/site-packages/wikiextractor/extract.py
```

找到大约第 378 行，将损坏的代码块替换为以下修正版本：

```python
# 旧的错误方式（在 Python 3.13 上失败）
# ExtLinkBracketedRegex = re.compile(
#     '\\[(((?i)' + '|'.join(wgUrlProtocols) + ')' + EXT_LINK_URL_CLASS + r'+)\s*([^\\]\x00-\x08\x0a-\x1F]*?)\\]',
#     re.S | re.U)

# 修正版本 – 将大小写不敏感标志移至 re.compile 的标志参数中
protocol_pattern = '|'.join(wgUrlProtocols)
ExtLinkBracketedRegex = re.compile(
    r'\\['
    r'(((' + protocol_pattern + r')' + EXT_LINK_URL_CLASS + r'+)'
    r'\s*([^\\]\x00-\x08\x0a-\x1F]*?)\\])',
    re.IGNORECASE | re.DOTALL | re.UNICODE
)
```

或者更简洁的方式（推荐）：

```python
ExtLinkBracketedRegex = re.compile(
    r'\\['
    r'(((' + '|'.join(wgUrlProtocols) + r')' + EXT_LINK_URL_CLASS + r'+)'
    r'\s*([^\\]\x00-\x08\x0a-\x1F]*?)\\])',
    re.I | re.S | re.U
)
```

`re.I` 与 `re.IGNORECASE` 相同，可以作为标志传递给 `re.compile`，而不是在模式内部嵌入 `(?i)`。

### 替代解决方案

1.  使用 Python 3.11 或 3.12（如果不想打补丁，这是最简单的方法）
    ```bash
    python3.11 -m pip install wikiextractor
    # 然后使用 python3.11 wikiextractor ... 运行
    ```

2.  使用已修复 Python 3.13 兼容性的维护分支：
    ```bash
    pip uninstall wikiextractor
    pip install git+https://github.com/attardi/wikiextractor.git
    ```

    Giuseppe Attardi 的分支已经更新以支持 Python 3.12+，并且在 3.13 上运行良好。

3.  使用非常快速的现代替代方案（对于大型转储文件高度推荐）：
    ```bash
    pip install wikiextractor-ng   # 或者 "wiki-dump-tools", "wikitextprocessor" 等
    ```

应用补丁或切换到已修复的分支后，您的命令将再次正常工作：

```bash
wikiextractor *.bz2
```

如果您需要一行式补丁或自动修复的精确 `sed` 命令，请告诉我。
