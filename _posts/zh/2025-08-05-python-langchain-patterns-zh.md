---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Python LangChain 模式
translated: true
type: note
---

以下是几个简洁的Python代码片段，展示了常见的LangChain使用模式。你可以自由组合这些模块来构建更复杂的工作流。

---

### 1. 使用PromptTemplate的简单LLM链

```python
from langchain import OpenAI, LLMChain, PromptTemplate

# 1. 初始化大语言模型
llm = OpenAI(temperature=0.7)

# 2. 创建提示词模板
template = PromptTemplate(
    input_variables=["product"],
    template="为以下产品撰写简短营销文案：{product}。"
)

# 3. 构建处理链
chain = LLMChain(llm=llm, prompt=template)

# 4. 执行链式调用
result = chain.run({"product": "无线降噪耳机"})
print(result)
```

---

### 2. 具备记忆功能的对话链

```python
from langchain import OpenAI, ConversationChain
from langchain.memory import ConversationBufferMemory

# 1. 初始化大语言模型和记忆模块
llm = OpenAI(temperature=0)
memory = ConversationBufferMemory()

# 2. 构建对话链
conv = ConversationChain(llm=llm, memory=memory)

# 3. 模拟对话流程
print(conv.predict(input="你好！"))
print(conv.predict(input="能提醒我们之前聊过什么吗？"))
```

---

### 3. 基于文档的检索问答（FAISS）

```python
from langchain import OpenAI, RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader

# 1. 加载并分割文档
loader = TextLoader("my_docs/guide.txt")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_documents(docs)

# 2. 构建向量索引
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# 3. 构建检索问答链
qa = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# 4. 执行问答查询
answer = qa.run("我们API的主要优势是什么？")
print(answer)
```

---

### 4. 配备工具集的智能体

```python
from langchain import OpenAI, SerpAPIWrapper, LLMMathChain, initialize_agent
from langchain.agents import Tool

# 1. 定义工具集
search = SerpAPIWrapper()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="适用于网络搜索"
    ),
    Tool(
        name="Calculator",
        func=LLMMathChain.from_llm(OpenAI(temperature=0)).run,
        description="适用于数学计算"
    )
]

# 2. 创建智能体
agent = initialize_agent(
    tools,
    llm=OpenAI(temperature=0),
    agent="zero-shot-react-description",
    verbose=True
)

# 3. 运行智能体
response = agent.run("法国的首都是哪里？这个结果加上二乘五等于多少？")
print(response)
```

---

欢迎灵活调整这些代码片段——你可以替换不同的大语言模型、更换检索器（如Chroma、Pinecone），或根据需要添加自定义工具和记忆模块类型！
