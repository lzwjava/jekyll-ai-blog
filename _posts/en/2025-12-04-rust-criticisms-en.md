---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Rust's Unpopular Criticisms
translated: false
type: note
---

Question: What are unpopular opinions about the Rust programming language, using Rust to develop projects, or adopting it in startups or big corporations?

Answer:

Rust is widely praised for its memory safety, performance, and concurrency features, but it also attracts strong criticism, especially around its complexity and fit for certain environments. Below, I've compiled a list of unpopular opinions drawn from developer discussions, blog posts, and forums. These highlight trade-offs in productivity, hiring, and real-world use cases. I've grouped them into categories for clarity, focusing on those that challenge the hype around Rust.

### General Opinions on Rust as a Language
- **Rust's borrow checker and ownership model create more friction than they solve for most developers**: While it prevents memory bugs, it often forces excessive refactoring and puzzle-solving, making simple tasks feel overly engineered. Even experienced users report constant struggles, leading to lower productivity compared to garbage-collected languages like Go or Python.
- **Rust is overhyped and not truly "safe" or revolutionary**: Critics argue it's just C++ with extra syntax sugar, still relying on `unsafe` blocks for real systems work, and it doesn't eliminate logical errors or vulnerabilities from OS-level issues like zero-terminated strings. The "memory safety" narrative ignores that most bugs stem from bad design choices, not just memory management.
- **The community is toxic and overly evangelical**: Rust's fans aggressively push it as superior, shaming users of "unsafe" languages like C++, which alienates potential adopters. This cult-like vibe, combined with DEI-focused onboarding (e.g., the official book's intro), feels more like social engineering than technical discussion.
- **Compile times and error messages are a nightmare**: Rust encourages generics and zero-cost abstractions, but this balloons build times (especially with dependencies) and produces cryptic, cascading errors that frustrate iteration. It's better for deliberate, optimized code than quick experimentation.
- **Rust isn't ideal for low-level or high-level work—it's stuck in the middle**: For bare-metal systems, `unsafe` makes it clumsier than C; for high-level apps, it's less expressive than languages with dependent types or built-in runtimes. It's only truly shines in a narrow "mid-level" niche.

### Opinions on Using Rust for Project Development
- **Rust hinders prototyping and personal projects**: It excels at production code but sucks for hacks or throwaway scripts—refactoring is mandatory instead of quick-and-dirty changes, and most early code gets discarded anyway. Stick to C or Python for experimentation.
- **Porting legacy code to Rust is a waste of time**: Decades-old C/C++ programs have already patched most bugs; rewriting introduces new errors without fixing logical flaws. Use Rust for greenfield projects only, not "rewrite it in Rust" cargo cults.
- **Rust's "shortcuts" undermine its safety promises**: Tempting ergonomics (e.g., auto-dereferencing) lead to performance regressions when fixed, clashing with "ship fast" culture. It's incompatible with enterprise pushes for speed over perfection.
- **Backend development in Rust is straightforward—stop overhyping the difficulty**: Unless you're building custom allocators or async runtimes, it's mostly data flow in handlers. The negativity stems from elitism; you can ship fast and error-free without "hard mode."

### Opinions on Using Rust in Startups
- **Rust kills velocity in startups—prioritize simpler languages like Python or JS**: Safety is great, but the steep learning curve slows onboarding and iteration. Startups need agility, not fighting the compiler; Rust's benefits rarely outweigh hiring and productivity costs.
- **Hiring Rust devs is a nightmare for scaling teams**: Few experienced Rust engineers exist, leading to knowledge silos and resentment between "Rust experts" and newcomers. It's a risky bet unless your product demands low-level perf from day one.

### Opinions on Using Rust in Big Corporations
- **Rust creates more problems than it solves in large orgs**: Success stories (e.g., high-perf services) often lead to over-adoption, but refactoring blasts and thin stdlib increase cognitive load in evolving codebases. Monoliths in safer languages scale better initially.
- **Corporate backing hides Rust's flaws**: Big Tech subsidies for tooling mask that it's not simple or versatile enough for broad enterprise use. It's pushed for security theater, but legacy integration and thin ecosystem make it a poor default.
- **Rust jobs are stable but less forgiving than legacy languages**: Less incompetence tolerance means higher pressure; it's not a "career dead-end" like feared, but big corps stick to C++/Java for their massive codebases, limiting Rust's footprint.

These opinions reflect a vocal minority frustrated by Rust's rigidity in non-ideal scenarios. That said, Rust's adoption in kernels (e.g., Linux) and companies like Microsoft shows it's thriving where it fits—systems and perf-critical code. If you're evaluating it, prototype a small project first to test the fit.

### References:
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
