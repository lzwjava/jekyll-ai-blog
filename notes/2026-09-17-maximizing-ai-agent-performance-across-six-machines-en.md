---
audio: false
generated: true
image: false
lang: en
layout: post
title: Maximizing AI Agent Performance Across Six Machines
translated: false
type: note
---

Question: How do you maximize AI agent performance across 6 computers in a room, and how do you efficiently build software with them?

Answer:

## Hardware & Network Setup

**Network**

- Connect all 6 machines via **Gigabit Ethernet** (not Wi-Fi) — low latency is critical for agent coordination
- Use a dedicated switch, not a consumer router
- Assign static IPs to each machine for reliable addressing

**Roles** — don't treat all 6 machines equally:

| Machine | Role |
| --- | --- |
| 1 | **Orchestrator** — task queue, job dispatch, monitoring dashboard |
| 2–4 | **Worker nodes** — run heavy agent workloads |
| 5 | **Model server** — host local LLMs (Ollama, vLLM, llama.cpp) |
| 6 | **Storage/DB** — vector DB (Qdrant/Chroma), shared file system, logs |

---

## Agent Architecture

**Use a multi-agent framework** designed for distributed work:

- **CrewAI** — role-based agents with defined tasks
- **LangGraph** — graph-based state machine for complex agent flows
- **AutoGen (Microsoft)** — multi-agent conversation and code execution
- **Ray** — distribute Python workloads across all 6 nodes natively

**Key pattern — Orchestrator + Workers:**

```
Orchestrator (Machine 1)
  ├── Agent A: Research      → Worker Node 2
  ├── Agent B: Code Writing  → Worker Node 3
  ├── Agent C: Testing       → Worker Node 4
  └── Agent D: Review        → Worker Node 2 (reused)
```

---

## Software Development Workflow

**1. Shared codebase**

- Git repo on Machine 6 (or GitHub/Gitea self-hosted)
- All agents pull/push from one source of truth

**2. Agent specialization for dev tasks**

| Agent | Responsibility |
| --- | --- |
| **Planner** | Breaks feature into subtasks |
| **Coder** | Writes implementation |
| **Tester** | Runs tests, reports failures |
| **Reviewer** | Checks code quality, suggests fixes |
| **Documenter** | Writes docs/comments |

**3. Task queue**

- Use **Redis** or **Celery** on Machine 6 to queue jobs
- Workers poll the queue and pick up tasks independently
- Avoids idle machines

**4. Parallel code generation**

- Split a large feature into independent modules
- Each worker machine builds one module simultaneously
- Orchestrator merges and resolves conflicts

---

## Performance Optimization

- **Local model hosting** (Machine 5) — eliminates API latency and cost for high-frequency calls; use cloud API only for complex reasoning
- **Caching** — cache repeated prompts/embeddings in Redis
- **Quantized models** — run `Q4_K_M` or `Q8` GGUF models to fit more throughput per machine
- **Async everywhere** — use `asyncio` in Python so agents don't block waiting on I/O
- **Monitor** — use **Grafana + Prometheus** to watch CPU/GPU, queue depth, and agent throughput per node

---

## Recommended Stack

```
Orchestration : LangGraph or CrewAI
LLM serving   : Ollama (easy) or vLLM (high throughput)
Task queue    : Redis + Celery
Vector DB     : Qdrant (Machine 6)
Shared storage: NFS or MinIO
Monitoring    : Grafana + Prometheus
Version control: Gitea (self-hosted) or GitHub
```

---

References:

- [Ray — Distributed Python for AI workloads](https://docs.ray.io)
- [CrewAI — Multi-agent role framework](https://docs.crewai.com)
- [LangGraph — Stateful agent graphs](https://langchain-ai.github.io/langgraph/)
- [vLLM — High-throughput LLM serving](https://docs.vllm.ai)
- [Ollama — Run local models easily](https://ollama.com)
- [AutoGen — Microsoft multi-agent framework](https://microsoft.github.io/autogen/)
