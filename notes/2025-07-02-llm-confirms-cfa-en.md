---
audio: false
generated: true
lang: en
layout: post
title: LLMs Confirm My CFA Insights
translated: false
type: note
---

https://weibo.com/6347862377/5183994120372979

https://substack.com/inbox/post/167355695

---

As mentioned in my previous Weibo post, I like using LLMs to handle complex, tedious things I don’t enjoy doing or reading. This includes many academic papers.

More than a decade after I created PySonar2 (a Python type inference and static analyzer) in 2009-2010, I found myself discussing control-flow analysis (CFA) with ChatGPT, which brought back memories of a debate I had with a certain “CFA student” ten years ago.

https://www.yinwang.org/blog-cn/2016/04/07/cfa

(The screenshots I uploaded to a website back then are now gone. Just make do with what’s left.)

It’s quite interesting—things I saw clearly over a decade ago have now been “confirmed” by ChatGPT.

Fifteen years ago, when PySonar2 was first created, it had already surpassed all academic CFA research at the time (including the latest CFA2). For a quasi-functional language like Python with lambda closures, it was the first to achieve such precise type inference. Not only was it highly accurate, but its performance was also decent enough to analyze all large-scale Python projects on GitHub.

The founder of Sourcegraph, PySonar2’s biggest user, told me back then that PySonar2’s analysis was surprisingly precise. At the time, I didn’t think much of it because my approach was so simple that I assumed anyone could have come up with it. It wasn’t until I realized no one else had done it before that I thought maybe I should highlight its value.

Even now, JetBrains’ PyCharm IDE can’t achieve such precise analysis or “find definition” functionality. For example, if you define a global variable initialized to None and later assign it a structure in some “initialization function,” you won’t be able to find the members of that structure. I’m not saying you should write such bad code, but this is one example.

If you knew what I accomplished at Indiana University, you’d understand that PySonar2 was really no big deal for me—it took only a small fraction of my effort. Back then, I didn’t care much about the Python language. And those CFA papers were so obscure that I had no interest in diving into them. I only skimmed them and could tell they were mostly nonsense. So, I built PySonar2 in a few months, let others use it freely, and didn’t bother writing a paper. I could explain its principles in just a few sentences.

I was too modest. Look at all the CFA, k-CFA, CFA2 papers—a pile of them, yet they couldn’t solve real-world problems and were never put into practical use. k-CFA even had a basic issue where “calls and returns couldn’t match,” something I never imagined could happen. PySonar2 never had this problem. How could someone make such a foolish design, publish a paper on it, and have successors continue to “improve” it?

Matt Might’s CFA2 introduced some “pushdown automaton,” which was just a way of recovering the function call stack from the flawed designs of earlier work. PySonar2 always had a “pushdown automaton” because a stack naturally arises when interpreting function calls.

Matt Might had a blog where he proudly explained how “automatic CPS transformation” came about, as if he was the only one who understood it. But his ideas clearly evolved from overly complex CPS papers and weren’t the result of independent thinking, carrying a lot of historical baggage. His writing often sounds profound but is hard to follow—can you actually understand it? His ideas can’t compare to my “40 lines of code” approach. I was laughing when I read his blog, but out of politeness and “modesty,” I kept quiet. I think Matt Might lacks real substance, and that group of people was just spouting nonsense. That’s the truth, which I can reveal after all these years.

Aren’t these papers just producing gibberish? Yes, I knew this over a decade ago. But who could understand what was going on? Now you can check with ChatGPT :)

In fact, ChatGPT also confirmed something else: the use of CPS in Olin Shivers’ foundational CFA paper was the root of all the trouble:

PySonar2 was built entirely independently, without referencing any academic work. It directly addressed the root problem without any academic baggage. That’s the value of simple thinking. This wasn’t the first time I independently surpassed both academia and industry with such a sharp result.

After I created PySonar2, a Google team spent over two years trying to build something better, but they ended up with nothing, and Google had to keep using my improved open-source code. Why? Because their strategy was wrong from the start. They wanted to use a logic programming language like Prolog for Python’s type inference, and I knew right away it was doomed to fail. How did I know? Because I had already implemented these methods and understood the limitations of the Hindley-Milner system and Prolog. How did I know that? Because I had implemented and improved logic programming languages at IU.

I must thank ChatGPT for clearly articulating the facts I saw, saving me from reading those obscure papers. I’m grateful for its validation of the value of my ideas. I feel LLMs will greatly contribute to human progress.

Now, I’m sharing a conversation I had with ChatGPT about CFA, hoping it will help researchers in this field:

https://chatgpt.com/share/6864e9a1-66c8-8002-b9f5-55e845fde7ae
