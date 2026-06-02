---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: AI编程工具的非主流观点
translated: true
type: note
---

问题：关于Claude Code和OpenAI Codex的冷门观点有哪些？

回答：

关于Anthropic的Claude Code和OpenAI的Codex等AI编码工具的冷门观点，通常会强调炒作与实际应用之间的差距，尤其是在复杂项目上。这些观点来自广泛测试过它们的开发者和用户，揭示了对可靠性、可用性和过度承诺的不满。下面我根据社区讨论，总结了按工具分类的关键冷门观点。这些观点挑战了AI完全取代人类编码员的说法。

### 关于Claude Code的冷门观点

- **它被过度炒作，只对那些不懂真正工程的“随性编码者”有用**：许多人认为Claude Code擅长快速原型开发，但在可维护的大规模代码库上表现不佳，会生成难以阅读或重复的代码。那些“随性编码”（没有结构地模糊提示）的用户喜欢它，但经验丰富的开发人员认为它只是一个初级工具，忽略了TDD或整洁架构等最佳实践。
- **终端用户体验笨拙，不如IDE集成工具如Cursor或Copilot**：尽管Claude的模型强大，其代码工具却显得过时——文件处理有bug、计划模式不佳、无法无缝进行内联编辑，这些都让日常工作变得令人沮丧。开发人员更喜欢将Claude的“大脑”嵌入到更好的用户界面中，而不是使用原始工具。
- **它经常出现幻觉，需要持续的人工干预，使得它比手动编码更慢**：Claude经常会凭空捏造不存在的方法、忽略规范，或过度关注语法而非逻辑，导致没完没了的调试循环。它对于简单任务表现出色，但会暴露出那些在没有监督的情况下构建不安全或有缺陷应用程序的“随性编码者”的问题。
- **对Claude的抵触来源于上下文过载，而非工具本身**：新用户一次性输入过多信息，导致工具“变笨”，但剥离上下文会使其在最初感觉更智能——直到提示再次膨胀。这种循环令人沮丧，但这更多是用户问题，而非模型缺陷。
- **它是一个尊重隐私的本地工具，但这只是其唯一的优势——对非开发人员来说并不具革命性**：虽然它可以在不上传文件的情况下处理本地文件（例如批量重命名或合同分析），但终端界面吓退了商业用户。大多数分享的示例过于技术性，限制了其广泛采用。

### 关于OpenAI Codex的冷门观点

- **尽管被大肆宣传，但它无法用于真实代码库——感觉像是匆忙推出的Claude竞争对手**：延迟、上下文限制和糟糕的错误处理使其在非简单工作上几乎无效。开发人员尝试一次后便转回Claude，称其封闭性质和半生不熟的CLI为“反开源”。
- **隐私噩梦：你的代码在没有明确保障的情况下被用于训练他们的模型**：企业用户因担心专有代码泄露到训练数据中而却步。没有本地部署选项或审计跟踪破坏了信任，尤其是每月200美元的价格——对于保护知识产权的专业人士来说，这是个致命的缺点。
- **异步功能对于单人开发者来说是超凡脱俗的，但受限于用量且感觉处于早期阶段**：类似蜂群的并行任务可以快速处理积压工作，但没有网络访问会导致依赖更新或构建受阻，而且用户体验缺乏GitHub同步。它功能强大但又有限，更适合炒作而非生产。
- **在负载下性能下降并卡在错误中——对代理“大吼大叫”成了新常态**：随着流量增加，性能急剧下降（例如，从“神级”降到“垃圾”），并且它会在故障中循环而无法自我修正。OpenAI内部使用（92%采用率）的版本可能更优越，这使得公共访问感觉像是一场测试骗局。
- **它更擅长规划而非执行——单一提示的表现优于其代理模式**：为了速度，具有完整上下文的原始GPT-5.1可以比Codex的工具调用循环更快地完成任务。它在理论上是代理式的，但在实践中不可靠，尤其对于分布式或GPU代码。

总的来说，这些观点强调了AI编码工具放大了熟练用户的优势，但也暴露了在提示、上下文管理和集成方面的弱点。它们是加速器而非自动化器——成功更多地取决于人工监督，而非工具本身。

参考资料：

