---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: 使用 xml.etree 解析 Python XML
translated: true
type: note
---

### Python 中的 xml.etree 概述

`xml.etree` 是 Python 内置模块（特指 `xml.etree.ElementTree`），用于解析和操作 XML 数据。它提供树状结构，可以高效地读取、写入、修改和遍历 XML 元素。该模块轻量级且无需外部库，非常适合基础 XML 处理任务。通过 `import xml.etree.ElementTree as ET` 导入使用。

### 解析 XML

通过以下方式将 XML 加载到内存中：

- **从字符串解析**：`ET.fromstring(xml_string)` 返回表示根节点的 Element 对象
- **从文件解析**：`ET.parse(filename)` 返回 ElementTree 对象，可通过 `.getroot()` 获取根节点

```python
import xml.etree.ElementTree as ET

# 从字符串解析
xml_data = "<root><child>text</child></root>"
root = ET.fromstring(xml_data)

# 从文件解析
tree = ET.parse('example.xml')
root = tree.getroot()
```

### 遍历元素

解析后可遍历 XML 树：

- **访问子元素**：使用 `root[0]` 按索引访问，或通过 `for child in root:` 迭代
- **查找元素**：
  - `root.find('tag')` 获取首个匹配子元素
  - `root.findall('tag')` 获取所有匹配子元素
- **访问文本与属性**：
  - 文本内容：`element.text`
  - 属性：`element.attrib`（字典类型）

```python
# 示例 XML: <bookstore><book id="1"><title>Python</title></book></bookstore>
for book in root.findall('book'):
    title = book.find('title').text
    book_id = book.attrib['id']
    print(f"图书 {book_id}: {title}")
```

### 修改 XML

动态编辑元素：

- **添加元素**：`ET.SubElement(parent, 'new_tag')` 创建并附加新子元素
- **设置文本/属性**：`element.text = '新文本'`；`element.set('attr', '值')`
- **删除元素**：`root.remove(child)`

```python
new_child = ET.SubElement(root, 'new_element')
new_child.text = '新增内容'
new_child.set('attr', '值')
```

### 写入 XML

将修改保存回 XML：

- **输出字符串**：`ET.tostring(root, encoding='unicode')`
- **写入文件**：`tree.write('output.xml')`

```python
xml_output = ET.tostring(root, encoding='unicode')
with open('output.xml', 'w') as f:
    f.write(xml_output)

# 或直接写入
tree.write('output.xml')
```

### 完整示例

以下为解析、修改和写入 XML 的完整脚本：

```python
import xml.etree.ElementTree as ET

# 输入 XML 字符串
xml_str = """<library>
  <book id="1"><title>1984</title><author>Orwell</author></book>
</library>"""

root = ET.fromstring(xml_str)

# 添加新图书
new_book = ET.SubElement(root, 'book', id="2")
ET.SubElement(new_book, 'title').text = 'Brave New World'
ET.SubElement(new_book, 'author').text = 'Huxley'

# 打印所有图书
for book in root:
    title = book.find('title').text
    author = book.find('author').text
    print(f"{title} 作者：{author}")

# 写入文件
ET.tostring(root, encoding='unicode')
# 或 root.write('library.xml')
```

### 注意事项
- 处理命名空间时在查询中使用 `xmlns='{命名空间}'`，例如 `root.find('{http://example.com}tag')`
- 处理大文件时可考虑使用 `ET.iterparse()` 进行迭代解析
- 处理用户输入的 XML 时需警惕 XML 注入等安全漏洞
- 复杂需求可选用 lxml 等提供扩展功能的库
