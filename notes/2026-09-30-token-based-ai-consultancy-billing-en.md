---
audio: false
generated: true
image: false
lang: en
layout: post
title: Token-Based AI Consultancy Billing
translated: false
type: note
---

**Question: Are there people doing software consultancy where they charge by token usage, with one project = one client API key?**

Yes. This model is emerging, especially for **AI engineering consultancies building LLM agents, RAG systems, automation workflows, and internal copilots**. It is not yet the dominant model for traditional software consulting, but the pattern is real: **meter AI consumption per client/project and pass through or markup token costs**. ([OneBill][1])

The common architecture looks like this:

```
Client A
  |
  | API key / project key
  v
Your AI Gateway
  |
  +--> OpenAI / Anthropic / Gemini / self-hosted models
  |
  +--> Usage ledger
        - input tokens
        - output tokens
        - model
        - tool calls
        - embeddings
        - GPU seconds
        - cost
        - markup
```

Then invoice:

```
Client A
January usage:

GPT-5:
  input tokens:   120M
  output tokens:   15M
  cost:            $850

Agent platform fee: $2,000

AI usage markup (30%): $255

Total: $3,105
```

### Existing examples of this pattern

1. **AI agencies / AI automation consultants**

Many agencies are moving from:

```
$20k fixed project
```

to:

```
$5k setup
+
$500/month platform
+
usage
```

because the customer's AI workload continues after deployment.

2. **AI SaaS infrastructure companies**

Companies building AI billing infrastructure explicitly support this model: metering tokens, API calls, agent actions, and turning them into invoices. ([GitHub][2])

3. **Agent platforms**

Some agent frameworks already implement:

```
project -> usage -> invoice
```

with per-project token tracking and client billing exports. ([Pepe Agent][3])

---

For a consultancy, I would actually avoid giving clients your raw OpenAI/Anthropic key.

Better:

```
client-api-key
       |
       v
your gateway
       |
       +-- project_id=acme
       +-- budget_limit=$1000/mo
       +-- allowed_models=[...]
       +-- logging
       +-- invoice events
```

Example minimal implementation:

```python
from openai import OpenAI

client = OpenAI(
    api_key="<YOUR_MASTER_KEY>"
)

def chat(project, messages):
    r = client.chat.completions.create(
        model="gpt-5",
        messages=messages
    )

    usage = r.usage

    ledger.append({
        "project": project,
        "input": usage.prompt_tokens,
        "output": usage.completion_tokens,
        "model": "gpt-5"
    })

    return r
```

Database:

```sql
CREATE TABLE usage_events (
    project_id TEXT,
    model TEXT,
    input_tokens INT,
    output_tokens INT,
    created_at TIMESTAMP
);
```

Then:

```sql
SELECT
 project_id,
 SUM(input_tokens),
 SUM(output_tokens)
FROM usage_events
GROUP BY project_id;
```

---

The interesting business model is not pure token resale. Pure token markup has weak margins.

The stronger model is:

```
Consulting retainer
        +
AI platform fee
        +
token pass-through
        +
outcome fee
```

Example:

* $5k/month AI engineering retainer
* $500/month hosting/platform
* LLM cost + 20% markup
* optional $50 per automated workflow completion

This is closer to how cloud companies evolved: AWS does not sell servers only; it sells metered infrastructure plus higher-level services.

A few years from now, "AI engineer" consultancies will probably look more like small managed AI infrastructure providers than classic software contractors.

I can also sketch a production-grade architecture for a **multi-client AI consultancy billing gateway** (similar to Stripe metering + OpenRouter proxy + Langfuse) if useful.

[1]: https://www.onebillsoftware.com/outcome-based-consumption-pricing-ai-agents/?utm_source=chatgpt.com "Outcome-Based Billing for AI Agents and GenAI Platforms | OneBill"
[2]: https://github.com/getlago/lago?utm_source=chatgpt.com "GitHub - getlago/lago: Open Source Metering and Usage Based Billing API ⭐️ Consumption tracking, Subscription management, Pricing iterations, Payment orchestration & Revenue analytics · GitHub"
[3]: https://pepe-agent.com/en/docs/billing/?utm_source=chatgpt.com "Billing & limits · Pepe docs"
