---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 人工智能会议中的双盲评审机制
translated: true
type: note
---

**问：** AI会议中如何使用双盲审稿，其规则、优势、挑战及当前争议有哪些？

**答：**

## 什么是双盲审稿？

双盲审稿指在同行评审过程中双方保持匿名：审稿人看不到作者的姓名或所属机构，作者也不知道审稿人是谁。目的很简单——会议希望论文基于其学术价值被评估，而非依据作者的声誉、机构或资历。

这与以下方式形成对比：

- **单盲审稿**：审稿人知道作者身份，但作者不知道审稿人身份。
- **开放评审**：双方互相知晓身份（部分会议采用，如ICLR在录用后阶段）。

---

## 哪些主要AI会议采用双盲审稿？

ICML、ICLR、NeurIPS、CVPR等顶级AI会议已将双盲同行评审作为标准，其论文影响力可与诸多知名期刊相媲美。

具体政策：

- **ICLR 2026**：投稿采用双盲形式——审稿人在评审时看不到作者姓名，作者也看不到审稿人姓名。任何在正文或补充材料中泄露作者身份信息的论文将被直接拒收。
- **ICML 2026**：所有论文均通过双盲流程进行评审。
- **AAAI**：评审采用双盲形式——评审人和作者均不应识别对方身份。首页应包含标题、摘要、内容领域和ID编号，但不包含作者姓名或所属机构。
- **IJCAI-ECAI 2026**：作者有责任对投稿进行匿名处理。稿件中不应包含作者姓名或机构信息，并应避免提供任何其他可识别信息，即使在补充材料中亦如此。

---

## 作者必须遵守的规则

**1. 移除标识信息：**
作者必须从投稿中移除所有作者和机构信息，可替换为其他信息如论文编号和关键词。致谢部分也应省略。

**2. 以第三人称进行自引：**
在提及自己先前工作时，作者应使用第三人称而非第一人称。例如，应说“先前，Hinton等人（2006）表明…”而非“在我们之前的工作中（Hinton等人，2006）我们证明了…”。

**3. 谨慎处理arXiv：**
允许投稿作品以未审阅预印本（如提交至arXiv、社交媒体或个人网站）的形式提前发布。然而，会议投稿不应引用或指向非匿名材料，且非匿名的在线材料也不应提及该作品已投稿至会议。

**4. 匿名化补充材料：**
补充材料和代码也应进行匿名化处理，包括可能暴露登录标识或机构的硬编码路径或URL。

---

## 审稿人必须遵守的规则

审稿人不得试图查找任何分配稿件的作者身份（例如通过arXiv搜索）。这将构成对双盲评审政策的主动违反。

双盲评审过程的目标是帮助评审成员在无偏见的情况下对论文做出判断，而非刻意使作者身份无法被探知。不应为了匿名化而削弱投稿质量或增加评审难度——例如，不应省略或匿名化重要的背景参考文献。

---

## 双盲审稿的优势

由于作者和审稿人均处于“盲态”，这能防止审稿人受作者声望影响。即使是领域内知名学者的投稿，也会基于其自身价值而非作者声誉进行评判。另一优势是减少了审稿人偏见可能性。

研究证据支持其有效性：
当Learning Representations会议（ICLR）从单盲评审转为双盲评审后，最具声望作者所获评分显著下降。同时发现，双盲评审在接纳高质量论文（引用率最高者）和拒收低质量论文方面更为有效。

研究还发现，采用双盲评审的会议中，新研究者的出现频率约为单盲评审会议的两倍，这表明单盲评审往往对尚未在社区内知名的研究者存在偏见。

---

## 挑战与局限

**1. 去匿名化仍可能发生：**
在小型研究社区中，审稿人仍可能通过主题、引用或写作风格猜出论文作者。

**2. arXiv带来的冲突：**
arXiv对双盲评审构成主要挑战。许多研究显示了因审稿人知晓作者信息而产生的偏见，且大量投稿由于arXiv预印本的存在，其评审条件最终与其他论文不同。

**3. 投稿量激增：**
至2025年，主要AI会议的论文投稿量已超10,000篇——例如仅2025年ICLR投稿量就增长了59.8%——使传统同行评审系统不堪重负。

**4. LLM生成的评审：**
Pangram Labs报告发现，ICLR 2026的75,800份同行评审中，惊人的21%完全由AI生成，超半数显示AI辅助痕迹。本为保障公平而设的双盲系统，却成为了学术失责的掩护——让任务过重或缺乏诚意的审稿人将其关键职责外包给大型语言模型。

**5. 安全漏洞：**
ICLR 2026评审过程因OpenReview API缺陷（被认定为访问控制失效问题）而遭受入侵，表明单个故障点就足以危害整个双盲系统。

---

## AI会议的适应措施

- **多阶段评审**：AAAI-26采用两阶段评审流程，通过第一阶段的论文将获得额外审稿人，且新增审稿人在提交自身评审前无法查看第一阶段评审意见。
- **作者反驳阶段**：大多数主要会议目前设有专门的反驳阶段，允许作者回应审稿意见。
- **LLM使用政策**：ICML允许作者使用生成式AI工具辅助写作或研究，但作者必须对所有内容负全责，包括任何可能被视为抄袭或学术不端的行为。
- **审稿人资格要求**：ICLR要求所有投稿必须至少有一位作者注册为审稿人并承诺评审至少3篇论文，若无作者注册为审稿人，将导致直接拒稿。

---

## 概要表

| 方面 | 细节 |
|---|---|
| 核心理念 | 作者与审稿人相互匿名 |
| 主要会议 | ICML、ICLR、NeurIPS、AAAI、IJCAI、CVPR |
| 作者义务 | 移除姓名、以第三人称自引、匿名化代码/补充材料 |
| 审稿人义务 | 不主动搜寻作者身份，独立评审 |
| 主要优势 | 减少声望/地位偏见；更注重论文质量而非作者名气 |
| 主要挑战 | arXiv预印本、LLM生成的评审、小众领域的去匿名化 |
| 近期危机 | ICLR 2026数据泄露 + 约21%AI生成评审被发现 |

**参考文献：**

- [What Is Double-Blind Review for Conference Papers? – AiScholar](https://www.aischolar.com/news/article/what-is-double-blind-review-for-conference-papers)
- [AAAI-26 Review Process](https://aaai.org/conference/aaai/aaai-26/review-process/)
- [ICLR 2026 Author Guide](https://iclr.cc/Conferences/2026/AuthorGuide)
- [ICML 2026 Call for Papers](https://icml.cc/Conferences/2026/CallForPapers)
- [IJCAI-ECAI 2026 Call for Papers](https://2026.ijcai.org/ijcai-ecai-2026-call-for-papers-main-track/)
- [NeurIPS 2025 Reviewer Guidelines](https://neurips.cc/Conferences/2025/ReviewerGuidelines)
- [Double-Anonymous Review for Robotics – arXiv](https://arxiv.org/html/2406.10059v1)
- [The AI Conference Peer Review Crisis – arXiv](https://arxiv.org/html/2505.04966v1)
- [The Glass Wall Shatters: ICLR 2026 Breach Reflection](https://www.gensee.ai/blogs/a-professor-s-reflection-on-the-iclr-2026.html)
- [ArXiv and the Future of Double-Blind Reviewing – ACL 2017 Blog](https://acl2017.wordpress.com/2017/02/19/arxiv-and-the-future-of-double-blind-conference-reviewing/)
- [Single or Double Blind Peer Review – ExOrdo](https://www.exordo.com/blog/the-peer-review-process-single-versus-double-blind)
