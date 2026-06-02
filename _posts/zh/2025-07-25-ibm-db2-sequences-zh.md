---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast:free
title: IBM DB2 序列使用指南
translated: true
type: note
---

### IBM DB2 序列使用与 NEXT VALUE FOR

在 IBM DB2 中，`NEXT VALUE FOR` 用于从序列中获取下一个值，该序列可生成唯一的递增数字。序列适用于生成主键或其他唯一标识符。

#### 示例：创建并使用序列

1. **创建序列**（在 DB2 环境中运行一次）：

   ```sql
   CREATE SEQUENCE my_sequence
   START WITH 1
   INCREMENT BY 1
   NO CYCLE;
   ```

   - 这将创建一个名为 `my_sequence` 的序列，从 1 开始，每次递增 1。

2. **在 INSERT 语句中使用序列**以获取下一个值：

   ```sql
   INSERT INTO employees (id, name, department)
   VALUES (NEXT VALUE FOR my_sequence, 'Alice Johnson', 'Engineering');
   ```

   - 这将插入一个新行，其中 `id` 为序列的下一个值（例如，首次使用为 1，下次为 2，依此类推）。

#### 关键注意事项

- 也可以在 SELECT 查询中使用：`SELECT NEXT VALUE FOR my_sequence FROM SYSIBM.SYSDUMMY1;`
- 序列独立于表，如果需要可以在多个表之间共享。
- 更多详细信息，请参阅 IBM DB2 关于序列的文档。如果您需要其他序列函数（如 `PREVIOUS VALUE FOR`）的示例，请告诉我！
