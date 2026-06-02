---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 跨团队信息图遍历
translated: true
type: note
---

**问题：** 在企业环境中，特别是在跨团队项目协作时，如何有效收集并关联 Teams/公司目录、GitHub、JIRA 和 Confluence 中的信息？

**回答：**

这本质上是一个**信息图谱遍历问题**。企业知识是一个有向无环图（DAG），节点是人/工单/文档/代码，边是隐式的（在评论中被提及、页面链接、团队成员关系）。目标是比其他人更快地遍历这个图。

---

## 先建立思维模型

```
人员（员工 ID）
  ├── 拥有 → JIRA 工单
  ├── 编写 → Confluence 页面
  ├── 提交 → GitHub 仓库
  ├── 属于 → Teams/AD 组
  └── 被引用 → 其他人的工单/页面
```

在跨团队工作中，你的任务是**尽快在本地构建这个图**。

---

## 第一层：身份解析（以员工 ID 为根）

每个企业都使用一个 **LDAP/Active Directory** 身份，该身份映射到所有其他系统。尤其是在银行，员工 ID 是规范主键。

```bash
# AD/LDAP 查询（如果你有 ldapsearch 权限）
ldapsearch -x -H ldap://your-corp-ldap -b "dc=bank,dc=com" \
  "(uid=zhiwei.li)" cn mail memberOf department manager

# 或者通过 Python
pip install ldap3

from ldap3 import Server, Connection, ALL
s = Server('ldap://corp.bank.com', get_info=ALL)
c = Connection(s, 'CN=you,OU=Users,DC=bank,DC=com', 'password', auto_bind=True)
c.search('DC=bank,DC=com', '(sAMAccountName=lzw123)', attributes=['*'])
print(c.entries[0])
```

从员工 ID 可以解析出：邮箱、汇报链、团队归属、AD 组（= 仓库/JIRA 项目访问权限）。

---

## 第二层：Confluence — 结构化知识挖掘

Confluence 有一个不错的 REST API。关键在于知道 **空间 → 页面 → 标签 → 人员** 是遍历路径。

```python
import requests
from requests.auth import HTTPBasicAuth

BASE = "https://confluence.yourbank.com/rest/api"
AUTH = HTTPBasicAuth("you@bank.com", "your-api-token")

def search_confluence(query, limit=20):
    """CQL（Confluence 查询语言）搜索"""
    r = requests.get(f"{BASE}/content/search", auth=AUTH, params={
        "cql": f'text ~ "{query}" AND type = page',
        "limit": limit,
        "expand": "metadata.labels,version,ancestors"
    })
    return r.json()["results"]

def get_page_by_staff_path(staff_id):
    """直接定位员工简介页面"""
    r = requests.get(f"{BASE}/content/search", auth=AUTH, params={
        "cql": f'title = "{staff_id}" AND space.key = "STAFF"',
        "expand": "body.storage,version"
    })
    return r.json()

def get_space_tree(space_key):
    """枚举空间中的所有页面"""
    r = requests.get(f"{BASE}/space/{space_key}/content", auth=AUTH,
                     params={"expand": "page.children.page", "limit": 50})
    return r.json()

# 通过创建者/最后修改者查找谁拥有什么
def find_pages_by_person(username):
    r = requests.get(f"{BASE}/content/search", auth=AUTH, params={
        "cql": f'creator = "{username}" ORDER BY created DESC',
        "limit": 50
    })
    return [(p["title"], p["_links"]["webui"]) for p in r.json()["results"]]
```

**跨团队工作中实际有用的 CQL 模式：**

```
# 查找所有引用某个工单的页面
text ~ "PROJ-1234"

# 查找最近 30 天更新过的空间中的页面
space.key = "ARCH" AND lastModified >= "2026-04-27"

# 查找某个团队创建的页面
creator in membersOf("team-payments") AND type = page

# 员工目录遍历
ancestor = "Staff Directory" AND title ~ "Platform"
```

---

## 第三层：JIRA — 工作图谱

JIRA 的 JQL 功能强大。跨团队情报来自于遍历工单链接、史诗和关注者。

