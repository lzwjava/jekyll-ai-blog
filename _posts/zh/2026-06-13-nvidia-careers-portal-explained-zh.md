---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA招聘门户详解
translated: true
type: note
---

**问题：** jobs.nvidia.com/careers 上的门户是什么？

**答案：**

这是 NVIDIA 的官方对外招聘门户——面向求职者的职位列表与申请网站。

底层基于 **Eightfold AI**（eightfold.ai）构建，这是一个由人工智能驱动的人才智能平台。配置信息揭示了它的许多运作方式：

- **基于 AI 的职位匹配**——它会根据你的个人资料与职位进行评分，并显示匹配百分比。配置中包含 `showMatchScore: true` 和 `strongMatchThreshold: 4`。
- **技能驱动的搜索**——可按职位类别、技能、地点、工作类型（全职/实习）、远程办公资格进行筛选。
- **人才网络**——你可以注册接收职位提醒，而无需立即申请。系统会利用候选人的个人资料（简历、技能、经验），每隔 7 天发送一次匹配的推荐。
- **ATS 后端**——申请会被重定向至 NVIDIA 的 Workday ATS（`nvidia.wd5.myworkdayjobs.com`）进行实际提交。申请按钮是一个指向 Workday 的链接，而非原生表单。
- **个人资料智能分析**——平台会解析你的简历，构建结构化的个人资料（经验、教育、技能、证书、项目），并以此对所有空缺职位进行匹配评分。

**为什么这对你来说特别重要：** NVIDIA 拥有大量 AI 基础设施相关岗位——CUDA 内核、GPU 架构、推理优化、大规模训练系统。其在计算、网络和 AI/ML 部门的职位与你的发展方向高度吻合。匹配评分系统意味着，一份精心打造、包含正确技能（如 CUDA、PyTorch、transformers、MoE、LoRA、RLHF）的个人资料，将使你在招聘人员的搜索中排名更靠前。如果你认真考虑在 NVIDIA 发展，值得在那里建立一份个人资料。
