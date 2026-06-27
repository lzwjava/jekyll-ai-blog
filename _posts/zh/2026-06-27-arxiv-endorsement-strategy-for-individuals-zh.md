---
audio: false
generated: true
image: false
lang: zh
layout: post
title: arXiv个人认可策略
translated: true
type: note
---

**问题：** 我需要一个 arXiv 的认可才能提交到 cs.AI。谁可以给我认可？获得认可的实际路径是什么？

**回答：**

先讲机制，再讲针对你具体情况（无学术机构背景、自学、公开构建）的现实策略。

## 硬性约束

认可者必须满足：
- 已在某个符合条件的 cs.* 类别（包括 cs.AI、cs.LG、cs.CL、cs.SE 等长列表）中提交过 **3 篇以上** 论文
- 这些论文的提交时间需在 **3 个月以上、5 年以内**（一个特定的时效窗口——2015 年的高产作者如果沉寂了就不符合条件）
- 作为 arXiv 提交者，信誉良好

你将邮箱中收到的唯一代码转发给他们；他们输入即可。他们是在担保你的论文看起来适合该类别——而不是进行同行评审。这是一个低门槛的信任，但需要一个符合资格的真人。

## 如何找到符合条件的认可者（AI 原生方法）

别瞎猜。arXiv 直接暴露了认可资格。根据说明中的验证技巧：在任何摘要页面上，**“本文作者中谁可以给予认可？”** 链接会明确告诉你哪些作者符合条件。因此工作流程是：

1. 找到与你提交主题密切相关的近期（过去 1-3 年）cs.AI/cs.LG 论文。
2. 点击认可链接，确认哪位作者符合条件。
3. 联系该特定作者。

你可以自动化发现过程。arXiv 有一个简洁的 API：

```bash
# 查找与你主题关键词匹配的近期 cs.AI 论文
curl -s "http://export.arxiv.org/api/query?search_query=cat:cs.AI+AND+all:nanoGPT&sortBy=submittedDate&sortOrder=descending&max_results=20" \
  | grep -E '<id>|<title>|<name>|<published>'
```

或者用 Python 提取作者 + 日期，并筛选到资格窗口：

```python
import urllib.request, feedparser, datetime as dt

def find_endorsers(query, want=30):
    url = ("http://export.arxiv.org/api/query?"
           f"search_query={query}&sortBy=submittedDate"
           f"&sortOrder=descending&max_results={want}")
    feed = feedparser.parse(urllib.request.urlopen(url).read())
    now = dt.datetime.now(dt.timezone.utc)
    for e in feed.entries:
        pub = dt.datetime(*e.published_parsed[:6], tzinfo=dt.timezone.utc)
        age_days = (now - pub).days
        # 认可者需要一篇 >3个月且 <5年的论文；近期活跃作者是最佳选择
        flag = "active" if 90 < age_days < 1825 else ""
        authors = ", ".join(a.name for a in e.authors)
        print(f"{pub.date()} [{flag}] {e.title.strip()[:60]}")
        print(f"    {authors}")

find_endorsers("cat:cs.AI+AND+all:large+language+model")
```

API 提供的作者列表给出候选人；每篇论文的认可链接确认资格（API 不直接暴露认可状态，因此最后一步需要手动检查）。

## 针对 *你* 的现实策略

说明中暗示了社会现实：“找一个与你有联系的认可者。”你没有论文导师。因此你的杠杆是 **你的公开工作**，这实际上相当可观——8000 条笔记、400 篇帖子、真实的模型训练经验。用它：

1. **选择合适的类别。** cs.AI 听起来容易但实际更难获得认可，因为它范围广，且版主会积极重新分类。如果你的论文涉及训练/架构，**cs.LG** 通常更合适，并且拥有更大规模的近期活跃认可者池。如果是 NLP/LLM 特定，**cs.CL**。将类别与你潜在认可者实际发表的领域匹配。

2. **与已经符合条件的人合著。** 这是最干净的路径，也是大多数人忽略的。如果你与任何有 arXiv 记录的人合作——即使只是松散合作——他们可以轻松给予认可，且联系是真实的。考虑到你的社交圈（前创业公司、银行 AI 团队、开源贡献者），可能已经有人与你相隔一度。

3. **尊重对方时间的冷接触。** 作者们会被大量的认可请求淹没。有效的是：简短、具体、表明你读过他们的工作，附上你的论文草稿和公开记录，以证明你不是一个怪人。例如——“我正在提交一篇关于[主题]的论文，标题为[标题]，与您的那篇[论文]密切相关。我是一名独立研究者（无机构关联）；这里是草稿和我的工作（lzwjava.github.io）。您是否愿意考虑为 cs.LG 予以认可？”附上草稿。草稿的质量会替你说服对方。

4. **arXiv 自己的逃生口。** 如果你确实找不到认可者，可以向 arXiv 版主发送邮件，说明你的情况并附上论文链接。他们有时会直接审核。这很慢且不能保证成功，但确实存在。

一个值得内化的诚实提醒：认可必要但不充分。版主会拒绝/重新分类看起来不够学术的独立提交。因此，你为获得认可所付出的同样努力——一份紧凑、结构良好且有实际结果的论文——也正是通过审核的关键。草稿是瓶颈，而不是认可。

**参考资料：**

- [arXiv 认可帮助](https://arxiv.org/help/endorsement)
- [arXiv 版主政策](https://arxiv.org/help/moderation)
- [arXiv API 用户手册](https://info.arxiv.org/help/api/user-manual.html)