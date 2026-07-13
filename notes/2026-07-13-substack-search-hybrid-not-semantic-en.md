---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Substack Search: Hybrid, Not Semantic"
translated: false
type: note
---

Question: Is Substack search good? For example, can I search Yin Wang’s Substack for "时间" and get semantic matches, not only exact keyword matches?

Answer:

Yes, Substack search is much better than a simple `grep "时间"` style search, but it is not a full semantic search engine like modern AI search.

For a publication like Yin Wang Substack, Substack provides search for posts/publications/topics through its search bar. ([Substack Support][1])

Your observation is basically correct:

* It does not only behave like exact string matching.
* Searching `时间` may return articles that:

  * contain the word "时间"
  * discuss related concepts
  * have titles/content semantically related to time, existence, life, thinking, etc.

This is closer to **hybrid search**:

```
query = "时间"

score =
    keyword_match_score
  + title_similarity
  + content_similarity
  + popularity/relevance signals
```

rather than:

```bash
grep -r "时间" posts/
```

A pure keyword engine would miss:

```
"人生为什么有限"
"不要浪费生命"
"过去与未来"
"意识和存在"
```

because they may not contain the character "时间", but semantically relate to time.

However, Substack search is not as powerful as building your own RAG system:

```
Yin Wang articles
        |
        v
crawl markdown/html
        |
        v
chunk documents
        |
        v
embedding model
        |
        v
vector database
        |
        v
query: "王垠关于时间的观点"
        |
        v
semantic retrieval
```

Then you can ask:

```
"Find all places where Yin Wang discusses time,
including related ideas like life, existence, change, and consciousness."
```

A local implementation would be simple:

```python
from sentence_transformers import SentenceTransformer
import faiss

model = SentenceTransformer("BAAI/bge-large-en-v1.5")

docs = load_yinwang_articles()

embeddings = model.encode(docs)

index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)

query = "王垠关于时间是什么的思考"

q = model.encode([query])

scores, ids = index.search(q, 10)

for i in ids[0]:
    print(docs[i])
```

This would probably outperform Substack search for deep philosophical research.

For someone like you who already has:

* 8000+ AI notes
* Jekyll blog
* LLM infrastructure experience

a very natural project is:

```
personal knowledge engine

Markdown
   |
   v
chunking
   |
   v
embedding
   |
   v
FAISS / Qdrant
   |
   v
LLM answer with citations
```

Basically a personal "AI second brain".

References:

* ([Substack Support][1])
* ([Substack Support][2])

[1]: https://support.substack.com/hc/en-us/articles/4406018060692-How-do-I-find-a-Substack-publication?utm_source=chatgpt.com "How do I find a Substack publication? – Substack, Inc"
[2]: https://support.substack.com/hc/en-us/articles/15853567274772-Guide-to-your-Substack-Posts-page?utm_source=chatgpt.com "Guide to your Substack Posts page – Substack, Inc"