- [r/ClaudeAI: Are people actually getting bad code from claude?](https://www.reddit.com/r/ClaudeAI/comments/1m6ienr/are_people_actually_getting_bad_code_from_claude/)
- [r/ClaudeAI: Most of the people complaining about Claude likely are no code programmers](https://www.reddit.com/r/ClaudeAI/comments/1fqs6py/most_of_the_people_complaining_about_claude/)
- [r/ClaudeAI: My hot take: the code produced by Claude Code isn't good enough](https://www.reddit.com/r/ClaudeAI/comments/1m4t7qk/my_hot_take_the_code_produced_by_claude_code_isnt/)
- [r/ClaudeAI: What am I missing here? Claude Code seems a joke when I use it](https://www.reddit.com/r/ClaudeAI/comments/1l4omv6/what_am_i_missing_here_claude_code_seems_a_joke/)
- [r/ChatGPTCoding: CLAUDE IS SO GOOD AT CODING ITS CRAZY!](https://www.reddit.com/r/ChatGPTCoding/comments/1l3bkwx/claude_is_so_good_at_coding_its_crazy/)
- [r/ClaudeAI: Do any programmers feel like they're living in a different reality when talking to people that say AI coding sucks?](https://www.reddit.com/r/ClaudeAI/comments/1ji1nsz/do_any_programmers_feel_like_theyre_living_in_a/)
- [OpenAI Codex: Future of Coding or Current Frustration?](https://latenode.com/blog/codex-future-coding-frustration)
- [r/OpenAI: Blown away by how useless codex is with o4-mini](https://www.reddit.com/r/OpenAI/comments/1k16lp8/blown_away_by_how_useless_codex_is_with_o4mini/)
- [r/ChatGPTCoding: I wonder if they use the same Codex we have? - 92% of OpenAI engineers are using Codex](https://www.reddit.com/r/ChatGPTCoding/comments/1o0g266/i_wonder_if_they_use_the_same_codex_we_have_92_of/)
- [r/singularity: OpenAI Codex is anti open-source](https://www.reddit.com/r/singularity/comments/1ko3rv9/openai_codex_is_anti_opensource/)
- [OpenAI Codex hands-on review | Hacker News](https://news.ycombinator.com/item?id=44042070)
- [r/OpenAI: Is Codex Enough to Justify Pro?](https://www.reddit.com/r/OpenAI/comments/1ko3f3e/is_codex_enough_to_justify_pro/)
- [r/LocalLLaMA: Tried OpenAI Codex and it sucked 👎](https://www.reddit.com/r/LocalLLaMA/comments/1k10rtg/tried_openai_codex_and_it_sucked/)
- [r/singularity: Apparently at OpenAI, insiders have graduated from coding: "we don’t program anymore we just yell at codex agents"](https://www.reddit.com/r/singularity/comments/1nidcr3/apparently_at_openai_insiders_have_graduated_from/)
- [r/OpenAI: Codex NEW mega update!!!](https://www.reddit.com/r/OpenAI/comments/1n1ua3n/codex_new_mega_update/)
- [r/OpenAI: What in the world is OpenAI Codex doing here?](https://www.reddit.com/r/OpenAI/comments/1k3ejji/what_in_the_world_is_openai_codex_doing_here/)
- [Jonathan Grahl on Claude Code maintainability](https://x.com/jonathangrahl/status/1945582527877374129) [post:1]
- [Ian Nuttall on anti-Claude sentiment](https://x.com/iannuttall/status/1970099519166746653) [post:3]
- [MK on Claude Code UX](https://x.com/maxbooooooiiiii/status/1996918155957223779) [post:6]
- [the Rich on Claude bug fixing](https://x.com/Duderichy/status/1857462027691733400) [post:7]
- [Allie K. Miller on non-engineer access](https://x.com/alliekmiller/status/1980627154304971049) [post:9]
- [Steve Yegge on Claude Code legacy bugs](https://x.com/Steve_Yegge/status/1898674257808515242) [post:17]
- [Shreya Shankar on terminal vs Cursor](https://x.com/sh_reya/status/1956830797543166121) [post:5]
- [Tenobrus on Codex usability](https://x.com/tenobrus/status/1912603821236449750) [post:30]
- [Taelin on Codex persistence](https://x.com/VictorTaelin/status/1980369947026158072) [post:32]
- [Max Kruger on Codex vs Claude](https://x.com/maxkruger/status/1995951063791202568) [post:33]
- [Riley Coyote on Codex async power](https://x.com/RileyRalmuto/status/1924611206901281154) [post:34]
- [Lee Robinson on Codex limitations](https://x.com/leerob/status/1925228406654050642) [post:40]
