---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Sourcegraph查询语言指南
translated: true
type: note
---

Sourcegraph 拥有灵活而强大的专属查询语言。以下是常用语法详解：

---

### 1. **基础关键词搜索**

* 直接输入术语：

  ```
  http client
  ```

  查找包含这两个词汇的文件或代码。

---

### 2. **逻辑运算符**

* `AND`（与）、`OR`（或）、`NOT`（非）（必须大写）：

  ```
  React AND useEffect
  React OR Vue
  logger NOT debug
  ```

---

### 3. **筛选器**

* `repo:` → 按代码库筛选

  ```
  repo:github.com/myorg/myrepo
  ```

* `file:` → 匹配文件路径（支持正则表达式）

  ```
  file:\.java$
  ```

* `lang:` → 限定编程语言

  ```
  lang:python requests
  ```

* `content:` → 强制文本搜索（忽略结构匹配）

  ```
  content:"SELECT * FROM"
  ```

* `case:yes` → 启用大小写敏感搜索

---

### 4. **正则表达式匹配**

* 默认支持正则表达式：

  ```
  foo(bar|baz)
  ^class\s+\w+
  ```

---

### 5. **结构化搜索**

使用 `:[var]` 模式占位符匹配代码结构：

```
if (:[cond]) { :[body] }
```

---

### 6. **版本/分支搜索**

* 附加 `@branch`、`@commit` 或 `@tag`：

  ```
  repo:myrepo@main lang:go fmt.Println
  ```

---

### 7. **符号与定义**

* `type:symbol` → 搜索符号名称
* `type:commit` → 搜索提交信息
* `type:diff` → 搜索代码差异

---

### 8. **示例**

* 查找 Go 文件中的所有 `TODO` 注释：

  ```
  TODO lang:go
  ```

* 仅在 `src/` 目录中搜索 Java 方法：

  ```
  file:^src/ lang:java "public static"
  ```

* 跨多个代码库搜索：

  ```
  repo:github.com/org/.* file:\.ts$ "useState"
  ```

---

👉 您是否需要我准备一份**常用 Sourcegraph 查询速查表**（比如可每日复用的单行查询），或是进行**高级模式深度解析**？
