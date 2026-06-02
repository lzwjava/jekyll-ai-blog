---
audio: false
generated: true
image: false
lang: en
layout: post
title: DeepWiki's Indexing Process Explained
translated: false
type: note
---

Question: What does DeepWiki do when it shows “Indexing in Progress” for a repository?

Answer:

This message means the system is currently processing your repository so it can be queried like a “knowledge wiki”.

In simple terms, **DeepWiki is building a searchable AI index of your codebase and documentation**. During the “indexing in progress” stage, it typically does the following:

### 1. Parse the repository

It scans your project files (code, markdown, configs, docs) and breaks them into structured chunks.

### 2. Build semantic embeddings

Each chunk is converted into vector representations so the system can understand meaning, not just keywords. This enables semantic search like “where is authentication handled?” even if that exact phrase doesn’t exist.

### 3. Create a retrieval index (RAG system)

The chunks are stored in a retrieval system (commonly used in RAG: Retrieval-Augmented Generation). This allows later AI queries to fetch relevant code sections quickly.

### 4. Prepare wiki-style navigation

It organizes relationships between files, modules, and concepts so the system can answer questions like:

* “How does login work?”
* “Where is the API client defined?”
* “What does this function do?”

### 5. Final availability

Once complete, you get an AI-powered “wiki layer” on top of your repo, where you can ask natural-language questions about your codebase.

---

### Why it says “queued” and “2–10 minutes”

* Your repo is waiting in a processing queue (you are position #1)
* Larger repositories take longer because they require more parsing and embedding generation

---

In short: **DeepWiki is turning your repository into a queryable AI knowledge system, and indexing is the setup step that makes that possible.**
