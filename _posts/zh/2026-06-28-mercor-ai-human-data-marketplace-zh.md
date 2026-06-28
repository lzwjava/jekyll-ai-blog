---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Mercor：人工智能人类数据市场
translated: true
type: note
---

问题：Mercor这家AI公司是什么？

回答：

让我搜索一下最新信息。

Mercor是一家美国AI公司，提供专家来训练AI模型和聊天机器人。它本质上是一个连接AI实验室和领域专家的人力数据市场——扮演的是高质量RLHF/专家数据的“新石油”角色，而非数据中心或模型本身。

**基本情况：**

- 2023年由Brendan Foody、Adarsh Hiremath和Surya Midha创立——三人是旧金山湾区的高中好友，来自Bellarmine辩论队，辍学后获得了Thiel Fellowship。总部位于旧金山。
- 最初是一家AI招聘初创公司——通过AI面试和匹配平台，将印度的自由职业程序员与美国公司连接起来。随后转型为数据标注/专家承包商匹配服务，为OpenAI等AI公司提供支持。
- 客户包括OpenAI和Anthropic。截至2025年10月，管理约3万名承包商——包括工程师、律师、医生、银行家和记者。

**融资情况：**

- 360万美元种子轮（2023年，General Catalyst）→ 3200万美元A轮（2024年，Benchmark，估值2.5亿美元）→ 1亿美元B轮（2025年2月，Felicis，估值20亿美元）。
- 2025年10月完成3.5亿美元C轮融资，估值达100亿美元——使当时22岁的创始人成为最年轻的白手起家亿万富翁。投资者包括Peter Thiel、Jack Dorsey和Adam D'Angelo。

**与你（基准测试）相关的内容：**
Mercor推出了**APEX-Agents**，这是一个涵盖投资银行、管理咨询和企业法务等480项任务的开源基准测试——包含工具实现、评分标准和评分流程。前沿模型在该基准测试上表现接近：GPT-5.4得分33.3%，Claude Opus 4.6得分33.0%，Gemini 3.1 Pro Preview得分32.0%——前三名仅相差1.3个百分点。他们还与Cognition合作构建了**APEX-SWE**，几乎所有前沿模型在近60%的真实生产软件工程任务上均失败。如果你正在对专业知识工作的智能体进行基准测试，值得一看。

**争议：**

- 2026年3月下旬，Mercor遭受了涉及LiteLLM包的供应链攻击，可能导致高达4TB的内部数据和承包商个人身份信息泄露——引发集体诉讼，并导致包括Meta在内的客户临时暂停合作。（对你来说特别值得注意——LiteLLM被广泛用作LLM代理/路由器。）
- 接受The Verge、NY Magazine和Wired采访的承包商表示，工作环境压力大、管理不善、薪酬下降。
- 一些批评者认为，“AI面试”部分是为了收集训练数据，而非纯招聘。

Foody提出的观点：如果AI自动化了经济中90%的工作，人类将成为剩余10%的瓶颈，从而使得每单位人类经济产出获得10倍杠杆。Mercor将自己定位为将稀缺人类专业知识分配给AI训练的市场。

参考资料：

- [Mercor - 维基百科](https://en.wikipedia.org/wiki/Mercor)
- [Mercor以20亿美元估值融资1亿美元 - TechCrunch](https://techcrunch.com/2025/02/20/mercor-an-ai-recruiting-startup-founded-by-21-year-olds-raises-100m-at-2b-valuation/)
- [Mercor | LinkedIn (APEX-Agents基准测试)](https://www.linkedin.com/company/mercor-ai)
- [什么是Mercor AI？ - eesel AI](https://www.eesel.ai/blog/mercor-ai)
