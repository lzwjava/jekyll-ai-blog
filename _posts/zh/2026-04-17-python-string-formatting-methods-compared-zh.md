---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Python字符串格式化方法比较
translated: true
type: note
---

问题：在Python中格式化字符串时，哪种方法更好？

答案：

这取决于**你关注什么**（可读性、性能、日志记录、兼容性）。没有一种方法是普遍“最佳”的，但在现代Python中，*存在*一个明确的默认选择。

---

# 1. 现代最佳选择：**f-strings（✅ 推荐）**

```python
name = "Alice"
age = 25
msg = f"{name} is {age} years old"
```

### 为何这是最佳选择：

* ✅ **可读性**最强
* ✅ 速度快（在CPython中通常最快）
* ✅ 直接且富有表现力
* ✅ 支持内联表达式

```python
f"{name.upper()} is {age + 1} next year"
```

👉 这是 **Python 3.6+ 的默认选择**

---

# 2. `.format()`（旧方法，灵活，但现在较少使用）

```python
msg = "{} is {} years old".format(name, age)
```

或：

```python
msg = "{name} is {age}".format(name=name, age=age)
```

### 优点：

* 在旧版本Python（<3.6）中可用
* 灵活的格式化系统

### 缺点：

* ❌ 更冗长
* ❌ 比f-strings慢
* ❌ 可读性较差

👉 如今：主要用于**遗留/兼容性场景**

---

# 3. `%` 格式化（旧式）

```python
msg = "%s is %d years old" % (name, age)
```

### 优点：

* 在**日志记录**中仍有用途（特殊情况）

### 缺点：

* ❌ 已过时
* ❌ 灵活性差
* ❌ 类型问题（`%d`、`%s`等）

👉 **仅用于日志记录**，不要用于通用字符串格式化。

---

# 4. 字符串拼接（`+`）

```python
msg = name + " is " + str(age) + " years old"
```

### 缺点：

* ❌ 难以阅读
* ❌ 容易出错
* ❌ 需要手动类型转换
* ❌ 不可扩展

👉 在几乎所有情况下都应避免使用。

---

# 5. 性能对比（大致直觉）

从最快到最慢（通常）：

```
f-string  ≥  % formatting  >  .format()  >  拼接
```

但除非在紧密循环中，否则差异很小。

---

# 6. 重要例外：**日志记录**

尽管f-strings通常是首选：

```python
logging.info(f"User {name}")   # ❌ 不理想
```

应使用：

```python
logging.info("User %s", name)  # ✅ 正确
```

因为日志记录采用**延迟格式化**。

---

# 7. 最终建议

### 使用以下规则：

* ✅ **通用字符串格式化 → f-strings**
* ✅ **日志记录 → 逗号分隔的 `%s`**
* ❌ 避免使用 `.format()`，除非必要
* ❌ 避免使用 `+` 拼接

---

# 8. 简单直觉

* f-string = **“直接表达你的意思”**
* `.format()` = **旧的灵活系统**
* `%` = **特殊用途（日志记录）**
* `+` = **原始方法，避免使用**

---

如果你愿意，我可以展示**`.format()`仍然优于f-strings的边缘情况**（存在一些微妙情况）。