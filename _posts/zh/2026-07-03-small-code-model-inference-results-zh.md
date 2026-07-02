---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 小代码模型推理结果
translated: true
type: note
---

## 推理结果总结

**测试模型：`out-github-code-124m`** — 124M 参数的 GPT-2，基于 GitHub 代码训练（14B tokens）

以下是每个 prompt 的输出结果：

---

### 1. `prompt_hashmap.txt` — Java HashMap（不完整的 `put` 方法）

```
public void put(K key, V value) {
    return this).Size;
         assertEquals("test for required ` + object)
  ...
```

**结论：** 毫无意义。模型知道这是 Java（大括号、`assertEquals`、`+` 字符串拼接），但生成的是语义上无意义的代码。`HashTable` 的概念有所体现——它输出了 `getNext_files` 和大小检查——但没有任何可编译的内容。

---

### 2. `prompt_java.txt` — Java BST（不完整的 `search` 方法）

```
boolean search(int key) {
    return this;
              }
                *handle = newkey;
             if ( str.key)) {
                         return;
  ...
```

**结论：** 具有 Java 形状的无意义内容。模型意识到应该返回一些东西并递归进入节点，但语法和逻辑都是错误的。

---

### 3. `prompt_python.txt` — 完整的 MiniGPT（151 行）

模型**完美地逐字重现**了整个 prompt（正如预期——这是最长的 prompt，并且模型在训练中见过类似的 PyTorch 代码），然后添加了：

```python
        return parse_s.array_or_id
           expect = self.current_index_c('und' ) * time_size_t'
                          self.send_dict_text_by_model(self).'=self.size)
  ...
```

**结论：** prompt 结束后，输出变为无意义内容。模型识别出这是 Python，但生成了不连贯的方法体。

---

### 4. `prompt_quicksort.txt` — 仅 `def quicksort(arr):`

```
def quicksort(arr):
                                     class     *                 (                               .
```

**结论：** 完全无意义。prompt 太短——模型没有可依赖的上下文，因此只输出空白和随机 token。

---

### 5. `prompt_webapp.txt` — 完整的 Flask 应用（258 行）

完美重现了整个 Flask 应用，然后附加了：

```python
        return 'Eailed', )
         end
  assert_backend = self._config_description_1('status'=True,
```

**结论：** prompt 被干净地重现，随后是无意义的延续。

---

### 与其他模型的比较

| 模型 | Java HashMap | 备注 |
|-------|-------------|-------|
| `out-github-code-124m` | 无意义（Java 形状） | 三个中最好的——至少知道 Java 语法 |
| `out-fineweb-gpt3`（124M） | 无意义（符号） | 更差——完全不懂 Java |
| `out-gpt2-200m`（200M） | `string type` × 200 | Web 文本模型，无代码知识 |

### 为什么会这样

**根本原因：** 124M 参数对于生成连贯的代码来说太小了。在这个规模下，模型：

1. **很好地学习了代码语法**——正确的缩进、大括号、关键字、方法结构
2. **学习了 token 级别的统计信息**——`return` 跟在 `{` 后面，`}` 结束代码块，`assertEquals` 出现在测试代码中
3. **没有语义理解的能力**——它无法在超过 50 个 token 的范围内维持连贯的计划，因为隐藏状态（768 维）过于压缩

作为参考，Codex（早期 GitHub Copilot 使用的模型）有 12B 参数。即使是 CodeGen-350M（350M 参数）也开始能生成半合理的补全。124M 实在太小了。

**要使用这些 prompt 进行 vibe-coding，需要像 CodeLlama-7B 或 GPT-2 XL（1.5B）这样的模型**，才能在部分 Java/Python 代码上获得语义上有意义的补全。