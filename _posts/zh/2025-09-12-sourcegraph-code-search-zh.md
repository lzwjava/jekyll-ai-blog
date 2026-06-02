---
audio: false
date: 2025-09-12
generated: true
image: false
lang: zh
layout: post
model: mistralai/mistral-medium-3.1
title: Sourcegraph代码搜索指南
translated: true
type: note
---

Sourcegraph 是一款强大的代码搜索与导航工具，可帮助开发者跨多个代码库进行搜索、理解代码依赖关系并高效浏览大型代码库。本指南涵盖**搜索语法、最佳实践及特定语言搜索（Java 与 Python）**。

---

## **1. 基础搜索语法**

Sourcegraph 支持**字面量搜索、正则表达式搜索和结构搜索**，并支持筛选器。

### **1.1 字面量搜索**

搜索精确文本：

```
"def calculate_sum"
```

### **1.2 正则表达式搜索**

使用 `/.../` 进行正则匹配：

```
/def \w+_sum\(/
```

### **1.3 结构搜索（测试版）**

搜索代码模式（如函数定义）：

```
type:func def calculate_sum
```

### **1.4 筛选器**

使用筛选器优化搜索：

- `repo:` – 在指定代码库中搜索

  ```
  repo:github.com/elastic/elasticsearch "def search"
  ```

- `file:` – 在指定文件中搜索

  ```
  file:src/main/java "public class"
  ```

- `lang:` – 按语言筛选

  ```
  lang:python "def test_"
  ```

- `type:` – 按符号类型筛选（函数、类等）

  ```
  type:func lang:go "func main"
  ```

---

## **2. 高级搜索技巧**

### **2.1 布尔运算符**

- `AND`（默认）：`def calculate AND sum`
- `OR`：`def calculate OR def sum`
- `NOT`：`def calculate NOT def subtract`

### **2.2 通配符**

- `*` – 匹配任意字符序列

  ```
  "def calculate_*"
  ```

- `?` – 匹配单个字符

  ```
  "def calculate_?"
  ```

### **2.3 大小写敏感**

- 默认不区分大小写
- 使用 `case:yes` 启用大小写敏感

  ```
  case:yes "Def Calculate"
  ```

### **2.4 注释搜索**

使用 `patternType:literal` 搜索注释内容：

```
patternType:literal "// TODO:"
```

---

## **3. Java 代码搜索**

### **3.1 查找类**

```
type:symbol lang:java "public class"
```

### **3.2 查找方法**

```
type:func lang:java "public void"
```

### **3.3 查找注解**

```
lang:java "@Override"
```

### **3.4 查找导入语句**

```
lang:java "import org.springframework"
```

### **3.5 查找异常处理**

```
lang:java "try {" AND "catch (Exception"
```

---

## **4. Python 代码搜索**

### **4.1 查找函数**

```
type:func lang:python "def calculate"
```

### **4.2 查找类**

```
type:symbol lang:python "class Calculator"
```

### **4.3 查找导入语句**

```
lang:python "import pandas"
```

### **4.4 查找装饰器**

```
lang:python "@app.route"
```

### **4.5 查找文档字符串**

```
lang:python '"""'
```

---

## **5. 最佳实践**

1. 使用 `lang:` 缩小搜索范围
2. 组合筛选器（`repo:`, `file:`, `type:`）提升精度
3. 使用正则表达式实现灵活模式匹配
4. 对常用查询保存搜索条件
5. 必要时使用 `case:yes`

---

## **6. 查询示例**

| **搜索目标** | **查询语句** |
|--------------|-------------|
| 查找所有 Java `main` 方法 | `lang:java "public static void main"` |
| 查找 Python 测试函数 | `lang:python "def test_"` |
| 查找 Go 语言中的 TODO 注释 | `lang:go "// TODO:"` |
| 查找 Spring Boot 控制器 | `lang:java "@RestController"` |
| 查找 JavaScript 中的 `if` 语句 | `lang:javascript "if ("` |

---

## **7. 总结**

Sourcegraph 的搜索功能**强大而灵活**，支持跨多种语言的**字面量、正则表达式和结构搜索**。通过掌握筛选器（`lang:`, `repo:`, `type:`），您可以高效浏览大型代码库。

### **后续步骤**

- 尝试使用**搜索收藏**功能管理常用查询
- 探索**代码智能**功能（悬停提示、跨仓库导航）
- 安装 **Sourcegraph 扩展**（VS Code、JetBrains）

是否需要深入了解某项特定功能？🚀
