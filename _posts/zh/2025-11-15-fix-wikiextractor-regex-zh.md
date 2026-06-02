---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 修复wikiextractor在Python 3.13中的正则表达式错误
translated: true
type: note
---

您遇到的错误是由于 `wikiextractor` 包与 Python 3.13 对正则表达式内联标志更严格的处理方式存在兼容性问题。具体来说，正则表达式模式中的 `(?i)` 标志被解释为全局标志，但未定位在表达式开头，导致 `re.PatternError` 错误。

要修复此问题，请编辑文件 `/home/lzw/.local/lib/python3.13/site-packages/wikiextractor/extract.py` 并修改第 378 行（或附近的 `ExtLinkBracketedRegex` 定义）：

- 原代码：`'\\[(((?i)' + '|'.join(wgUrlProtocols) + ')' + EXT_LINK_URL_CLASS + r'+)\s*([^\\]\x00-\x08\x0a-\x1F]*?)\\]'`
- 修改为：`'\\[(((?i:' + '|'.join(wgUrlProtocols) + ')' + EXT_LINK_URL_CLASS + r'+)\s*([^\\]\x00-\x08\x0a-\x1F]*?)\\]'`

通过在 `(?i` 后添加冒号，将其改为局部内联标志 `(?i:...)`，该标志仅适用于协议匹配组，从而解决解析错误。

此外出现的 `SyntaxWarning: invalid escape sequence '\\['` 警告来自包含转义符的非原始字符串（Python 3.13 对此处理更严格，但不会导致主要故障）。目前可暂时忽略这些警告，若需处理可在同一文件中将这些字符串更新为原始字符串（例如改为 `r'\\['`）。

编辑完成后重新运行 `wikiextractor *.bz2`。如果软件包版本过旧，建议通过 `pip install --upgrade wikiextractor` 检查更新，或使用旧版 Python（如 3.10）的虚拟环境作为临时解决方案。
