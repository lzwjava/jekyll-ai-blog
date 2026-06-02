---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Rust 的冷门批评
translated: true
type: note
---

问题：关于 Rust 编程语言、使用 Rust 开发项目或在初创公司或大公司中采用 Rust，有哪些不受欢迎的观点？

回答：

Rust 因其内存安全、性能和并发特性而广受赞誉，但它也招致了强烈的批评，尤其是在其复杂性和对特定环境的适用性方面。下面，我整理了一份来自开发者讨论、博客文章和论坛的不受欢迎的观点清单。这些观点强调了在生产力、招聘和实际用例方面的权衡。为了清晰起见，我将它们分组归类，重点关注那些挑战 Rust 炒作的观点。

### 关于 Rust 作为一门语言的一般观点

- **Rust 的借用检查器和所有权模型给大多数开发者带来了比解决更多的问题的摩擦**：虽然它能防止内存错误，但它往往会强制进行过度的重构和问题解决，使得简单的任务感觉过于工程化。即使是经验丰富的用户也表示经常遇到困难，导致生产力低于像 Go 或 Python 这样的垃圾回收语言。
- **Rust 被过度炒作，并非真正“安全”或具有革命性**：批评者认为它只是 C++ 加上额外的语法糖，仍然依赖于 `unsafe` 块来进行实际的系统工作，并且它无法消除逻辑错误或操作系统级别问题（如零终止字符串）带来的漏洞。“内存安全”的说法忽略了大多数 bug 源于糟糕的设计选择，而不仅仅是内存管理。
- **社区有毒且过于传教式**：Rust 的粉丝咄咄逼人地将其推崇为 superior，羞辱使用 C++ 等“不安全”语言的用户，这疏远了潜在的采用者。这种类似邪教的氛围，加上以 DEI 为重点的入门（例如，官方书籍的介绍），感觉更像是社会工程，而非技术讨论。
- **编译时间和错误消息简直是噩梦**：Rust 鼓励泛型和零成本抽象，但这会导致构建时间膨胀（尤其是有依赖项时），并产生难以理解的级联错误，令人沮丧。它更适合经过深思熟虑、优化的代码，而不是快速实验。
- **Rust 不适合低级或高级工作——它卡在中间**：对于裸机系统，`unsafe` 使其比 C 更笨拙；对于高级应用程序，它不如具有依赖类型或内置运行时的语言富有表现力。它只在狭窄的“中级”利基市场中真正闪耀。

### 关于使用 Rust 进行项目开发的观点

- **Rust 阻碍了原型开发和个人项目**：它擅长生产代码，但对于黑客或一次性脚本来说却很糟糕——重构是强制性的，而不是修改，而且大多数早期代码无论如何都会被丢弃。坚持使用 C 或 Python 进行实验。
- **将遗留代码移植到 Rust 是浪费时间**：几十年前的 C/C++ 程序已经修补了大部分 bug；重写会引入新的错误，而不会修复逻辑缺陷。只将 Rust 用于绿地项目，而不是“用 Rust 重写”的 Cargo Cult。
- **Rust 的“捷径”破坏了其安全承诺**：诱人的工程学（例如，自动解引用）在修复时会导致性能下降，这与“快速发布”文化相冲突。它与企业追求速度而非完美的推动不兼容。
- **Rust 中的后端开发很简单——别再夸大难度了**：除非你正在构建自定义分配器或异步运行时，否则它大部分是处理程序中的数据流。消极情绪源于精英主义；你可以在没有“硬核模式”的情况下快速、无错误地发布。

### 关于在初创公司中使用 Rust 的观点

- **Rust 扼杀了初创公司的发展速度——优先选择 Python 或 JS 等更简单的语言**：安全固然很好，但陡峭的学习曲线减缓了入职和迭代速度。初创公司需要敏捷性，而不是与编译器作斗争；Rust 的好处很少能抵消招聘和生产力成本。
- **招聘 Rust 开发人员对于扩展团队来说是个噩梦**：经验丰富的 Rust 工程师很少，导致知识孤岛以及“Rust 专家”和新手之间的不满。这是一个冒险的赌注，除非你的产品从第一天起就要求低级性能。

### 关于在大型公司中使用 Rust 的观点

- **Rust 在大型组织中带来的问题多于解决的问题**：成功案例（例如，高性能服务）通常会导致过度采用，但重构和薄弱的标准库增加了不断发展的代码库的认知负荷。使用更安全语言的单体最初扩展性更好。
- **企业支持掩盖了 Rust 的缺陷**：大型科技公司对工具的补贴掩盖了它不够简单或通用，无法广泛用于企业。它被用于安全剧场，但遗留集成和薄弱的生态系统使其成为一个糟糕的默认选择。
- **Rust 职位稳定但比遗留语言的宽容度低**：对能力不足的容忍度较低意味着更高的压力；它不像人们担心的那样是“职业死胡同”，但大型公司仍然坚持使用 C++/Java 来处理其庞大的代码库，限制了 Rust 的足迹。