```python
import requests

JIRA_BASE = "https://jira.yourbank.com/rest/api/2"
AUTH = HTTPBasicAuth("you@bank.com", "token")

def jql(query, fields="summary,assignee,reporter,status,labels,issuelinks,comment"):
    r = requests.get(f"{JIRA_BASE}/search", auth=AUTH, params={
        "jql": query,
        "fields": fields,
        "maxResults": 100
    })
    return r.json()["issues"]

# 跨团队：查找某人参与的所有史诗
issues = jql('assignee = "zhiwei.li" OR reporter = "zhiwei.li" OR watcher = "zhiwei.li"')

# 查找谁和你操作同一个组件
issues = jql('component = "PaymentGateway" AND updated >= -30d ORDER BY updated DESC')

# 查找跨项目的所有阻塞项
issues = jql('issueType = "Story" AND "Epic Link" = "PLAT-100" AND project in (PLAT, RISK, DATA)')

# 以编程方式遍历工单链接
def get_linked_issues(issue_key):
    r = requests.get(f"{JIRA_BASE}/issue/{issue_key}", auth=AUTH,
                     params={"fields": "issuelinks,subtasks,parent"})
    data = r.json()["fields"]
    links = []
    for link in data.get("issuelinks", []):
        linked = link.get("inwardIssue") or link.get("outwardIssue")
        if linked:
            links.append((link.get("type", {}).get("name"), linked["key"], linked["fields"]["summary"]))
    return links
```

**跨团队的 JQL 模式：**

```
# 任何项目中与你团队组件相关的所有内容
component in ("Auth", "Gateway") AND project != MYTEAM

# 查找审阅或评论过相关工单的人
issue in watchedIssues("relevant.person@bank.com")

# 跨团队冲刺视图
sprint in openSprints() AND project in (PLAT, DATA, RISK, INFRA)

# 查找某员工曾经操作过的所有工单
(assignee = "staff123" OR reporter = "staff123") ORDER BY updated DESC
```

---

## 第四层：企业版 GitHub

GitHub Enterprise 有很棒的 API。关键洞察：**组织团队映射到 AD 组**，而 AD 组又映射回你的 LDAP 图。

```python
import requests

GHE = "https://github.yourbank.com/api/v3"
HEADERS = {"Authorization": "token ghp_yourtoken", "Accept": "application/vnd.github.v3+json"}

def get_org_teams(org):
    r = requests.get(f"{GHE}/orgs/{org}/teams", headers=HEADERS)
    return [(t["name"], t["slug"]) for t in r.json()]

def get_team_members(org, team_slug):
    r = requests.get(f"{GHE}/orgs/{org}/teams/{team_slug}/members", headers=HEADERS)
    return [m["login"] for m in r.json()]

def find_repos_by_topic(org, topic):
    r = requests.get(f"{GHE}/search/repositories",
                     headers=HEADERS,
                     params={"q": f"org:{org} topic:{topic}"})
    return [(repo["name"], repo["html_url"]) for repo in r.json()["items"]]

def get_cross_team_contributors(org, repo):
    """谁在你团队之外向此仓库提交代码？"""
    r = requests.get(f"{GHE}/repos/{org}/{repo}/contributors", headers=HEADERS)
    return [(c["login"], c["contributions"]) for c in r.json()]

def code_search(org, query):
    """在组织范围内查找某个 API/类的所有使用"""
    r = requests.get(f"{GHE}/search/code",
                     headers=HEADERS,
                     params={"q": f"org:{org} {query}"})
    return [(i["repository"]["name"], i["path"], i["html_url"]) for i in r.json()["items"]]
```

**杀手级用例：** 在组织范围内进行 code_search，找出谁还调用了你的 API，然后交叉引用他们的 GitHub 登录名和 JIRA 经办人，找到需要沟通的正确人员。

---

## 第五层：Teams / Microsoft Graph API

如果公司使用 Microsoft 365（银行中很常见），MS Graph 就是你的人员图谱。

```python
import requests

# 认证：通过 client_credentials 或 device_flow 获取 token
TOKEN = "your_ms_graph_token"
GRAPH = "https://graph.microsoft.com/v1.0"
H = {"Authorization": f"Bearer {TOKEN}"}

def find_person(name_or_email):
    r = requests.get(f"{GRAPH}/users", headers=H,
                     params={"$filter": f"startswith(displayName,'{name_or_email}')",
                             "$select": "displayName,mail,jobTitle,department,manager"})
    return r.json()["value"]

def get_manager_chain(user_id, depth=3):
    """向上遍历组织架构"""
    chain = []
    current = user_id
    for _ in range(depth):
        r = requests.get(f"{GRAPH}/users/{current}/manager", headers=H,
                         params={"$select": "displayName,mail,id"})
        if r.status_code != 200:
            break
        mgr = r.json()
        chain.append(mgr["displayName"])
        current = mgr["id"]
    return chain

def get_team_channels(team_id):
    r = requests.get(f"{GRAPH}/teams/{team_id}/channels", headers=H)
    return [(c["displayName"], c["id"]) for c in r.json()["value"]]

def get_person_groups(user_id):
    """此人所属的所有 AD/Teams 组"""
    r = requests.post(f"{GRAPH}/users/{user_id}/getMemberGroups", headers=H,
                      json={"securityEnabledOnly": False})
    return r.json()["value"]  # 组 ID → 与 GitHub 团队交叉引用
```

