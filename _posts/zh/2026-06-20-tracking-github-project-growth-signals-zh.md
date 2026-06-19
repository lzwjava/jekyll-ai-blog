---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 追踪GitHub项目增长信号
translated: true
type: note
---

**问题：** 如何识别哪些 GitHub 项目正在长期增长——类似于 Google Trends 或 SimilarWeb，但针对 GitHub 仓库，例如追踪 2025 年 12 月 OpenClaw 或 Hermes 的采用情况？  
**回答：**

GitHub 趋势页面是一个糟糕的信号检测器——它没有记忆。你真正想要的是 **在任意历史窗口内的增长速度**——导数，而不是快照。以下是完整的工具集，从“直接使用”到“构建自己的信号”分层呈现：

---

## 第一层：已有此功能的工具

### 1. **star-history.com** —— 面向 Star 的 Google Trends  
Star History 以交互式折线图的形式展示任何仓库的 GitHub Star 增长情况。它不只显示静态的 Star 数量，而是揭示项目增长的快慢，这能告诉你更多关于真实势头和社区健康度的信息。一个拥有 50,000 Star 的项目可能已经废弃两年，而一个只有 8,000 Star 的新项目可能正在爆发式增长——增长曲线才是关键。

你可以像 Google Trends 一样进行多仓库对比：
```
https://star-history.com/#NousResearch/hermes-function-calling&opencog/opencog&Date
```

### 2. **OSSInsight** —— 最深度的免费数据集  
OSSInsight 分析超过 100 亿行的 GitHub 事件数据——包括 Star、Fork、贡献者增长、地理分布、公司构成、基于任意指标的并排比较。它拥有 AI 原生界面，你可以用自然语言查询 GitHub 数据，并获得基于 SQL 的可视化结果。

关键端点（免费，无需认证）：
```bash
# 仓库的 Star 历史
curl "https://api.ossinsight.io/v1/repos/{owner}/{repo}/stargazers/history"

# PR 创建者历史
curl "https://api.ossinsight.io/v1/repos/{owner}/{repo}/pull-request-creators/history"

# 趋势仓库（优于 GitHub 的趋势——包含历史时段）
curl "https://api.ossinsight.io/v1/trends/repos/?period=past_month&language=Python"
```

该 API 还暴露 Issue 创建者历史、PR 创建者历史、Star 用户的国家分布和组织构成——所有数据均可历史查询。

### 3. **Daily Stars Explorer** —— 每日粒度  
Daily Stars Explorer 使用 GitHub GraphQL API 追踪每日 Star 增量（而非累计值）。它克服了 star-history.com 的 40,000 Star 限制，并使用 FB Prophet 显示趋势线。它展示了诸如 spikes（产品发布、HN 帖子）与持续有机增长（如 Keycloak 长达十年的稳定曲线）等模式。

---

## 第二层：包下载信号（比 Star 更强）

Star 是虚名，下载量才是行为。对于 Python 和 JS 项目：

**PyPI 下载量**（实际使用代理）：
```bash
pip install pypistats
pypistats overall transformers --start-date 2024-12-01 --end-date 2025-01-31 --format json
```

或者直接调用 API：
```bash
curl "https://pypistats.org/api/packages/torch/overall?start=2024-12-01&end=2025-01-31"
```

**npm 下载量**（JS 包）：
```bash
curl "https://api.npmjs.org/downloads/range/2024-12-01:2025-01-31/langchain"
```

**pip-trends.com** 和 **npmtrends.com** —— 两者都提供类似 Google Trends 的界面，用于跨时间比较包。

---

## 第三层：构建你自己的信号（真正的 Alpha）

Star 可以被操纵且是滞后的。提交速度 + 贡献者增长 + Issue 解决率能告诉你更多信息。以下是一个提取增长向量的最小脚本：

