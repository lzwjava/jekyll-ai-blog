---
audio: false
generated: true
image: false
lang: en
layout: post
title: "LangChain: LLM Application Framework"
translated: false
type: note
---

Question: What is LangChain, and how should I understand it as an AI/LLM engineer?

Answer:

**LangChain is an application framework for building software around LLMs.**

The core idea is simple:

> **LLM call + tools + state + retrieval + control flow = AI application**

Instead of writing everything yourself around `openai.chat.completions()` / Anthropic / local models, LangChain gives you abstractions for connecting these pieces.

### 1. The simplest LangChain program

Conceptually:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-5")

response = llm.invoke("Explain KV cache in one paragraph")

print(response.content)
```

That's basically an LLM wrapper.

But LangChain becomes more interesting when you compose operations:

```text
user
 ↓
prompt
 ↓
LLM
 ↓
tool call?
 ├── yes → tool → LLM
 └── no
 ↓
answer
```

### 2. The important abstractions

I'd think about LangChain in roughly these layers:

```text
                    LangChain
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
      Models          Tools          Retrieval
        │              │              │
   OpenAI/Qwen      Python/API     Vector DB
   Claude/etc.      Browser        Documents
        │              │              │
        └──────────────┼──────────────┘
                       ↓
                    Agents
                       │
                       ↓
                 LangGraph
```

**Models**

A unified interface over different LLMs:

```python
llm.invoke(messages)
```

So you can swap:

```text
OpenAI
Anthropic
Google
Qwen
DeepSeek
Ollama
vLLM
...
```

without rewriting your whole application.

---

**Tools**

A tool is simply a function the model can invoke.

```python
@tool
def search_database(query: str):
    return db.search(query)
```

The LLM might produce something conceptually like:

```json
{
  "tool": "search_database",
  "arguments": {
    "query": "LangChain"
  }
}
```

Your runtime executes it and feeds the result back to the model.

This is where LangChain starts becoming useful for **agents**.

---

**Retrieval / RAG**

LangChain also provides components for:

```text
PDF
 ↓
split documents
 ↓
embeddings
 ↓
vector database
 ↓
similarity search
 ↓
relevant chunks
 ↓
LLM
```

For example:

```python
docs = loader.load()

chunks = splitter.split_documents(docs)

vectors = embeddings.embed_documents(chunks)

results = vector_db.similarity_search(
    "What is the refund policy?"
)
```

So you can build RAG systems without implementing every connector yourself.

---

### 3. Chains

The original LangChain idea was essentially **chains**.

For example:

```text
question
   ↓
retrieve documents
   ↓
generate prompt
   ↓
LLM
   ↓
answer
```

You can express this as a pipeline:

```python
chain = retriever | prompt | llm | parser

answer = chain.invoke(
    {"question": "What is the refund policy?"}
)
```

This `|` composition is one of the characteristic LangChain ideas.

It's essentially functional composition:

```text
f(x) → y
g(y) → z

g(f(x)) → z
```

---

### 4. Agents

This is probably the part most relevant to what you're building.

An agent is roughly:

```text
                    ┌─────────────┐
                    │     LLM     │
                    └──────┬──────┘
                           │
                    decide next action
                           │
             ┌─────────────┼─────────────┐
             ↓             ↓             ↓
          search         python        terminal
             │             │             │
             └─────────────┼─────────────┘
                           ↓
                        result
                           │
                           ↓
                          LLM
                           │
                    continue / finish
```

Pseudo-code:

```python
while not finished:
    action = llm.decide(state)

    if action.type == "tool":
        result = execute(action)
        state.append(result)

    elif action.type == "final":
        return action.answer
```

This is why LangChain became popular during the early agent boom.

---

### 5. LangGraph is arguably more important for serious agents

Today, I'd distinguish:

**LangChain**

> Components and abstractions for LLM applications.

**LangGraph**

> Stateful, controllable execution graphs for agents.

For example, a production coding agent might look like:

```text
START
  ↓
understand task
  ↓
inspect repository
  ↓
write code
  ↓
run tests
  ↓
tests pass? ── no ──→ debug
  │                    │
 yes                   └──→ run tests
  ↓
review
  ↓
DONE
```

That's much closer to a **state machine / workflow engine** than a simple "LLM wrapper."

LangGraph lets you explicitly represent that state and control flow.

---

### 6. Why not just write it yourself?

You absolutely can.

For someone with your engineering background, a minimal agent is probably only ~100 lines:

```python
messages = []

while True:
    response = llm(messages)

    if response.tool_calls:
        for call in response.tool_calls:
            result = tools[call.name](**call.args)

            messages.append({
                "role": "tool",
                "content": result,
            })
    else:
        break
```

And honestly, **doing this yourself is a great way to understand agents**.

LangChain's value is more about the ecosystem:

```text
                   Your Agent
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
     Models          Tools           RAG
        │              │              │
   50+ providers    databases       vector DBs
   streaming        APIs            loaders
   structured       search          retrievers
   output
```

You don't have to build every integration.

---

### 7. The downside

LangChain can also become **too abstract**.

You can end up with:

```text
AgentExecutor
  ↓
RunnableSequence
  ↓
RunnablePassthrough
  ↓
RunnableLambda
  ↓
Retriever
  ↓
PromptTemplate
  ↓
ChatModel
```

when the actual operation is simply:

```python
result = llm(prompt)
```

This is a common criticism.

For an experienced engineer, I'd recommend:

> **Understand the underlying LLM/tool-call/state-machine mechanics first, then use LangChain where its abstractions actually save code.**

Don't learn LangChain as if it were the fundamental technology. **LLMs, tool calling, retrieval, state, scheduling, and inference are the fundamentals. LangChain is infrastructure on top.**

### 8. How I'd position it in the AI stack

For your work, I'd think about the ecosystem like this:

```text
┌───────────────────────────────────────────┐
│              AI Application               │
│       coding agent / research agent       │
├───────────────────────────────────────────┤
│             LangGraph / Agent             │
│       state + control flow + tools        │
├───────────────────────────────────────────┤
│                LangChain                  │
│       models / tools / retrievers         │
├───────────────────────────────────────────┤
│          OpenAI / Anthropic / Qwen        │
│                  LLM                      │
├───────────────────────────────────────────┤
│       vLLM / SGLang / llama.cpp           │
│              inference                    │
├───────────────────────────────────────────┤
│         CUDA / ROCm / GPU hardware        │
└───────────────────────────────────────────┘
```

Given that you're already looking at **mini-sgl, KV cache, schedulers, MoE, training and coding agents**, I wouldn't spend weeks "learning LangChain." I'd spend **an afternoon reading its core abstractions**, then implement a tiny tool-calling agent yourself and compare it with LangGraph.

References:

* [LangChain documentation](https://docs.langchain.com/?utm_source=chatgpt.com)
* [LangGraph documentation](https://docs.langchain.com/oss/python/langgraph/overview?utm_source=chatgpt.com)
* [LangChain GitHub repository](https://github.com/langchain-ai/langchain?utm_source=chatgpt.com)