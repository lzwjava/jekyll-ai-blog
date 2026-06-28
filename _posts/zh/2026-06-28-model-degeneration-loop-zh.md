---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 模型退化循环
translated: true
type: note
---

好了，给你1000个新令牌。情况只会越来越糟：

- 第1-48行：提示词逐字重放（正常）
- 第49-65行：混乱的类似Java的代码，包含随机的类名和方法名
- 第66行之后：崩溃成重复的 `S.S.S.S.S` 模式，随机标点，`this.S.S.BufferType = array.S.S.S.S = null` 等等

大约在200个令牌后就进入了退化循环——模型不知道接下来该生成什么，只是在高概率的垃圾令牌之间循环。`S.S.S.S.S` 的重复表明令牌分布已经坍缩到一个狭窄的模式中。

这是小型语言模型的典型失败模式——它们能记住训练样本，但无法组成新的序列。