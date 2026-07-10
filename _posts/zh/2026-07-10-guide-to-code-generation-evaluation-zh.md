---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 代码生成评估指南
translated: true
type: note
---

文件结构很简单——以下是阅读方法：

**分隔符：**
```
======================================================================
```
那个 `=` 行分隔每个样本。每个样本以 `<|bos|>` 开头，这是序列起始标记。

**阅读模式：**
1. 向下滚动，跳过日志/初始化行（第1-5行）
2. 两个 `======` 行之间的每个块是一个生成的样本
3. 在每个块内：**输入提示** 是你提供的所有内容，然后是**模型的续写**

**示例：**
```
<|bos|>def fibonacci(n):     ← 提示（你提供的内容）
    if n == 0:              ← 模型的生成
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
    ...
```

总计：**8个样本**（fibonacci、reverse_linked_list、sort_dict_by_value、Stack、numpy import、CSV comment、is_palindrome、binary_search）。要从终端快速跳转样本：

```bash
grep '^====' -n /mnt/data/zz/codeparrot/eval/results/python_samples.log
```

这会打印所有分隔符的行号：

```
6:  ======  ← 样本1: fibonacci
24: ======  ← 样本2: reverse_linked_list
48: ======  ← 样本3: sort_dict_by_value
68: ======  ← 样本4: Stack
94: ======  ← 样本5: numpy import
116: ====== ← 样本6: CSV comment
120: ====== ← ...等等，CSV只有1行？让我检查一下
139: ====== ← 样本7: is_palindrome
175:        ← 样本8: binary_search（末尾，结尾没有=====）
```

然后按行范围读取特定样本：

```bash
sed -n '6,23p' /mnt/data/zz/codeparrot/eval/results/python_samples.log
```

评估生成质量的方法：

- **语法正确吗？** 使用 `python3 -c "compile(open('/dev/stdin').read(), '<test>', 'exec')"` 并粘贴代码运行
- **语义正确吗？** 通读一遍——函数是否真正解决了问题？
- **出现幻觉了吗？** 是否引用了不存在的 API？（例如 `head.is_linked()`——看似合理但实际不存在）
- **循环/递归终止了吗？** 会无限循环还是正常终止？