---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 伯克利的开源创新传承
translated: true
type: note
---

Question: Why does the University of California, Berkeley have a great tradition of open source?

Answer: 

**University of California, Berkeley** (UC Berkeley) 拥有最强大且最悠久的 open source 软件传统之一，这主要归功于它在 Unix 早期阶段的先驱地位，以及其持续不断的为了研究和创新而分享 code 的文化。

以下是主要原因：

- **Berkeley Software Distribution (BSD) 与早期 Unix 分享（1970s–1990s）**  
  UC Berkeley 的 Computer Systems Research Group (CSRG) 从 Bell Labs 接收了 Unix 的早期版本（当时包含了 source code，这在当时并不寻常）。从 1977-1978 年开始，Berkeley 开始分发增强版本，即 **Berkeley Software Distribution (BSD)**。  
  这些版本包含了重大改进，如 vi 编辑器、C shell、virtual memory 支持，特别是 TCP/IP networking stack，它成为了现代 Internet 的基石。  
  Berkeley 将这些附带 source code 的软件广泛分发给其他大学和机构，建立了学术界最早的协作式、source-available 软件开发模式之一。

- **BSD license —— 最初的宽松型 open source licenses 之一**  
  Berkeley 开发了 **BSD license**，它非常宽松：只要保留版权声明，就允许自由使用、修改和重新分发（甚至可以用于 proprietary 产品）。  
  这种“非 copyleft”的方法与后来的 GPL 风格 license 形成对比，使得 BSD 衍生品对学术界和工业界都极具吸引力。现代 open source 后裔（FreeBSD、OpenBSD、NetBSD）甚至 macOS/iOS 的部分组件（通过 Darwin）都可以追溯到这一传统。

- **开放与协作的学术文化**  
  在 20 世纪 70-80 年代，学术界的 computer science 部门（特别是像 Berkeley 这样的地方）有着公开分享 code、论文和结果的长久传统。  
  Unix 本身在早期版本中就附带了 source code，Berkeley 的研究人员将软件视为科学知识——一种需要共同改进的东西，而不是被锁定。

- **通过现代 open source 项目持续施加影响**  
  Berkeley 将这种文化延续至今，拥有众多具有影响力的项目，例如：  
  - **RISC-V**（开放 instruction set architecture）  
  - **Apache Spark**（起源于 Berkeley 的 AMPLab，现在是 big data 的基石）  
  - **Berkeley DB**（被广泛使用的 embedded database）  
  - 来自 RISE Lab、Sky Computing Lab 等实验室的许多工具均以 open source licenses 发布。  
  这催生了众多围绕 Berkeley 源起 open source 软件建立的成功公司（Databricks、Anyscale、SiFive 等）。

- **大学对 open source 创业公司和授权的支持**  
  UC Berkeley 拥有 Open Source Software Startup Program (OS3) 等项目，鼓励研究人员在 open source licenses 下发布软件并剥离出公司，同时平衡大学的利益。

总结来说，Berkeley 的 open source 传统始于 20 世纪 70 年代后期的 BSD，并得到了宽松授权和学术分享规范的强化，通过数十年的影响力项目得以延续。很少有其他大学在发布重塑 Internet、operating systems、databases、machine learning frameworks 和 hardware design 的基础 open source 软件方面，拥有如此悠久、一致且具有影响力的历史。

References:  

- [Berkeley Software Distribution - Wikipedia](https://en.wikipedia.org/wiki/Berkeley_Software_Distribution)
- [History of the Berkeley Software Distribution - Wikipedia](https://en.wikipedia.org/wiki/History_of_the_Berkeley_Software_Distribution)
- [UC Berkeley Open Source Software Startup Program](https://ipira.berkeley.edu/open-source-software-startup-program)
- [How a group of Berkeley researchers took over the chip industry (RISC-V)](https://boldandopen.substack.com/p/how-a-group-of-berkeley-researchers)