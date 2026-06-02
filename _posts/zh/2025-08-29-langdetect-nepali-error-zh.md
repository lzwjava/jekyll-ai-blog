---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 语言检测误将文本识别为尼泊尔语
translated: true
type: note
---

啊，原来如此——感谢说明。

在你粘贴的日志中：

```
Debug: raw langdetect output: [('ne', 0.9999953270916105)]
Debug: normalized langdetect output: [('ne', 0.9999953270916105)]
Debug: Detected languages: [('ne', 0.9999953270916105)]
```

这里的 **`ne` 并非法语单词**——它实际上是 `langdetect` 输出的**语言代码**。

`langdetect` 库有时会返回 `"ne"` 作为**尼泊尔语**的 ISO 639-1 代码。

* `"en"` = 英语
* `"fr"` = 法语
* `"hi"` = 印地语
* `"ne"` = 尼泊尔语

因此在这种情况下，`langdetect` 认为你的文本有 `~0.99999` 的概率是尼泊尔语。

这就是你的验证失败并显示以下信息的原因：

```
Translated text does not contain the target language 'hi' (detected: [('ne', 0.9999953270916105)])
```

👉 总结如下：

* 此处的 `ne` = **尼泊尔语**的 ISO 语言代码，而非法语否定词 `"ne"`。
* 当 `langdetect` 判定你的输入类似尼泊尔语时，就会出现此代码。

需要我为你演示如何**规范化或重映射** `ne`（尼泊尔语）到你的 `_map_target_code` 中，以避免验证器在遇到意外语言时出错吗？
