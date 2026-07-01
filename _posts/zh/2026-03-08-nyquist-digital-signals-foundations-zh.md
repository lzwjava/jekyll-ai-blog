---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 奈奎斯特数字信号基础
translated: true
type: note
---

**问题：** Harry Nyquist是谁，他对工程和通信理论的主要贡献是什么？

**答案：**

---

## Harry Nyquist — 全面介绍

### 1. Harry Nyquist是谁？

Harry Theodor Nyquist（1889年2月7日 – 1976年4月4日）是一位瑞典裔美国物理学家和电子工程师，他对通信理论做出了重要贡献。他是一位多产的发明家，在电信领域做出了基础性的理论和实践贡献。

---

### 2. 早年生活和教育

Nyquist 出生于瑞典Värmland省Stora Kil教区Nilsby村。1907年，他移民到美国。他的家族原姓为Jonsson。他的父母在瑞典收邮件时遇到问题，因为该地区还有其他名叫Lars Jonsson的男子——于是家族将姓氏改为Nyquist。

他于1912年进入University of North Dakota，并分别于1914年和1915年获得电气工程专业的B.S.和M.S.学位。1917年，他在Yale University获得物理学Ph.D.学位。

---

### 3. 在AT&T和Bell Laboratories的职业生涯

1917年至1934年，Nyquist受雇于American Telephone and Telegraph Company的开发与研究部门，在那里他从事电报、图片和语音传输的研究。从1934年至1954年，他在Bell Telephone Laboratories工作，继续从事通信工程，特别是传输工程和系统工程。1954年退休时，Nyquist是系统研究助理主任。

他在Bell Laboratories的37年职业生涯包括对长途电话技术的贡献，以及开发传输图片的通信系统。他的成就从理论到实践均有涉及。

---

### 4. 主要贡献和理论

#### A. Nyquist采样定理（1924 & 1928）

1924年，他发表了论文*"Certain Factors Affecting Telegraph Speed"*，分析了电报系统的速度与所用信号值数量之间的关系。他的1928年论文*"Certain Topics in Telegraph Transmission Theory"*完善了早期的结果，并确立了将连续信号采样转换为数字信号的原则。Nyquist采样定理表明，采样率必须至少是样本中最高频率的两倍，才能重建原始信号。

这引出了两个密切相关的概念：

- **Nyquist Rate** — 忠实重建信号所需的最小采样率（最高信号频率的两倍）。
- **Nyquist Frequency** — 采样率的一半；低于此值的信号频率可以无歧义地表示。

采样定理的实际意义巨大。这就是为什么音频CD的采样率为44.1 kHz。人耳通常能听到高达约20 kHz的频率，因此略高于两倍的采样率确保所有可听频率被准确捕获。这也是数字图像具有特定分辨率（以像素计）和数字视频具有特定帧率的原因。

#### B. 热噪声（Johnson–Nyquist Noise，1927）

1927年，Nyquist为J.B. Johnson研究的不预期强烈的热噪声提供了数学解释。对噪声的理解对通信系统至关重要。热噪声有时被称为Johnson noise或Nyquist noise，因为他们在该领域开创性的工作。

#### C. Nyquist稳定性准则（1932）

1932年，Nyquist发现了如何判断负反馈放大器是否稳定。他的准则，通常称为Nyquist稳定性定理，具有极大的实际重要性。二战期间，它帮助控制使用机电反馈系统的火炮。

Nyquist稳定性准则提供了一种图形方法，用于判断系统（如放大器或控制系统）是稳定还是不稳定。它是工程设计中的基本概念，有助于确保系统可靠运行而不失控振荡。

#### D. 传真（Fax）技术

他与Herbert E. Ives合作，帮助开发了AT&T于1924年公开发布的第一批传真机。

---

### 5. 遗产和对信息理论的影响

Nyquist的两篇论文，连同R.V.L. Hartley的一篇，被引述在Claude Shannon经典论文*"The Mathematical Theory of Communication"*（1948年）的第一段中，承认它们在信息理论发展中的开创性作用。

他的思想对其他理论家产生了关键影响；他早期发现传输信息所需的带宽要求，为数学家和科学家Claude Shannon奠定了基础，从而导致了信息理论的发展。

以Nyquist命名的术语和概念包括：

- Nyquist Frequency
- Nyquist Rate
- Nyquist Stability Criterion (Nyquist Plot)
- Nyquist ISI Criterion
- Johnson–Nyquist Noise
- Nyquist (一种编程语言)

---

### 6. 专利和发明

他是一位多产的发明家，持有超过130项美国专利。

---

### 7. 奖项和荣誉

Nyquist于1960年获得IRE Medal of Honor，以表彰他对“热噪声、数据传输和负反馈的定量理解的根本贡献”。1960年10月，他获得Franklin Institute的Stuart Ballantine Medal。1969年，他获得National Academy of Engineering的第四届Founder's Medal，以表彰“他对工程的诸多根本贡献”。

---

### 8. 逝世

Nyquist退休后居住在Texas州的Pharr，并于1976年4月4日在Texas州的Harlingen逝世。

---

### 总结表格

| 领域 | 贡献 | 年份 |
| --- | --- | --- |
| Signal Sampling | Nyquist Sampling Theorem | 1928 |
| Telegraph Theory | Telegraph speed & bandwidth | 1924 |
| Thermal Noise | Johnson–Nyquist Noise model | 1927 |
| Control Systems | Nyquist Stability Criterion | 1932 |
| Facsimile | AT&T first fax machine | 1924 |
| Information Theory | Foundation for Claude Shannon's work | 1920s–1940s |

---

**参考文献：**

- [Harry Nyquist – Wikipedia](https://en.wikipedia.org/wiki/Harry_Nyquist)
- [Harry Nyquist – Britannica](https://www.britannica.com/biography/Harry-Nyquist)
- [Harry Nyquist – Engineering and Technology History Wiki](https://ethw.org/Harry_Nyquist)
- [Harry Nyquist – AllAboutCircuits Historical Engineers](https://www.allaboutcircuits.com/news/historical-engineers-harry-nyquist-a-trail-blazer-in-digital-communications/)
- [Harry Nyquist – Moonraker Pioneers of Radio](https://moonrakeronline.com/blog/the-pioneers-of-radio-harry-nyquist---the-master-of-sampling)
- [Harry Nyquist – UND College of Engineering](https://blogs.und.edu/cem/2024/02/from-und-graduate-to-famous-inventor-and-thought-pioneer/)
