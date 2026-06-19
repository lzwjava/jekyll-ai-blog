---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tracking GitHub Project Growth Signals
translated: false
type: note
---

**Question:** How to identify which GitHub projects are growing long-term — like Google Trends or SimilarWeb, but for GitHub repos — e.g. tracking OpenClaw or Hermes adoption back in December 2025?**Answer:**

The GitHub Trending page is a terrible signal detector — it's memoryless. What you actually want is **growth velocity over arbitrary historical windows** — the derivative, not the snapshot. Here's the full toolkit, layered from "just use it now" to "build your own signal":

---

## Tier 1: Tools That Already Do This

### 1. **star-history.com** — The Google Trends for Stars

Star History charts GitHub star growth for any repo as an interactive line chart. Instead of showing just a static star count, it reveals how fast a project is growing, which tells you far more about real momentum and community health. A project with 50,000 stars might have been abandoned for two years, while a newer one with 8,000 stars might be exploding in adoption right now — the growth curve is what matters.

You can do multi-repo comparison like Google Trends:

```
https://star-history.com/#NousResearch/hermes-function-calling&opencog/opencog&Date
```

### 2. **OSSInsight** — The Deepest Free Dataset

OSSInsight analyzes 10+ billion rows of GitHub event data — stars, forks, contributor growth, geographic distribution, company breakdown, side-by-side comparisons on any metric. It has an AI-native interface where you can query GitHub data in natural language and get SQL-backed visualizations.

Key endpoints (free, no auth):

```bash
# Stargazer history for a repo
curl "https://api.ossinsight.io/v1/repos/{owner}/{repo}/stargazers/history"

# PR creator history
curl "https://api.ossinsight.io/v1/repos/{owner}/{repo}/pull-request-creators/history"

# Trending repos (better than GitHub's — includes historical periods)
curl "https://api.ossinsight.io/v1/trends/repos/?period=past_month&language=Python"
```

The API also exposes issue creator history, PR creator history, stargazer country distribution, and organization breakdown — all queryable historically.

### 3. **Daily Stars Explorer** — Daily Granularity

Daily Stars Explorer tracks the daily delta (not cumulative) in stars using the GitHub GraphQL API. It overcomes the 40K star limit that star-history.com hits, and uses FB Prophet to show trend lines. It shows patterns like spikes (product launches, HN posts) vs. constant organic growth like Keycloak's decade-long steady curve.

---

## Tier 2: Package Download Signals (Stronger Than Stars)

Stars are vanity; downloads are behavior. For Python and JS projects:

**PyPI downloads** (actual usage proxy):

```bash
pip install pypistats
pypistats overall transformers --start-date 2024-12-01 --end-date 2025-01-31 --format json
```

Or hit the API directly:

```bash
curl "https://pypistats.org/api/packages/torch/overall?start=2024-12-01&end=2025-01-31"
```

**npm downloads** (JS packages):

```bash
curl "https://api.npmjs.org/downloads/range/2024-12-01:2025-01-31/langchain"
```

**pip-trends.com** and **npmtrends.com** — both have Google Trends-style UI for comparing packages over time.

---

## Tier 3: Build Your Own Signal (The Real Alpha)

Stars are gameable and lagging. Commit velocity + contributor growth + issue resolution rate tells you more. Here's a minimal script to pull growth vectors:

```python
import requests
from datetime import datetime, timedelta
import json

GH_TOKEN = "<API_KEY>"  # your GitHub PAT
HEADERS = {"Authorization": f"Bearer {GH_TOKEN}", "Accept": "application/vnd.github+json"}

def repo_growth_snapshot(owner: str, repo: str, since_days: int = 90):
    base = f"https://api.github.com/repos/{owner}/{repo}"

    # Basic stats
    r = requests.get(base, headers=HEADERS).json()
    stars = r["stargazers_count"]
    forks = r["forks_count"]
    open_issues = r["open_issues_count"]
    pushed_at = r["pushed_at"]

    # Commit count in window
    since = (datetime.utcnow() - timedelta(days=since_days)).isoformat() + "Z"
    commits = requests.get(f"{base}/commits?since={since}&per_page=1", headers=HEADERS)
    # GitHub returns Link header with last page = total count
    link = commits.headers.get("Link", "")
    commit_count = 1
    if 'rel="last"' in link:
        last_url = [x.split(";")[0].strip("<>") for x in link.split(",") if 'rel="last"' in x][0]
        commit_count = int(last_url.split("page=")[-1])

    # Contributor count
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
        "fork_to_star_ratio": round(forks / max(stars, 1), 3),  # high = builders using it
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

The `fork_to_star_ratio` is a sleeper metric — high ratio means engineers are actually building on it, not just bookmarking.

---

## Tier 4: Signals That Go Beyond GitHub

For the "what was hot in Dec 2025" use case:

| Signal | Source | What It Tells You |
|---|---|---|
| HN mentions | `hn.algolia.com/api/v1/search?query=repo&dateRange=custom` | Dev mindshare spikes |
| Reddit mentions | Pushshift / Reddit API | Community buzz |
| Twitter/X velocity | Search `github.com/owner/repo` + date filter | Viral moments |
| ArXiv citations | Semantic Scholar API | Research adoption |
| Docker pulls | `hub.docker.com/v2/repositories/{org}/{repo}` | Production deployments |

---

## Summary: What to Actually Use

For retrospective analysis (Dec 2025 Hermes etc): **OSSInsight API + star-history.com**

For ongoing monitoring of "pre-breakout" projects: build a weekly cron that pulls commit velocity + star delta + PyPI downloads for a watchlist, store in SQLite, plot the derivatives. That's your Google Trends for GitHub — and nobody else has your specific watchlist.

The real edge isn't the tool, it's the **watchlist curation** — knowing which 200 repos to track before they blow up. That comes from reading papers, following researchers like Karpathy/Andrej's bookmarks, watching Hugging Face model releases, and cross-referencing with OSSInsight's AI framework leaderboards.

**References:**

- [star-history.com](https://star-history.com)
- [OSSInsight](https://ossinsight.io)
- [OSSInsight Public API docs](https://ossinsight.io/docs/api)
- [Daily Stars Explorer](https://dev.to/emanuelef/tool-to-get-daily-github-stars-history-1mik)
- [pip-trends.com](https://piptrends.com)
- [npmtrends.com](https://npmtrends.com)
