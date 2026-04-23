---
audio: false
generated: true
image: false
lang: en
layout: post
title: How Cloudflare AI Agent Lee Works
translated: false
type: note
---

Question: How does Cloudflare AI Agent “Lee” (Ask AI) work?

Answer:

The “Ask AI” feature you’re referring to is part of Cloudflare’s broader push into edge AI—often demonstrated through internal agents like “Lee” or similar assistants. While “Lee” itself isn’t a widely formalized public product name, it represents a pattern of how Cloudflare builds AI agents on its infrastructure.

Here’s how it works conceptually:

---

## 1. Core Idea: AI Runs at the Edge

Cloudflare operates a global edge network (data centers close to users). Instead of sending AI requests to centralized servers (like typical APIs), Cloudflare runs AI models **near the user** using:

* Cloudflare Workers
* Workers AI

This reduces:

* latency (faster responses)
* cost (less bandwidth + centralized compute)
* privacy risk (data stays closer to origin)

---

## 2. “Ask AI” = Retrieval + LLM + Edge Execution

An AI agent like “Lee” typically follows this pipeline:

### Step 1: User Query

User asks something like:

> “What does this API do?” or “Explain this doc”

---

### Step 2: Retrieval (Context Injection)

Instead of blindly querying a model, the system:

* Searches relevant data (docs, code, logs, knowledge base)
* Uses vector search (embeddings)

Often powered by:

* Vectorize

This is called **RAG (Retrieval-Augmented Generation)**.

---

### Step 3: LLM Inference

The system sends:

* user question
* retrieved context

to a model via:

* Workers AI

Cloudflare supports open models (e.g., Llama, Mistral), not just proprietary ones.

---

### Step 4: Agent Logic (Optional)

If it's a true “agent” (like Lee), it can:

* call APIs
* chain reasoning steps
* execute actions (e.g., query logs, modify configs)

This is orchestrated inside:

* Cloudflare Workers

So the agent is basically:

> code + AI model + tools

---

### Step 5: Response at the Edge

The answer is generated and returned directly from the nearest Cloudflare node.

---

## 3. Why Cloudflare’s Approach Is Different

### Traditional AI (e.g., OpenAI API)

* Centralized servers
* Higher latency
* Data leaves your environment

### Cloudflare AI Agent

* Runs on edge network
* Lower latency (global distribution)
* Can integrate directly with your infra (logs, APIs, DBs)

---

## 4. Typical Use Cases

“Ask AI” / agents like Lee are used for:

* Documentation assistants (“ask your docs”)
* Dev tools (explain code, debug logs)
* Customer support bots
* Internal knowledge assistants
* Security analysis (logs, traffic patterns)

---

## 5. Mental Model

You can think of it like this:

> Cloudflare AI Agent =
> **(Serverless function)** + **(LLM)** + **(Search over your data)** + **(Tools/APIs)**
> running **globally at the edge**

---

## 6. Simple Flow Diagram (Conceptual)

```
User Question
     ↓
Edge Worker (Cloudflare Workers)
     ↓
Retrieve context (Vectorize / KV / R2)
     ↓
Call LLM (Workers AI)
     ↓
Optional tool usage (APIs, logs)
     ↓
Response returned from nearest edge
```

---

## 7. Key Insight

The important shift is:

* Not “AI as a remote API”
* But **AI as infrastructure embedded into your backend**

Cloudflare is essentially turning AI into something like:

> “Just another function call inside your serverless app”

---

If you want, I can break down a real minimal example (like building your own “Ask AI” agent using Cloudflare Workers + Workers AI) so you can see how little code it actually takes.