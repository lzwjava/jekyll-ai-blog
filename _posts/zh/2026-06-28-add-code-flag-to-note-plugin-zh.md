---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为笔记插件添加 --code 标志
translated: true
type: note
---

完成。已更新 `~/.hermes/plugins/note/__init__.py`：

- 添加了 `--code` 标志解析
- 当设置了 `--code` 时：在入队前对助手响应内容调用 `wrap_code_snippets()`，并在队列条目中存储 `"code": true`
- 更新了文档字符串和 `args_hint`

用法：
```
/note --code              # 保存最后一条响应并包裹代码
/note 3 --code            # 保存第3条响应并包裹代码
/note --title "Foo" --code
```

队列条目像往常一样流经 `ww note watch` / `ww note process` —— 内容在入队时已经包裹，与 CLI 路径相同。