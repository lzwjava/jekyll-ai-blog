---
audio: false
generated: true
image: false
lang: en
layout: post
title: Programming Wisdom Unlocked
translated: false
type: note
---

Question: What does the article "编程的智慧" (The Wisdom of Programming) by Wang Yin say, as found at the GitHub link <https://github.com/AlexiaChen/YinWangBak/blob/master/编程的智慧.md>?

Answer:

## Overview

The file is part of a GitHub repository called **YinWangBak**, which is a collection of articles written by **Wang Yin (王垠)** — a well-known and influential (though controversial) Chinese computer scientist. The article is titled **"编程的智慧" (The Wisdom of Programming)**, originally published on his blog. Below is a comprehensive summary of its content.

---

## Introduction

Programming is described as a creative endeavor and an art form. Mastering any art requires much practice and insight. The "wisdom" referenced in the title is not a miracle shortcut — it cannot replace hard work. However, because the software industry tends to overcomplicate simple things, the article aims to point confused people in the right direction so they can waste less effort.

---

## 1. Repeatedly Refine Your Code

Some people boast about how many thousands of lines of code they have written, as if quantity is the measure of programming skill. However, if you always rush to write code without going back to scrutinize, revise, and refine it, you cannot actually improve. You will keep producing mediocre or even bad code. In this sense, many people's so-called "work experience" does not necessarily correlate with code quality.

Good programmers delete more code than they keep. If someone writes a lot of code but rarely deletes any, their codebase is likely full of garbage.

If you reach a plateau where refining no longer yields progress, set the code aside. Come back weeks or months later — fresh inspiration often appears. After many such cycles, you accumulate wisdom and intuition, enabling you to approach new problems more directly and correctly.

---

## 2. Write Elegant Code

People hate "spaghetti code" because it tangles logic and makes it impossible to follow. Elegant code, by contrast, looks like neatly stacked, nested boxes — organized and hierarchical. Like organizing a room: instead of dumping everything into one big drawer, you use smaller boxes inside it to categorize items.

Elegant code also has a tree-like structure. Programs mostly deal with information passing and branching. Think of code like an electrical circuit — current flows through wires and splits at junctions. This mindset leads to `if` statements that almost always have two branches (an `if` and an `else`), creating clear and airtight logic.

---

## 3. Write Modular Code

True modularity is not about splitting code across many files and directories — that is only a superficial and often counterproductive approach. Real modularity is logical. A module should behave like a circuit chip with well-defined inputs and outputs. The best modularization tool that already exists is simply the **function**: each function has clear inputs (parameters) and outputs (return values).

Key principles for modular code:

- **Keep functions short** — ideally under 40 lines, so the whole function fits in your visual field without scrolling.
- **Create small utility/helper functions** — even a two-line helper can greatly simplify the main function's logic.
- **Each function should do one simple thing** — avoid multi-purpose functions that branch internally based on conditions; split them into separate, specialized functions instead.
- **Avoid using global variables or class members to pass information between functions** — use local variables and parameters instead, to preserve clear, isolated function logic.

---

## 4. Write Readable Code

Truly elegant and readable code hardly needs comments. If you find yourself needing to write many comments, it likely means your code's logic is unclear. Programming languages are actually more powerful and precise than natural languages — they contain the equivalent of nouns, verbs, conditionals, and so on. If you use the language's expressive power fully, the code itself explains what it does.

Specific tips for readable code:

- Use meaningful function and variable names.
- Declare local variables close to where they are used.
- Keep local variable names short and context-specific.
- Don't reuse local variables for different purposes.
- Extract complex logic into named helper functions.
- Extract complex expressions into intermediate variables with meaningful names.
- Break lines at sensible points to improve visual clarity.

---

## 5. Write Simple Code (Avoid Over-Engineering)

The article warns against unnecessary complexity:

- Avoid deep inheritance hierarchies and over-use of design patterns.
- Don't add abstractions or generalization until you actually need them.
- Resist the temptation to "future-proof" code prematurely — this usually adds complexity without benefit.

---

## 6. Handle Errors Correctly

The article discusses proper error handling in depth. Error handling is not unique to Java — even in C, the same fundamental issues arise, and no language lets you escape from it. You must understand what exceptions mean and handle them properly, rather than blindly catching all exceptions or adding `throws Exception` everywhere.

---

## 7. Avoid Null and Use Safe Alternatives

The article strongly criticizes the use of `null` as a return value, calling it the source of many bugs. It recommends using constructs like `Optional` (though it also critiques Java 8's verbose implementation) or other safe patterns that make the absence of a value explicit and force callers to handle it.

---

## Overall Philosophy

The article presents practical, hard-earned programming knowledge and techniques. It emphasizes that programmers should know what to do — and what not to do — at each stage. These are not just personal preferences but broadly shared principles of good coding. The central message is: **quality over quantity, clarity over cleverness, and continual refinement over hasty production.**

---

References:

- [王垠-编程的智慧 (cnblogs mirror)](https://www.cnblogs.com/zhaoqingqing/p/12328120.html)
- [王垠 original blog post](https://www.yinwang.org/blog-cn/2015/11/21/programming-philosophy)
- [编程的智慧 - TecHug](https://www.techug.com/post/programming-philosophy/)
- [知乎 discussion on the article](https://www.zhihu.com/question/37762361)
