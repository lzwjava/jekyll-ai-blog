---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rasa Enterprise AI Agent Platform
translated: false
type: note
---

## Question: Introduction to Rasa platform ([https://rasa.com](https://rasa.com))

## Answer:

Rasa is an enterprise AI agent platform focused on building **reliable, controllable conversational AI systems**. It started in 2016 as an open-source conversational AI/NLU framework and has evolved into a platform for production-grade AI agents that combine LLM capabilities with deterministic business logic. ([Rasa][1])

### What problem does Rasa solve?

Modern LLM chatbots have a common problem:

```
User
 |
 v
LLM
 |
 v
Answer
```

The model is flexible but can:

* hallucinate
* ignore business rules
* fail compliance requirements
* behave inconsistently

Rasa's philosophy is:

```
                 +----------------+
User ----------> | Language Model |
                 +----------------+
                         |
                         v
              +--------------------+
              | Dialogue Manager   |
              | Business Logic     |
              | Workflow Engine    |
              +--------------------+
                         |
                         v
              APIs / Database / CRM
```

The LLM handles language understanding, while Rasa controls execution flow. ([Rasa][2])

---

## Core products

### 1. Rasa Platform

The main enterprise platform.

Features:

* AI agent orchestration
* conversation memory
* workflow management
* integrations
* testing and analytics
* deployment control

It supports both:

* **No-code**: Rasa Studio
* **Pro-code**: developer workflow

([Rasa][3])

---

### 2. CALM (Conversational AI with Language Models)

This is Rasa's LLM-native architecture.

Instead of traditional chatbot design:

```
Intent:
  book_flight

Entity:
  destination = Tokyo

Rule:
  ask_date()
```

CALM allows:

```
User:
"I need to change my flight tomorrow"

          |
          v

LLM understands intent

          |
          v

Rasa Flow decides:

1. Verify identity
2. Check booking
3. Call airline API
4. Confirm change
```

The important part:

LLM ≠ controller.

LLM suggests; Rasa executes. ([Rasa][4])

---

## Typical architecture

Enterprise deployment:

```
                 Web / Mobile / Voice
                         |
                         v
                 +---------------+
                 |     Rasa      |
                 | AI Agent Core |
                 +---------------+
                         |
        +----------------+----------------+
        |                |                |
        v                v                v

    CRM System      Knowledge Base    Internal APIs

        |
        v

 Salesforce / SAP / Banking System
```

Common industries:

* banking
* insurance
* healthcare
* telecom
* government
* customer service

because these need predictable behavior and private deployment. ([Rasa][5])

---

## Developer experience

Rasa is Python-based.

Example:

```bash
pip install rasa

rasa init

rasa train

rasa run
```

Typical project:

```
my-agent/

├── domain.yml
├── flows/
├── actions/
├── config.yml
├── credentials.yml
└── tests/
```

Custom business action:

```python
class CheckBalance(Action):

    def run(self, dispatcher, tracker, domain):

        user_id = tracker.get_slot("user_id")

        balance = bank_api.get_balance(user_id)

        dispatcher.utter_message(
            text=f"Your balance is {balance}"
        )
```

---

## Rasa vs LangChain / AutoGen / CrewAI

| Platform                 | Main idea                                                  |
| ------------------------ | ---------------------------------------------------------- |
| Rasa                     | Enterprise conversational agents with controlled workflows |
| LangChain                | LLM application framework                                  |
| LlamaIndex               | Data/RAG framework                                         |
| AutoGen                  | Multi-agent experimentation                                |
| CrewAI                   | Agent teams                                                |
| OpenAI Assistants/Agents | Managed agent platform                                     |

Rasa is closer to:

```
Air traffic control system
```

while many agent frameworks are closer to:

```
Autonomous robots exploring freely
```

For banking, insurance, telecom, Rasa's controlled approach is attractive.

---

## Strengths

### 1. Enterprise reliability

Good for:

* "Change my account address"
* "Submit insurance claim"
* "Reset corporate password"

where mistakes are expensive.

### 2. Self-hosting

Can run:

* private cloud
* Kubernetes
* on-premise

Useful for regulated companies. ([Rasa][6])

### 3. Open ecosystem

Historically strong open-source community.

GitHub:

[Rasa GitHub Repository](https://github.com/RasaHQ/rasa?utm_source=chatgpt.com)

---

## Weaknesses

Compared with modern LLM-native stacks:

* More engineering effort
* Less "magic" than pure GPT agents
* Requires conversation design
* Smaller ecosystem than LangChain

For simple:

```
PDF chatbot
+
RAG
+
GPT-4/Qwen
```

Rasa may be overkill.

For:

```
10 million customer conversations
+
compliance
+
workflow
+
audit
```

Rasa becomes much more valuable.

---

## My view for an AI consulting company

For enterprise AI projects, Rasa fits well as the **agent orchestration layer**:

```
              User

               |
               v

        Rasa Agent Layer

               |
       +-------+-------+
       |       |       |

      RAG    Tools   LLM

       |       |       |

  VectorDB   APIs   Qwen/GPT/Claude

```

A modern stack could be:

* Rasa → workflow + guardrails
* vLLM → self-hosted models
* Qwen/DeepSeek → reasoning model
* Milvus/PGVector → RAG
* Kubernetes → deployment

This matches the direction of enterprise "AI application platform" projects.

References:

* [Rasa Official Website](https://rasa.com/?utm_source=chatgpt.com)
* [Rasa Platform Documentation](https://rasa.com/docs/learn/platform-introduction/?utm_source=chatgpt.com)
* [Rasa GitHub Repository](https://github.com/RasaHQ/rasa?utm_source=chatgpt.com)

[1]: https://rasa.com/about?utm_source=chatgpt.com "About Rasa | Building Trustworthy, Scalable AI Agents"
[2]: https://rasa.com/platform?utm_source=chatgpt.com "Rasa Platform | Build Reliable AI Agents with Full Control"
[3]: https://rasa.com/docs/learn/platform-introduction/?utm_source=chatgpt.com "Introduction to the Rasa Platform | Rasa Documentation"
[4]: https://rasa.com/docs/pro/intro/?utm_source=chatgpt.com "Welcome to Rasa | Rasa Documentation"
[5]: https://rasa.com/ai-info-page?utm_source=chatgpt.com "AI Info"
[6]: https://info.rasa.com/rasa-conversational-ai-platform-for-customer-experience?utm_source=chatgpt.com "Rasa Conversational AI Platform for Superior Customer Experience"
