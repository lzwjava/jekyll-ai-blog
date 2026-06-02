---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Google Cloud 考试监考与防作弊
translated: true
type: note
---

Question: 我们需要通过线下现场还是在线参加 Google Cloud 认证考试？如果是在线，他们如何防止 AI 作弊？

Answer:

Google Cloud 认证考试提供**两种选择** —— 你可以选择：

- **Online-proctored**（在家或办公室远程监考）
- **Onsite-proctored**（在实体考试中心现场参加）

你**不是必须**去现场参加；在通过考试注册平台（目前是 Kryterion 的 Webassessor，从 2026 年 2 月下旬开始将过渡到 Pearson VUE）进行预约时，可以自行选择。无论选择哪种交付方式，考试价格都是一样的，且如果需要，你可以在在线和现场之间切换（视考位情况而定）。

大多数考生为了方便选择在线选项，尽管有些人更倾向于考试中心，以避免家庭环境配置问题（例如：严格的技术/环境要求）。

### 关于远程监考 (Online-Proctored) 考试

这些考试通过真人监考（一名监考员实时通过远程监控你）结合监考软件来完成。主要的防作弊措施包括：

- **真人实时监考 (Live human proctor)**：在整个考试过程中观看你的视频流，如果发生可疑行为，可以干预或终止考试。
- **摄像头监控**：持续拍摄你的面部和测试环境（在开始前，你必须进行房间扫描/展示 360° 全景）。
- **屏幕共享/锁定**：你的屏幕会受到监控；通常使用安全浏览器来防止打开其他标签页或 App。
- **身份验证 (ID verification)**：监考员会实时检查政府颁发的带照片身份证件。
- **音频监控**：麦克风保持开启状态，以检测异常的声音或对话。
- **环境规则**：房间内不允许有其他人，附近不得有笔记、设备、食物或饮料，桌面需清空，不得频繁视线移开等。
- **行为标记 (Behavioral flags)**：监考员会标记违规行为，如离开摄像头视野、音视频质量不佳、使用未经授权的辅助工具或可疑的动作/按键。
- **考后复审**：录像可以被重新审查；违规行为会导致考试成绩作废、吊销认证或禁考。
- **禁止行为**（在考试条款与条件中明确列出）：使用未经授权的辅助工具、代考服务、AI 工具、复制粘贴、外部协助等。

针对具体的 **AI 作弊**（例如在考试期间使用 ChatGPT 或类似工具）：

- 真人监督 + 软件限制的组合使得实时使用 AI 变得非常困难且极易被发现（例如：输入长查询、出声或默念答案、将屏幕共享到另一个设备，或者视线过度移动到第二个屏幕，这些都可能被监考员标记）。
- Google 和 Kryterion 会积极调查疑似违规行为（包括 AI 协助），违规者可能面临严重的处罚。
- 虽然没有任何系统能 100% 防止作弊，但与无监考或全自动系统相比，实时监考 + 录像 + 严格规则提供了强大的威慑和检测能力。

了解最新详情（特别是 2026 年 2 月切换到 Pearson VUE 之后），请在预约考试时务必查看官方注册页面和监考要求。

References:

- [https://support.google.com/cloud-certification/answer/9907748](https://support.google.com/cloud-certification/answer/9907748) — Online Proctored Exams 详情
- [https://support.google.com/cloud-certification/answer/9907651](https://support.google.com/cloud-certification/answer/9907651) — 注册与预约（提到两种选项）
- [https://cloud.google.com/certification/terms](https://cloud.google.com/certification/terms) — 考试条款与条件（禁止行为和失效规则）
- [https://support.google.com/cloud-certification/answer/9907852](https://support.google.com/cloud-certification/answer/9907852) — 监考考试的测试要求
- [https://support.google.com/cloud-certification/answer/16803278](https://support.google.com/cloud-certification/answer/16803278) — 即将变更至 Pearson VUE (2026 年起)
