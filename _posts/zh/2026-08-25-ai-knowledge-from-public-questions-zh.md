---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI来自公众问题的知识
translated: true
type: note
---

问题：一个**公开、开放的LLM聊天/搜索平台**——问题和答案默认公开，答案成为永久可搜索的页面，通过广告变现——是否是一个可行的产品？

回答：**是的。我认为这实际上是一个很强的想法，但关键是要把它视为“AI生成的公共知识”，而不是“免费的ChatGPT”。**

其有趣架构如下：

```text
                    ┌─────────────────────┐
用户提问 ────>       │       LLM           │
                    └──────────┬──────────┘
                               │
                     答案 + 引用
                               │
                               v
                    ┌─────────────────────┐
                    │   公开问题           │
                    │      + 答案         │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              v                v                v
         搜索索引          分类          推荐
              │                │                │
              └────────────────┼────────────────┘
                               v
                          Google流量
                               │
                            AdSense
```

### 真正重要的洞察

传统搜索是：

```text
问题 → 文档 → 用户阅读
```

LLM聊天是：

```text
问题 → 答案
```

你的系统会是：

```text
问题
   ↓
LLM答案
   ↓
永久公开文档
   ↓
被Google索引
   ↓
未来用户发现它
   ↓
相关问题
   ↓
更多流量
```

所以**每次推理都可能创建一个可复用的资产**。

这极大地改变了经济模型。

如果有人问：

> vLLM中的KV缓存是如何工作的？

你不仅仅花费0.01美元生成一个答案。

你创建了：

```text
/qa/how-does-kv-cache-work-in-vllm

标题：
How does KV cache work in vLLM?

答案：
...

相关：
- PagedAttention详解
- vLLM vs llama.cpp
- KV缓存内存计算
- KV缓存消耗多少VRAM？
```

现在，这个答案可能在未来获得**10,000次访问，而无需再进行任何LLM推理**。

这比普通的聊天机器人经济模型有趣得多。

---

## 我会让默认行为是公开的

类似于：

```text
┌────────────────────────────────────────────┐
│ 提问任何问题...                            │
│                                            │
│ KV缓存是如何工作的？                  [→] │
└────────────────────────────────────────────┘

这个问题和答案将是公开的。
```

然后：

```text
问题
   ↓
一次性生成
   ↓
永久保存
   ↓
任何人都可阅读
   ↓
任何人都可搜索
```

私密聊天成为明确的**退出选项**，而不是默认选项。

这样你就拥有了一个巨大的潜在知识图谱。

---

## 杀手级功能实际上不是LLM

我会围绕**公开问题**来构建产品。

例如：

```text
                  AI知识
                       │
       ┌───────────────┼───────────────┐
       ↓               ↓               ↓
     搜索           主题           问题
       │               │               │
       ↓               ↓               ↓
 "KV cache"         LLMs           15,238个问题
```

一个问题页面可能看起来像：

```text
vLLM中的KV缓存是如何工作的？

[AI答案]

来源：
- vLLM论文
- GitHub
- 文档

──────────────────────────────

相关问题

→ KV缓存占用多少内存？
→ 什么是PagedAttention？
→ vLLM为什么使用块表？
→ KV缓存与MQA有何不同？
→ llama.cpp如何实现KV缓存？
```

这开始看起来不像ChatGPT，而更像是：

**维基百科 + Google + Stack Overflow + LLM**。

---

# 还有一个更好的循环

用户不一定需要提出全新的问题。

系统可以自动生成问题。

例如：

```text
问题：
KV缓存是如何工作的？

答案
   ↓
LLM生成相关问题

├── KV缓存在GPU内存中如何存储？
├── 为什么KV缓存会随序列长度增长？
├── 什么是PagedAttention？
├── 前缀缓存是如何工作的？
├── KV缓存如何影响吞吐量？
└── vLLM如何管理碎片化的KV缓存？
```

然后：

```text
              一个问题
                    │
        ┌───────────┼───────────┐
        ↓           ↓           ↓
       Q1          Q2          Q3
        │           │           │
       Q4          Q5          Q6
        │           │           │
        └───────────┼───────────┘
                    ↓
              知识图谱
```

这就是它变得强大的地方。

---

# 而且你不需要实时回答每个问题

这可能是最重要的工程/经济优化。

假设：

```text
100,000用户
每个用户每月10个问题
= 1M个问题
```

天真的做法：

```text
1M个问题
→ 1M次LLM推理请求
```

成本高昂。

替代方案：

```text
问题
   ↓
标准化
   ↓
语义搜索
   ↓
已存在答案？
   ├── 是 → 返回缓存答案
   │
   └── 否 → 生成
              ↓
           存储答案
```

所以：

```python
def ask(question):
    q = normalize(question)

    answer = semantic_search(q)

    if answer.similarity > 0.95:
        return answer

    answer = llm.generate(q)
    db.save(q, answer)

    return answer
```

最终比例变为类似：

