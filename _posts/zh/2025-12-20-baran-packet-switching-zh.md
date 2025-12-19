---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 保罗·巴兰发明了分组交换
translated: true
type: note
---

问题：Paul Baran 的生平是怎样的，他是如何发明数据包交换的？

回答：

Paul Baran 是一位杰出的美国工程师，于1926年4月29日出生在波兰格罗德诺（当时属于波兰，现在在白俄罗斯），他的意第绪语名字是 Pesach Baran。他的家人于 1928 年移民到美国，最初定居在波士顿，后来搬到费城，他的父亲在那里开了一家杂货店。Baran 在成长过程中一直帮助家里的生意。

1949 年，他获得了德雷塞尔大学的电气工程学士学位。在他的职业生涯早期，他在 Eckert-Mauchly Computer Corporation 担任技术员，参与了 UNIVAC I（首批商用计算机之一）的工作。他后来加入了 Hughes Aircraft，从事雷达系统的工作，同时利用业余时间在加州大学洛杉矶分校攻读工程学硕士学位，并于 1959 年完成学业。

1959 年，Baran 加入了 RAND Corporation，这是一个非营利智库，在冷战期间专注于国家安全和政策问题。在那里，他解决了一个关键问题：设计一个能够经受住核攻击的通信系统。传统的集中式电话网络很容易受到攻击，因为摧毁关键的交换中心可能会使整个系统瘫痪。

Baran 的创新解决方案是一个具有高冗余度的**分布式网络**——没有单一的故障点。他建议将数字消息分成小块（他称之为“消息块”），通过互连节点的网状结构独立发送它们，并在目的地重新组装它们。每个节点将存储和转发这些块，并自适应地绕过损坏的部分进行路由（他称之为“热土豆路由”技术）。这个概念，现在被称为**数据包交换**，使得即使许多节点或链路被摧毁，网络也能保持运行。

他在名为《论分布式通信》（On Distributed Communications，1960-1964 年出版）的 11 份 RAND 报告中详细阐述了这一点。Baran 最初称之为“分布式自适应消息块交换”。独立地，英国科学家 Donald Davies 在 1965-1966 年左右提出了一个类似的想法，并创造了“数据包交换”（packet switching）这个术语（使用“packets”而不是“message blocks”）。Baran 和 Davies 承认了彼此的并行发明，Baran 指出他们是独立得出相同概念的。

虽然 Leonard Kleinrock 在 20 世纪 60 年代早期为消息交换贡献了排队论分析，但历史学家和消息来源主要将 Baran 和 Davies 视为构成现代网络基础的数字数据包交换的独立发明者。

Baran 的思想影响了 20 世纪 60 年代后期 ARPANET（互联网的前身）的发展，尽管最初被像 AT&T 这样的实体不屑一顾。他于 1968 年离开 RAND，共同创立了未来研究所（Institute for the Future），一个专注于长期预测的非营利组织。后来，他成为了一名成功的企业家，创立了多家科技公司（其中五家上市），其中包括推动有线调制解调器、DSL 和无线网络的公司。他还发明了第一台机场安全金属探测器，并拥有多项专利。

Baran 获得了许多荣誉，包括被收录到国家发明家名人堂、获得国家技术与创新奖章，并被公认为互联网先驱。他始终保持谦虚，将互联网视为一项集体成就。他于 2011 年 3 月 26 日在加利福尼亚州帕洛阿尔托去世，享年 84 岁，死于肺癌并发症。

参考文献：

- [Paul Baran - Wikipedia](https://en.wikipedia.org/wiki/Paul_Baran)
- [Paul Baran | Biography, Packet Switching, Distributed Networks, & Facts | Britannica](https://www.britannica.com/biography/Paul-Baran)
- [Paul Baran and the Origins of the Internet | RAND](https://www.rand.org/pubs/articles/2018/paul-baran-and-the-origins-of-the-internet.html)
- [NIHF Inductee Paul Baran, Who Invented Packet Switching](https://www.invent.org/inductees/paul-baran)
- [Packet switching - Wikipedia](https://en.wikipedia.org/wiki/Packet_switching)
- [Obituary: Paul Baran, RAND Researcher and Pioneer of the Internet | RAND](https://www.rand.org/news/press/2011/03/28/index1.html)