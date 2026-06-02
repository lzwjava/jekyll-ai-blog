---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Codeforces 样例悬停高亮行为
translated: true
type: note
---

Question: 对于 Codeforces，在提供输入时，将鼠标光标悬停在一个 test case 上，是否会用黄色背景突出显示该 case，并同时突出显示输出区域中对应的输出部分？

Answer:

是的，这**正是** Codeforces 的运作方式。

当你查看题目的 sample input/output 时：

- 如果你将鼠标悬停在 **Input** 区域的任何一行（或一组行）上，该行/块会获得**黄色背景高亮**。

- 与此同时，**Output** 区域中**相应的部分**也会以同样的黄色背景高亮显示。

这是一个非常有用的功能，尤其是当：
- 有多个 sample test cases 时
- 输入/输出规模很大时
- 你想快速查看哪个输出属于哪个输入时

输入和输出部分之间的高亮是同步的。Codeforces 会将对应的输入/输出对进行分组，当你悬停在其中任意一侧时，系统会同时高亮它们。

这种行为已经存在多年，并且在 2026 年依然存在。

References:
