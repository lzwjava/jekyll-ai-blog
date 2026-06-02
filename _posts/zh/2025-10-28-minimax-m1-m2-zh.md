---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: MiniMax M1与M2模型概览
translated: true
type: note
---

### MiniMax M1 与 M2：核心贡献者、论文作者与技术负责人

MiniMax M1 和 M2 是由中国人工智能初创企业 MiniMax AI 开发的先进AI模型，该公司专注于大语言模型（LLM）与多模态AI技术。这两款模型均属于其开放权重版本，其中M1侧重长上下文推理（最高达100万token）与高效测试时计算，而M2则专注于编程、智能体工作流及多智能体支持。模型的开发由MiniMax团队协同完成，但公开信息中对具体人员归属披露有限。

#### 核心贡献者
- **核心团队**：模型由MiniMax AI的大规模工程与研发团队构建。M1的训练涉及软件工程、工具使用等多样化任务的强化学习（RL），仅用三周时间在512张H800 GPU上高效完成。M2采用类似的混合架构，但针对智能体效率进行了优化。
- 除团队集体荣誉外，未单独列出“核心贡献者”个人。外部合作包括SGLang团队为M2部署提供的支持。

#### 论文作者
- **MiniMax-M1**：技术报告《MiniMax-M1: Scaling Test-Time Compute Efficiently with Lightning Attention》（arXiv:2506.13585）中详述。作者按字母顺序排列（共50余人，均隶属于MiniMax）：
  - 陈爱丽、李傲年、龚邦伟、蒋滨阳、费博、杨波、单博际、余长清、王超、朱诚、肖成军、杜成宇、张弛、乔楚、张春浩、杜春辉、郭丛超、陈达、丁德明、孙殿君、李冬、焦恩伟、周海刚、张海默、丁晗、孙浩海、冯浩宇、蔡怀光、朱海潮、孙健、庄佳奇、蔡佳仁、宋家源、朱晋、李景阳、田金浩、刘金莉、徐俊浩、闫俊杰、刘俊腾、何俊贤、冯恺毅、杨珂、肖克成、韩乐、王乐扬、于联飞、冯立衡、李林、郑琳、杜凌格、杨凌宇、曾伦斌、于明辉、陶明良、池明远、张墨汁、林慕杰、胡楠、狄农宇、高鹏、李鹏飞、赵鹏宇、任其冰、徐启迪、李启乐、王钦、田荣、冷瑞涛、陈绍祥、陈绍宇、石盛敏、翁世通、管舒畅、于淑琪、李思辰、朱松泉、李腾飞、蔡天驰、梁天润、程威宇、孔维泽、李文科、陈贤才、宋向军、罗潇、苏晓、李小波、韩晓东、侯新竹、卢璇、邹洵、沈旭阳、龚岩、马岩、王洋、石一奇、钟亦然、段永宏（及另外27位作者）。
  - 注：闫俊杰（CEO）位列作者名单。
- **MiniMax-M2**：公开渠道未发现专属学术论文或作者列表。该模型通过Hugging Face发布，荣誉归属MiniMax AI整体，提及内部创新但未列出具体人员。

#### 技术负责人
- **闫俊杰**：MiniMax AI创始人兼CEO（公司成立于2021年）。他主导包括M1与M2模型开发在内的技术方向。作为前商汤科技高管，闫俊杰曾在重要会议（如2025世界人工智能大会）就这些模型发表主题演讲，并位列M1作者名单。他是公司AI技术进展的主要公开代表。

MiniMax的技术路径强调高效、可扩展的AI普惠应用，M1与M2体现了开源推理模型的快速迭代能力。

#### 参考资料
- [MiniMax-M1 arXiv论文](https://arxiv.org/abs/2506.13585)
- [MiniMax-M1 GitHub](https://github.com/MiniMax-AI/MiniMax-M1)
- [MiniMax-M2 Hugging Face](https://huggingface.co/MiniMaxAI/MiniMax-M2)
- [闫俊杰人物简介（南华早报）](https://www.scmp.com/topics/yan-junjie)
- [MiniMax Crunchbase档案](https://www.crunchbase.com/organization/minimax-a48a)
