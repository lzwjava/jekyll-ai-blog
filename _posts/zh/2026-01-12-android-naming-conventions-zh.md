---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Android 命名规范以提高可读性
translated: true
type: note
---

我非常同意！Android 的命名规范是清晰、易读代码的典范。以下是它们遵循的核心原则：

## 为什么使用完整单词效果更好

**Android 中的优秀示例：**
- `wrap_content` 而不是 `wrp_cnt`
- `match_parent` 而不是 `mtch_prnt`
- `onClickListener` 而不是 `onClkLstnr`

**带来的好处：**
- **瞬间可读** - 不需要脑内转换
- **易于搜索** - 你可以轻松使用 grep 查找 `wrap_content`
- **自说明性** - 新开发者能立即理解
- **避免歧义** - `btn` 可能是 "button" 也可能是 "between"

## 黄金法则：简短且清晰

最好的命名既简洁又完整：
- `src` vs `source` - `src` 是全行业通用的
- `temp` vs `temperature` - 上下文能让 `temp` 的含义很明确
- `config` vs `configuration` - 常见的缩写，广为人知
- `id` vs `identifier` - `id` 已成为标准

## 何时可以使用缩写

缩写在以下情况适用：
1. **领域标准 (Domain standard)** - `html`, `json`, `api`, `url`
2. **通用常识** - `max`, `min`, `avg`
3. **极度常见** - `num`, `str`, `err`

## 何时必须使用完整单词

在以下场景中始终优先使用完整单词：
- **Business logic** - `calculateInvoiceTotal` 而不是 `calcInvTot`
- **领域概念** - `customerAddress` 而不是 `custAddr`
- **较少见的术语** - `threshold` 而不是 `thrshld`

核心指导原则：为阅读进行优化，而不是为编写。代码被阅读的次数远比编写的次数多 10 倍以上。
