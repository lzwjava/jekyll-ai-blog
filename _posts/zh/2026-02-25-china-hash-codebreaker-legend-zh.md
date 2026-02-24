---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 中国哈希破解传奇
translated: true
type: note
---

Question: 王小云是谁，这位传奇的中国网络安全专家、山东大学教授？

Answer:

## 王小云 (Wang Xiaoyun) — 中国密码学传奇

### 背景与早年生活

王小云（1966 年生于山东省诸城）是世界上最著名的密码学家和数学家之一。她在山东大学完成了她的整个早期学术历程，1987 年获得学士学位，1990 年获得硕士学位，1993 年获得数学博士学位，导师是著名数学家潘承洞。然后她加入教职团队，1995 年成为助理教授，2001 年成为正教授。

### 学术职位

王小云在其职业生涯中一直拥有享有盛誉的双重任职：

- **Shandong University** — 数学与系统科学系教授，以及 Cryptographic Technology and Information Security Laboratory 负责人。
- **Tsinghua University** — 2005 年，被任命为高级研究中心 **Chen Ning Yang (C.N. Yang) Professor**，这是中国最负盛名的学术荣誉之一，以诺贝尔奖得主物理学家命名。
- **Chinese Academy of Sciences** — 2017 年当选院士，中国科学界的最高荣誉。

### 震惊世界的突破：MD5 和 SHA-1

王小云最传奇的成就出现在 **CRYPTO 2004**，这是世界上顶级密码学会议之一，她和她的合著者们在“rump session”（非正式快速演示环节）站起来，展示了针对 **MD5、SHA-0 和其他 hash function** 的 **collision attacks**。观众给予他们 **standing ovation**——在密码学会议上几乎闻所未闻的反应。

**hash collision** 发生在两个不同的数据块产生相同的 hash 输出时。这对安全来说是灾难性的，因为 digital signatures、password verification、SSL certificates 和 data integrity checks 都依赖于碰撞在计算上不可能找到的假设。

她们的攻击打破了针对 MD5 的这一假设，MD5 被认为安全超过十年，并在全球数亿系统中部署。

随后在 **2005 年 2 月**，王小云和合著者 Yiqun Lisa Yin 以及 Hongbo Yu 宣布她们攻破了 **SHA-1**——由 NSA 设计的美国政府标准，并在全球最关键的安全基础设施中使用。她们的攻击需要不到 2⁶⁹ 次操作，而此前认为需要 2⁸⁰ 次操作——减少了超过 2000 倍。在 **CRYPTO 2005** 上，与 Andrew Yao 和 Frances Yao 一起宣布了复杂度为 2⁶³ 的改进版本。

后果巨大：**MD5 和 SHA-1 最终从几乎所有主要软件系统中淘汰**，包括 Windows 和 Linux。她们的退役直接促使了下一代 hash 标准如 SHA-3 和 BLAKE2 的开发。

### 关键技术贡献：基于位的模块差分密码分析

王小云的方法论创新是开发了 **bit-based modular differential cryptanalysis**——一种系统分析输入中微小差异如何通过 hash function 内部结构传播的技术。这种方法是革命性的，因为它将 hash function 分析从一门艺术转变为更系统的科学，使她能够发现其他人多年来错过的弱点。

### 设计中国的国家 hash 标准：SM3

除了攻破现有标准，王小云还 **设计** 了一个。她领导了 **SM3** 的开发，这是中国的国家密码 hash function 标准。SM3 已广泛部署在中国金融系统、交通基础设施、国家电网和其他关键部门。**2018 年 10 月**，SM3 被正式采纳为 **ISO/IEC** 国际标准，使其在全球舞台上获得认可，并成为全球区块链和 digital signature 应用的 viable 标准。

### 奖项与荣誉

王小云的工作为她赢得了非凡的荣誉列表：

- **IACR Fellow** (2019) — 国际密码学研究协会会士，“表彰对 hash function 的密码分析和设计的本质贡献”。
- **Future Science Prize — Mathematics and Computer Science** (2019) — 她成为 **首位赢得** 这一享有盛誉的中国奖项的女性，常被比作中国的诺贝尔奖。
- **Levchin Prize for Real-World Cryptography** (2020) — 表彰密码安全实际影响的领先行业奖项。
- **CRYPTO 2005 Test-of-Time Award** (2020) — 表彰她的 SHA-1 论文 15 年后的持久影响。
- **Tan Kah Kee Science Award** (2006)
- **Qiushi Outstanding Scientist Award** (2006)
- **Thomson Reuters Research Fronts Award** (2007)
- **2nd Class Prize, Chinese National Natural Science Award** (2008)
- **CSIAM Su Buchin Prize** (2010)
- **Special Prize for Cryptographic Innovation**, Chinese Association for Cryptologic Research (2014)

她的 CRYPTO 2005 关于 SHA-1 和 MD5 的论文都获得了 **Best Paper Awards**——在任何研究社区中都是罕见的壮举，更不用说在世界顶级密码学场所了。

### 遗产与影响

王小云的工作从根本上改变了密码学家对 hash function 安全的思考方式。在她之前，MD5 和 SHA-1 被视为互联网安全架构的可靠基石。在她之后，整个领域不得不重新审视其假设。她证明了来自中国大学的科研人员——而非西方情报机构或硅谷实验室——能够为全球密码安全做出地震般的贡献。

她仍是活跃的研究者，贡献于包括对 MAC (Message Authentication Code) 方案的攻击、quantum cryptanalysis 和 cipher design 等领域。她的工作继续影响着全球现代密码标准的开发和评估方式。

References:

- [Wang Xiaoyun — Wikipedia](https://en.wikipedia.org/wiki/Wang_Xiaoyun)
- [Future Science Prize — Wang Xiaoyun Laureate Profile](http://www.futureprize.org/en/laureates/detail/37.html)
- [Tsinghua ICAS Profile](http://www.castu.tsinghua.edu.cn/publish/casen/1695/2010/20101224093253705266640/20101224093253705266640_.html)
- [Shandong University Cryptography Lab](https://infosec.sdu.edu.cn/info/1043/1121.htm)