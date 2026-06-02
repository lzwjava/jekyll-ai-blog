---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: IntelliJ IDEA Criticisms and Unpopular Opinions
translated: false
type: note
---

Question: What are some unpopular opinions about IntelliJ IDEA, the Java IDE?

Answer:

IntelliJ IDEA is widely praised as the gold standard for Java development, but it has its detractors with strong takes. Here are some unpopular opinions drawn from developer discussions, often clashing with the common hype around its productivity features:

- **It's resource-hungry and slow, especially on modest hardware**: Many users complain that IDEA's indexing and re-indexing processes make it unusable for minutes (or hours) after startup or project changes, turning a powerful tool into a sluggish one. One developer called it "slow, slow, and s-l-o-o-w," arguing it's worse than lighter alternatives like NetBeans or even basic text editors for quick tasks.

- **The new UI redesign is a step backward**: The 2023 update to a flatter, more "modern" interface has drawn ire for wasting screen real estate, increasing clicks for common actions, and feeling less intuitive than the classic look. Critics say it prioritizes aesthetics over ergonomics, with one user declaring, "I'm in total love with the old UI—it was more productive."

- **Maven/Gradle integration is unreliable and buggy**: Despite being a JVM powerhouse, IDEA often fails at basic tasks like recognizing dependencies or compiling code, forcing manual refreshes or rebuilds. Users report it "can't even compile a Java class" reliably, making it frustrating for enterprise setups where these tools are essential.

- **It's overkill for small projects and perpetuates JVM bloat**: The default `src/main/java` structure and heavy setup entrench the idea that Java development is heavyweight, raising barriers for prototypes or scripts. One Kotlin lead called this convention "one of the worst things that ever happened to the JVM ecosystem," arguing it scares off newcomers who could otherwise appreciate Java's strengths.

- **Eclipse or VS Code are actually better for most workflows**: Amid the fanboyism, some swear by Eclipse's plugin ecosystem or VS Code's lightweight extensibility, dismissing IDEA as bloated with "leaky abstractions" that get in the way. A long-time user noted, "After 10 years, I switched because the DX [developer experience] in other IDEs is snappier for non-JVM work."

- **The AI features (like Copilot integration) are underwhelming and disruptive**: While hyped, plugins like GitHub Copilot lag behind VS Code's version, generating verbose or error-prone code that requires more fixes than it saves. One engineer said it "confidently breaks the entire codebase" and turns coding into prompt engineering rather than creation.

These views highlight how even top tools have pain points, especially as projects scale or hardware varies. If you're debating a switch, trying the Community Edition for a week often settles it.

References:

- [Why do people hate IntelliJ IDEA?](https://www.quora.com/Why-do-people-hate-IntelliJ-IDEA-What-are-its-disadvantages-compared-to-other-IDEs-like-NetBeans-or-Eclipse)
- [Most unprofessional IDEA review](https://intellij-support.jetbrains.com/hc/en-us/community/posts/206320709-Most-unprofessional-IDEA-review)
- [Am I the only one that doesn't like Intellij?](https://www.reddit.com/r/java/comments/4uburp/am_i_the_only_one_that_doesnt_like_intellij/)
- [I really don't like the new IntelliJ IDEA UI](https://www.reddit.com/r/Jetbrains/comments/17lf1xd/i_really_dont_like_the_new_intellij_idea_ui/)
- [This IDE is sub-par and I hate it](https://intellij-support.jetbrains.com/hc/en-us/community/posts/11365123809298-This-IDE-is-sub-par-and-I-hate-it)
- [Is there ever any reason not to use IntelliJ?](https://www.reddit.com/r/java/comments/1976lzh/is_there_ever_any_reason_not_to_use_intellij/)
- [Unpopular opinion: the defacto standard src/main/java boilerplate directory structure](https://x.com/relizarov/status/1305414701552209921)
- [all JVM languages (Java or Kotlin) are honestly such a pain](https://x.com/mrousavy/status/1993405762303840665)
