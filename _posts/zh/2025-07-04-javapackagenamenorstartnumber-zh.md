---
audio: false
generated: true
lang: zh
layout: post
title: Java 包名不能以数字开头
translated: true
type: note
---

在Java中，包名**不能以数字开头**。根据Java命名规范和Java语言规范要求：

- 包名必须是有效的标识符
- 有效的Java标识符必须以字母（A-Z或a-z）、下划线（`_`）或美元符号（`$`）开头
- 数字（0-9）允许在标识符中使用，但只能出现在**首字符之后**

例如：

- 有效的包名：`com.example`、`my_package`、`a123`
- 无效的包名：`123example`、`1package`

若尝试使用数字开头的包名，Java编译器将抛出语法错误。解决方案包括：

- 使用字母或下划线作为包名开头，例如：`a123.example` 或 `_123.example`
- 采用符合规范的描述性名称，如 `com.example.project123`

此规则确保了Java命名系统的一致性和兼容性。
