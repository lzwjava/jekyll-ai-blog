---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python LangChain Patterns
translated: false
type: note
---

Here are a few concise, illustrative Python snippets showing common LangChain patterns. You can mix and match these pieces to build more complex workflows.

---

### 1. Simple LLM Chain with a PromptTemplate

```python
from langchain import OpenAI, LLMChain, PromptTemplate

# 1. Initialize the LLM
llm = OpenAI(temperature=0.7)

# 2. Create a prompt template
template = PromptTemplate(
    input_variables=["product"],
    template="Write a short marketing blurb for the product: {product}."
)

# 3. Build the chain
chain = LLMChain(llm=llm, prompt=template)

# 4. Run it
result = chain.run({"product": "wireless noise-cancelling headphones"})
print(result)
```

---

### 2. Conversation Chain with Memory

```python
from langchain import OpenAI, ConversationChain
from langchain.memory import ConversationBufferMemory

# 1. LLM and memory
llm = OpenAI(temperature=0)
memory = ConversationBufferMemory()

# 2. Build the conversation chain
conv = ConversationChain(llm=llm, memory=memory)

# 3. Simulate dialogue
print(conv.predict(input="Hi there!"))
print(conv.predict(input="Can you remind me what we talked about before?"))
```

---

### 3. Retrieval + QA over Documents (FAISS)

```python
from langchain import OpenAI, RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader

# 1. Load and split documents
loader = TextLoader("my_docs/guide.txt")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_documents(docs)

# 2. Embed and index
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# 3. Build a RetrievalQA chain
qa = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# 4. Ask questions
answer = qa.run("What are the primary benefits of our API?")
print(answer)
```

---

### 4. Agent with Tools

```python
from langchain import OpenAI, SerpAPIWrapper, LLMMathChain, initialize_agent
from langchain.agents import Tool

# 1. Define tools
search = SerpAPIWrapper()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Useful for web searches"
    ),
    Tool(
        name="Calculator",
        func=LLMMathChain.from_llm(OpenAI(temperature=0)).run,
        description="Useful for math calculations"
    )
]

# 2. Create agent
agent = initialize_agent(
    tools,
    llm=OpenAI(temperature=0),
    agent="zero-shot-react-description",
    verbose=True
)

# 3. Run agent
response = agent.run("What's the capital of France plus two times five?")
print(response)
```

---

Feel free to adapt any of these snippets—swap in different LLMs, change retrievers (e.g., Chroma, Pinecone), or add your own tools and memory types as needed!
