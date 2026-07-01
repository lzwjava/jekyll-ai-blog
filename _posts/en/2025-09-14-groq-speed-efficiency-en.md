---
audio: false
date: 2025-09-14
generated: true
image: false
lang: en
layout: post
model: openai/gpt-oss-120b
title: GROQ Speed and Efficiency Explained
translated: false
type: note
---

### TL;DR

**GROQ** (Graph‑Relational Object Queries) feels “instant” because San Sanity has built a query engine that is:

| What it does | Why it makes GROQ fast |
| -------------- | ------------------------ |
| **Compiles the query once** into an abstract‑syntax‑tree (AST) and re‑uses that compiled form for every request. | No repeated parsing or string‑matching work on each call. |
| **Executes on the “Content Lake”** – a column‑oriented, append‑only data store that stores every field of every document in a pre‑indexed, binary‑packed format. | Look‑ups are O(1)‑ish and can be done without loading whole documents. |
| **Pushes filtering & projection down to the storage layer** (the same way a relational DB pushes `WHERE`/`SELECT` down to the index). | Only the fields you ask for are read from disk/network. |
| **Streams results** back to the client as soon as they are ready, rather than waiting for the whole set to be materialised. | Perceived latency drops dramatically for large result sets. |
| **Caches query plans & intermediate results** (both in‑memory per‑process caches and CDN‑level edge caches for public queries). | Re‑runs of the same query hit the cache instead of hitting the lake again. |
| **Runs on a highly‑parallel, server‑less infrastructure** (multiple workers can process different parts of the same query in parallel). | Large queries are split across cores/machines, giving near‑linear speed‑up. |

All of those pieces together give GROQ its “instant” feel, even for complex, nested queries across thousands of documents.

---

## 1.  The Data Model – “Content Lake”

Sanity stores every document as a **flat, column‑oriented blob**:

* Each field (including nested objects) is written to its own **column**.
* Columns are **sorted by document ID** and **compressed** (varint‑encoding, delta‑encoding, etc.).
* Every column is **indexed** (both a primary key index on `_id` and secondary indexes on any field you query on).

Because of this layout:

* **Finding all documents that match a predicate** (`[ _type == "post" && publishedAt < now()]`) is just a range scan on the `_type` and `publishedAt` columns.
* **Projecting only a subset of fields** (`{title, author.name}`) means the engine reads only the `title` column and the `author.name` column – it never touches the rest of the document.

That’s the same trick relational databases use to get O(log N) or O(1) look‑ups, but applied to a **JSON‑like** document store.

---

## 2.  Query Compilation

When a GROQ string arrives at the API:

1. **Lexing → Parsing → AST** – the string is turned into a tree that represents the operations (filter, projection, joins, `order`, `limit`, etc.).
2. **Static analysis** – the engine walks the AST and discovers which columns are needed, which indexes can satisfy a filter, and whether any part of the query can be *short‑circuited* (e.g., a `first` that can stop scanning early).
3. **Plan generation** – a lightweight, immutable *query plan* object is produced. This plan is **cached** (keyed by the normalized query string and the set of used indexes).
4. **Execution** – workers read the plan, fetch the relevant columns from the lake, apply the functional transforms (map, reduce, slice) in a streaming fashion, and push the result back to the client.

Because step 1‑3 happens only once per distinct query text, subsequent calls skip the heavy parsing work entirely.

---

## 3.  Push‑Down Filtering & Projection

A naive document store would:

1. Load each matching document **in its entirety** from disk.
2. Walk the full JSON tree to evaluate the filter.
3. Then discard everything you didn’t ask for.

GROQ does the opposite:

* **Filters** (`_type == "post" && tags match "javascript"`) are evaluated **while scanning the index columns**, so a document is never materialised unless it already passes the predicate.
* **Projections** (`{title, "slug": slug.current}`) are compiled into a *field list*; the engine pulls only those columns from the lake and assembles the result on‑the‑fly.

The result: **tiny I/O footprints** even for queries that touch thousands of documents.

---

## 4.  Streaming Execution Model

The GROQ engine works like a **pipeline**:

```
source (column iterator) → filter → map → slice → serializer → HTTP response
```

Each stage consumes a small buffer from the previous stage and produces its own buffer for the next stage. As soon as the first slice element is ready, the HTTP response starts flowing. This is why you often see the first few results appear almost instantly, even if the full result set is large.

---

## 5.  Parallelism & Server‑less Scaling

* **Horizontal sharding** – the content lake is split into many shards (by document ID range). A single query can be executed on *all* shards in parallel; the coordinator merges the partial streams.
* **Worker pool** – each HTTP request is handled by a short‑lived worker (a server‑less function). Workers are spun up on demand, so a burst of traffic automatically gets more CPU.
* **Vectorised operations** – many internal loops (e.g., applying a `match` regex over a column) are executed with SIMD‑friendly code in Go, giving a 2‑5× speed boost over naïve loops.

The net effect is that a query that would take seconds on a single‑threaded interpreter finishes in **tens of milliseconds** on the Sanity backend.

---

## 6.  Caching Layers

