---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 手动编辑的YAML顺序中断测试
translated: true
type: note
---

## 根本原因

这里有两个层次共同作用：

**1. `scripts/create/file.py` 模板中没有 `prompt` 字段。**
该模板按以下顺序生成键：`audio, generated, image, lang, layout, title, translated` —— 已经是字母顺序，没有 `prompt`。因此新建的文件没有问题。

**2. 后来手动添加了 `prompt`，放在了 `title` 之后。**
在某个时间点，你（或某个编辑）添加了翻译提示：
```
prompt: 不要翻译不确定的项目名称、公司名称或学校名称等具体条目
```
正好放在 `title:` 之后。按字母顺序，`prompt` 应位于 `layout` 与 `title` 之间，而非其后。这一处手动编辑破坏了排序 —— 也正因如此，测试精确地标记了一个错位的键（`title` 出现在了本应是 `prompt` 的位置）。

**为什么翻译后的副本不会在此测试中失败：**
`scripts/translation/markdown_translate_client.py:54` 将字典传入 `yaml.dump(...)`，默认情况下会按字母顺序对键进行排序。因此 `-zh.md`、`-ja.md` 等文件顺序是正确的。但源文件 `-en.md` 从未经过 `yaml.dump` 的重新处理，所以手动编辑的顺序被原样保留。

**为什么 `_posts/en/...` 和 `original/...` 都会失败：**
它们是同一个文件，由 `publish.py:78`（`shutil.move`）移动而来 —— `publish.py` 不会规范化前置元数据。错误的顺序就此传播。

## 修复方案

- **快速修复（仅针对此文件）：** 将 `original/` 和 `_posts/en/` 两个副本中的 `prompt:` 行移至 `layout:` 与 `title:` 之间。
- **永久修复：** 要么在 `scripts/create/file.py` 模板中添加一个 `prompt: ""` 占位槽（按字母顺序位置），要么让 `publish.py` 在移动草稿前通过 `yaml.dump` 规范化键的顺序。

需要我对这两个文件应用快速修复，还是在 `publish.py` 中应用永久修复，或者两者都做？
