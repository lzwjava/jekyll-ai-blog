---
audio: false
generated: true
image: false
lang: en
layout: post
title: GitHub Code Search Tips JSON
translated: false
type: note
---

You can write a GitHub code search query like this:

```
"deepseek/deepseek-chat-v3.1" language:JSON
```

### Notes:

* The quotes ensure GitHub searches for the exact string `deepseek/deepseek-chat-v3.1`.
* `language:JSON` (or `lang:json`, both work) restricts results to JSON files.
* If you want to include JSON-looking configs that aren’t in `.json` files (like `.ipynb` or `.eslintrc`), you can drop the `lang:` filter.

Examples:

* Search only JSON files:

  ```
  "deepseek/deepseek-chat-v3.1" lang:json
  ```

* Search all file types but still highlight JSON results:

  ```
  "deepseek/deepseek-chat-v3.1"
  ```

Do you also want me to show you how to refine this further — for example, searching only inside repositories, issues, or code?
