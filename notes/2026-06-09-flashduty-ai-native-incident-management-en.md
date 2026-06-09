---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Flashduty: AI-Native Incident Management"
translated: false
type: note
---

**Question:** What is Flashduty and how does it fit into AI-native incident management?

**Answer:**

Flashduty is a one-stop alarm event response platform that supports alarm aggregation, noise reduction, scheduling, and collaboration. Think of it as a central nervous system for incident response — it sits between your monitoring stack (Prometheus, Zabbix) and your team, filtering noise and routing alerts intelligently.

## Core Architecture

**Alert aggregation & correlation**: Raw alerts flood in from distributed systems. Flashduty deduplicates, groups related alerts, and reduces alert fatigue through ML-based noise filtering. This matters because alert storms are the #1 killer of incident response velocity.

**Multi-channel dispatch**: Built-in notification methods include Feishu/DingTalk/WeChat/SMS/Teams/Slack/Zoom/phone, responding to and processing alarms in IM and App. Your team gets notified in their native channel — synchronous for critical, async for informational.

**On-call scheduling**: Manages shift rotations, escalation chains, and duty calendars. MTTA/MTTR optimization through full lifecycle tracking.

## Why You Should Care: The MCP Angle

The Flashduty MCP Server bridges AI agents and incident management, with MCP described as the "USB-C for AI." This is the key. Instead of your incident response workflow being manual (alert → Slack → human reads → human acts), you can inject an AI agent into the loop:

```python
# Pseudocode: AI agent handling incident autonomously
# Via MCP, your agent can:

1. Query recent alerts from Flashduty API
2. Fetch context (metrics, logs) from observability stack
3. Classify severity & root cause with Claude
4. Execute remediation (restart service, trigger runbook)
5. Update incident status in Flashduty
6. Notify team with diagnostic summary
```

There's a flashduty-tools repository on GitHub with incident exporters and API scripts for programmatic access. The API supports cursor-based pagination, so you can bulk-export incident data for analysis or feed it into your own ML pipelines.

## Integration Points for Your Stack

**Direct API access** (no MCP required):
```python
import requests

FLASHDUTY_API = "https://api.flashcat.cloud"
INTEGRATION_KEY = "<INTEGRATION_KEY>"

# Send a custom alert
payload = {
    "title": "High latency detected",
    "event_status": "Critical",
    "description": "P99 latency > 500ms",
    "alert_key": "service-latency-2024",
    "labels": {"service": "auth-api", "region": "us-east"}
}

response = requests.post(
    f"{FLASHDUTY_API}/alert",
    headers={"Authorization": f"Bearer {INTEGRATION_KEY}"},
    json=payload
)
```

**MCP Server** (for Claude Code / Cursor):
If you're using Claude Code or building a Cursor agent, you can wire Flashduty as an MCP provider and have your agent autonomously query incidents, acknowledge alerts, and trigger responses. This is genuinely powerful for SRE automation — your agent becomes a force multiplier during incidents.

## Practical Use Case (Your Bank Context)

You mentioned being top 6% in LLM token usage at a bank. Incident response at financial institutions is brutal — you need fast MTTA, compliance audit trails, and clear escalation. Flashduty handles the mechanical parts (routing, scheduling, dedup). Pair it with an AI agent that:

- Ingests alerts + context (metrics, logs, error traces)
- Reasons about failure modes (disk full? connection pool exhausted? deployment conflict?)
- Runs non-destructive diagnostics
- Summarizes for on-call human in natural language

This shifts on-call from "dumb alert reader" to "intelligent debugger supervisor."

## Caveats

- Flashduty is noise reduction + dispatch, not observability. You still need Prometheus/Datadog/CloudWatch.
- The MCP server is newer (late 2024) — adoption still ramping. Expect rough edges.
- Chinese company (Flashcat Cloud) — check your org's vendor policy if security-sensitive.

## Next Steps

1. Check their docs at https://docs.flashcat.cloud/en/flashduty/getting-started
2. If building an agent, explore the MCP server setup — it's the most direct path to automation
3. For your current stack, export incident data and build ML models around MTTA optimization (neural net on alert features → time-to-resolution prediction)

---

**References:**

- [Flashduty AWS Marketplace](https://aws.amazon.com/marketplace/pp/prodview-iwx3dlyfwunr2)
- [Flashduty Tools Repository](https://github.com/flashcatcloud/flashduty-tools)
- [Flashduty MCP Server Guide](https://skywork.ai/skypage/en/flashduty-mcp-server-ai-engineer-guide-incident-automation/1980939640330305536)
