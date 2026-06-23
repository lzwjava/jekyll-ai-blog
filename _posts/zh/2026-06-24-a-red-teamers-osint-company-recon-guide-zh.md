---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 红队成员的OSINT公司侦察指南
translated: true
type: note
---

**问题：** 什么是公司的“公开信息”？如何系统性地利用这些信息——再加上黑客/OSINT技术——在加入公司前深入调查其产品、技术栈和基础设施，并借助AI智能体增强调查效果？

**回答：**

这就是将OSINT（开源情报）应用于公司尽职调查。核心思路是：你扮演的是进行侦察的红队成员，而不是只看Glassdoor的求职者。

---

## 公开信息面

### 1. 人员层
- **LinkedIn / 脉脉 / GitHub 资料** — 工程师会透露技术栈（他们的仓库、星标项目、博客文章）
- **会议演讲 / 论文** — 工程师在SDCC、QCon、InfoQ等会议演讲中可能无意间提到内部系统名称
- **招聘信息** — 最被低估的信号。“有Flink、Kafka、ClickHouse、K8s on AWS经验” = 他们的确切技术栈
- **专利申请** — 揭示专有算法和架构方法

### 2. 产品/前端层
- **HTTP流量分析** — 在它们的应用上使用 Charles Proxy / mitmproxy / Wireshark
  - API端点、版本号（`/v3/`、`/api/internal/`）
  - 认证方案（JWT结构、OAuth流程）
  - 嵌入的第三方SDK（Sentry、DataDog、Amplitude = 它们的可观测性技术栈）
  - CDN头部（`X-Served-By`、`CF-Ray`、`X-Cache`）
- **JS包分析** — `source-map-explorer`、未压缩的包会泄露框架选择、功能开关，甚至内部路由名称
- **移动端APK/IPA** — `apktool`反编译 → smali/Java → 内部包名、端点，有时会硬编码测试环境URL
- **浏览器DevTools Network标签** — 显而易见但功能强大

### 3. 基础设施层
- **DNS枚举**
  ```bash
  # 子域名暴力破解
  subfinder -d target.com | httpx -title -tech-detect
  amass enum -d target.com

  # 证书透明度日志（无需主动扫描）
  curl "https://crt.sh/?q=%.target.com&output=json" | jq '.[].name_value' | sort -u
  ```
- **IP范围/ASN**
  ```bash
  # 查找它们的ASN
  whois -h whois.radb.net -- '-i origin AS12345'
  # 或者通过 bgp.he.net
  curl https://bgp.he.net/dns/target.com
  ```
- **Shodan / Censys / FOFA** — 扫描它们的IP范围查找暴露的服务
  ```
  org:"TargetCompany Inc" port:6379  # Redis暴露？
  ssl:"target.com" http.title:"Grafana"  # 监控面板？
  ```
- **云服务商线索**
  - S3存储桶命名：`target-prod-logs.s3.amazonaws.com`
  - GCP：`storage.googleapis.com/target-*`
  - **CloudFlare、Fastly的头部**有时会泄露源站IP

### 4. 代码/产物层
- **GitHub** — 搜索 `org:targetcompany`，同时搜索公有仓库、Gist、提交信息中的 `"target.com" internal`
  ```bash
  # GitHub dork
  site:github.com "target.com" "internal" "staging"
  # 在其公有仓库上运行 truffleHog / gitleaks
  trufflehog github --org=targetcompany
  ```
- **npm / PyPI / Maven** — 发布的包会透露内部命名规范、依赖关系
- **Docker Hub** — 公开镜像有时包含内嵌凭据的层
  ```bash
  docker pull target/someimage
  docker history target/someimage --no-trunc
  ```
- **Wayback Machine** — 旧的JS包、旧的API文档、已废弃的端点

### 5. 云服务特有注意事项 ⚠️

这是法律敏感地带。被动侦察 = 没问题。主动利用 = 违法。

