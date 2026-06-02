---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GitHub代码搜索技巧JSON
translated: true
type: note
---

你可以这样编写 GitHub 代码搜索查询：

```
"deepseek/deepseek-chat-v3.1" language:JSON
```

### 注意事项：

* 引号确保 GitHub 精确搜索字符串 `deepseek/deepseek-chat-v3.1`
* `language:JSON`（或 `lang:json`，两者等效）将结果限定在 JSON 文件内
* 若需搜索非 `.json` 扩展名的类 JSON 配置文件（如 `.ipynb` 或 `.eslintrc`），可移除 `lang:` 过滤器

示例：

* 仅搜索 JSON 文件：

  ```
  "deepseek/deepseek-chat-v3.1" lang:json
  ```

* 搜索所有文件类型但仍高亮 JSON 相关结果：

  ```
  "deepseek/deepseek-chat-v3.1"
  ```

需要我进一步演示如何优化搜索吗？比如限定在代码仓库、议题或代码片段中的搜索方式？