```text
100个问题
        │
        ├── 70 → 已有答案
        │
        ├── 20 → 从已有答案合成
        │
        └── 10 → 昂贵的LLM生成
```

这是一个**完全不同的成本结构**。

---

# 静态页面极具价值

我实际上会将每个答案渲染为普通的HTML页面。

不是：

```text
/api/chat
```

而是：

```text
/q/how-does-kv-cache-work
```

带有：

```html
<h1>KV缓存是如何工作的？</h1>

<article>
    ...
</article>

<nav>
    相关问题...
</nav>
```

然后：

```text
Google
   ↓
公开HTML
   ↓
答案
   ↓
相关问题
   ↓
另一个答案
```

你实际上是在构建一个**AI生成的SEO语料库**。

但有一个重要警告：Google越来越关注有用/原创的内容，而不是简单地大规模生成的页面。因此，盲目生成数百万个内容单薄的AI页面可能是一个糟糕的SEO策略。

这些页面需要具备：

* 有用的答案
* 引用来源
* 稳定的URL
* 良好的内部链接
* 去重
* 修正/编辑历史
* 强大的主题结构
* 最好有用户贡献

---

# 收入

你的AdSense想法对免费/公开层是有意义的。

可能的漏斗：

```text
Google
   ↓
免费公开答案
   ↓
广告
   ↓
$收入
```

但我之后会添加多个收入来源：

```text
                     公开AI
                         │
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
     广告             API            高级版
        │                │                │
    AdSense        开发者            私密聊天
                                     无广告
                                     更好的模型
```

可能的情况：

### 免费

```text
无限问题
默认公开
缓存答案
广告
```

### 高级版

```text
私密对话
无广告
更好的模型
文件上传
长上下文
```

### API

```text
GET /search?q=...
GET /answer?id=...
```

有趣的是，**你的公开语料库本身也会变得有价值**。

---

# 我还会添加投票/修正功能

这是你可以超越纯AI生成网站的地方。

```text
答案

👍 1,284
👎 31

这个答案有用吗？

[修正] [添加来源] [讨论]
```

然后最终：

```text
LLM答案
    +
人工反馈
    +
来源
    +
版本历史
```

你会得到一个更接近活的知识库的东西。

Stack Overflow是：

```text
人类 → 答案 → 投票
```

你可以有：

```text
LLM → 答案 → 人类 → 投票/修正 → 更好的答案
```

---

# 一个危险：垃圾内容爆炸

这是最大的问题。

想象一下：

```text
“什么是比特币？”

“比特币到底是什么？”

“比特币解释”

“给我解释一下比特币”

“比特币含义”

“比特币如何运作？”
```

你不希望有六个独立的页面。

你需要：

```text
语义聚类
        ↓
规范问题
        ↓
别名
```

例如：

```text
规范问题：

比特币如何运作？

别名：

- 什么是比特币？
- 解释比特币
- 比特币解释
- 比特币实际上如何运作？
```

然后一个规范的答案。

这本质上是一个**基于LLM的去重/索引问题**。

而这对你来说是一个非常可解的工程问题。

---

# 我会把MVP构建得非常小

你可能可以用以下内容来原型化：

```text
Next.js
Postgres
pgvector
一个LLM API
Cloudflare
Google Search Console
AdSense
```

Schema：

```sql
CREATE TABLE questions (
    id          BIGSERIAL PRIMARY KEY,
    slug        TEXT UNIQUE,
    question    TEXT NOT NULL,
    answer      TEXT NOT NULL,
    embedding   VECTOR(1536),
    created_at  TIMESTAMP DEFAULT now()
);

CREATE INDEX questions_embedding_idx
ON questions
USING hnsw (embedding vector_cosine_ops);
```

请求：

```python
q = embed(user_question)

existing = db.semantic_search(q, limit=5)

if existing[0].score > 0.94:
    return existing[0]

answer = llm(user_question)

db.insert(
    question=user_question,
    answer=answer,
    embedding=q,
)

return answer
```

然后生成：

```text
/sitemap.xml
/robots.txt
/q/...
/topic/...
/search?q=...
```

这基本上就是第一个版本。

---

# 战略性问题

我不会将其定位为：

> **免费ChatGPT**

因为你无法赢得那场战斗。

我会从概念上将其定位为：

> **互联网的公共AI知识库。**

区别在于：

```text
ChatGPT
    ↓
对话

你的产品
    ↓
知识
```

而基础资产变成了：

```text
                数百万个问题
                         ↓
                数百万个答案
                         ↓
                语义图谱
                         ↓
            可搜索的AI知识
```

这比另一个聊天界面更具防御性。

**我认为这值得原型化。** MVP可以极其便宜：一个公开问题页面、缓存答案、语义去重、搜索、相关问题和广告。有趣的实验不是人们是否喜欢与之聊天——那已经得到验证。实验在于**公开的LLM答案能否以比推理+审核+托管成本增长更快的速度积累为自然搜索流量。**