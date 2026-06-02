---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 结构代码对比工具简介
translated: true
type: note
---

我来搜索关于 ydiff 的信息，并为你提供一个全面的介绍。问题：GitHub 仓库 yinwang0/ydiff 中关于 ydiff 的全面介绍是什么？

答案：

## 概述

ydiff 是由王垠开发的一款结构对比工具，主要面向 Lisp 家族语言，并试验性地支持 C++ 和 JavaScript。与传统的基于文本行比较的 diff 工具不同，ydiff 将程序解析为抽象语法树（AST），以提供基于语言结构的对比。

## 主要特性

### 1. 语言感知解析
ydiff 会解析程序并理解基本的语言结构，避免进行无意义的比较，例如不会将字符串 "10000" 与整数 10000 进行比较，尽管它们看起来相似。它会先尝试匹配同名的函数，然后再比较不同名的函数。

### 2. 格式不敏感
对比结果不受空格、换行符或缩进差异的影响。例如，仅仅因为用 if 条件包裹了一段代码块，ydiff 不会因此产生大量的差异报告。

### 3. 移动代码检测
ydiff 可以识别重构过的代码——无论代码是重命名、移动、重新排序、包裹、提升、合并还是拆分——无论这些变更在程序结构中有多深。

### 4. 人性化的输出
输出结果设计得便于人类理解，拥有交互式 UI，可以帮助用户高效地浏览和理解变更。界面中的左右窗口始终保持相对位置锁定。

## 实现细节

ydiff 使用 Racket 语言实现，这是一种基于 Scheme 的编程语言。该工具是王垠“结构化编程”愿景的一部分，该愿景希望程序能直接以数据结构而非文本形式存储，从而消除解析的必要。

## 语言支持

尽管 ydiff 最初旨在支持多种语言，但开发者发现实现解析器非常繁琐，因此决定主要专注于 Lisp 家族。当前支持包括：

- **主要支持**：Lisp 家族语言（Scheme, Clojure, Emacs Lisp）
- **试验性支持**：C++ 和 JavaScript
- **独立实现**：Python（通过名为“PyDiff”的工具）

C++ 解析器是为了演示如何在两天内构建一个基本可用的解析器而创建的。

## 安装与使用

### 构建 ydiff

构建该工具的步骤如下：

1. 进入包含源代码的目录
2. 运行 `make` 命令
3. 这将编译生成几个可执行文件，如 diff-lisp, diff-cpp 和 diff-js
4. 将这些可执行文件复制到你的 PATH 环境变量包含的目录中

### 运行 ydiff

使用示例：
```bash
diff-lisp demos/mk1.ss demos/mk2.ss
```

这将在当前目录生成一个名为 "mk1-mk2.html" 的 HTML 文件。该 HTML 文件需要同目录下有支持文件 nav.js 和 diff.css 才能正常显示。

## 使用场景

ydiff 有助于理解代码变更，也可用于检测编程课程中的抄袭或版权侵权。对于大规模的抄袭检测，MOSS 可能更合适，但 ydiff 从根本上更加精确，因为它会解析程序。

## 演示

项目包含多个演示，展示了 ydiff 的能力：

- 对比 ydiff 自身算法的不同版本
- 对比原始的 miniKanren 与支持否定操作符的修改版本
- 对比 Emacs 的 paredit-mode 的两个版本（v20 和 v23）
- 对比 Typed Clojure 的不同提交

## 许可证

ydiff 是自由软件，根据 GNU 通用公共许可证第 3 版或更新版本授权。

参考文献：

- [https://github.com/yinwang0/ydiff](https://github.com/yinwang0/ydiff)
- [https://yinwang0.wordpress.com/2012/01/03/ydiff/](https://yinwang0.wordpress.com/2012/01/03/ydiff/)
- [https://yinwang0.substack.com/p/ydiff](https://yinwang0.substack.com/p/ydiff)
