---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Adapter Responsibilities in Android Development
translated: false
type: note
---

**Correct answer: B. Provide data and create views for each item**

The **Adapter** is the core component that acts as a bridge between your data source (e.g., a List, Array, Cursor, or any collection) and the RecyclerView/ListView.

Its main responsibilities are:

- Telling the RecyclerView/ListView **how many items** exist (`getItemCount()` in RecyclerView.Adapter).
- **Creating** the view holder for each item when needed (`onCreateViewHolder()`).
- **Binding** the data to the views for a specific position (`onBindViewHolder()`).
- Providing the actual data item for a position when requested (`getItem()` in some adapters).

In short: The adapter supplies the data and generates/binds the views that represent each list item.

### Quick comparison of the options:
- **A. Manage layout inflation** → Partially true but incomplete. The adapter *does* inflate layouts inside `onCreateViewHolder()`, but that’s just one small part of its job.
- **B. Provide data and create views for each item** → Correct and complete description.
- **C. Handle network requests** → No, that’s done elsewhere (ViewModel, Repository, etc.).
- **D. Store user preferences** → No, that’s SharedPreferences or DataStore.

So yes, **B** is the right answer!
