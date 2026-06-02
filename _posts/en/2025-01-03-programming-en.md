---
audio: false
generated: false
image: false
lang: en
layout: post
title: Complete Programming Philosophy
translated: false
type: post
---

### Table of Contents

1. [Programming](#programming)
   - Programming as Creative Activity
   - Personal Project Development
   - Technology Trends and Curiosity-Driven Learning
   - Debugging and Problem-Solving Philosophy
   - User-Focused Development
   - Code Quality and Simplicity
   - AI Integration and Automation

2. [Become an Unlimited Engineer](#become-an-unlimited-engineer)
   - Working Within Corporate Constraints
   - Maximizing Internal Resources
   - AI-Era Tool Building
   - Mindset Transformation
   - Breaking Perceived Limitations

3. [Benefits of Accumulating Logs](#benefits-of-accumulating-logs)
   - Log Management in Corporate Environments
   - Historical Context and Problem-Solving
   - Log File Organization Strategies
   - Long-term Project Maintenance
   - Knowledge Preservation and Sharing
   - Automated Log Collection Methods

## Programming

- It is okay to do competitive programming as long as it motivates you.

- Programming is like writing. Programming is a creative activity.

- Do your own project. Write your technical blog. Program for a project that you will maintain for years, just like maintaining a 10-year-long blog.

- Usually, you do not need to pursue what's hot in technology now, as many trends will fade after a few years.

- Pursue your curiosity and program for your own sake.

- Try to create programs for yourself. They are not work assignments.

- If you feel unhappy often when programming, then you are doing it the wrong way.

- iOS, Android, Backend, Frontend, AI are all good. One can at least try to make a small project using them or learn about them for a few months.

- Debugging is about being suspicious. Do not trust every line of your code; you can think of a better way to do it.

- In programming, even a character or a line of log is important. They tell you something.

- Using programming makes products for others to use. It is interesting to have users.

- You do not need to be harsh. A few hundred users really loving your product is better than tens of thousands of users who just kindly like your product.

- Remember why you got into programming and never forget it.

- Apply knowledge in programming to every aspect of life. They are the same. Doing things in batches or one by one. How to separate jobs into units. The underlying tech behind every app. The nuanced details behind network requests.

- The abstraction and logical thinking. The detail-oriented thinking. The thinking out of every solution.

- Truth is truth. Usually, the computer won't be wrong. The electric circuit won't be wrong. The compiler won't be wrong. Don't feel upset when there is a bug.

- Pursue elegant and simple solutions. Simplicity is the ultimate sophistication. You need to think hard to leave what's essential and remove what's extra.

- For programming languages, the languages that get the work done are okay. I personally recommend Java and Python.

- Follow Yin Wang at [https://www.yinwang.org](https://www.yinwang.org). He is one of the few geniuses in programming, though he says geniuses never exist.

- The knowledge and principles of programming can be easily applied to language learning, hardware repairing, life hacking, and scientific researching.

- For most programming tasks, you don't need fancy math besides high school math.

- Reflect on your old code after years or maintain a code project for a long time. It will teach you a lot.

- If you lose your passion for programming, just do other things for some time.

- The timing of testing is important. Just do it naturally. You often don't need to write tests for your project. Try not to write tests, write unit tests, write integration tests, write API tests. Compare them wisely.

- Try AI code editors. Use ChatGPT or other chatbots often. As AI tools are easy to use now, you can focus on more creative or important parts.

- When debugging, check if you're using the latest version of libraries. If a library is unmaintained, look for actively maintained clones or forks.

- When improving something like network speed or program running time, there must be a quantitative metric. Otherwise, you won't know exactly if there was a trivial improvement or degradation.

- For personal projects, it's okay not to write test code, but it's better to do local testing after changing a significant amount of code. Consider the affected code, how long it will run in the cloud pipeline, and how frequently it might lead to errors, and then write test code accordingly. Use methods that allow for easy testing without negatively impacting user experience.

- Write simple and elegant code. Minimize duplication, although sometimes duplication leads to a simpler solution. Minimize special cases. Make it easy to test. Refactor to use common functions or processes, use recursion or loops, and look for patterns.

- Handle errors properly. Think about the root cause, the responsibility, and whether we can change it or if it is an external error. Consider the rescue method, the impact scope, where to handle it, whether we should categorize errors, how likely it is to happen, and the worst-case scenarios.

- The difference between using replace or using startWith followed by slice is that the former disregards the string's position. Apply similar thinking to every detail of programming.

- Minimize the possible values for one item; use just one value for one case. Do not use null if we already have false. If we have a translated true or false flag, we need to ensure that every time we have a translated flag, we do not treat the non-existence of a translated flag as false.

- Use GitHub or Sourcetree to review changed code blocks frequently. They are more convenient for reading code.

- In programming, there are often no trivial things. Every character, the order of list items, every string, every number, and every variable name matter. Every execution order and every log matter.

- Do the things that excite you the most. There's no need to worry about not following the mainstream.

- Use commands frequently, as they can help automate tasks or assist with LLMs. UI interface operations are harder to automate.

- Save the logs of a program, including local, UAT, microservices, and pipeline logs, in a directory. In programming, these logs contain numerous connections. Search through them to identify relationships, collecting relevant data or context.

- With collected logs, when you encounter a problem, it is easier to determine whether you have encountered it before. From previous logs, you might know how to fix it. Logs provide a better understanding of how everything works and how computers execute programs. Unlike code, logs are time-related and offer more information about the running status. They are also more lightweight for debugging.

- Debugging shows a lot of information, including the values of surrounding variables, thread names, and function stacks.

- Automate everything, such as proxy updates and selection of the best proxy server. Use Python to write scripts extensively.

- Keep things simple, make functions small, and keep files small. This makes them easy to test, verify, and check with one sample.

- It is the AI era, so use AI tools to make thorough tests and everything as perfect as possible. Raise exceptions earlier. Add tests for the code and run them in the pipeline every day. Mistakes are okay, but don't make the same mistake twice. Prevent this with code checking.

---

## Become an Unlimited Engineer

- Big companies enforce strict data security policies where employees or contractors receive laptops in the first week and return them upon leaving.

- Projects involve many details, but employees often forget information during their work, especially after leaving for a year or more.

- Memories from the experience include project outlines, team interactions, and LinkedIn connections, but no documented records remain due to strict information controls.

- The first contracting experience in such companies can be upsetting, making software engineering more challenging and significantly impacting work.

- Recently, I figured out how to make the environment feel unlimited by leveraging internal resources, even if it is not truly unrestricted.

- Thousands of software options are available, especially compilers on Windows, enabling the creation of scripts and small tools.

- Learn as many libraries and programming languages as possible; maximize the use of what is given internally.

- Support exists for languages like Go, Rust, C/C++ build tools, JavaScript with npm, and C#, increasing flexibility with more knowledge.

- In the AI era, build custom tools like Postman using Python scripts or write database scripts if tools lack features.

- Use AI to automate tasks, such as Selenium scripts for testing or performance testing scripts.

- Initial feelings of limitation in big companies stemmed from mindset, as policies do not prevent building things or working effectively.

- In life, perceived limitations often arise from not thinking deeply enough; trying more can lead to unique ideas.

- Becoming an unlimited engineer in big companies means becoming an unlimited person overall.

---

## Benefits of Accumulating Logs

When I worked as a contractor for a bank before, we used a multi-cloud application platform to serve the microservices. At that time, I started to accumulate logs when working in the company.

Several years have passed, and I still think it is one of the best ways to help me work or do software engineering. As time goes by, in my logs directory, there are hundreds of log files.

I don't have specific subdirectories or formal log file names for those. Sometimes, I just use that JIRA task name as my log file name prefix or that feature. And then I add a number to the suffix. It is like mutual-fund-1.log, mutual-fund-2.log etc. It means in the mutual fund microservice, I have that log when running that microservice.

Sometimes, when working on projects that serve multiple regions, I will add that country as a suffix, like mutual-fund-cn-1.log, mutual-fund-sg-1.log. The file names of logs are somehow casual. Because at that time, I needed to focus on error stacks or the surrounding function calling.

The logs of the programs matter. Everyone knows. However, I want to overstate the importance of accumulating logs instead of just watching them in the console and letting them go. You will know more convenience when the project is going on. You have more time to find the previous logs. You may need to know whether similar database stored procedure calling happened before. You may need to know whether the same error happened before. You may need to recall how to fix this problem last time.

There are tons of details in a big project or tens of microservices. And the errors, exceptions, or problems are happening again and again. The log is just like the running document of a program. And they are generated by the program automatically without human typing. And for developers, these logs are readable. So when starting a new task or fixing a new bug, you have hundreds of logs in your hand to fix this new bug. You are not alone.

Why do we accumulate them? Because things or knowledge are easily forgotten.

There was human civilization progress when paper was invented. And when computers were invented, there was another level of human civilization. Keeping notes on paper is just like accumulating logs in computers.

Not just for humans, but for AI chatbots, LLM tooling, these logs are becoming more and more important. The GreptimeDB, a database for the unified collection and analysis of observability data (metrics, logs, and traces) established in 2022 is not a coincidence.

Why didn't I do that before? After I worked as a contractor for big banks, I needed to do more collaboration and work on bigger projects. Before that, most of the time in the startup or my startup period, I worked solo. When I worked at LeanCloud before, I worked on the IM app LeanChat for like half of the time.

And when I went into the more formal corporate world, development of the projects was different from my personal project or startup project. They have SIT, UAT testing environments. And the production environment is often just open to certain small team peers. Getting the logs from them and fixing problems becomes long and somewhat tedious. And running a project takes time, and the Jenkins pipeline often needs half an hour to run.

So I can't run or test the program like a fly. I can't do a deployment by simply typing a command on my personal computer and uploading code to the server for running.

So it somehow lets me accumulate logs to have more context to handle tasks. We better fix problems at first shot. We better verify our fix in just a few times. We are not easily able to get logs of the program that is running in a cloud or the server of the company, so we better copy it and save it on the local laptop, to do analysis.

And now, for my personal projects, I will accumulate the logs too. It becomes a habit. After working in big companies for some years, I somehow have more patience or strategy to make my projects bigger and longer. So I know I need these logs as time goes by.

Someone may say that you just need to have elegant code and a working project. You don't need to accumulate the logs or error stack traces. It's okay. When we have a bug or a new feature, we can run the program to get the current logs. We don't need the logs from the development process. They are like the detailed records of scientific experiments. At first sight, it seems okay. But in the long term, if one day you want to work on it again, or you want to share it, or let others take over it, it may not be good.

I think there might be good opportunities here. In companies, why don't we encourage every developer to share their accumulated logs? In open source projects, we should have that too. We don't find others' logs appealing because we don't know them. We lose the context when saving those logs. And inside there, there seem to be tons of unrelated or trivial messages.

But the effort to accumulate logs is just trivial. It is just copy and paste every time we see some logs, especially those error logs. And how about we do it in an automated way? It's a good idea to record the logs in a directory every time we run a project, like those Spring Boot projects.

The world becomes more and more digital, so accumulating logs of digital programs is just like accumulating books in a physical world.