---

## 第六层：构建你自己的跨系统索引

真正的杠杆在于将这些连接成一个本地索引。下面是一个最小化版本：

```python
# enterprise_graph.py — 本地跨系统知识图谱
import json, sqlite3

conn = sqlite3.connect("enterprise.db")
conn.executescript("""
CREATE TABLE IF NOT EXISTS people (
    staff_id TEXT PRIMARY KEY,
    email TEXT, display_name TEXT,
    github_login TEXT, jira_username TEXT,
    team TEXT, manager_chain TEXT
);
CREATE TABLE IF NOT EXISTS artifacts (
    id TEXT PRIMARY KEY,
    type TEXT,  -- 'confluence_page' | 'jira_ticket' | 'github_repo'
    title TEXT, url TEXT, owner_staff_id TEXT,
    tags TEXT, updated TEXT
);
CREATE TABLE IF NOT EXISTS edges (
    from_id TEXT, to_id TEXT, relation TEXT
    -- 'mentions' | 'assigned_to' | 'blocks' | 'contributes_to'
);
""")

def ingest_person(staff_id, email, github, jira, team, manager_chain):
    conn.execute("""INSERT OR REPLACE INTO people VALUES (?,?,?,?,?,?,?)""",
                 (staff_id, email, None, github, jira, team, json.dumps(manager_chain)))
    conn.commit()

def find_person_artifacts(staff_id):
    return conn.execute("""
        SELECT type, title, url FROM artifacts WHERE owner_staff_id = ?
    """, (staff_id,)).fetchall()

def find_connected_people(staff_id, hops=2):
    """通过边进行广度优先搜索，寻找相关人员"""
    visited = {staff_id}
    frontier = [staff_id]
    for _ in range(hops):
        next_frontier = []
        for node in frontier:
            neighbors = conn.execute("""
                SELECT DISTINCT to_id FROM edges WHERE from_id = ?
                UNION SELECT DISTINCT from_id FROM edges WHERE to_id = ?
            """, (node, node)).fetchall()
            for (n,) in neighbors:
                if n not in visited:
                    visited.add(n)
                    next_frontier.append(n)
        frontier = next_frontier
    return visited - {staff_id}
```

---

## 跨团队工作的战术手册

| 目标 | 命令 |
|------|---------|
| 谁拥有组件 X？ | JQL: `component = X ORDER BY updated DESC` → 查看经办人 |
| 查找 Confluence 运行手册 | CQL: `text ~ "X" AND ancestor = "Runbooks"` |
| 还有谁在使用我的 API？ | GitHub 代码搜索: `org:bank "MyServiceClient"` |
| 团队 Y 中的正确联系人是谁？ | LDAP → AD 组 → GitHub 团队成员 → JIRA 关注者 |
| 某人 X 构建了什么？ | Confluence: `creator = X`, GitHub: `/users/X/repos`, JIRA: `assignee = X` |
| 查找未文档化的依赖 | GitHub: 跨仓库 import 搜索 → 交叉引用 JIRA 组件负责人 |

---

## 用 CLI 代理实现自动化

既然你已经构建了 CLI 代理（ww, iclaw, zz），可以把这些功能集成进去：

```bash
# 跨所有系统查询人员
ent-search person "zhiwei.li"
# → AD 档案、GitHub 仓库、JIRA 工单、Confluence 页面

# 查找某个主题的负责人
ent-search topic "payment gateway rate limiting"
# → Confluence 页面 + JIRA 工单 + GitHub 代码 + 相关人员

# 映射跨团队史诗
ent-search epic PLAT-100
# → 所有关联工单、所有经办人、所有提及它的 Confluence 页面
```

这确实是在银行中你能构建的最高杠杆工具——能够更快地导航信息图谱的工程师会发挥出超比例的影响力，尤其是在跨团队项目中，上下文才是瓶颈，而不是代码。