这些观点反映了少数对 Rust 在非理想场景下的严谨性感到沮丧的开发者。尽管如此，Rust 在内核（例如 Linux）和像 Microsoft 这样的公司中的采用表明，它在适合的领域——系统和性能关键代码——正在蓬勃发展。如果你正在评估它，请先原型化一个小项目来测试其适应性。

### 参考文献

- [The Rust programming language absolutely positively sucks](https://www.reddit.com/r/rust/comments/12b7p2p/the_rust_programming_language_absolutely/)
- [What are some unpopular opinions on Rust that you’ve come across?](https://www.reddit.com/r/rust/comments/1b4uny4/what_are_some_unpopular_opinions_on_rust_that/)
- [Why are some people against the Rust-Lang?](https://users.rust-lang.org/t/why-are-some-people-against-the-rust-lang/93906)
- [Why do people hate Rust?](https://www.reddit.com/r/rust/comments/cgs9lj/why_do_people_hate_rust/)
- [My negative views on Rust](https://chrisdone.com/posts/rust/)
- [Negative views on Rust (not mine!)](https://users.rust-lang.org/t/negative-views-on-rust-not-mine/69566)
- [I hate Rust (programming language)](https://dorinlazar.ro/240228-i-hate-rust-programming-language/)
- [I hate Rust (programming language) | Hacker News](https://news.ycombinator.com/item?id=40091427)
- [A genuine question, why do people hate rust](https://devrant.com/rants/7730580/a-genuine-question-why-do-people-hate-rust)
- [What are legitimate problems with Rust?](https://www.reddit.com/r/rust/comments/uum5re/what_are_legitimate_problems_with_rust/)
- [Using Rust at a startup: A cautionary tale](https://mdwdotla.medium.com/using-rust-at-a-startup-a-cautionary-tale-42ab823d9454)
- [Using Rust at a Startup: A Cautionary Tale - Slashdot](https://it.slashdot.org/story/22/12/02/1735218/using-rust-at-a-startup-a-cautionary-tale)
- [Rust Unpopular Opinion | Hacker News](https://news.ycombinator.com/item?id=34386622)
- [Using Rust at a startup: A cautionary tale | Hacker News](https://news.ycombinator.com/item?id=33714007)
- [Using Rust at a startup: A cautionary tale](https://www.reddit.com/r/golang/comments/z4bg24/using_rust_at_a_startup_a_cautionary_tale/)
- [Using Rust at a startup: A cautionary tale](https://scribe.rip/using-rust-at-a-startup-a-cautionary-tale-42ab823d9454)
- [Why is Rust so unpopular among programmers?](https://www.quora.com/Why-is-Rust-so-unpopular-among-programmers-Is-it-because-of-its-difficulty-or-something-else)
- [Why Rust is a great choice for startups | Hacker News](https://news.ycombinator.com/item?id=31736703)
- [Rust? Seriously? Why bother with it?](https://www.reddit.com/r/rust/comments/14lyvfx/rust_seriously_why_bother_with_it/)
- [Rust success story that killed Rust usage in a company](https://www.reddit.com/r/rust/comments/1kp74t2/rust_success_story_that_killed_rust_usage_in_a/)
- [Why don't you use Rust at your company?](https://www.reddit.com/r/rust/comments/1ital1t/why_dont_you_use_rust_at_your_company/)
- [Is Rust a career dead-end?](https://www.reddit.com/r/rust/comments/1f5mt1f/is_rust_a_career_deadend_as_opposed_to_c_or_any/)
- [Why is Rust community being so political?](https://www.reddit.com/r/rust/comments/v88mm6/why_is_rust_community_being_so_political/)
- [I actually might lose credibility for this one, but I don't think startups should be using Rust](https://x.com/charliermarsh/status/1867927883421032763)
- [We (IT crowd) need more common sense and less hysteria around Rust](https://x.com/Komorebi_Knight/status/1996219456448524553)
- [Rust is a great production language (engine programming), but it's not a perfect prototyping language](https://x.com/SebAaltonen/status/1858777286037635441)
- [Rust is a great language... but dang I still struggle with the borrow checker constantly!](https://x.com/devongovett/status/1858273608982024477)
- [My general thoughts on Rust: Excellent for short-lived programs... Clunky for long-lived programs... Toxic community](https://x.com/awesomekling/status/1822241531501162806)
- [The problem seems to be that Rust offers too many tempting shortcuts for a tool that prides itself on safety](https://x.com/ccarp87/status/1995528037882814826)
- [Porting decades old programs to Rust is dumb](https://x.com/antoniosarosi/status/1988376391608660019)
- [I've done some rust dev, not a fan of the language](https://x.com/CongoCart/status/1995656806006407565)
- [Unless you’re doing systems-level work... Rust for backend development is surprisingly straightforward](https://x.com/chinedu_10/status/1991787938489811212)
- [Terrible idea for enterprise critical use software](https://x.com/Zerotrust4m/status/1994594547393782039)
- [Rust, for me, sits in this weird spot](https://x.com/aramh/status/1913182592758657491)
- [I use rust. I have a lot of complaints about rust](https://x.com/wlp3s0/status/1995524306726756594)
- [Rust is worth learning, but after writing it for a few years, Im disenchanted with it](https://x.com/0xglitchbyte/status/1875580441358422343)