```python
import requests
from datetime import datetime, timedelta
import json

GH_TOKEN = "<API_KEY>"  # 你的 GitHub PAT
HEADERS = {"Authorization": f"Bearer {GH_TOKEN}", "Accept": "application/vnd.github+json"}

def repo_growth_snapshot(owner: str, repo: str, since_days: int = 90):
    base = f"https://api.github.com/repos/{owner}/{repo}"

    # 基本统计
    r = requests.get(base, headers=HEADERS).json()
    stars = r["stargazers_count"]
    forks = r["forks_count"]
    open_issues = r["open_issues_count"]
    pushed_at = r["pushed_at"]

    # 时间窗口内的提交数
    since = (datetime.utcnow() - timedelta(days=since_days)).isoformat() + "Z"
    commits = requests.get(f"{base}/commits?since={since}&per_page=1", headers=HEADERS)
    # GitHub 在 Link 头部返回最后一页 = 总数
    link = commits.headers.get("Link", "")
    commit_count = 1
    if 'rel="last"' in link:
        last_url = [x.split(";")[0].strip("<>") for x in link.split(",") if 'rel="last"' in x][0]
        commit_count = int(last_url.split("page=")[-1])

    # 贡献者数量
    contributors = requests.get(f"{base}/contributors?per_page=1&anon=true", headers=HEADERS)
    contributor_link = contributors.headers.get("Link", "")
    contributor_count = 1
    if 'rel="last"' in contributor_link:
        last_url = [x.split(";")[0].strip("<>") for x in contributor_link.split(",") if 'rel="last"' in x][0]
        contributor_count = int(last_url.split("page=")[-1])

    return {
        "repo": f"{owner}/{repo}",
        "stars": stars,
        "forks": forks,
        "open_issues": open_issues,
        "commits_last_90d": commit_count,
        "contributors": contributor_count,
        "last_push": pushed_at,
        "fork_to_star_ratio": round(forks / max(stars, 1), 3),  # 高数值意味着开发者在实际使用它构建
    }

repos = [
    ("NousResearch", "hermes-function-calling"),
    ("vllm-project", "vllm"),
    ("ggerganov", "llama.cpp"),
]

for owner, repo in repos:
    snap = repo_growth_snapshot(owner, repo)
    print(json.dumps(snap, indent=2))
```

`fork_to_star_ratio` 是一个隐藏指标——高比例意味着工程师实际上在它之上进行构建，而不只是收藏。

---

## 第四层：超越 GitHub 的信号

针对“2025 年 12 月什么热门”的使用场景：

| 信号 | 来源 | 含义 |
|---|---|---|
| HN 提及 | `hn.algolia.com/api/v1/search?query=repo&dateRange=custom` | 开发者心智份额激增 |
| Reddit 提及 | Pushshift / Reddit API | 社区热度 |
| Twitter/X 速度 | 搜索 `github.com/owner/repo` + 日期筛选 | 病毒式传播时刻 |
| ArXiv 引用 | Semantic Scholar API | 研究领域的采用 |
| Docker 拉取 | `hub.docker.com/v2/repositories/{org}/{repo}` | 生产部署情况 |

---

## 总结：实际应该使用什么

对于回顾性分析（2025 年 12 月的 Hermes 等）：**OSSInsight API + star-history.com**

对于持续监控“爆发前夜”的项目：建立一个每周定时任务，为观察列表拉取提交速度 + Star 增量 + PyPI 下载量，存储到 SQLite 中，绘制导数图。这就是你专属的 GitHub Google Trends——而且没有其他人拥有你的特定观察列表。

真正的优势不在于工具，而在于**观察列表的筛选**——知道在哪些项目爆发前追踪哪 200 个仓库。这来自于阅读论文、关注 Karpathy/Andrej 等研究者的书签、留意 Hugging Face 模型发布，并与 OSSInsight 的 AI 框架排行榜交叉引用。

**参考资料：**

- [star-history.com](https://star-history.com)
- [OSSInsight](https://ossinsight.io)
- [OSSInsight 公共 API 文档](https://ossinsight.io/docs/api)
- [Daily Stars Explorer](https://dev.to/emanuelef/tool-to-get-daily-github-stars-history-1mik)
- [pip-trends.com](https://piptrends.com)
- [npmtrends.com](https://npmtrends.com)