| 技术 | 合法？ | 备注 |
|------|--------|------|
| 证书透明度 | ✅ | 完全被动 |
| Shodan查询 | ✅ | 被动，Shodan已扫描 |
| DNS枚举 | ✅ | 被动 |
| 子域名暴力破解 | ⚠️ | 灰色地带——会发送数据包 |
| 访问暴露的S3存储桶 | ⚠️/❌ | 即使是“公开”存储桶也有法律风险 |
| 对API进行模糊测试 | ❌ | 属于CFAA管辖范围 |
| 利用任何漏洞 | ❌ | 刑事犯罪 |

---

## 为此设计的AI智能体架构

下面是一个实用的智能体，用于自动化侦察流程：

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
        "description": "通过证书透明度和被动DNS枚举子域名",
        "input_schema": {
            "type": "object",
            "properties": {"domain": {"type": "string"}},
            "required": ["domain"]
        }
    },
    {
        "name": "fetch_crtsh",
        "description": "查询证书透明度日志获取子域名",
        "input_schema": {
            "type": "object",
            "properties": {"domain": {"type": "string"}},
            "required": ["domain"]
        }
    },
    {
        "name": "fetch_job_postings",
        "description": "获取并分析招聘信息以推断技术栈",
        "input_schema": {
            "type": "object",
            "properties": {"company_name": {"type": "string"}},
            "required": ["company_name"]
        }
    },
    {
        "name": "analyze_headers",
        "description": "从URL获取HTTP头部以检测CDN、云服务商、框架",
        "input_schema": {
            "type": "object",
            "properties": {"url": {"type": "string"}},
            "required": ["url"]
        }
    },
    {
        "name": "github_search",
        "description": "在GitHub上搜索公司仓库和泄露信息",
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
        return {"subdomains": names[:50]}  # 限制数量

    elif name == "analyze_headers":
        url = inputs["url"]
        r = httpx.head(url, follow_redirects=True, timeout=10)
        return {
            "headers": dict(r.headers),
            "status": r.status_code,
            "final_url": str(r.url)
        }

    elif name == "github_search":
        # 使用GitHub搜索API
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

    return {"error": f"工具 {name} 未实现"}

def recon_agent(target_company: str, target_domain: str) -> str:
    messages = [
        {
            "role": "user",
            "content": f"""对以下公司进行被动OSINT侦察：公司 '{target_company}'，域名为 '{target_domain}'。

你的目标：构建一份技术情报报告，涵盖：
1. 基础设施（云服务商、CDN、IP范围）
2. 技术栈（框架、数据库、监控）
3. 工程团队信号（来自GitHub）
4. 能揭示内部产品架构的子域名

按顺序使用工具。先从证书透明度开始，然后是头部分析，再是GitHub。
仅限被动侦察——不进行主动扫描或利用。"""
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

        # 处理工具调用
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"[agent] 调用 {block.name}({block.input})")
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

## 综合层——AI的优势

原始OSINT数据是噪音。智能体的真正价值在于综合：

```
发现的子域名：
  api-internal.target.com → 暗示存在独立的内部API网关
  grafana.target.com → Prometheus/Grafana可观测性技术栈
  kafka-ui.target.com → 正在使用Kafka，管理界面暴露
  staging-ml.target.com → 独立的机器学习服务基础设施

招聘信息中提到：
  "PyTorch, Ray, vLLM" → 机器学习推理技术栈
  "Temporal用于工作流编排"
  "ClickHouse用于分析"

GitHub：
  3个公有仓库使用了它们的内部SDK → 命名规范暴露

结论：基于AWS，采用Kafka+Temporal事件驱动架构，
Ray/vLLM用于机器学习服务，Grafana可观测性，很可能使用Kubernetes。
根据LinkedIn和提交速度判断，工程团队约40人。
```

不需要内部信息。一个积极主动的外部人员借助这套工具，对公司产品技术栈的了解程度可能超过许多非技术岗位的员工。

---

## 你无法获取的信息（除非进入公司内部）

- 内部Slack/Lark讨论、政治动态
- 实际收入数字（除非公开）
- 故障复盘报告（除非他们公开发布）
- 团队士气、技术债务严重程度
- 谁是真正的高级工程师，谁只是拥有高级头衔

但产品质量、架构、规模、可观测性成熟度、安全卫生——这些都可以从外部观察到。