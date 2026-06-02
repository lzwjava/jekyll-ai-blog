---
audio: false
generated: true
lang: zh
layout: post
title: 修复LaTeX撇号渲染问题
translated: true
type: note
---

您遇到的 "HSBC's" 中撇号显示问题，很可能与 LaTeX 在 PDF 输出中处理某些引号/撇号字符的方式有关。以下是几种改善渲染效果的方法：

## 1. 使用正确的 LaTeX 撇号

将直撇号 (') 替换为正确的 LaTeX 撇号：

```latex
\item {通过 TEKsystems 外包至汇丰银行的后端工程师，在汇丰银行企业技术部门为 \href{https://www.google.com/search?q=Finance+Transformation+Platform+HSBC}{金融转型平台} 开发和优化后端系统。}
```

改为：

```latex
\item {通过 TEKsystems 外包至汇丰银行的后端工程师，在汇丰银行企业技术部门为 \href{https://www.google.com/search?q=Finance+Transformation+Platform+HSBC}{金融转型平台} 开发和优化后端系统。}
```

## 2. 使用 `\textquotesingle` 命令

```latex
汇丰银行\textquotesingle{}的
```

## 3. 使用 `\textasciigrave` 和 `\textquotesingle` 方法

```latex
汇丰银行\textquotesingle{}的
```

## 4. 添加 `textcomp` 宏包

在导言区添加：

```latex
\usepackage{textcomp}
```

然后使用：

```latex
汇丰银行\textquotesingle{}的
```

## 5. 使用 UTF-8 编码（如果尚未使用）

确保文档使用 UTF-8 编码：

```latex
\usepackage[utf8]{inputenc}
```

## 6. 尝试使用 `babel` 宏包以获得更好的排版效果

```latex
\usepackage[british]{babel}
```

## 最可靠的解决方案

为了获得最佳效果，我建议使用反引号-撇号组合，这是 LaTeX 中实现正确排版的传统方式：

```latex
\item {通过 TEKsystems 外包至汇丰银行的后端工程师，在汇丰银行企业技术部门为 \href{https://www.google.com/search?q=Finance+Transformation+Platform+HSBC}{金融转型平台} 开发和优化后端系统。}
```

这将在 PDF 输出中以正确的排版间距和弯曲度呈现。反引号 (`) 后接撇号 (') 可为 LaTeX 中的所有格形式创建正确的外观。
