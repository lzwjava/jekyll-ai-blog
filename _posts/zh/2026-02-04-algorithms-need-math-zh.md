---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 算法追求数学而非代码
translated: true
type: note
---

我将搜索有关 Leslie Lamport 以此为标题的演讲信息。根据我的搜索，虽然我没有找到完全以此为题的特定演讲，但 Leslie Lamport 在多次演讲和文章中都一致阐述了这一观点。他的核心信息如下：

Lamport 认为，program verification 的困难在于 algorithm 本身，而不是用于表达它的 programming language。他认为，即使是精通 C++ 等语言的 programmers，往往仍然无法写出符合预期功能的 programs。

他的主要观点包括：

**Mathematics 优于 programming languages**：Lamport 主张 algorithm 应该用 mathematics 而不是 programming languages 来表达，因为处理大型程序和生成高效代码的需求增加了 programming languages 的复杂性，并限制了它们的 expressiveness。

**Think before you code**：Lamport 认为，获得更好的 programs 的最佳方法是教会 programmers 如何更好地思考，而不是给他们新的 languages 或更好的 debugging tools。他感叹 programmers 往往在编写正式的 specification 之前就胡乱拼凑出一个系统。

**TLA+ 是他的解决方案**：他创建了 TLA+，旨在迫使 engineers 在 coding 之前进行数学化思考并编写 specifications。他希望人们能够“跳出框框思考”——而这个“框框”就是指用 coding languages 进行“programmatically 思考”，而不是进行数学化思考。

他的批评从根本上指出，过度关注 programming languages 是舍本逐末——真正的挑战在于清晰的 algorithmic thinking，而这通过 mathematical specifications 才能得到最好的表达。