---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: MiniMax M1 and M2 Model Overview
translated: false
type: note
---

### MiniMax M1 and M2: Major Contributors, Paper Authors, and Tech Lead

MiniMax M1 and M2 are advanced AI models developed by MiniMax AI, a Chinese AI startup focused on large language models (LLMs) and multimodal AI. Both models are part of their open-weight releases, with M1 emphasizing long-context reasoning (up to 1 million tokens) and efficient test-time compute, while M2 targets coding, agentic workflows, and multi-agent support. The development is a collaborative effort by the MiniMax team, but specific attributions are limited in public releases.

#### Major Contributors

- **Core Team**: The models are built by a large engineering and research team at MiniMax AI. For M1, training involved reinforcement learning (RL) on diverse tasks like software engineering and tool use, completed efficiently on 512 H800 GPUs in just three weeks. M2 builds on similar hybrid architectures but optimizes for agent efficiency.
- No individual "major contributors" are singled out beyond the collective team, as credits are team-based. External collaborations include the SGLang team for M2 deployment support.

#### Paper Authors

- **MiniMax-M1**: Detailed in the technical report *"MiniMax-M1: Scaling Test-Time Compute Efficiently with Lightning Attention"* (arXiv:2506.13585). Authors are listed alphabetically (over 50 total, all affiliated with MiniMax):
  - Aili Chen, Aonian Li, Bangwei Gong, Binyang Jiang, Bo Fei, Bo Yang, Boji Shan, Changqing Yu, Chao Wang, Cheng Zhu, Chengjun Xiao, Chengyu Du, Chi Zhang, Chu Qiao, Chunhao Zhang, Chunhui Du, Congchao Guo, Da Chen, Deming Ding, Dianjun Sun, Dong Li, Enwei Jiao, Haigang Zhou, Haimo Zhang, Han Ding, Haohai Sun, Haoyu Feng, Huaiguang Cai, Haichao Zhu, Jian Sun, Jiaqi Zhuang, Jiaren Cai, Jiayuan Song, Jin Zhu, Jingyang Li, Jinhao Tian, Jinli Liu, Junhao Xu, Junjie Yan, Junteng Liu, Junxian He, Kaiyi Feng, Ke Yang, Kecheng Xiao, Le Han, Leyang Wang, Lianfei Yu, Liheng Feng, Lin Li, Lin Zheng, Linge Du, Lingyu Yang, Lunbin Zeng, Minghui Yu, Mingliang Tao, Mingyuan Chi, Mozhi Zhang, Mujie Lin, Nan Hu, Nongyu Di, Peng Gao, Pengfei Li, Pengyu Zhao, Qibing Ren, Qidi Xu, Qile Li, Qin Wang, Rong Tian, Ruitao Leng, Shaoxiang Chen, Shaoyu Chen, Shengmin Shi, Shitong Weng, Shuchang Guan, Shuqi Yu, Sichen Li, Songquan Zhu, Tengfei Li, Tianchi Cai, Tianrun Liang, Weiyu Cheng, Weize Kong, Wenkai Li, Xiancai Chen, Xiangjun Song, Xiao Luo, Xiao Su, Xiaobo Li, Xiaodong Han, Xinzhu Hou, Xuan Lu, Xun Zou, Xuyang Shen, Yan Gong, Yan Ma, Yang Wang, Yiqi Shi, Yiran Zhong, Yonghong Duan (and 27 additional authors).
  - Note: Junjie Yan (CEO) is among the authors.
- **MiniMax-M2**: No dedicated academic paper or author list found in public sources. It's released via Hugging Face with team credits to MiniMax AI overall, referencing internal innovations but no named individuals.

#### Tech Lead

- **Yan Junjie**: Founder and CEO of MiniMax AI (established in 2021). He oversees the technical direction, including model development for M1 and M2. A former SenseTime executive, Yan has delivered keynotes on these models (e.g., at WAIC 2025) and is credited in M1's author list. He's the primary public face for the company's AI advancements.

MiniMax's approach emphasizes efficient, scalable AI for broad applications, with M1 and M2 representing rapid iterations in open-source reasoning models.

#### References

- [MiniMax-M1 arXiv Paper](https://arxiv.org/abs/2506.13585)
- [MiniMax-M1 GitHub](https://github.com/MiniMax-AI/MiniMax-M1)
- [MiniMax-M2 Hugging Face](https://huggingface.co/MiniMaxAI/MiniMax-M2)
- [Yan Junjie Profile (SCMP)](https://www.scmp.com/topics/yan-junjie)
- [MiniMax Crunchbase](https://www.crunchbase.com/organization/minimax-a48a)
