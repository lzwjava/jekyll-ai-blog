---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cross-Team Information Graph Traversal
translated: false
type: note
---

**Question:** In enterprise environments, how do you effectively gather and connect information across Teams/company directories, GitHub, JIRA, and Confluence — especially when working on cross-team projects?

**Answer:**

This is fundamentally an **information graph traversal problem**. Enterprise knowledge is a DAG where nodes are people/tickets/docs/code and edges are implicit (mentioned in comments, linked pages, team memberships). The goal is to traverse it faster than everyone else.

---

## Mental Model First

```
Person (Staff ID)
  ├── owns → JIRA tickets
  ├── wrote → Confluence pages
  ├── commits to → GitHub repos
  ├── belongs to → Teams/AD groups
  └── referenced in → other people's tickets/pages
```

Your job cross-team is to **build this graph locally** as fast as possible.

---

## Layer 1: Identity Resolution (Staff ID as Root)

Every enterprise uses an **LDAP/Active Directory** identity that maps to everything else. In banks especially, the Staff ID is the canonical key.

```bash
# AD/LDAP lookup (if you have ldapsearch access)
ldapsearch -x -H ldap://your-corp-ldap -b "dc=bank,dc=com" \
  "(uid=zhiwei.li)" cn mail memberOf department manager

# Or via Python
pip install ldap3

from ldap3 import Server, Connection, ALL
s = Server('ldap://corp.bank.com', get_info=ALL)
c = Connection(s, 'CN=you,OU=Users,DC=bank,DC=com', 'password', auto_bind=True)
c.search('DC=bank,DC=com', '(sAMAccountName=lzw123)', attributes=['*'])
print(c.entries[0])
```

From Staff ID you can resolve: email, manager chain, team membership, AD groups (= repo/JIRA project access).

---

## Layer 2: Confluence — Structured Knowledge Mining

Confluence has a decent REST API. The trick is knowing that **Space → Pages → Labels → People** is the traversal path.

```python
import requests
from requests.auth import HTTPBasicAuth

BASE = "https://confluence.yourbank.com/rest/api"
AUTH = HTTPBasicAuth("you@bank.com", "your-api-token")

def search_confluence(query, limit=20):
    """CQL (Confluence Query Language) search"""
    r = requests.get(f"{BASE}/content/search", auth=AUTH, params={
        "cql": f'text ~ "{query}" AND type = page',
        "limit": limit,
        "expand": "metadata.labels,version,ancestors"
    })
    return r.json()["results"]

def get_page_by_staff_path(staff_id):
    """Directly hit staff profile pages"""
    r = requests.get(f"{BASE}/content/search", auth=AUTH, params={
        "cql": f'title = "{staff_id}" AND space.key = "STAFF"',
        "expand": "body.storage,version"
    })
    return r.json()

def get_space_tree(space_key):
    """Enumerate all pages in a space"""
    r = requests.get(f"{BASE}/space/{space_key}/content", auth=AUTH,
                     params={"expand": "page.children.page", "limit": 50})
    return r.json()

# Find who owns what by creator/lastModified
def find_pages_by_person(username):
    r = requests.get(f"{BASE}/content/search", auth=AUTH, params={
        "cql": f'creator = "{username}" ORDER BY created DESC',
        "limit": 50
    })
    return [(p["title"], p["_links"]["webui"]) for p in r.json()["results"]]
```

**CQL patterns that actually matter cross-team:**
```
# Find all pages referencing a ticket
text ~ "PROJ-1234"

# Find pages in a space updated in last 30 days
space.key = "ARCH" AND lastModified >= "2026-04-27"

# Find pages created by someone's team
creator in membersOf("team-payments") AND type = page

# Staff directory traversal
ancestor = "Staff Directory" AND title ~ "Platform"
```

---

## Layer 3: JIRA — Graph of Work

JIRA's JQL is powerful. Cross-team intelligence comes from traversing issue links, epics, and watchers.

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

# Cross-team: find all epics a person is involved in
issues = jql('assignee = "zhiwei.li" OR reporter = "zhiwei.li" OR watcher = "zhiwei.li"')

# Find who is touching the same component as you
issues = jql('component = "PaymentGateway" AND updated >= -30d ORDER BY updated DESC')

