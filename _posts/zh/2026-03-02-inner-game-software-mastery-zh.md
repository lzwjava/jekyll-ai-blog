---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 软件精通的内在游戏
translated: true
type: note
---

问题：如何将 **The Inner Game of Tennis** 的理念应用到软件工程工作中？

回答：

**The Inner Game of Tennis**（作者：W. Timothy Gallwey）将表现描述为有两个部分：

- **Outer game** —— 外部障碍、工具、目标（在网球中：opponent、racket、court；在软件中：bugs、deadlines、tech stack、requirements）。
- **Inner game** —— 自己头脑中的内部障碍（self-doubt、overthinking、anxiety、self-criticism、loss of focus）。

核心模型是 **Self 1** 与 **Self 2**：

- **Self 1** —— 批判性的、言语化的、控制性的、以自我为中心的头脑，它给出指令、评判、担心显得愚蠢、害怕失败。
- **Self 2** —— 自然的、直觉的、有能力的、潜意识的头脑，它实际执行复杂动作（在网球中：协调时机、平衡、muscle memory；在编码中：pattern recognition、architectural intuition、debugging insight）。

核心论点：**Self 1 通过过度指令和评判干扰 Self 2** → 表现下降。减少干扰 → flow、creativity 和更高表现自然浮现。

以下是将主要 Inner Game 原则直接翻译到日常软件工程工作中的内容：

1. **让 Self 1 的持续言语指令安静下来**  
   不要想“我必须写更干净的代码，我总是写糟糕的变量名，这次用更好的名字，别忘了 SOLID，资深工程师会怎么想？”→ 信任当专注于问题时 Self 2 会产生合理的代码。  
   过度指令通常会产生紧张、笨拙、更慢的编码。

2. **用非评判性的觉察取代评判**  
   写完代码后的经典 Self 1 模式：“这是垃圾/丑陋/慢/初级水平/尴尬。”  
   Inner Game 替代方案：中性观察 → “这个循环运行的迭代次数比预期多 3 倍……有趣。”  
   非评判性觉察减少情绪干扰，让 Self 2 从反馈中更快学习。

3. **用图像/可视化取代言语规则**  
   不要背诵规则列表（“如果 >10 行就 extract method、single responsibility 等”），而是想象期望的最终状态：  
   - “这个 business rule 的优雅、可读代码会是什么样子？”  
   - 可视化数据通过小型、专注的函数干净流动。  
   Self 2 对生动的心理图像的反应远好于言语命令。

4. **将注意力集中在当下发生的事情上（放松的集中）**  
   Gallwey 的著名技巧：观察球的接缝。  
   软件等价物：  
   - 观察通过 debugger 逐步执行的确切值。  
   - 在脑海中强烈关注 call stack / data structure 的形状。  
   - 注意当你“in the zone”时与强迫时手指在键盘上的感觉差异。  
   这将注意力锚定在当下 → 安静 Self 1 的喋喋不休 → 深度 flow 状态出现。

5. **信任 Self 2 —— 让它发生**  
   许多最佳 architectural insights、优雅 refactors 和棘手 bug 发现发生在你停止强迫、散步、盯着窗外或只是实验性输入而不评判时。  
   当你想“我现在必须解决这个”时 → Self 1 收紧控制 → creativity 下降。

6. **不通过强迫来改变习惯**  
   不要“更努力地先写测试”→  
   - 中性观察当前行为（“我又先写了逻辑”）。  
   - 要求一个小转变（“如果我在实现前写一个微小的测试呢？”）。  
   - 让 Self 2 实验并感受结果。  
   - 重复而不自责。

7. **更频繁达到 flow**  
   编程是最类似于体育的活动之一，它能产生深度 flow 状态（时间消失，200 次错误尝试感觉充满活力）。  
   Inner Game 实践使 flow 更频繁且可持续——特别是在长时间 debugging 会话、on-call incidents 或复杂 refactors 中尤为重要。

软件工程师成功使用的日常实践实验：

- 开始任务前，花 30 秒可视化干净、简单的代码解决问题（图像，不是文字）。  
- 卡住时，大声说（或写）：“我注意到我的头脑在说这是不可能的……” → 标记 Self 1 故事 → 返回观察代码。  
- 在 code review 评论中：将反馈视为中性信息，而不是对你价值的判决。  
- Pair-programming：专注于对伙伴思维的好奇，而不是证明你聪明。

最终目标不是第一次就完美代码——而是**减少自我干扰**，从而加速学习、增加享受，并让高质量工作随着时间变得更自然。

参考文献：

- [The Inner Game and software development](https://aaronsumner.com/posts/2010/09/inner-game-software-development)
- [Inner Game of Software Engineering](https://www.linkedin.com/pulse/inner-game-software-engineering-prathik-rajendran-m-llapc)
- [The Inner game, applied to code](https://medium.com/@nicholasmonroeeubanks/the-inner-game-applied-to-code-b4279d50fbb1)
- [The Inner Game of Software Development](https://dev.to/codingmindfully/the-inner-game-of-software-development-323n)
- [Code Watch: The inner game of programming](https://sdtimes.com/flow/code-watch-the-inner-game-of-programming)