---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: DeepMind controversial 的阴暗面
translated: true
type: note
---

问题：关于 DeepMind，有哪些不那么受欢迎的观点或鲜为人知的事实？

答案：

DeepMind 是 Google 在 2014 年收购的 AI 研究实验室，因 AlphaGo 和 AlphaFold 等突破性成就而备受赞誉，但它也因伦理失误、夸大研究以及内部动荡而受到大量批评。以下，我根据公开讨论、报告和分析，整理了一份不受欢迎的观点和争议事实清单。这些内容突显了其科学雄心与实际影响之间的矛盾，而这些矛盾在 AI 热潮中往往被轻描淡写。

### 不受欢迎的观点

- **DeepMind 的科学主张常被夸大并证伪**：虽然 AlphaFold 彻底改变了蛋白质折叠领域，但近期关于自主材料发现（例如生成数百万种无机化合物）的论文却因方法论缺陷和结果不稳定而受到化学家的质疑。批评者认为，这反映了 DeepMind 在物理科学方面存在“胡说八道探测器”警报的模式，即优先考虑华丽的发布而非严谨的验证。
- **Google 的收购扼杀了 DeepMind 的独立性和创新**：2014 年的收购（Elon Musk 曾出于安全担忧试图阻止但未成功）将 DeepMind 整合到 Alphabet 以利润为导向的生态系统。这导致了 ChatGPT 之后出版物上的“无线电静默”（例如，没有 GATO 或 Sparrow 的更新），因为 Google 优先考虑商业产品而非纯粹的研究。一个不受欢迎的观点是：DeepMind 现在“为 Google 的 AI 风险提供掩护”，却没有提供独立的产品。
- **DeepMind 对大型语言模型 (LLM) 的关注是分散了对更深层限制的注意力**：尽管 Gemini 等取得了进展，但该实验室在 ChatGPT 之后转向大型语言模型，却忽视了其根本缺陷——幻觉、缺乏真正的推理能力以及环境成本（例如，大规模数据中心消耗大量水资源）。观点：扩大 LLM 的规模并不能产生通用人工智能 (AGI)；它们只是模仿而没有理解，DeepMind 的“创造性”数学证明（例如 IMO 银奖）是针对 LLM 友好问题的蛮力胜利，而非天才的飞跃。
- **尽管备受关注，DeepMind 在实际应用方面却滞后**：围绕 AlphaGo 的早期炒作已逐渐消退，实验室也转向科学应用，但其产出仍冗长、易出错且对终端用户而言难以执行。看法：这更像是“研究表演”而非实用工具，其代码生成功能实用但臃肿（例如不必要的工厂、不遵循 SOLID 原则），迫使用户事后进行清理。

### 争议事实

- **大规模 NHS 数据隐私丑闻**：2016 年，DeepMind 未经适当同意或伦理审查，获取了伦敦皇家自由医院的 160 万份未匿名化患者记录，表面上是为了开发肾损伤应用程序 (Streams)。英国信息专员办公室 (ICO) 于 2017 年裁定其非法，理由是数据保护方面存在缺陷。2021 年，受影响的患者提起诉讼，指控数据滥用，批评者指出缺乏足够的保障措施来防止 Google 的商业剥削。
- **联合创始人 Mustafa Suleyman 的欺凌调查和解职**：2019 年，Suleyman（应用 AI 负责人）因员工投诉其激进的管理风格而被停职，并由一家外部律师事务所进行调查。这发生在他负责的 NHS 丑闻之后，以及 DeepMind 的健康部门被并入 Google Health 之后。他后来前往 Inflection AI，此前有报道称内部存在权力斗争。
- **拖延处理性行为不端指控**：2022 年，一名举报人指控 DeepMind 耗时 10 个月才解决她对一名高级研究员性行为不端的投诉，人力资源部门还威胁如果她对外公开将采取纪律处分。该公司据称拖延处理过程并强迫她继续互动，这突出显示了尽管有道德委员会，但其文化仍然存在问题。
- **未能争取从 Alphabet 获得法律独立性**：DeepMind 曾寻求（但后来放弃）在 2021 年建立独立的结构，以保护其 AI 免受 Alphabet 的监控或军事用途（例如与五角大楼的联系）。首席执行官 Demis Hassabis 轻描淡写了风险，但批评者认为这使得“强大技术”容易被滥用，例如虚假信息或偏见工具。
- **模型中固有的透明度和偏见**：DeepMind 的大型语言模型（例如 Gemini）嵌入了训练者的价值观，导致审查或礼貌偏见。事实：像这样的模型会延续刻板印象、实现监控，并由于有缺陷的训练数据而产生幻觉，没有真正的自我修正——然而它们却被宣传为“谨慎的”进步。

