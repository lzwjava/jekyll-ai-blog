---
audio: false
generated: true
image: false
lang: en
layout: post
title: Local AI Deep Research Agent
translated: false
type: note
---

Question: intro to `LearningCircuit/local-deep-research`

Answer:

[Local Deep Research GitHub Repository](https://github.com/LearningCircuit/local-deep-research?utm_source=chatgpt.com) is an open-source **local AI deep research agent**. Think of it as a self-hosted version of systems like ChatGPT Deep Research / Gemini Deep Research, but you control the model, data, and infrastructure.

The core idea:

```
User question
      |
      v
Research Agent
      |
      +--> Web search
      |
      +--> Academic search
      |
      +--> Local documents
      |
      +--> Multiple LLM calls
      |
      v
Synthesized report + citations
```

It is not just RAG. It is closer to an **agentic research workflow**.

## Architecture

Main components:

```
                 +----------------+
                 |      User      |
                 +--------+-------+
                          |
                          v
              +-----------+------------+
              | Local Deep Research    |
              |        Agent           |
              +-----------+------------+
                          |
        +-----------------+----------------+
        |                 |                |
        v                 v                v

    LLM Backend       Search Tools      Knowledge Base

    Ollama            SearXNG           PDFs
    vLLM              Web                Papers
    OpenAI API        arXiv              Notes
    Claude API        PubMed             Documents
```

The project supports:

* local LLMs through Ollama
* OpenAI-compatible endpoints
* web search
* academic sources
* your own document library

The README describes it as an "AI-powered research assistant for deep, agentic research" that uses multiple LLMs and search engines with citations.

## The interesting part: agent strategy

The important piece is **LangGraph Agent Strategy**.

Traditional:

```
Question
   |
Search 5 URLs
   |
Summarize
   |
Answer
```

Agentic:

```
Question

LLM thinks:

"Need more information about X"

        |
        v

Search X

        |
        v

Read results

        |
        v

"Need academic sources"

        |
        v

Search arXiv/PubMed

        |
        v

Compare sources

        |
        v

Generate report
```

The agent decides:

* what to search
* which search engine to use
* when enough evidence exists
* when to synthesize

The repo claims this LangGraph agent mode is behind its benchmark results.

## Local hardware

Interesting for your setup:

The project specifically targets local GPU usage.

README mentions:

> fully-local on a single RTX 3090 (Qwen3.6-27B)

and reports benchmark numbers around:

* SimpleQA ~95%
* xbench-DeepSearch ~77%

on local hardware.

Your RTX 4070 12GB is more limited, but possible configurations:

### Small local setup

```
RTX 4070
 |
 +-- Qwen3 8B / 14B
 |
 +-- Ollama
 |
 +-- Local Deep Research
```

### Serious setup

```
2 x RTX 3090 24GB

48GB VRAM

      |
      +-- Qwen3 32B
      +-- Deep Research Agent
      +-- Embedding model
```

This is exactly the type of workload where multiple GPUs are useful.

## Installation

Simplest:

```bash
pip install local-deep-research

python -m local_deep_research.web.app
```

Then connect:

```
LLM:
  Ollama
  vLLM
  OpenAI API compatible

Search:
  SearXNG
```

The project also provides Docker deployment.

## Compared with ChatGPT Deep Research

|                     | ChatGPT Deep Research | Local Deep Research |
| ------------------- | --------------------- | ------------------- |
| Model               | OpenAI models         | Any model           |
| Data privacy        | Cloud                 | Local               |
| Custom knowledge    | Limited               | Strong              |
| Cost                | Subscription/API      | Hardware cost       |
| Agent customization | Limited               | Full code access    |
| Research workflow   | Closed                | Open                |

The interesting future direction:

```
10 models
   |
100 research agents
   |
cross verification
   |
final scientific report
```

This project is basically a building block toward that.

## For your "AI token factory" idea

This repo is very close to the "research department" of an AI company.

Imagine:

```
                    Manager Agent

                         |
       +-----------------+----------------+
       |                 |                |

 Literature Agent   Code Agent     Market Agent

 Claude             Qwen            Gemini

       |                 |                |

       +-------- Debate / Verification --+

                         |

                  Final Report
```

Local Deep Research gives you one worker. The next evolution is an **agent organization**.

For someone building CLI agents, model training experiments, and multi-model workflows, this repo is worth studying mainly for:

1. LangGraph orchestration
2. search planning
3. citation pipeline
4. local model integration
5. persistent knowledge base

It is not just a "ChatGPT clone"; it is closer to an open-source research operating system.

References:

* [Local Deep Research GitHub Repository](https://github.com/LearningCircuit/local-deep-research?utm_source=chatgpt.com)
