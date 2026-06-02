---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: Python正则表达式指南
translated: true
type: note
---

### 导入 `re` 模块

`re` 模块（正则表达式缩写）是 Python 标准库的组成部分。它并非独立的 "regex 包"，而是内置模块。请在脚本开头导入：

```python
import re
```

### 基础概念

正则表达式（regex）是用于匹配、搜索和操作字符串的模式。它们使用特殊字符如：

- `.`（任意字符）
- `*`（零次或多次出现）
- `+`（一次或多次出现）
- `[]`（字符类，例如 `[a-z]` 表示小写字母）
- `^`（字符串开头），`$`（字符串结尾）

示例基于 Python 的 `re` 文档编写。为提高效率，复杂模式应使用 `re.compile()` 进行编译。

### 核心函数与用法

#### 1. **从起始位置匹配模式**

- `re.match(pattern, string)`：检查模式是否从字符串开头匹配
- 返回匹配对象或 `None`

   示例：

   ```python
   import re
   result = re.match(r"Hello", "Hello world")
   print(result.group())  # 输出：Hello
   ```

#### 2. **在字符串任意位置搜索**

- `re.search(pattern, string)`：查找任意位置首次出现的模式
- 返回匹配对象或 `None`

   示例：

   ```python
   result = re.search(r"world", "Hello world")
   print(result.group())  # 输出：world
   ```

#### 3. **查找所有匹配项**

- `re.findall(pattern, string)`：返回所有非重叠匹配的列表

   示例：

   ```python
   matches = re.findall(r"\d+", "我有3只猫和42只狗")
   print(matches)  # 输出：['3', '42']
   ```

#### 4. **分割字符串**

- `re.split(pattern, string)`：按模式出现位置分割字符串

   示例：

   ```python
   parts = re.split(r"\s+", "Hello    world   example")
   print(parts)  # 输出：['Hello', 'world', 'example']
   ```

#### 5. **替换匹配项**

- `re.sub(pattern, replacement, string)`：将匹配项替换为指定字符串

   示例：

   ```python
   new_string = re.sub(r"bad", "good", "This is bad")
   print(new_string)  # 输出：This is good
   ```

#### 6. **编译模式以供复用**

- 重复使用时，可将正则表达式编译为模式对象以获得更好性能

   示例：

   ```python
   pattern = re.compile(r"\d+")
   matches = pattern.findall("101室和102室")
   print(matches)  # 输出：['101', '102']
   ```

### 最佳实践

- 使用原始字符串（`r""`）编写正则模式，避免反斜杠转义问题
- 处理匹配对象：使用 `.group()` 获取匹配内容，`.span()` 获取索引范围
- 复杂任务可使用在线工具或 Python 交互式环境测试模式
- 更多示例和标志位（如 `re.IGNORECASE`）请参考 Python 官方文档：<https://docs.python.org/3/library/re.html>

如有具体使用场景或错误信息，欢迎提供更多细节！
