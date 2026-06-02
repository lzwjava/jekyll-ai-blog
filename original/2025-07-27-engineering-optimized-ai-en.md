---
audio: false
generated: false
image: false
lang: en
layout: post
title: Optimizing Software Engineering for AI
translated: false
type: post
---

### Table of Contents

1. [Optimizing Software Engineering for AI](#optimizing-software-engineering-for-ai)
    - Flat Architecture for AI-First Development
    - Python's Advantages in AI-Driven Workflows
    - Context Engineering and Token Optimization
    - Structuring Code for AI Assistance

2. [Thriving as a Manual AI Agent](#thriving-as-a-manual-ai-agent)
    - Working with AI Tools in Enterprise Environments
    - Tool Selection and Context Management
    - Building Reusable Prompt Systems

3. [Leveraging Python for Java Development](#leveraging-python-for-java-development)
    - Python Scripts for Java Project Support
    - Cross-Language Development Strategies
    - AI-Assisted Code Generation

4. [Programming Languages in the AI Era](#programming-languages-in-the-ai-era)
    - Future of Python, Rust, and Java
    - Performance vs. Simplicity Trade-offs
    - Language Evolution and AI Integration

### Optimizing Software Engineering for AI

In this blog, I utilized hundreds of scripts to assist with translation, playground, frontmatter maintenance, and Telegram bots. I believe this development approach might represent the future of software engineering optimized for AI.

I don't rely much on Python module functionality, nor do I want to structure code like a large Java Spring project.

I have worked on many software projects throughout my career. I have observed impressive banking architectures, microservices, effective multi-country designs that minimize duplication, robust foundational frameworks built on top of Spring, and strong governance with centralized configuration.

While these banking architectures are impressive, if we were to start today, I would consider optimizing for LLMs and AI. This would involve better context engineering, improved separation of concerns, and prioritizing AI-first thinking over human-centric design. Although Spring offers multiple layers and good abstraction, it can be challenging for LLMs and AI to navigate.

I believe we should aim for flatter structures, similar to a flat organization. This means using just two levels: the first level calls the second level. In a function, it's better to call another 50 functions directly rather than having 50 nested levels or stacks. AI/LLM struggle to judge or infer overly complex, nested structures, but they excel at handling smaller functions of 100 to 200 lines of code. Python is well-suited for calling and importing from other files.

One reason Python code is easier than Java is that its dependency management is simple. You just need to use `pip install` to add a dependency. With Maven, you need to write the dependency in a POM XML file and then use `mvn compile` to let Maven download the dependencies.

Another reason for Python's simplicity is that its code can be directly run without hassle.

Though starting with Java 11, the `java` command can directly execute single-file source-code programs without needing to compile them separately using `javac`. However, often for Java projects, they are large, so one has to run them with `mvn spring-boot:run` along with some properties configuration.

A third reason is that Python's module design is simple; you can use `from` and `import` to easily import code from other files.

For now, many AI chatbots can run Python code directly in the chatbot window, like Grok.

When comparing 100 Java files, each with around 1000 lines of code, to some simple Python scripts, it is not a fair comparison. For this kind of project, I would prefer to have 1000 Python files, each with around 100 lines of code.

It is acceptable to select lines of code or a function to edit. However, you need to know where to select. Why not let this task be handled by AI to make our lives easier? So, we just need to use "select all" to select all the code and tell AI/LLM how to edit.

For Python, it is easier to use `if __name__ == "__main__":` to run and test functions in a file. It is also easier for other Python files to call the functions inside this file without needing to run the test.

This is context engineering optimized for AI. Could we approach it in other ways? AI/LLM is auto-regressive. However, when we use Copilot or Claude Code, we don't know how the AI Software Agent helps us. They should think about it instead of us.

Could we, on the user side, arrange code specifically to reduce token usage? For this point, the approach of having 1000 Python files with each 100 lines of code is good for this purpose. Because you can verify functions and code files easily before letting other Python code call them.

But one problem is that if you want to change several files of code together, it is not easy to do so. For a simple way, you can copy the code to AI chatbots and let them tell you how to edit code in these files.

Possibly, we don't need to use the number of lines to separate functions or logic. But we should do it to separate logic into small functions. We can do this by naturally separating them by type of logic, so they appear shorter.

Why do we want Software Engineering Optimized for AI? Because AI is powerful, we should optimize everything for AI and then let AI help software engineering as much as possible.

It is possible not just for code, but for any text too. Suppose we are very picky editors; we don't want AI to edit our large texts at once. We want to check paragraph by paragraph. For code, we can tolerate minor errors or bugs. For text, we can tolerate them because most readers are not so picky.

But code is different in that sometimes, even a minor error can lead to the complete malfunction of a large project.

For XML or YAML files, we probably don't need to separate them as much because they are already highly structured.

And for HTML files, we should do some separation. Instead of writing hundreds of JavaScript files together with hundreds of HTML files, making it easy to exceed 1000 lines of code, we should use `import` for JavaScript to manage this. For JavaScript code, we can use the above ways to separate.

We want to structure code in ways that let AI help us easily add, edit, delete, and run code. This is the beginning. Think of a day when all code can be generated or fixed by AI easily. The world will be highly digitalized.

Imagine myself writing 100 big software projects and providing APIs to connect with others. This includes my daily agenda; I am, myself, like a 1000-employee tech company nowadays. They are customized for my needs, to earn money or spend money for my benefits. This is really amazing.

### Thriving as a Manual AI Agent

AI Agents should be automatically run with code. Now, the title of this essay is "Manual AI Agent." You might think I am kidding, but I am not.

The reason I say "manual AI agent" is that for big companies, technology adoption is slow due to security data concerns and long-term considerations.

There are a lot of new technologies in the market; who knows what will last or what will disappear quickly.

They also have security data concerns. Typically, they want to partner with big brands whose data policies are strict and monitored by the public. This explains why Microsoft has become a top partner among Fortune 500 companies. Other companies use their Teams, Microsoft Office 365, Azure, and Copilot.

That means we will use a lot of tools to work, similar to tool use or function calling in those APIs. We will do our own prompt engineering or context engineering.

Instead of using Claude Code or Manus to do a complex task, we may perform tasks ourselves with a plain AI chatbot and its APIs.

AspectJ is good because it uses AOP programming to intercept methods. Filters in Spring are also good for capturing the logs of HTTP requests. The logger in Log4j is good for redirecting specific logs to a file. IntelliJ IDEA is good because it has a function to export objects as text.

SQL clients are good because they can easily export CSV or Excel files of rows. Git diff is good because it can give you comparison text.

They all help you provide better context for AI chatbots. And AI chatbots can also help a lot of Python scripts to perform tasks.

To be an effective AI agent, you need to use many effective tools to help you do tasks, whether simple or complex.

So you do not need to ask AI chatbots many times like those automatic AI agents. You can carefully select the tools that you will use.

So working like a manual AI agent has its benefits. However, AI agent technology evolves fast and shows its potential to the world.

If they are very useful, big companies will adopt them just like AI chatbots. Otherwise, they cannot compete with other companies that have adopted them—not just other big companies, but also small startups. Because AI is so powerful now, a startup with tens of employees may beat those with 1,000 employees.

Working as manual AI agents is sometimes unavoidable. The job has other benefits besides lacking advanced AI technology. It is not easy to find good jobs, too. So in this case, it happens to give us space to use our traditional wisdom to make the most use of AI chatbots.

And it means that we can organize and accumulate our prompts to create system prompts for AI chatbots, similar to those used by Claude or Grok that have been exposed. This way, we don't need to write prompts repeatedly. We can use Python scripts to assist us in writing prompts. We can obtain the logs of HTTP requests and write prompts to generate API test cases.

The magic of programming lies in its unlimited levels of abstraction. It's akin to functions where you can have 100 levels of function calls. For instance, WeChat is built on top of iOS, and WeChat Mini Programs are built on top of WeChat. iOS itself is built on top of Objective-C or Swift, which in turn are built on top of LLVM and the instruction set of Apple's ARM chips.

### Leveraging Python for Java Development

How to use Python to help Java development in the AI era? I like Python. I have worked with Python the most in the last around 3 years, since ChatGPT was released at the end of November 2022.

One way to help is using Python to write SQL helper scripts, test scripts, and log searching scripts for Java projects.

Use Python to analyze POM files and package dependencies for Java. Use Python to check data consistency in Java. There are a lot of things we can do in Python instead of Java.

But Java doesn't have PyTorch. Python can help with anything in 200 lines of code that would take 500 lines in Java. But by using AI tools, you can't easily get your own version of PyTorch either. Even something like TinyGrad takes time to build.

Why write our own scripts first? One reason is that it is super customizable. There are no public software or open-source projects that can help us directly in our projects, especially those in big companies.

The big projects in big companies are developed over one decade or more. They already have a lot of customization.

So in the future, there will be a lot of surrounding projects around the big projects in big companies. There will be more Claude-like code routers in internal coding agent tools in big companies. There will be more customized Postman, SQL clients, and compilers for big companies.

Using Python code can connect to Java agents too.

It means that I need to learn Python and Java well, so that I know how to use one to help the other.

And I can use Python with the help of AI to create a lot of things for myself and in corporate projects too. Java seems like no obstacle. Java, with Spring, databases, and with Angular, Vue, or React serving as frontend, shouldn't be an obstacle to having Python help a lot.

Programming is such a flexible thing. The limit is our imagination.

So AI is growing fast. We can measure AI's progress by how much and how easily we can use code to achieve things with AI's help in coding and learning.

Could we one day write some AI agents, and then these agents help create an entire TikTok, including its lots of microservices and big iOS or Android projects?

If AI is so powerful, what should we do today? Probably nothing, as what we do today will be easy to implement with AI. In 2025, our 1 year's work with the help of AI probably can be done in 1 month with 2030's AI ability.

This brings up our essential question: What's our life purpose? What's all this about? How to live a good life?

AI is coming out like other technologies to bring us freedom. But it seems everyone is busy like a machine in this capital society.

Coming back to the topic. So Python can help write Java code too. You can use Python to get the context for writing code and let Copilot write it for you to do it right on the first shot.

AI is about prompt engineering and context engineering. Prompts and context help the responses of AI chatbots.

Python can help with context; Python can help generate prompts.

So this is not just about Java, but every other programming language. Python can help them deeply. So why do we still need to use other programming languages?

It is Python's intrinsic design that makes it perform poorer than other programming languages, like C, C++, or Rust.

### Programming Languages in the AI Era

AI is so powerful now that we have to rethink everything from the perspective of AI. Which programming languages will be popular in the next 10 years?

Python surely will be. Many AI chatbots use Python to execute code in the browser, like Grok. Python is popular for its simplicity, ease of learning, and decent performance. It is adopted by many software projects.

Python is slower than C++, Java, and Rust. Java has a large community. Rust is built on top of C.

I wonder whether many projects will be rewritten or replaced by Rust. Being rewritten in Rust means referring to an old project and using Rust to implement the same functionality. Being replaced means that software written in other languages is now replaced by similar software written in Rust.

Rust has a relatively complex syntax. But in the AI era, that is not a big problem, because AI will help write code. For complex syntax, humans don't actually have much trouble either.

I think Hindi or Tamil are quite complex. But for Indians who live in the North, Hindi is not a problem, and for those in the South, Tamil is not a problem either.

But for a Chinese citizen like me, I think it is a big problem to learn.

At first glance, all characters in Hindi look similar to me. I think the difference between Hindi and Arabic is like the difference between Chinese and Japanese, or English and Spanish.

The differences between programming languages are less than those between natural languages. One big reason is that programming languages only differ in character appearance, while natural languages also differ in sound. Natural languages differ in two aspects: character set and pronunciation.

Programming languages have only about a century of history, but natural languages have more than 100 centuries. The more time people spend on something, the more differences develop. People with slightly different opinions will create their own versions of things.

That explains the English accent. In some TikTok videos, people say the worst English accent is Birmingham.

So actually, Rust doesn't have much of a problem. Its performance is quite good, as it is built on top of C/C++.

Performance is critical for many applications. Nowadays, many apps are used by billions of people. For underlying cloud computing infrastructure, their services are called many times. So even a small performance gain can save a lot of money.

Does Rust have many disadvantages? One thing people complain about is that it is hard to learn. The learning curve is steep. AI brings good news, as it helps with learning a lot.

I don't need to know much about Rust. As a software engineer with 10 years of experience, I can use AI to help write many simple Rust applications. I just need to know the basic Rust compilation commands like `cargo` and `cargo build`. I don't even need to know much about Rust syntax itself.

For Rust, the mutability or borrow model doesn't cause trouble for me. For simple applications with fewer than 200 lines of code, I can ask AI to fix errors directly by providing error messages.

But why do people still use Python a lot if Rust is that good? Because Python is good in another aspect. It is very easy to use and learn. It has a large community and many libraries.

Python still has good enough performance and can support products for millions, even tens of millions, of users. Most products don't get that many users. If you do have that many users, you can hire Rust or Java programmers to optimize performance.

Python is good for a lot of development: machine learning, web development, math, teaching, and scripting. While Python is not good at desktop applications, MicroPython is used in Raspberry Pi.

How about Java in the AI era? It will be good too, as it has a large user base and community. AI helps a lot with that. It is used by many big companies. They tend not to change their major programming languages. For some of their large legacy projects, using a new programming language to rewrite a project would take a decade of effort. AI will help with that, but the process will still be slow.

Often, rational people in big companies won't consider changing their main programming language. Their major business is in other sectors. They don't care much about technology. If they did, they would become software or Internet companies and lead in open source communities. However, not many Fortune 500 companies care about that.

There will be a lot of startups due to AI. Startups like to do new things, so they will try new programming languages. In the AI era, agile programming languages will win in small and medium enterprises.

In algorithm competitions, will the favorite programming language change? C++ has dominated this sector for decades. In actual algorithm competitions, you can't use AI. But I think that in the AI era, fewer people will participate.

Since those people are very good at programming, and there are so many opportunities due to AI, why wouldn't more people build actual products for users instead of practicing algorithm problems? Even the GOAT of algorithm competitions, Gennady Korotkevich, chose to join Devin.

But algorithm competitions can be a relaxing or retiring hobby for smart programmers. It is just like chess or basketball. People do it because they like it or need it, not for other reasons. Many people play basketball in their 30s or 40s. They probably do it for health reasons or to make life more fun.

For iOS and Android, it is Java, Kotlin, Swift, and Objective-C. There won't be significant changes due to AI, because there are limited choices. On the end-user side, performance requirements are not so high. Google and Apple have very high control over their platforms. If Google and Apple don't change, programmers won't change.

But for servers, there are many choices. Languages that are more AI-friendly will win.

Procedural programming languages will win more than object-oriented languages. Procedural languages are direct and easy to generate by AI, while OOP languages have many nested levels or design patterns.

Will there be more programming languages because of AI? I think so. Zed and OCaml will have more users. LLMs/AI are very good at learning patterns, so it is easy to rewrite projects in other languages.

Programming languages will face more competition in the future. Those that are good at performance, syntax, and compiler quality will inherently become more popular. The competition is just like with LLMs. Those that are inherently good, like Claude and DeepSeek, become popular.

What if AI becomes so powerful that we don't need to learn programming anymore? That is still a long way off. Suppose we have a very big project with 1,000 Java files. AI would probably need 10 years to perform tasks on that easily.
