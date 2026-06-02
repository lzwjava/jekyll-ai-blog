---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 互联网骨干网之母
translated: true
type: note
---

以下是关于 Radia Perlman 的全面介绍，她是一位计算机科学家和网络工程师，她的发明构成了现代计算机网络的基础。

Radia Perlman 是一位美国计算机程序员和网络工程师，经常被称为“Internet 之母”。这个绰号源于她发明了 Spanning Tree Protocol (STP)，这是一种基本技术，解决了网络设计中的一个关键问题，并使大型、可靠且可扩展的局域网 (LANs) 的创建成为可能。她的工作深刻塑造了数据在世界范围内传输的方式，使她成为计算机科学历史上最具影响力的人物之一。

### 🧬 早年生活与教育：从小神童到 MIT 先驱

- **在新泽西的早年生活**：Radia Perlman 于 1951 年 12 月 18 日出生于弗吉尼亚州朴茨茅斯，在新泽西州 Asbury Park 附近长大。她的父母均为美国政府工程师——父亲从事雷达工作，母亲是数学家兼计算机程序员。
- **早期兴趣**：从很小的时候起，Perlman 就觉得数学和科学“毫不费力且引人入胜”，尽管她也喜欢音乐，会弹钢琴和法国号。
- **发现编程**：她在高中编程课上对计算机产生了兴趣，当时她是班上唯一的女生。
- **MIT 之旅**：20 世纪 60 年代末，她进入 Massachusetts Institute of Technology (MIT) 学习，当时女生仅占学生总数的不到 5%。在那里，她于 1971 年在 MIT Artificial Intelligence Laboratory 获得了第一份带薪编程工作。
- **与儿童的开创性工作**：在传奇计算机科学家 **Seymour Papert** 的指导下，她开发了教育机器人语言 LOGO 的儿童友好版本，名为 **TORTIS ("Toddler's Own Recursive Turtle Interpreter System")**。1974 年至 1976 年间，年仅三岁半的孩子就能使用她的系统来编程机器人乌龟。这项工作使她被描述为**儿童计算机编程教学的先驱**。
- **博士论文**：Perlman 获得了数学专业的 B.S. 和 M.S. 学位，后来返回 MIT 攻读计算机科学博士学位，并于 1988 年完成。她的博士论文《Network layer protocols with Byzantine robustness》探讨了即使网络部分组件恶意行为时网络路由的复杂问题。这项工作仍是网络安全领域的基础。

### 💡 里程碑发明：Spanning Tree Protocol (STP)

- **循环问题**：20 世纪 80 年代初，Perlman 在 **Digital Equipment Corporation (DEC)** 担任咨询工程师。当时的挑战是构建具有冗余的可靠网络。如果一条路径失败，另一条路径可以接管。然而，当时的 Ethernet 技术中，这些冗余路径会产生“循环”。数据包会被无休止地转发，导致网络因广播风暴而崩溃。
- **优雅解决方案**：1984 年，Perlman 发明了 **Spanning Tree Protocol (STP)** 来解决这个问题。她的算法巧妙地将具有潜在循环的物理网络转变为逻辑树状结构，在任意两点之间仅有一条活跃路径。它通过网络桥的通信来实现：
    1. 选举一个单一的“root bridge”作为参考点。
    2. 计算每个其他桥到该根的最短路径。
    3. 自动**禁用不属于此最短路径树的任何冗余路径**，从而消除循环，同时保留它们作为备份。
- **标准的诞生**：该协议允许网络具有用于可靠性的冗余，而不会面临灾难性故障的风险。后来，它被 **Institute of Electrical and Electronics Engineers (IEEE)** 标准化为 802.1D，成为 Ethernet 网络的基石。
- **诗意触碰**：Perlman 一贯如此，她在技术论文旁发布了一首诗来解释 STP，她称之为“Algorhyme”：

> I think that I shall never see
> A graph more lovely than a tree.
> A tree whose crucial property
> Is loop-free connectivity.
> ...
> A mesh is made by folks like me
> Then bridges find a spanning tree.

### 🔬 持续创新的职业生涯

Perlman 的天才并非昙花一现。她在网络领域的众多其他方面做出了基础性贡献。

- **路由协议**：她是 **DECnet IV 和 V 协议** 的**主要设计师**，并在 **IS-IS routing protocol** 的开发中发挥了重要作用。IS-IS 是一种链路状态路由协议，对大型网络（包括互联网服务提供商的网络）至关重要。她在容错路由信息广播方面的工作也影响了 **Open Shortest Path First (OSPF)** 协议的开发，这是互联网路由的另一个基石。
- **超越 STP：TRILL**：几十年后，Perlman 承认 STP 虽然革命性，但存在局限性。它会通过禁用冗余链路浪费网络带宽。为克服这一点，她发明了一种新协议，名为 **TRILL (TRansparent Interconnection of Lots of Links)**。TRILL 允许网络高效利用所有可用路径，将 Ethernet 的简单性与路由的灵活性相结合。秉承传统，她还为这个新协议写了一个第二版诗“Algorhyme V2”。
- **职业历程**：在漫长的职业生涯中，Perlman 在主要科技公司担任过重要职位，包括 **DEC、Novell、Sun Microsystems 和 Intel**。截至 2022 年，她是 **Dell Technologies** 的 Fellow。
- **作者与教育者**：她是备受推崇的网络教材 **"Interconnections: Bridges, Routers, Switches, and Internetworking Protocols"** 的作者，以及热门安全教材 **"Network Security: Private Communication in a Public World"** 的合著者。她还在 Harvard、MIT 和 University of Washington 等顶尖大学教授课程。
- **专利与荣誉**：Perlman 拥有**超过 100 项美国专利**。她的开创性工作获得了众多 prestigious 奖项，包括：
  - 当选 **National Academy of Engineering** (2019)。
  - 入选 **Internet Hall of Fame** (2014)。
  - 入选 **National Inventors Hall of Fame** (2016)。
  - 来自 **USENIX** (2006) 和 **ACM SIGCOMM** (2010) 的终身成就奖。

### 🤔 谦逊的遗产

尽管贡献卓著，Radia Perlman 以谦逊闻名，她不愿被称为“Internet 之母”。她认为互联网是许多人的共同努力，这样的头衔会削弱他们的集体贡献。她也是一个注重隐私的人，避免使用社交媒体和智能手机，更喜欢专注于计算机科学的复杂智力挑战，以及她的音乐和喜剧兴趣。

Radia Perlman 的遗产不仅仅是她发明的协议，而是她解决问题的方式——优雅、鲁棒，甚至带有一丝诗意。她构建了使我们互联世界运转的无形结构，使她成为数字时代真正的巨人。

希望这份全面介绍能让您对她的生平和工作有很好的概述。您是否想进一步探讨她职业生涯的某个特定方面，例如她的安全研究或路由协议工作？
