---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 视觉Transformer作者及其贡献
translated: true
type: note
---

### 《一幅图像价值16x16个词汇：规模化图像识别的Transformer模型》作者简介

2020年由Alexey Dosovitskiy与谷歌同事共同发表的突破性论文《一幅图像价值16x16个词汇：规模化图像识别的Transformer模型》，标志着计算机视觉领域的重大转折。该论文提出了Vision Transformer（ViT）模型，将原本为自然语言处理设计的Transformer架构直接应用于图像块，在大型数据集（如JFT-300M）上进行预训练后，在ImageNet等基准测试中达到了顶尖性能。这项工作证明了在充足算力和数据支持下，纯Transformer模型在效率和准确度上能够超越卷积神经网络（CNN），对多模态AI和可扩展视觉模型的后续发展产生了深远影响。

这篇论文是12位研究人员（主要来自谷歌大脑苏黎世团队）的合作成果，融合了深度学习、序列建模和大规模训练领域的专业经验。以下是对核心作者的概述，重点介绍他们的背景及对领域的贡献。（为简洁起见，此处聚焦于主要贡献者；完整名单包括Dirk Weissenborn、Thomas Unterthiner、Mostafa Dehghani、Matthias Minderer、Georg Heigold、Sylvain Gelly和Jakob Uszkoreit——这些谷歌系研究者均在Transformer架构、优化算法及视觉-语言融合领域有深厚积累。）

#### 核心作者与背景

- **Alexey Dosovitskiy（第一作者）**：作为ViT模型的推动者，Dosovitskiy提出了将图像视为块序列的核心概念。他拥有莫斯科国立罗蒙诺索夫大学的数学硕士和博士学位，随后在弗莱堡大学从事无监督特征学习的博士后研究。2019年加入谷歌大脑后，他主导了ViT的开发，并于2021年转投柏林AI公司Inceptive。他的研究涵盖计算机视觉、生成模型和仿生机器学习，论文引用量超13.6万次。

- **Lucas Beyer**：Beyer在ViT的工程实现、基准测试评估和效率优化方面发挥了关键作用。这位比利时研究者曾在亚琛工业大学攻读机械工程，2018年获得机器人学与人工智能博士学位，主要研究游戏AI与强化学习。博士毕业后加入谷歌大脑苏黎世团队，后晋升为谷歌DeepMind主任研究科学家。2025年成为Meta顶级AI人才引进之一，持续致力于视觉Transformer和数据中心化机器学习研究。

- **Alexander Kolesnikov**：Kolesnikov为ViT的扩展实验和迁移学习研究做出贡献，重点验证了模型在中等规模数据集上的性能。他拥有莫斯科国立大学数学硕士学位，2018年获奥地利科学技术学院机器学习与计算机视觉博士学位。2018年加入谷歌大脑，后于DeepMind担任主任研究员，历经OpenAI后于2025年加入Meta——其高效视觉模型专长成为重点引进原因。

- **翟晓华**：翟晓华专注于ViT的预训练策略和多模态扩展研究，其工作源于在表征学习领域的积累。他持有北京大学电子工程博士学位，2015年以软件工程师身份加入谷歌，2017年转入谷歌大脑研究院，2023年加入DeepMind。现通过OpenAI苏黎世分部任职Meta研究员，其研究成果贯通视觉、语言与自监督学习领域，引用量超10万次。

- **Neil Houlsby（资深作者）**：作为团队负责人，Houlsby统筹了ViT的架构设计及其对视觉规模定律的深远影响。他于2010年左右获得谷歌欧洲博士奖学金，完成机器学习博士学位。从实习期便长期任职谷歌，曾在谷歌大脑和DeepMind领导神经网络架构与视觉-语言模型团队。2025年加入Anthropic负责新苏黎世办公室，专注于安全AI规模化研究。

这场主要由谷歌大脑苏黎世团队主导的合作，充分利用团队与TPU集群的地理优势开展大规模实验——累计超2.5万TPU日——证明了Transformer架构在文本领域之外的可行性。多数作者后续流向Meta、OpenAI和Anthropic等顶尖AI实验室，印证了ViT对领域的持久影响力。

#### 参考文献

- [《一幅图像价值16x16个词汇：规模化图像识别的Transformer模型》（arXiv）](https://arxiv.org/abs/2010.11929)
- [Alexey Dosovitskiy谷歌学术档案](https://scholar.google.com/citations?user=FXNJRDoAAAAJ)
- [Lucas Beyer谷歌学术档案](https://scholar.google.com/citations?user=p2gwhK4AAAAJ)
- [Alexander Kolesnikov谷歌学术档案](https://scholar.google.com/citations?user=H9I0CVwAAAAJ)
- [翟晓华谷歌学术档案](https://scholar.google.com/citations?user=8gruapYAAAAJ)
- [Neil Houlsby谷歌学术档案](https://scholar.google.com/citations?user=sm1-TZMAAAAJ)
- [从博士绕行道到Meta顶级AI人才：Lucas Beyer（印度时报）](https://timesofindia.indiatimes.com/education/news/lucas-beyer-educational-qualification-from-ph-d-detour-and-google-rejection-to-becoming-metas-top-ai-hire/articleshow/122158414.cms)
- [扎克伯格从OpenAI挖角Alexander Kolesnikov（印度时报）](https://timesofindia.indiatimes.com/education/news/zuckerberg-poached-alexander-kolesnikov-from-sam-altmans-openai-where-did-this-ai-genius-study/articleshow/122158654.cms)
- [Anthropic从谷歌DeepMind挖角Neil Houlsby（欧洲新闻）](https://www.euronews.com/next/2025/02/13/anthropic-poaches-google-deepmind-talent-to-lead-new-european-office)
