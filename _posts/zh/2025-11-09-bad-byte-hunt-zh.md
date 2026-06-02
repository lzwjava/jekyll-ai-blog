---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 追捕坏字节
translated: true
type: note
---

### 为什么这个方法找不到坏字节
你获取的 `hexdump` 输出匹配的是**文件偏移量** (`000008d0`)，而不是实际内容中的 `\x8D` 字节。Grep 是在全文搜索，而 "8d" 出现在十六进制地址中（例如 `08d0`），所以它提取了这条无关内容。该位置的数据字节 (`6f 67 20 ...`) 只是普通的 ASCII 字符 `"og = og_images[i"`，没有问题。

### 更好的查找 `\x8D` 的方法
在你的项目目录中（`_layouts/default.html` 旁边）尝试以下命令。它们会直接扫描文件的字节数据。

1. **改进的 Hexdump（在数据中搜索字节）**：
   这个方法通过添加空格来匹配十六进制字节（而非偏移量）：
   ```
   hexdump -C _layouts/default.html | grep ' 8d '
   ```
   - 如果找到匹配，你会看到偏移量（左列）及相邻字节。记下偏移量，然后在编辑器中跳转到该位置（例如 VS Code：Ctrl+G > 字节偏移量 / 16 获取大致行号）。
   - 命中时的示例输出：`00001234  ...  8d  20  61  62  ... |... ab...|`

2. **使用 `xxd`（通常比 Hexdump 更好用）**：
   macOS 系统内置了 `xxd`：
   ```
   xxd _layouts/default.html | grep 8d
   ```
   - 类似原理：匹配十六进制字节中的 "8d"。如果无输出，说明该字节不存在（这种情况很少见，但可能存在于其他文件中）。

3. **二进制 Grep（直接字节搜索）**：
   ```
   grep -a -o -P '\x8d' _layouts/default.html | hexdump -C
   ```
   - 这会精确匹配字节并以十六进制格式输出。如果结果为空，则不存在 `\x8D`。

4. **Ruby 单行命令（精确定位）**：
   按我之前建议的运行此命令获取字节索引：
   ```
   ruby -e "File.open('_layouts/default.html', 'rb') { |f| f.read.each_byte.with_index { |b, i| puts \"Found at byte #{i}: #{b.chr(Encoding::ASCII_8BIT).inspect}\" if b == 0x8D } }"
   ```
   - 输出示例：`Found at byte 1234: "\x8D"`。然后进行编辑：打开文件，跳转到约第 1234 个字符位置（或行号 ≈1234/80），删除这个不可见字符（它可能显示为空白，选中并删除周边内容）。

### 如果没有匹配项？
- `\x8D` 可能存在于**其他文件**中（例如通过布局文件中的 `{{ content }}` 渲染的 `_posts/` 目录下的文章）。扫描整个网站：
  ```
  find . -name "*.md" -o -name "*.html" | xargs grep -l $'\x8D'
  ```
  （或对每个可疑文件使用 Ruby 脚本。）
- 或者它是文件开头的 BOM/不可见字符：在编辑器中打开文件，如果首行为空则删除，重新保存为 UTF-8 格式。

清除该字符后，再次运行 `bundle exec jekyll serve --incremental`。如果问题依旧存在，请粘贴其中一条命令（或 Ruby 命令）的输出结果，我们将彻底解决它。

[字节搜索的 Hexdump 技巧](https://unix.stackexchange.com/questions/38331/finding-bad-characters-in-hex-dump)
