---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: GPL 与 MIT 许可证详解
translated: true
type: note
---

Question: What is the GPL license, and what is the difference between GPL and MIT?

Answer:

**GPL** (GNU General Public License) 是最著名的 **open-source licenses** 之一。它是由 Richard Stallman 和 Free Software Foundation 创建的一种 **copyleft** license。其主要目标是保证软件永远保持 **free**（指自由）——用户必须拥有运行、学习、修改和分享软件的权利。

GPL 的核心理念是：
“如果你分发该软件（或其修改版本），你必须在相同的 GPL license 下提供 **source code**。”

这产生了一种“传染性”或保护性效应：任何包含或链接到 GPL 代码的更大程序通常也必须在 GPL 下发布（特别是在使用 **GPLv3** 或分发 binaries 时）。

目前最常见的版本是 **GPLv2**（由 Linux kernel 使用）和 **GPLv3**（更新的版本，具有更强的 patent 和 anti-DRM 保护）。

相比之下，**MIT License** 是一种非常简短且 **permissive** 的 license（最初源自 MIT）。它基本规定：

- 你可以运行、复制、修改、合并、出版、分发、sublicense 和/或销售软件副本。
- 唯一的要求是在所有副本或实质性部分中 **包含原始的 copyright notice 和 license text**。

**GPL** 与 **MIT** 的主要区别：

| Aspect                  | GPL (copyleft)                              | MIT (permissive)                           |
|-------------------------|---------------------------------------------|--------------------------------------------|
| **Type**                | Strong copyleft                             | Permissive                                 |
| **Can be used in closed-source / proprietary software?** | No — 如果你分发一个使用 GPL 代码的程序，整个程序通常必须是 GPL（必须共享 source code） | Yes — 你可以将其包含在 proprietary/closed-source 产品中 |
| **Modifications**       | 如果分发，修改部分也必须使用 GPL + 提供 source code | 没有强制要求分享修改部分或 source code |
| **Requirements when distributing** | 必须提供 source code + 使用 GPL license | 仅需保留 copyright & license notice |
| **"Viral" effect**      | Yes — 会传染给更大的作品 | No — 对 commercial use 非常友好 |
| **Length / complexity** | 篇幅长且详细（特别是 GPLv3） | 非常简短（约 150–200 单词） |
| **Philosophy**          | 永远为所有用户保护软件自由 | 最大的灵活性，“做你想做的任何事” |
| **Popular examples**    | Linux kernel, Git, WordPress, MySQL | React, Vue.js, Ruby on Rails, 大量小型 libraries |

**简单来说**：
- 如果你希望你的代码被尽可能广泛地使用——即使是在 closed-source commercial 产品中，请选择 **MIT**。
- 如果你想强制衍生作品保持 open source，并将改进回馈给社区，请选择 **GPL**。

References:

- [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)
- [MIT License](https://opensource.org/license/mit)
- [Choose a License – GPL vs MIT comparison](https://choosealicense.com/licenses)
- [Wikipedia – GNU General Public License](https://en.wikipedia.org/wiki/GNU_General_Public_License)