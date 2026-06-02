---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复推理模型令牌限制
translated: true
type: note
---

已经修复了两个文件。以下是总结：

    问题：DeepSeek v4 Flash 是一个推理模型 —— 它在可见答案之前生成内部 chain-of-thought。当 max_tokens=60 时，仅推理就消耗了全部预算，导致 content: null 且 finish_reason: "length"。

    修复：在两个文件中将 max_tokens 从 60 增加到 300：
    - /home/xiaoxin/projects/ww/ww/note/create_note_utils.py:75
    - /home/xiaoxin/projects/ww/ww/note/screenshot_log.py:102

    300 tokens 足够为推理 + 大约 6 个词的标题提供余量。模型仍会产生你想要的简短输出 —— 额外的预算只是给推理阶段留出了空间。

    为什么之前 60 能用：你很可能使用的是非推理模型（旧版 DeepSeek、GPT、Claude），它们没有单独的推理/思考阶段。那些模型直接将 tokens 转化为可见输出，所以 60 tokens 对于"最多 6 个词"来说是足够的。切换到 deepseek/deepseek-v4-flash 后，它增加了推理 tokens。

    再试一次 ww note —— 现在应该可以了。
