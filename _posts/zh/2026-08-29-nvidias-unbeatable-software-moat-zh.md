---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 英伟达无与伦比的软件护城河
translated: true
type: note
---

**问题：** 为什么像微星或英特尔这样的公司无法制造出与英伟达相抗衡的GPU，尽管主板和GPU在表面上看起来非常相似？

**答案：**

这是个很好的直觉性问题——它们外观确实相似，但内部差距巨大。原因有多个层面：

**1. 微星并非GPU设计公司，而是组装商**

实际上，只有两家公司设计GPU：英伟达和AMD。微星、华硕、技嘉等厂商是AIB（附加板卡）合作伙伴——它们从英伟达或AMD那里获得基础GPU芯片，然后自行添加散热器、RGB灯效和适度超频。核心的PCB和硅片设计完全来自英伟达。因此，问“为什么微星无法与英伟达竞争”属于范畴错误——微星*销售*的是英伟达的GPU。

**2. 英特尔尝试过——但举步维艰**

英特尔的GPU项目（Arc系列）几乎在每个环节都遭遇困境：新冠疫情导致的延误、全球芯片短缺，以及严重的驱动/软件质量问题。至少有一家AIB合作伙伴因质量问题完全退出了Arc项目。英特尔拥有资金和制造能力，但这仍然不够。

**3. 真正的护城河是软件，而非硬件**

这是核心答案。英伟达的优势根植于其并行计算平台CUDA。即便竞争对手能提供相媲美的峰值硬件性能，经过优化的CUDA内核也能使英伟达GPU实现远胜于对手的实际利用率——竞争对手不仅需要制造出更优秀的硬件，还必须匹配一个根深蒂固、全方位覆盖的软件生态系统。

在21世纪初，黄仁勋下了一个重大的战略赌注：大力投资CUDA，使GPU可编程用于通用计算。CUDA提供了库、调试器和API——而且关键的是，它向后兼容数亿块英伟达GPU，经过多年持续投入实现了广泛采用。

**4. 二十年累积的生态系统效应**

英伟达的主导地位并非源自单一突破，而是一场精心策划、跨越二十年的战略胜利。核心武器并非GPU芯片本身，而是那个看似“免费”的软件平台——CUDA。如今，CUDA在AI开发框架中占据约92%的市场份额。这不是硬件锁定——而是开发者锁定：每位AI研究者都在学习CUDA、基于CUDA开发、并为CUDA进行优化。

**5. 其他公司难以匹敌的研发投入规模**

英伟达的研发支出高达129.1亿美元，反映出其在硬件和软件上持续领先的驱动力。AMD在硬件规格上展开竞争，但即便拥有纸面参数上的竞争力（如MI300X），AMD仍未能撼动英伟达的市场地位，因为软件生态系统的差距实在过大。

**类比：** 击败英伟达好比试图打造一个YouTube的竞争对手——你不仅需要一个更好的平台，还需要一个积累了数十年的相当规模的视频内容库。

因此，简而言之：微星不是GPU设计公司；英特尔尝试过，却发现门槛比看起来高得多；而英伟达真正的统治力在于20多年来积累的软件基础设施，这是单纯硬件无法在一夜之间复制的。

---

**参考资料：**

- [英伟达的护城河不是硅，而是CUDA（Rayhan Press）](https://rayhanpress.com/nvidias-moat-isnt-silicon-its-cuda/)
- [CUDA优势：英伟达如何主导AI（Medium）](https://medium.com/@aidanpak/the-cuda-advantage-how-nvidia-came-to-dominate-ai-and-the-role-of-gpu-memory-in-large-scale-model-e0cdb98a14a0)
- [英伟达第三部分：软件护城河与竞争（Punch Card Investor）](https://punchcardinvestor.substack.com/p/nvidia-part-3-beyond-gpus-software)
- [英特尔Arc从一开始就注定失败（TechRadar）](https://www.techradar.com/news/intel-arc-was-doomed-from-the-start-and-msis-new-gpu-wont-change-that)
