---
audio: false
generated: true
image: false
lang: en
layout: post
title: A Red Teamer’s OSINT Company Recon Guide
translated: false
type: note
---

**Question:** What counts as "public information" about a company, and how can you systematically use it — plus hacker/OSINT techniques — to deeply research a company's products, technology stack, and infrastructure before joining, augmented by an AI agent?

**Answer:**

This is OSINT (Open Source Intelligence) applied to corporate due diligence. The mental model: you're a red-teamer doing recon, not a job applicant skimming Glassdoor.

---

## The Public Information Surface

### 1. People Layer

- **LinkedIn / 脉脉 / GitHub profiles** — engineers reveal stack (their repos, starred projects, blog posts)
- **Conference talks / papers** — engineers at SDCC, QCon, InfoQ talks name internal systems by accident
- **Job postings** — the most underrated signal. "Experience with Flink, Kafka, ClickHouse, K8s on AWS" = their exact stack
- **Patent filings** — reveal proprietary algorithms and architectural approaches

### 2. Product / Frontend Layer

- **HTTP traffic analysis** — Charles Proxy / mitmproxy / Wireshark on their app
  - API endpoints, versioning (`/v3/`, `/api/internal/`)
  - Auth schemes (JWT structure, OAuth flows)
  - Third-party SDKs embedded (Sentry, DataDog, Amplitude = their observability stack)
  - CDN headers (`X-Served-By`, `CF-Ray`, `X-Cache`)
- **JS bundle analysis** — `source-map-explorer`, unminified bundles leak framework choices, feature flags, even internal route names
- **Mobile APK/IPA** — `apktool` decompile → smali/Java → internal package names, endpoints, sometimes hardcoded staging URLs
- **Browser DevTools Network tab** — obvious but powerful

### 3. Infrastructure Layer

- **DNS enumeration**

  ```bash
  # Subdomain brute-force
  subfinder -d target.com | httpx -title -tech-detect
  amass enum -d target.com

  # Certificate transparency logs (no active scanning needed)
  curl "https://crt.sh/?q=%.target.com&output=json" | jq '.[].name_value' | sort -u
  ```

- **IP ranges / ASN**

  ```bash
  # Find their ASN
  whois -h whois.radb.net -- '-i origin AS12345'
  # Or via bgp.he.net
  curl https://bgp.he.net/dns/target.com
  ```

- **Shodan / Censys / FOFA** — scan their IP ranges for exposed services

  ```
  org:"TargetCompany Inc" port:6379  # Redis exposed?
  ssl:"target.com" http.title:"Grafana"  # Monitoring dashboard?
  ```

- **Cloud provider hints**
  - S3 bucket naming: `target-prod-logs.s3.amazonaws.com`
  - GCP: `storage.googleapis.com/target-*`
  - **CloudFlare, Fastly headers** leak origin IPs sometimes

### 4. Code / Artifact Layer

- **GitHub** — search `org:targetcompany` but also `"target.com" internal` in public repos, gists, commit messages

  ```bash
  # GitHub dork
  site:github.com "target.com" "internal" "staging"
  # truffleHog / gitleaks on their public repos
  trufflehog github --org=targetcompany
  ```

- **npm / PyPI / Maven** — published packages reveal internal naming conventions, dependencies
- **Docker Hub** — public images sometimes have layers with credentials baked in

  ```bash
  docker pull target/someimage
  docker history target/someimage --no-trunc
  ```

- **Wayback Machine** — old JS bundles, old API docs, deprecated endpoints

### 5. Cloud-Specific Caution ⚠️

This is where it gets legally sensitive. Passive recon = fine. Active exploitation = illegal.

| Technique | Legal? | Notes |
| ----------- | -------- | ------- |
| Certificate transparency | ✅ | Fully passive |
| Shodan lookup | ✅ | Passive, Shodan scanned it |
| DNS enumeration | ✅ | Passive |
| Subdomain brute-force | ⚠️ | Gray area — sends packets |
| Accessing exposed S3 buckets | ⚠️/❌ | Even "public" buckets are legally risky |
| Fuzzing their APIs | ❌ | CFAA territory |
| Exploiting any vulnerability | ❌ | Criminal |

---

## AI Agent Architecture for This

Here's a practical agent that automates the recon pipeline:

