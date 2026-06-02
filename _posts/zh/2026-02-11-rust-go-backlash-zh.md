---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 对 Rust 和 Go 负面评价的真实呈现
translated: true
type: note
---

**Question: Analyze this Weibo post in English.**

**Answer:**

这篇微博文章（背景为 2026 年 2 月或更早）是一位显然已退休或资深的 Programmer 表达的带有强烈主观色彩的个人抱怨。作者对围绕两种现代流行语言——**Go**（早期浪潮）和 **Rust**（当前浪潮）的 **hype cycles**（炒作周期）、**community cultures**（社区文化）以及 **technical choices**（技术选择）表达了深切的挫败感和鄙夷。

### 核心观点与论据

1. **历史平行对照：Go → Rust**
   作者将 Rust 目前的统领地位和粉丝狂热视为 2010-2015 年间 Go 所经历过程的重演。两种语言都经历过（或正在经历）爆发式的人气、通过 meetup/hackathon 进行的大规模营销，以及一种让作者感到傲慢且不友好的社区氛围。

2. **技术批评**
   - **Go**：
     主要只解决了一个好用的功能（通过 goroutines 实现轻量级 concurrency），但刻意忽略了先前语言中的许多“优秀”特性（如 generics——很晚才加入；exceptions 等）。这导致代码冗长、重复且容易出错。作者声称，在实践中 Go 的 codebase 会变得混乱，甚至不如写得好的 C。随着许多老牌语言现在也提供 async/await 或类似的轻量级 concurrency，Go 已经失去了其独特的卖点。
   - **Rust**：
     设计过度复杂。borrow checker 和 ownership 模型虽然解决了 memory safety 问题，但也带来了沉重的认知负荷，分散了对实际 business problem 的注意力。作者认为它并没有优雅地解决 memory management，反而制造了新层面的困难。

3. **社区与文化批判（主题）**
   - 特定语言的 meetup 反复令人失望：没有进行深入的技术讨论，取而代之的是自命不凡的演讲者吹嘘自己的背景（例如：“我以前用 Haskell，现在 Rust 让我成了精英”）。
   - 轶事：
     - Go meetup 的参与者轻蔑地问：“如果你不用 Go，你来这儿干嘛？”
     - 在东京的一位 Rust 演讲者表现出极强的支配欲（敲桌子）。
     - 一位前“Haskell programmer”同事导致了项目长期延误，产出了有问题的设计，后来转而狂热地推广 Rust，却没能交付任何有用的成果。
   - 更广泛的模式：那些不断强调自己使用哪种语言的人，往往是素质较低的 engineer。那些大声广告“我们使用 Go/Rust”的公司，通常具有令人不快、教条主义的氛围。
   - 预测：Rust 将产生与之前的 Scala 和 Go 类似的负面结果（over-engineering、有毒的内部文化、项目停滞）。

4. **个人立场与动机**
   作者承认自己存有偏见（公开称 Go 是“屎”，并预期 Rust 也会如此）。他们之前写过关于 Go 和 Scala 的批评性评价，一些读者（如前 Twitter 员工）后来证实对 Scala 的批评符合现实。
   由于现在已经“退休”且没有求职压力，该帖子旨在为那些仍在此类环境中受苦的人提供警告或情感宣泄。
   邀请他人分享真实的 Go/Rust 经历，以验证这种直觉是否成立。

### 整体语调与风格
非常直率、愤世嫉俗且具有轶事性——很大程度上依赖于个人故事而非系统性的证据。使用了强烈的措辞（“傲慢”、“自命不凡”、“教条主义”等），并对语言的 evangelism（传教）/部落主义表现出明显的蔑视。

### 这种观点罕见吗？
并不罕见——类似的抱怨多年来一直在英语社区流传：
- 当出现任何设计批评时，Go 有时会被称为具有“毒性”（防御性反应）。
- Rust 在某些圈子中长期以来一直以社区傲慢/不友好而闻名（尤其是对 Stack Overflow、Discord 等平台上的初学者），经常出现“与 borrow checker 作斗争”的职业倦怠故事以及对狂热主义的指责。
- 编程语言的部落主义/追星现象在许多语言中都是众所周知的现象（包括 Haskell、JavaScript 框架等）。
作者的经历与网上反复出现的关于语言 evangelism 导致邪教般的 meetup 行为，以及过度认同某种语言的公司中糟糕的团队文化的讨论是一致的。

简而言之，这篇文章是“老牌经验丰富的 Programmer 对抗现代语言炒作”流派的典型代表——对时尚驱动的技术采用持怀疑态度，不信任将自我价值与语言选择挂钩的社区，并坚信在考虑现实的代码质量和团队动态时，技术简单性 + pragmatism（务实主义）优于功能繁重的“安全”语言。

**References:**

- [Why is the Rust community often so arrogant? (Rust Users Forum, 2020)](https://users.rust-lang.org/t/why-is-the-rust-community-often-so-arrogant/51415)
- [Rust's Community Toxicity Is Driving Away Better Engineers Than It Attracts (Medium, 2026)](https://medium.com/@kp9810113/rusts-community-toxicity-is-driving-away-better-engineers-than-it-attracts-2b6df0165380)
- [Why the Go community is so toxic? (Reddit r/golang)](https://www.reddit.com/r/golang/comments/1bvl207/why_the_go_community_is_so_toxic/)
- [Rust vs Go community discussions and comparisons (various sources including Hacker News, forums)](https://news.ycombinator.com/item?id=30442235)
