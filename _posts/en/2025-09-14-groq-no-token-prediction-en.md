---
audio: false
date: 2025-09-14
generated: true
image: false
lang: en
layout: post
model: openai/gpt-oss-120b
title: GROQ Does Not Predict Tokens
translated: false
type: note
---

## Short answer

**GROQ itself never “predicts the next token”.**
It is a **database‑style query language** that selects, filters, and reshapes the **structured JSON documents** you have stored in Sanity.
The “semantic” power you see in Sanity‑based products comes from **two separate things**:

| What you’re asking about | How it is actually done |
|--------------------------|--------------------------|
| **Understanding the meaning of the content you stored (e.g., “show me all posts about React hooks”)** | GROQ uses **indexes, column‑store scans and Boolean predicates** to find the right documents. The “meaning” is encoded in the **explicit fields** you have (tags, categories, references, author, etc.) – no neural net needed. |
| **Generating new text or completing a sentence (“write a summary of this article”)** | You have to call a **large language model (LLM)** – OpenAI, Anthropic, Cohere, a self‑hosted transformer, etc. The LLM does the heavy‑weight tensor‑matrix math (K‑Q‑V attention, softmax, etc.). The result is then **written back** to Sanity (or used as a prompt) via a normal API call. |

So the short answer is: **Sanity’s speed comes from a classic, highly optimised query engine; any “next‑token prediction” or deep semantic understanding is performed **outside** of GROQ, by an external transformer‑based service.**

Below is a more detailed walk‑through that explains why this separation exists, how the two pieces fit together, and what you can do if you need *both* fast content retrieval **and** high‑quality language‑model predictions.

---

## 1. What GROQ *actually* does

| Feature | What it looks like to the developer | How it works under the hood (no tensors) |
|---------|--------------------------------------|------------------------------------------|
| **Filtering** (`*[_type == "post" && publishedAt < now()]`) | “Give me every post that is already published.” | Scans the `_type` and `publishedAt` **columns** of the Content Lake. Uses a B‑tree/bitmap index to jump directly to matching rows. |
| **Projection** (`{title, slug, author->{name}}`) | “Only return these fields, and resolve the author reference.” | Reads only the `title`, `slug`, and `author._ref` columns, then does a **join** by looking up the referenced author document (again column‑wise). |
| **Ordering & slicing** (`|order(publishedAt desc)[0...10]`) | “Give me the 10 newest posts.” | Uses the sorted `publishedAt` column to produce a **pre‑ordered stream**; stops after 10 items (no need to materialise the rest). |
| **Full‑text match** (`title match "react*"`) | “Find titles that start with ‘react’.” | Leverages a **text index** (inverted index) that lives alongside the column store, similar to how Elasticsearch works, but built directly into the lake. |
| **Streaming** | Results start arriving after the first few rows are ready. | The engine pipelines: source → filter → map → serializer → HTTP response, sending bytes as soon as they’re produced. |

All of those operations are **deterministic, integer‑based, and I/O‑bounded** – they never require matrix multiplication or gradient calculations. That’s why a pure GROQ query typically finishes in **single‑digit to low‑double‑digit milliseconds**.

---

## 2. Where “semantic” and “next‑token” capability *does* come from

| Use‑case | Where the LLM lives | Typical flow (sanity‑centric) |
|----------|---------------------|------------------------------|
| **Summarisation** | `POST https://api.openai.com/v1/chat/completions` (or any other LLM endpoint) | 1️⃣ Use GROQ to fetch the article body. <br>2️⃣ Send that text as a prompt to the LLM. <br>3️⃣ Receive the generated summary and write it back (`PATCH /documents/{id}`) via the Sanity API. |
| **Semantic search** | Vector‑DB (Pinecone, Weaviate, Qdrant) + embeddings model (OpenAI `text‑embedding‑ada‑002`, etc.) | 1️⃣ Export candidate docs → embed once (offline). <br>2️⃣ Store embeddings in a vector DB. <br>3️⃣ At query time: embed the user query → nearest‑neighbour search → get list of `_id`s → **GROQ** `*[_id in $ids]{title,slug}` for the final payload. |
| **Auto‑tagging / classification** | Small classifier model (could be a fine‑tuned transformer or even a logistic‑regression on top of embeddings) | 1️⃣ Webhook fires on document creation. <br>2️⃣ Serverless function calls the classifier → receives tags. <br>3️⃣ Function patches the document with the tags (fast GROQ mutation). |
| **Chat‑assistant that references your content** | LLM for dialogue + GROQ to fetch context | 1️⃣ User asks “What did we say about caching?” <br>2️⃣ Backend runs a GROQ query that pulls all relevant sections. <br>3️⃣ Those sections are inserted into the prompt sent to the LLM. <br>4️⃣ LLM returns a response; the response can be displayed or stored. |