```python
import anthropic
import subprocess
import json
import httpx
from typing import Any

client = anthropic.Anthropic()

tools = [
    {
        "name": "run_subfinder",
        "description": "Enumerate subdomains via certificate transparency and passive DNS",
        "input_schema": {
            "type": "object",
            "properties": {"domain": {"type": "string"}},
            "required": ["domain"]
        }
    },
    {
        "name": "fetch_crtsh",
        "description": "Query certificate transparency logs for subdomains",
        "input_schema": {
            "type": "object",
            "properties": {"domain": {"type": "string"}},
            "required": ["domain"]
        }
    },
    {
        "name": "fetch_job_postings",
        "description": "Fetch and analyze job postings to infer tech stack",
        "input_schema": {
            "type": "object",
            "properties": {"company_name": {"type": "string"}},
            "required": ["company_name"]
        }
    },
    {
        "name": "analyze_headers",
        "description": "Fetch HTTP headers from a URL to detect CDN, cloud provider, frameworks",
        "input_schema": {
            "type": "object",
            "properties": {"url": {"type": "string"}},
            "required": ["url"]
        }
    },
    {
        "name": "github_search",
        "description": "Search GitHub for company repos and leaked info",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"]
        }
    }
]

def run_tool(name: str, inputs: dict) -> Any:
    if name == "fetch_crtsh":
        domain = inputs["domain"]
        r = httpx.get(
            f"https://crt.sh/?q=%.{domain}&output=json",
            timeout=15
        )
        names = list(set(
            entry["name_value"]
            for entry in r.json()
            if "*" not in entry["name_value"]
        ))
        return {"subdomains": names[:50]}  # cap it

    elif name == "analyze_headers":
        url = inputs["url"]
        r = httpx.head(url, follow_redirects=True, timeout=10)
        return {
            "headers": dict(r.headers),
            "status": r.status_code,
            "final_url": str(r.url)
        }

    elif name == "github_search":
        # Use GitHub search API
        query = inputs["query"]
        r = httpx.get(
            "https://api.github.com/search/repositories",
            params={"q": query, "sort": "updated", "per_page": 10},
            headers={"Accept": "application/vnd.github.v3+json"},
            timeout=10
        )
        items = r.json().get("items", [])
        return [{"name": i["full_name"], "desc": i["description"],
                 "stars": i["stargazers_count"], "lang": i["language"]}
                for i in items]

    return {"error": f"Tool {name} not implemented"}

def recon_agent(target_company: str, target_domain: str) -> str:
    messages = [
        {
            "role": "user",
            "content": f"""Do a passive OSINT recon on company '{target_company}' with domain '{target_domain}'.

Your goal: build a technical intelligence report covering:
1. Infrastructure (cloud provider, CDN, IP ranges)
2. Tech stack (frameworks, databases, monitoring)
3. Engineering team signals (from GitHub)
4. Subdomains that reveal internal product architecture

Use tools sequentially. Start with cert transparency, then headers, then GitHub.
Only passive recon — no active scanning or exploitation."""
        }
    ]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            return next(
                b.text for b in response.content
                if hasattr(b, 'text')
            )

        # Process tool calls
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"[agent] calling {block.name}({block.input})")
                result = run_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result)
                })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

if __name__ == "__main__":
    report = recon_agent("Anthropic", "anthropic.com")
    print(report)
```

---

## The Synthesis Layer — What AI Adds

Raw OSINT data is noise. The agent's real value is synthesis:

```
Subdomains found:
  api-internal.target.com → suggests separate internal API gateway
  grafana.target.com → Prometheus/Grafana observability stack
  kafka-ui.target.com → Kafka in use, exposed management UI
  staging-ml.target.com → separate ML serving infrastructure

Job postings mention:
  "PyTorch, Ray, vLLM" → ML inference stack
  "Temporal for workflow orchestration"
  "ClickHouse for analytics"

GitHub:
  3 public repos using their internal SDK → naming conventions revealed

Conclusion: AWS-based, Kafka+Temporal event-driven architecture,
Ray/vLLM for ML serving, Grafana observability, likely Kubernetes.
Engineering team ~40 people based on LinkedIn + commit velocity.
```

No insider info needed. A motivated outsider with this toolkit knows more about the product stack than many employees in non-technical roles.

---

## What You Can't Get (Without Going Inside)

- Internal Slack/Lark discussions, political dynamics
- Actual revenue numbers (unless public)
- Incident post-mortems (unless they publish them)
- Team morale, technical debt severity
- Who's actually senior vs. who has a senior title

But product quality, architecture, scale, observability maturity, security hygiene — all visible from outside.
