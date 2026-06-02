---
audio: false
date: 2025-09-14
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: LibreChat Docker Compose Service Breakdown
translated: false
type: note
---

What you pasted is a `docker-compose.yaml` setup for running **LibreChat** along with its dependencies. Let me break it down clearly:

---

## High-Level View

The setup defines **6 services (containers)** that work together:

1. **LibreChat API/UI (`api`)**
2. **MongoDB (`mongodb`)**
3. **Meilisearch (`meilisearch`)**
4. **Postgres with pgvector (`vectordb`)**
5. **RAG API (`rag_api`)**
6. **Volumes for persistent storage**

These are all wired together using Docker Compose so that you can start everything with a single `docker-compose up`.

---

## Service Explanations

### 1. LibreChat API (`api`)

* **Container name:** `LibreChat`
* **Image:** `ghcr.io/danny-avila/librechat-dev:latest` (the dev build of LibreChat)
* **Ports:** Exposes `${PORT}` from `.env` to your host machine.
* **Dependencies:** Waits for `mongodb` and `rag_api` before starting.
* **Environment variables:**

  * `MONGO_URI`: Connection string for MongoDB.
  * `MEILI_HOST`: Points to Meilisearch service.
  * `RAG_API_URL`: Connects to the local RAG API container.
* **Volumes:**

  * `.env` file is mounted inside the container.
  * `images`, `uploads`, and `logs` are persisted locally so you don’t lose them when the container restarts.

👉 This is the main app you interact with (the LibreChat web/API service).

---

### 2. MongoDB (`mongodb`)

* **Container name:** `chat-mongodb`
* **Image:** `mongo` (official MongoDB image).
* **Purpose:** Stores chat data, user sessions, config, etc.
* **Command:** Runs `mongod --noauth` (no authentication).
* **Volumes:** `./data-node:/data/db` so your database persists outside the container.

---

### 3. Meilisearch (`meilisearch`)

* **Container name:** `chat-meilisearch`
* **Image:** `getmeili/meilisearch:v1.12.3`
* **Purpose:** Provides **fast full-text search** capabilities for LibreChat.
* **Environment variables:**

  * `MEILI_NO_ANALYTICS=true` (privacy).
  * `MEILI_MASTER_KEY` is pulled from `.env`.
* **Volumes:** `./meili_data_v1.12:/meili_data` for persistence.

---

### 4. Vector Database (`vectordb`)

* **Container name:** `vectordb`
* **Image:** `pgvector/pgvector:0.8.0-pg15-trixie` (Postgres with pgvector extension).
* **Purpose:** Stores embeddings for RAG (Retrieval Augmented Generation).
* **Environment:**

  * `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`.
* **Volume:** `pgdata2:/var/lib/postgresql/data` for persistence.

---

### 5. RAG API (`rag_api`)

* **Container name:** `rag_api`
* **Image:** `ghcr.io/danny-avila/librechat-rag-api-dev-lite:latest`
* **Purpose:** Handles RAG workflows — retrieving documents and augmenting model responses with external knowledge.
* **Environment:**

  * `DB_HOST=vectordb` (connects to Postgres vector DB).
  * `RAG_PORT` defaults to `8000`.
* **Depends on:** `vectordb`.
* **Env file:** Reuses your `.env`.

---

### 6. Volumes

* **`pgdata2`** → Persistent data for Postgres/pgvector.
* Other volumes like `./meili_data_v1.12`, `./data-node`, and mounted directories (`images`, `uploads`, `logs`) ensure your data survives restarts.

---

## How They Work Together

1. **LibreChat (UI/API)** is the central service you interact with.
2. It stores **chat/session data in MongoDB**.
3. It queries **Meilisearch** for text search features.
4. For RAG (document retrieval), LibreChat calls **rag\_api**.
5. The **RAG API** fetches vector embeddings from **vectordb (Postgres + pgvector)**.
6. Everything persists on local volumes, so data is not lost when containers restart.

---

✅ In short:

* **MongoDB** → chat/user data
* **Meilisearch** → fast keyword search
* **Postgres+pgvector** → vector embeddings for RAG
* **RAG API** → retrieval augmentation layer
* **LibreChat** → the app tying it all together

---

Do you want me to also show you a **diagram-style flow (textual)** of how requests move through these containers (from you → LibreChat → RAG API → Vector DB)? That might make it even clearer.
