---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Unpopular Opinions on Programming Lists
translated: false
type: note
---

Question: What are unpopular ideas about lists in programming?

Answer: 

Lists in programming (often referring to dynamic arrays like Python's list, Java's ArrayList, or C++'s vector, as well as linked lists) are a common data structure, but several contrarian or less mainstream opinions challenge their widespread use or praise. Here are some notable unpopular ideas drawn from developer discussions:

- **Linked lists are overrated and rarely useful in practice**: A common view is that linked lists perform poorly due to poor cache locality, making traversal slower than contiguous arrays despite theoretical O(1) insertions/deletions in some cases. Many argue they should be avoided unless in very specific scenarios (e.g., intrusive lists in systems programming), and dynamic arrays (vectors) are almost always superior for real-world performance.

- **Standard lists (dynamic arrays) in languages like Python are inefficient for numerical work**: Python lists are flexible but overkill and slow for homogeneous data; NumPy arrays or other specialized structures are far better for speed and memory in computations.

- **List comprehensions (e.g., in Python) reduce code readability**: While popular for conciseness, some find them harder to read and debug than explicit loops, preferring verbosity for clarity, especially in team or maintenance contexts.

- **Prefer fixed-size arrays over dynamic lists whenever possible**: Dynamic lists add overhead (resizing, indirection); if the size is known or bounded, plain arrays are faster, use less memory, and are simpler.

- **Teaching linked lists early harms understanding**: They are emphasized in education but rarely used professionally without abstraction; focusing on them distracts from more practical structures like arrays/vectors.

These opinions often stem from performance concerns on modern hardware, where cache efficiency trumps theoretical big-O advantages.

References:  

- [In Defense Of Linked Lists (countering the hate, but acknowledging the debate)](https://www.rfleury.com/p/in-defense-of-linked-lists)  
- [Python Lists Are Overrated (for numerical tasks)](https://towardsdatascience.com/python-lists-are-overrated-776e87cda3e5/)  
- [Reddit: Does anyone else hate list comprehension?](https://www.reddit.com/r/learnprogramming/comments/19a0fvn/does_anyone_else_hate_list_comprehension/)  
- [Bjarne Stroustrup on avoiding linked lists](https://www.reddit.com/r/programming/comments/1h7ikrt/bjarne_stroustrup_why_you_should_avoid_linked/)  
- [Why you should never, ever, EVER use linked-list in your code again](https://kjellkod.wordpress.com/2012/02/25/why-you-should-never-ever-ever-use-linked-list-in-your-code-again/)  
- [Hacker News discussions on linked lists vs arrays](https://news.ycombinator.com/item?id=33473497)