---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Android 持久化键值存储类
translated: true
type: note
---

问题：在 Android 中，哪一个类用于简单的 key-value 持久化存储？

A) SQLiteDatabase
B) FileOutputStream
C) SharedPreferences
D) ContentValues

答案：

正确答案是 **C) SharedPreferences**。

**解释**：

- **SharedPreferences** 是专门为存储和检索以 key-value 对形式存在的少量原始数据（例如 boolean, float, int, long, string 和 string sets）而设计的 Android API。它非常轻量、易于使用，并且可以在应用重启和设备重启后保持数据持久化。数据存储在应用私有目录下的 XML 文件中。

- **SQLiteDatabase** 用于使用 SQL 查询的结构化关系型数据库存储，适用于更大或更复杂的数据集，而不是简单的 key-value 对。

- **FileOutputStream** 是一个底层的 API，用于将原始字节写入文件，需要手动处理文件 I/O 和数据序列化，并非专为简单的 key-value 存储而设计。

- **ContentValues** 是一个辅助类，用于临时保存 key-value 对，以便通过 ContentResolver 或 SQLiteDatabase 在 SQLite 数据库中插入或更新行；它本身不提供持久化存储。

SharedPreferences 是 Android 应用中进行简单持久化 key-value 存储的标准且推荐的选择。
