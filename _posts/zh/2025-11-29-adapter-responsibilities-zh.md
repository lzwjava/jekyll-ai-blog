---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Android开发中的适配器职责
translated: true
type: note
---

**正确答案：B. 为每个条目提供数据并创建视图**

**Adapter** 是核心组件，它在数据源（如 List、Array、Cursor 或任何集合）与 RecyclerView/ListView 之间充当桥梁。

其主要职责包括：

- 告知 RecyclerView/ListView **存在多少条目**（通过 RecyclerView.Adapter 的 `getItemCount()` 方法）。
- 在需要时**创建**每个条目的视图持有者（通过 `onCreateViewHolder()` 方法）。
- 将数据**绑定**到特定位置的视图（通过 `onBindViewHolder()` 方法）。
- 在请求时提供指定位置的实际数据条目（某些适配器中的 `getItem()` 方法）。

简而言之：适配器负责提供数据，并生成/绑定代表每个列表条目的视图。

### 选项快速比较

- **A. 管理布局填充** → 部分正确但不完整。适配器确实会在 `onCreateViewHolder()` 中填充布局，但这只是其职责的一小部分。
- **B. 为每个条目提供数据并创建视图** → 正确且完整的描述。
- **C. 处理网络请求** → 错误，该功能由其他组件（如 ViewModel、Repository 等）实现。
- **D. 存储用户偏好** → 错误，该功能由 SharedPreferences 或 DataStore 实现。

因此，**B** 是正确答案！