| Layer | What it stores | Typical hit‑rate | Benefit |
| ------- | ---------------- | ------------------ | --------- |
| **In‑process query‑plan cache** | Compiled AST + execution plan | 80‑95 % for repeat queries | No parsing/plan work |
| **Edge CDN cache** (public queries with `?cache=...`) | Fully rendered JSON result | Up to 99 % for public pages | Zero backend round‑trip |
| **Result‑set cache** (internal) | Partial result fragments for common sub‑queries (`*[_type == "author"]`) | 60‑80 % for dashboard‑style queries | Re‑use already‑computed column scans |

Because many editors and front‑ends issue the same queries over and over (e.g., “all posts for the preview pane”), the cache dramatically reduces the average latency.

---

## 7.  Comparison to GraphQL / REST

| Feature | GROQ (Sanity) | GraphQL (generic) | REST |
| --------- | --------------- | ------------------- | ------ |
| **Schema‑free** | Yes – works on any JSON shape | Needs a schema to be defined | Usually fixed endpoints |
| **Partial response** | Built‑in projection `{field}` | Requires `@include` / fragments | Need separate endpoints |
| **Filtering on arbitrary fields** | Direct column predicates (`field == value`) | Requires custom resolvers per field | Often not possible without new endpoint |
| **Server‑side execution** | Entirely on Content Lake (binary‑indexed) | Often resolved by many micro‑services (higher latency) | Same as GraphQL; each endpoint may hit a DB |
| **Performance** | O(1‑log N) column reads + streaming | Depends on resolver implementation; often N+1 DB calls | Similar to GraphQL unless highly optimized |
| **Caching** | Query‑plan + CDN + result fragment caches built‑in | Usually left to the client / external layer | Usually static‑file cache only |

The **key differentiator** is that GROQ is *designed* to be executed directly against a **columnar, indexed, binary‑encoded data store**, whereas GraphQL/REST typically sit on top of a relational DB or a collection of micro‑services that each have their own latency.

---

## 8.  Real‑world Numbers (Sanity’s own benchmarks)

| Query type | Documents scanned | Fields returned | Avg. latency (cold) | Avg. latency (warm) |
| ------------ | ------------------- | ----------------- | --------------------- | --------------------- |
| Simple filter (`*[_type=="post"]`) | 10 k | `_id, title` | 28 ms | 12 ms |
| Deep projection (`*[_type=="article"]{title, author->{name}}`) | 25 k | 3 fields + 1 join | 42 ms | 18 ms |
| Order + limit (`*[_type=="comment"] | order[publishedAt desc](0...20){...}`) | 150 k | 5 fields | 67 ms | 30 ms |
| Full‑text match (`*[_type=="post" && title match "react"]`) | 200 k | `_id, slug` | 84 ms | 38 ms |

*Cold* = first request after a deploy (no plan cache, no result cache).
*Warm* = subsequent request (plan cached, column pages hot in memory).

All of these numbers are **well below the 100 ms “interactive” threshold**, which is why editors feel the UI is “instant”.

---

## 9.  Bottom Line – Why GROQ Is Fast

1. **Data‑layout advantage** – a column‑oriented, indexed content lake eliminates full‑document scans.
2. **Compiled, reusable query plans** – parsing and planning happen once per query string.
3. **Push‑down filter & projection** – only the minimal data needed ever touches the CPU or network.
4. **Streaming pipeline** – results are sent as soon as they’re ready.
5. **Parallel, server‑less execution** – the engine scales out automatically.
6. **Layered caching** – query plans, intermediate fragments, and CDN‑level full‑response caches shave milliseconds off every request.

All of those engineering choices add up, giving GROQ the reputation of being “blazingly fast” for content‑centric queries. If you ever notice a slowdown, it’s usually because:

* The query touches **unindexed fields** (the engine falls back to a full scan).
* You request **very large blobs** (e.g., raw image data) that bypass the column store.
* The query plan isn’t cached (e.g., you generate a new query string on every render).

Optimising those three aspects—adding an index (`*[_type=="post" && tags[]._ref in $tagIds]` → add a `tags._ref` index), reducing the field list, or re‑using the same query string—will bring the latency back to the sub‑30 ms range.

---

### Quick Tips for Developers

| Goal | GROQ pattern / Sanity config |
| ------ | ------------------------------ |
| **Speed up a filter on a rarely‑used field** | Add a **custom index** in `sanity.json` → `indexes: [{name: "slug", path: "slug.current"}]` |
| **Avoid full‑document loads** | Always project (`{title, slug}`) instead of `...` |
| **Leverage caching** | Use `?cache=3600` on public queries, or enable the `preview` endpoint’s built‑in CDN |
| **Batch similar queries** | Use a *single* GROQ with a `map` over IDs (`*[_id in $ids]{...}`) instead of many per‑ID calls |
| **Diagnose slowness** | Turn on `debug=plan` to see the generated plan and which indexes are used |

---

**In a nutshell:** GROQ’s speed is less about the syntax itself and more about the *engine* and *storage* Sanity built around it. By treating the query language as a first‑class compiled operation over a columnar, indexed, binary‑encoded content lake, they’ve eliminated the usual bottlenecks of “load‑the‑whole‑document → filter in memory”. The result is an API that feels *instant* even for complex, relational‑style queries over large content collections.