**Key point:** The *semantic* heavy lifting (embeddings, attention, token prediction) is performed **by the LLM service**, not by GROQ. GROQ’s job in those pipelines is simply to **fetch the right pieces of structured data** (or to store the output).

---

## 3. Why the separation makes sense (performance & architecture)

| Reason | Explanation |
|--------|--------------|
| **Specialisation** | A content store is optimized for *exact* matches, range scans, and fast projection. A transformer is optimized for *probabilistic* language modelling. Trying to make one system do both well leads to compromises. |
| **Cost control** | Running a transformer on every request would be expensive (GPU minutes). By keeping GROQ cheap, you only pay for the AI part when you actually need it. |
| **Scalability** | GROQ queries can be cached at CDN edges, sharded across many workers, and served with sub‑30 ms latency. LLM inference can be off‑loaded to a separate autoscaling pool that may be region‑specific. |
| **Flexibility** | You can swap the LLM vendor (OpenAI → Anthropic → locally hosted) without changing any GROQ code. The query language stays stable. |
| **Security & compliance** | Structured content stays in your own Sanity project; only the *derived* embeddings or prompts leave the system, making it easier to audit data flows. |

---

## 4. If you *do* want token‑level prediction inside Sanity, how would it look?

1. **Create a serverless function** (e.g., Vercel, Cloudflare Workers, AWS Lambda) that receives a request like `POST /api/generate`.
2. Inside that function:
   ```js
   // 1️⃣ Pull the context you need
   const ctx = await sanityClient.fetch(`*[_id == $docId]{title, body}[0]`, {docId});

   // 2️⃣ Build a prompt (maybe with few‑shot examples)
   const prompt = `Summarize this article:\n\n${ctx.body}\n\nSummary:`;

   // 3️⃣ Call the LLM (OpenAI example)
   const resp = await fetch('https://api.openai.com/v1/chat/completions', {
     method: 'POST',
     headers: { 'Authorization': `Bearer ${process.env.OPENAI_KEY}`, 'Content-Type': 'application/json' },
     body: JSON.stringify({
       model: 'gpt-4o-mini',
       messages: [{role: 'user', content: prompt}],
       temperature: 0.2
     })
   });
   const {content} = (await resp.json()).choices[0].message;

   // 4️⃣ Store the result back in Sanity (fast GROQ mutation)
   await sanityClient.patch(docId).set({summary: content}).commit();
   ```
3. The **latency you see** in the client is the sum of:
   - Network round‑trip to the LLM (often 30‑120 ms if the LLM is on a fast edge location).
   - LLM inference time (depends on model size; small models < 50 ms, large GPT‑4‑class > 300 ms).
   - The GROQ mutation (≈ 5‑10 ms).

If you need sub‑100 ms total latency for a *chat* UI, you typically **run the model at the edge** (e.g., Cloudflare Workers‑AI, Lambda@Edge, or a locally hosted 8‑bit model) so that the network hop is essentially zero. The GROQ part remains negligible.

---

## 5. How to get *good* semantics without paying for a full‑blown transformer on every request

