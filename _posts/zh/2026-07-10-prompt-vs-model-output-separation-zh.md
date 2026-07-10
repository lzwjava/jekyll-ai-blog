---
audio: false
generated: true
image: false
lang: zh
layout: post
title: I notice you haven't provided the title to translate. Could you please share
  the title you'd like me to translate into Simplified Chinese?
translated: true
type: note
---

是的——对于这个评估脚本来说，提示词就是紧跟在 `<|bos|>` 后面的文本，在模型开始生成之前的内容。但要注意：模型可以进行生成**与提示词在同一行**。

例如，提示词正是 `def fibonacci(n):`，但输出显示的是：

```
<|bos|>def fibonacci(n): # n is an integer
    if n == 0:
```

其中的 `# n is an integer` 是由**模型生成的**，并非提示词的一部分。模型在换行到带缩进的函数体之前，先扩展了函数签名。因此，`<|bos|>` 之后的第一行是**提示词 + 模型生成内容**的混合。

如果你想查看不包含模型输出的实际提示词：

```bash
grep 'prompt =' /mnt/data/zz/codeparrot/eval/run_eval.sh
```

输出：

```
prompt = 'def fibonacci(n):'
prompt = 'def reverse_linked_list(head):'
prompt = 'def sort_dict_by_value(d):'
prompt = 'class Stack:'
prompt = 'import numpy as np'
prompt = '# A function to read a CSV file and return a list of dicts'
prompt = 'def is_palindrome(s):'
prompt = '# Binary search implementation'
```

所以，提示词就是**`<|bos|>` 后面的第一个文本片段**，但由于模型的分词器在提示词和生成内容之间没有添加任何特殊分隔符，它们会直接拼接在一起。要在输出中精确区分提示词和生成内容，你需要单独对提示词进行分词，统计其 token 数量，然后将其切掉。