这些论点强调了 DeepMind 的双重遗产：开创性但有缺陷，创新性但道德上充满挑战。虽然它推进了科学，但商业化的冲动往往会放大风险而非利益。

**参考文献：**

- [两项研究驳斥 DeepMind 的材料发现主张](https://www.reddit.com/r/singularity/comments/1bzlx9l/two_studies_have_now_come_out_that_have_now/)
- [DeepMind 怎么了？](https://www.reddit.com/r/singularity/comments/116c4pg/whats_up_with_deepmind/)
- [化学家质疑 DeepMind 研究](https://www.reddit.com/r/singularity/comments/1agf8tr/chemists_dispute_google_deepmind_research/)
- [Elon Musk 和 DeepMind 的故事](https://www.reddit.com/r/singularity/comments/1p9r78s/the_story_of_elon_musk_and_deepmind_is/)
- [Google DeepMind vs. OpenAI](https://www.moravio.com/blog/google-deepmind-vs-openai-a-clash-of-titans)
- [对 DeepMind 健康数据事件的回应](https://link.springer.com/article/10.1007/s12553-018-0226-6)
- [关于 DeepMind 的新纪录片](https://www.reddit.com/r/BetterOffline/comments/1p79gsa/new_documentary_on_deepmind_the_thinking_game/)
- [DeepMind CEO 敦促对 AI 保持谨慎](https://time.com/6246119/demis-hassabis-deepmind-interview/)
- [DeepMind 的内部纷争](https://bdtechtalks.com/2019/08/26/deepmind-mustafa-suleyman-commercial-ai/)
- [性行为不端举报人](https://www.theverge.com/2022/4/4/23003311/deepmind-ai-sexual-misconduct-google-alphabet-fire-researcher-accused)
- [Google 让 DeepMind 高管休假](https://observer.com/2019/08/google-mustafa-suleyman-ai-deepmind-on-leave-health-controversy/)
- [Hacker News 上的 Google DeepMind](https://news.ycombinator.com/item?id=35643049)
- [DeepMind 联合创始人被调查](https://www.cnbc.com/2021/01/27/deepmind-co-founder-investigated-by-law-firm-after-staff-complaints-.html)
- [NHS 交易诉讼](https://www.cnbc.com/2021/10/01/google-deepmind-face-lawsuit-over-data-deal-with-britains-nhs.html)
- [DeepMind 的热度消退](https://www.cnbc.com/2020/06/05/google-deepmind-alphago-buzz-dissipates.html)
- [DeepMind IMO 银牌热点评论](https://x.com/anpaure/status/1816545995926462728)
- [LLM 代码问题](https://x.com/DeeperThrill/status/1995986039156924486)
- [AI 局限性吐槽](https://x.com/ChombaBupe/status/1887704781621243929)
- [DeepSeek 与 OpenAI 比较](https://x.com/stevehou/status/1884189182475514308)
- [Sridhar Vembu 谈 AI 偏见](https://x.com/svembu/status/1886737354708173174)
- [Aravind Srinivas 谈 Gemini](https://x.com/AravSrinivas/status/1732942104081694991)