| Technique | What it buys you | Approximate cost (as of 2025) |
|-----------|------------------|------------------------------|
| **Pre‑computed embeddings + vector DB** | Fast “semantic similarity” look‑ups (< 5 ms per query). | One‑time embedding cost (≈ $0.0001 per 1 k tokens with OpenAI), plus cheap vector‑DB storage. |
| **Fine‑tuned small model (e.g., `distilbert-base-uncased` quantised to int8)** | Good classification / tagging on‑device, < 10 ms inference on a modern CPU. | Free if you host it yourself; otherwise $0.02‑$0.05 per 1 k tokens on managed services. |
| **Prompt‑engineering + few‑shot examples** | Improves the accuracy of a *large* LLM without extra fine‑tuning. | Same per‑token cost as the LLM, but you can keep prompts short (≤ 200 tokens) to stay cheap. |
| **Hybrid retrieval‑augmented generation (RAG)** | Combine exact keyword match (GROQ) with a small LLM for the final answer. | You only call the LLM on a *few* retrieved documents, reducing token count dramatically. |

**Best practice:**
- **Use GROQ first** to *narrow* the candidate set (e.g., fetch all posts of a certain type, or all docs that contain a specific tag).
- **If you need a “semantic” ranking**, run those candidates through a *vector similarity* step (still cheap).
- **Only then** call the LLM for generation or summarisation on the *top‑N* items.

---

## 6. Frequently asked “What about next‑token prediction?”

| Question | Answer |
|----------|--------|
| *“Can GROQ autocomplete a field as I type?”* | No. GROQ returns data; it does not generate new tokens. You would need a separate autocomplete service (e.g., OpenAI `gpt‑3.5‑turbo` with `stream:true`) that you call from your UI, then write the chosen value back to Sanity with a mutation. |
| *“Do Sanity’s built‑in UI components use AI to suggest content?”* | The default Studio editor does **not** use an LLM. Some community plugins (e.g., `sanity-plugin-asset-source-llm`) call external models to generate alt‑text or titles, but that is optional and external. |
| *“If I store the output of a language model in Sanity, will GROQ understand it better?”* | The model’s output is just more structured text. GROQ can filter on it (e.g., `summary match "react"`), but any *semantic* understanding still comes from how you **structured** the data (tags, categories, embeddings) and not from GROQ itself. |
| *“Can I train a model inside Sanity?”* | No. Sanity is a CMS, not a training platform. You can store training data (datasets, annotation JSON) and trigger external training jobs via webhooks, but the model runs elsewhere. |

---

## 7. TL;DR Checklist for a “fast, semantically aware” product

| ✅ Goal | How to achieve it |
|--------|-------------------|
| **Instant content lookup** | Use pure GROQ queries with proper indexes (`_type`, `publishedAt`, custom fields). |
| **Semantic similarity / search** | Pre‑compute embeddings → store in a vector DB → at query time: embed the user query → vector‑search → feed resulting IDs into a GROQ filter. |
| **On‑the‑fly text generation (summaries, copy‑writing, chat)** | Call an external LLM (OpenAI, Anthropic, self‑hosted) *after* you have fetched the needed context with GROQ. Write the result back via a normal mutation. |
| **Low latency for the AI part** | • Quantise the model or use a small hosted model.<br>• Deploy the inference at the edge (Cloudflare Workers‑AI, Vercel Edge Functions).<br>• Cache recent embeddings or LLM responses when possible. |
| **Keep costs predictable** | • Separate the two layers (GROQ = cheap, token‑based LLM = pay‑as‑you‑go).<br>• Batch embeddings offline (once per document).<br>• Use `limit`/`slice` in GROQ to avoid pulling massive payloads into the LLM. |

---

### Bottom line

- **GROQ ≠ transformer.** It is a *deterministic query engine* that can retrieve data in milliseconds because it works on a column‑store with indexes and streaming execution.
- **Accurate semantics or next‑token generation** are **outside the scope** of GROQ; they come from *separate* language‑model services that you call when you need them.
- By **combining** the two (fast GROQ for data plumbing + a modern LLM for generative or similarity tasks) you get a system that is both **high‑performance** and **semantically powerful**.

If you have a concrete workflow you’d like to optimise—e.g., “autocomplete product descriptions while the editor types” or “search my knowledge base with natural‑language queries”—let me know and I can sketch a concrete architecture diagram and sample code. Happy building!
