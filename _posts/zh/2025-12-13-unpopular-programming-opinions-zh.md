---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 关于编程列表的一些冷门观点
translated: true
type: note
---

问题：关于编程中列表有哪些不受欢迎的观点？

回答：

编程中的列表（通常指Python的list、Java的ArrayList或C++的vector等动态数组，以及链表）是一种常见的数据结构，但一些非主流或反主流的观点挑战了它们的广泛使用或受到的赞扬。以下是一些来自开发者讨论的值得注意的不受欢迎的观点：

- **链表被高估了，在实践中很少有用**：一种普遍的观点是，由于缓存局部性差，链表表现不佳，导致遍历速度比连续数组慢，尽管在某些情况下理论上可以实现O(1)的插入/删除操作。许多人认为，除非在非常特定的场景（例如，系统编程中的侵入式列表），否则应该避免使用链表，动态数组（向量）在实际性能上几乎总是更优。

- **像Python这样的语言中的标准列表（动态数组）对于数值计算效率低下**：Python列表很灵活，但对于同构数据来说过于复杂且速度慢；NumPy数组或其他专门的结构在计算速度和内存方面要好得多。

- **列表推导式（例如，在Python中）降低了代码可读性**：尽管它们因简洁性而受欢迎，但有些人发现它们比显式循环更难阅读和调试，更喜欢冗长以提高清晰度，尤其是在团队或维护环境中。

- **尽可能优先使用固定大小的数组而不是动态列表**：动态列表增加了开销（重新调整大小、间接寻址）；如果大小已知或有界，普通数组更快，使用的内存更少，并且更简单。

- **早期教授链表会损害理解**：它们在教育中受到强调，但很少在没有抽象的情况下专业使用；过分关注它们会分散对更实用的结构（如数组/向量）的注意力。

这些观点通常源于对现代硬件的性能担忧，其中缓存效率胜过理论上的大O优势。

参考文献：

- [为链表辩护（反驳批评，但承认争议）](https://www.rfleury.com/p/in-defense-of-linked-lists)
- [Python列表被高估了（对于数值任务）](https://towardsdatascience.com/python-lists-are-overrated-776e87cda3e5/)
- [Reddit: 有没有人讨厌列表推导式？](https://www.reddit.com/r/learnprogramming/comments/19a0fvn/does_anyone_else_hate_list_comprehension/)
- [Bjarne Stroustrup关于避免链表](https://www.reddit.com/r/programming/comments/1h7ikrt/bjarne_stroustrup_why_you_should_avoid_linked/)
- [为什么你不应该再在你的代码中使用链表](https://kjellkod.wordpress.com/2012/02/25/why-you-should-never-ever-ever-use-linked-list-in-your-code-again/)
- [Hacker News上关于链表与数组的讨论](https://news.ycombinator.com/item?id=33473497)