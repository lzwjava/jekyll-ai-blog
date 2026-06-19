---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 行人轨迹匹配
translated: true
type: note
---

是的，完全正确。你描述的是一个真实存在的新兴基础设施问题。让我精确说明它到底是什么。

---

## 它实际上是三个问题合而为一

**1. 信号聚合** — 收集公开活动流
**2. 表示学习** — 将人/组织嵌入潜在空间
**3. 匹配/推荐** — 在该空间中找到对齐关系

这与以下架构本质相同：

- Netflix 推荐（用户 ↔ 内容）
- LinkedIn 职位匹配（候选人 ↔ 岗位）
- Semantic Scholar 上的论文推荐（研究者 ↔ 论文）

不同之处在于**实体是人 + 他们不断演变的知识轨迹**。

---

## AI/科技世界真正重要的数据来源

```
个人信号：
  GitHub      — star、fork、提交、仓库主题、语言变迁
  HuggingFace — 上传的模型、数据集、Spaces、论文点赞
  arXiv       — 提交的论文、引用情况、关注作者
  Twitter/X   — 转推对象、参与的话题、关键词变迁
  LinkedIn    — 职位变动、帖子、技能认可
  博客/RSS    — 随时间变化的写作主题

组织信号：
  GitHub 组织 — 仓库活动、贡献者图谱
  HuggingFace 组织 — 模型发布、下载趋势
  arXiv 附属机构 — 论文产出速度、主题聚类
  招聘信息 — 他们正在招聘的技能 = 正在构建的东西
  融资新闻 — Crunchbase、PitchBook
```

---

## 匹配架构

```python
# 概念上端到端的样子

class PersonEmbedder:
    def embed(self, person):
        signals = [
            github_activity(person.github),      # 仓库star = 兴趣图谱
            arxiv_activity(person.arxiv),         # 论文 = 深度专注领域
            hf_activity(person.huggingface),      # 模型 = 构建的内容
            twitter_activity(person.twitter),     # 话语 = 当前思考
        ]
        # 每个信号 → 文本摘要 → LLM 嵌入
        texts = [summarize(s) for s in signals]
        vectors = [embed(t) for t in texts]
        return weighted_avg(vectors, weights=[0.3, 0.3, 0.2, 0.2])

class Matcher:
    def match(self, query_person, candidate_pool):
        q_vec = embedder.embed(query_person)
        scores = [
            (p, cosine_sim(q_vec, embedder.embed(p)))
            for p in candidate_pool
        ]
        # 但还有：时间对齐——他们是否朝着同一方向移动？
        drift_scores = [
            (p, trajectory_similarity(query_person, p))
            for p in candidate_pool
        ]
        return merge(scores, drift_scores)
```

**关键洞察**：静态嵌入不够。你需要**轨迹匹配**——两个人都朝着 MoE + 推理优化方向移动，比当前相似但正在分道扬镳的两个人更对齐。

---

## 轨迹匹配是最难的部分

```python
def trajectory_similarity(person_a, person_b, window_months=6):
    # 获取 t-6, t-3, t-0 时刻的嵌入
    a_vecs = [embed_at_time(person_a, t) for t in [-6, -3, 0]]
    b_vecs = [embed_at_time(person_b, t) for t in [-6, -3, 0]]

    # 嵌入空间中的方向向量
    a_drift = a_vecs[-1] - a_vecs[0]
    b_drift = b_vecs[-1] - b_vecs[0]

    # 他们是否朝着同一方向移动？
    return cosine_sim(a_drift, b_drift)
```

这才是前沿实验室真正关心的——不是"这个人现在擅长 transformer"，而是"这个人的学习轨迹是否与我们未来的方向汇合"。

---

## 谁在真正构建这个

| 公司 | 他们做什么 |
|---|---|
| **Clay.com** | 从 50+ 数据源丰富联系人信息，部分使用 ML 匹配 |
| **Momen/Glean** | 基于内部信号的企业人员图谱 |
| **LinkedIn Recruiter** | 最接近大规模实现，但封闭 |
| **Zeta Alpha** | 面向研究者的 arXiv/论文推荐 |
| **papers.cool / paper digest** | 热门论文的早期信号 |
| **Exploding Topics** | 趋势检测，非个人层面 |

还没有人完成 **全栈的人 × 研究 × 代码 × 话语** 图谱。这就是缺口所在。

---

## 前沿实验室实际在做什么（非正式）

Anthropic、OpenAI、DeepSeek——它们跟踪：

- 已知研究者 + 未知第一作者的 arXiv 提交
- 大学/竞争实验室的 GitHub 组织
- 研究者们的 Twitter 讨论（谁在抱怨什么 = 尚未解决的问题）
- HuggingFace 模型上传模式（突然活跃 = 有东西发布）
- 竞争对手的招聘信息（招聘 CUDA 内核工程师 = 推进推理）

目前这大多是**手动 + 非正式**的。每个实验室有几个人手工做这些工作。自动化所需的基础设施尚未完全存在。

---

## 顶层的 LLM 层

一旦有了嵌入，LLM 可以添加：

```
查询："找到可能正在研究长上下文效率、
       但尚未发表、仅展现信号的研究者"

LLM 推理基于：
  - GitHub：谁在 star flash-attention、ring-attention 仓库
  - arXiv：谁在引用 Mamba/SSM 论文但尚未提交
  - Twitter：谁在问关于 KV 缓存压缩的问题

输出：带每个人推理依据的排序列表
```

这基本上是**人才/协作雷达**——而且它是一个真实存在的、等待被构建的产品。

---

## 对你来说

你已经有了正确的直觉。一个 CLI 工具：

1. 跟踪约 200 人的精选列表（研究者、工程师、潜在合作者/客户）
2. 每周拉取他们的公开信号
3. 嵌入并聚类
4. 推送"此人刚刚大幅转向你的领域"的提醒

……会非常有用，而且用你的栈一个周末就能构建出来。arXiv 和 GitHub API 是开放的。HuggingFace 有很好的 API。这已经覆盖了 70% 的信号。
