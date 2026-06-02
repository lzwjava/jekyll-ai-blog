---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 语言识别代码与置信度
translated: true
type: note
---

在 `langid` 中，`classify(text)` 函数返回一个元组 `(lang, confidence)`，其中：

* **`lang`** 是双字母 ISO 639-1 语言代码（有时会扩展包含地区代码，如 `zh-cn` 或 `zh-tw`）
* **`confidence`** 是介于 0 到 1 之间的浮点数，表示模型的置信度

`lang` 的可能取值集合来自 `langid.py` 支持的语言。默认包含 **97 种语言**，常见示例如下：

* `en` → 英语
* `zh` / `zh-cn` / `zh-tw` → 中文（通用/简体/繁体）
* `ja` → 日语
* `ko` → 韩语
* `fr` → 法语
* `de` → 德语
* `es` → 西班牙语
* `hi` → 印地语
* `ar` → 阿拉伯语
* `ru` → 俄语

此外还涵盖许多其他语言——完整列表包含世界上主要语种（南非荷兰语、孟加拉语、希腊语、希伯来语、意大利语、葡萄牙语、斯瓦希里语、泰语、土耳其语、越南语等）。

👉 如果您需要，我可以提供 `langid` 支持的 **97 个语言代码完整列表**。需要我输出这个列表吗？
