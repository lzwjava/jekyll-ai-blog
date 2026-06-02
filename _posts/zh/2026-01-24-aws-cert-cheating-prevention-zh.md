---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: AWS 认证考试与作弊防范
translated: true
type: note
---

Question: AWS Certification 是否有考试中心？它是如何防止 AI 作弊的？

Answer:

是的，**AWS Certification 考试确实设有考试中心**。

AWS 与 **Pearson VUE** 合作，通过两种主要方式提供考试：

- **在线下考试中心参加考试** — 您可以在 Pearson VUE 的实体考试中心参加考试。这些网点遍布全球（包括新加坡及许多其他国家/地区）。要查找您附近的中心，请登录 AWS Certification 门户，选择您的考试，并在预约时通过邮政编码或位置搜索考试中心。

- **在线监考（在家/办公室）** — 所有 AWS 考试也可以通过 Pearson VUE 的 OnVUE 平台进行，该平台提供 24/7 的英语服务（其他语言在特定时间段提供）。

大多数考生会选择更方便的方式 —— 许多人因为灵活性而偏好在线考试，而有些人则选择考试中心以避免家庭环境配置问题。

### AWS 如何防止作弊（包括使用 ChatGPT 或类似工具的 AI 辅助作弊）

AWS 和 Pearson VUE 采用多层防御机制来维护考试的完整性：

#### 针对 **在线监考考试**（AI 作弊最受关注的领域）：
- 真人 Proctor（监考员）通过摄像头和屏幕共享实时监控。
- 开考前，您必须展示整个房间（360° 扫描）、桌面和周围环境。
- 严格规则：房间内严禁使用手机、笔记、额外显卡、Headphones 或出现其他人；禁止携带的物品必须移走或显示已关机。
- Proctor 会观察您的眼睛、头部动作和行为 —— 频繁向别处看或有可疑模式会触发立即干预（他们可以暂停或终止考试）。
- 全程录音录像（视频 + 音频 + 屏幕）供事后回溯。
- 不允许使用书写材料（与某些线下考试中心的设置不同）。
- 系统检查会拦截 Virtual Machines、未经授权的软件等。

#### 针对 **在线和线下考试**：
- **数据取证和行为分析 (Data forensics and behavioral analytics)** — AWS 使用统计分析来检测异常情况（例如：异常快速的答题模式、对已知泄露题目的相同错误答案、不符合常理的鼠标/键盘操作、或偏离预期分布的分数）。这可以检测出使用 Brain-dump、死记硬背 Dump 答案或 AI 工具生成的模式。
- 如果被系统标记，AWS 将进行调查 — 结果可能被判无效，Credential 将被撤销，且考生可能被禁止参加未来的考试（有时是永久性的）。
- 题目会定期轮换，且考试表单各不相同，使得记忆式或 AI 生成的答案可靠性降低。
- 严厉处罚：作弊行为（即使是在考试后检测到的）会导致成绩取消、证书撤销，以及取消补考资格或合作伙伴福利。

在实际操作中，由于实时监控和取证技术的存在，在考试期间使用 AI 工具极难不被发现。许多考生反映监考员非常严格（例如，轻微的偏头或房间环境问题都会被警告）。考试中心则增加了物理层面的监督，进一步降低了远程作弊的风险。

如果您担心环境配置或公平性，选择实体考试中心对某些人来说可能会感到更加稳妥。

References:

- [AWS Certification Testing Options](https://aws.amazon.com/certification/certification-prep/testing)
- [Pearson VUE AWS OnVUE Online Testing](https://www.pearsonvue.com/us/en/aws/onvue.html)
- [AWS Certification General Policies (including data forensics)](https://aws.amazon.com/certification/policies/general-policies)
- [AWS Certification FAQs](https://aws.amazon.com/certification/faqs)