# Find all blockers across projects
issues = jql('issueType = "Story" AND "Epic Link" = "PLAT-100" AND project in (PLAT, RISK, DATA)')

# Traverse issue links programmatically
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

**JQL patterns for cross-team:**
```
# Everything touching your team's components in any project
component in ("Auth", "Gateway") AND project != MYTEAM

# Find people who reviewed/commented on related tickets
issue in watchedIssues("relevant.person@bank.com")

# Sprint cross-team view
sprint in openSprints() AND project in (PLAT, DATA, RISK, INFRA)

# Find all tickets a staff member ever touched
(assignee = "staff123" OR reporter = "staff123") ORDER BY updated DESC
```

---

## Layer 4: Enterprise GitHub

GitHub Enterprise has a great API. Key insight: **org teams map to AD groups**, which maps back to your LDAP graph.

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
    """Who outside your team commits here?"""
    r = requests.get(f"{GHE}/repos/{org}/{repo}/contributors", headers=HEADERS)
    return [(c["login"], c["contributions"]) for c in r.json()]

def code_search(org, query):
    """Find all usages of an API/class across org"""
    r = requests.get(f"{GHE}/search/code",
                     headers=HEADERS,
                     params={"q": f"org:{org} {query}"})
    return [(i["repository"]["name"], i["path"], i["html_url"]) for i in r.json()["items"]]
```

**The killer use case:** code_search across org to find who else calls your API, then cross-reference their GitHub logins to JIRA assignees to find the right people to talk to.

---

## Layer 5: Teams / MS Graph API

If the company uses Microsoft 365 (common in banks), MS Graph is your people graph.

```python
import requests

# Auth: get token via client_credentials or device_flow
TOKEN = "your_ms_graph_token"
GRAPH = "https://graph.microsoft.com/v1.0"
H = {"Authorization": f"Bearer {TOKEN}"}

def find_person(name_or_email):
    r = requests.get(f"{GRAPH}/users", headers=H,
                     params={"$filter": f"startswith(displayName,'{name_or_email}')",
                             "$select": "displayName,mail,jobTitle,department,manager"})
    return r.json()["value"]

def get_manager_chain(user_id, depth=3):
    """Walk up the org chart"""
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
    """All AD/Teams groups this person belongs to"""
    r = requests.post(f"{GRAPH}/users/{user_id}/getMemberGroups", headers=H,
                      json={"securityEnabledOnly": False})
    return r.json()["value"]  # group IDs → cross-ref with GitHub teams
```

---

## Layer 6: Build Your Own Cross-System Index

The real leverage is connecting these into a local index. Here's a minimal version:

```python
# enterprise_graph.py — local cross-system knowledge graph
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
    """BFS over edges to find related people"""
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

## Tactical Playbook for Cross-Team Work

| Goal | Command |
|------|---------|
| Who owns component X? | JQL: `component = X ORDER BY updated DESC` → look at assignees |
| Find the Confluence runbook | CQL: `text ~ "X" AND ancestor = "Runbooks"` |
| Who else uses my API? | GitHub code search: `org:bank "MyServiceClient"` |
| Who's the right person in team Y? | LDAP → AD group → GitHub team members → JIRA watchers |
| What did person X build? | Confluence: `creator = X`, GitHub: `/users/X/repos`, JIRA: `assignee = X` |
| Find undocumented dependencies | GitHub: cross-repo import search → cross-ref JIRA component owners |

---

## Automate It With a CLI Agent

Since you already build CLI agents (ww, iclaw, zz), wire this into one:

```bash
# Query person across all systems
ent-search person "zhiwei.li"
# → AD profile, GitHub repos, JIRA tickets, Confluence pages

# Find who to talk to about a topic
ent-search topic "payment gateway rate limiting"
# → Confluence pages + JIRA tickets + GitHub code + people involved

# Map a cross-team epic
ent-search epic PLAT-100
# → all linked tickets, all assignees, all Confluence pages mentioning it
```

This is genuinely the highest-leverage tool you can build at a bank — engineers who can navigate the information graph faster have outsized impact, especially in cross-team projects where context is the bottleneck, not code.