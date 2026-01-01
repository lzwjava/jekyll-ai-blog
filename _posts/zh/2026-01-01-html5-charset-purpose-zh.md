---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: HTML5 Meta Charset 标签的作用
translated: true
type: note
---

问题：HTML5 中 `<meta charset="utf-8">` 标签的主要作用是什么？

A) 设置页面背景颜色  
B) 指定文档的 character encoding  
C) 定义页面标题  
D) 链接外部 CSS 文件

答案：

正确答案是 **B) 指定文档的 character encoding**。

在 HTML5 中，`<meta charset="utf-8">` 标签（以前更为冗长的 meta 元素的简化形式）被放置在 `<head>` 部分，用于声明文档中使用的 character encoding。最常用且推荐的值是 "utf-8"，它支持来自几乎所有语言的广泛字符和符号。这一声明有助于 browser 正确解析和 render 特殊字符，防止出现乱码（例如 "mojibake"）。

- 选项 A 是错误的，因为背景颜色由 CSS 处理（例如 `body { background-color: ... }`）。
- 选项 C 是错误的，因为页面标题是使用 `<title>` 标签定义的。
- 选项 D 是错误的，因为外部 CSS 文件是使用 `<link rel="stylesheet" href="styles.css">` 标签链接的。

该标签应该是 `<head>` 中的首批元素之一，以确保在解析任何内容之前正确检测 encoding。

你选择的 B 是正确的。