---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 确定性文件名slug生成
translated: true
type: note
---

整洁且正确。以下是第二次修复的总结：

**问题：** 第二次 LLM 调用（用于 `short_title`）出现了同样的问题——模型胡言乱语，生成了如 `basedonthetitlerequirementhereisaconcisefilenameblockchain-learning-reflectionmd` 这样的垃圾内容。在 `_validate_and_clean_short_title` 剥离所有非字母数字字符后，这些啰嗦的文字堆成了一个没有连字符的长单词，无法通过“最多 8 个词”的验证。

**修复：** 完全移除了第二次 LLM 调用。不再要求模型生成文件名 slug（这是一个纯机械性任务），而是通过 `_title_to_slug` 从 `full_title` 中程序化地派生它：

1. 转为小写、移除引号、将空格替换为连字符
2. 剥离非 a-z0-9- 的字符
3. 合并重复的连字符
4. 截断至最多 8 个词、最多 80 个字符

**为什么这样更好：**
- LLM 胡言乱语的风险为零——这纯粹是字符串操作
- 减少一次 API 调用（节省时间和金钱）
- 确定性——相同的标题总是生成相同的 slug
- 该 slug 派生逻辑已在 `_titles_from_custom`（第 42-45 行）中得到验证，此处只是应用相同方法并做更优验证