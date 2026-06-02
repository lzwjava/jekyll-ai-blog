---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 在IBM DB2中创建索引
translated: true
type: note
---

### 在 IBM DB2 中创建索引

IBM DB2 支持通过索引优化查询性能，实现更快的数据检索。可以在表的一个或多个列上创建索引。下面我将介绍基础知识，包括唯一索引和多列（复合）索引。请注意，"联合索引"并非 DB2 文档中的标准术语——它可能指代复合索引（涵盖多个键）或是对查询中联合操作的误解。如果您有其他特定含义，请提供更多细节！

#### 基础索引创建

使用 `CREATE INDEX` 语句在单列上构建简单索引，可加速对该列的搜索、排序和连接操作。

**语法：**

```sql
CREATE INDEX 索引名称
ON 表名 (列名 [ASC | DESC]);
```

**示例：**

```sql
CREATE INDEX idx_employee_id
ON employees (employee_id ASC);
```

- `ASC` 表示升序排序（默认值）；使用 `DESC` 表示降序
- 索引默认允许重复值（非唯一索引）

#### 唯一索引（强制唯一键约束）

唯一索引确保被索引列不存在重复值，类似于唯一约束。当定义主键或唯一约束时，DB2 会自动创建唯一索引。

**语法：**

```sql
CREATE UNIQUE INDEX 索引名称
ON 表名 (列名 [ASC | DESC]);
```

**示例：**

```sql
CREATE UNIQUE INDEX uidx_email
ON users (email ASC);
```

- 此索引将阻止插入重复邮箱
- 要实现部分唯一性（如忽略空值），可添加 `WHERE NOT NULL`：

  ```sql
  CREATE UNIQUE WHERE NOT NULL INDEX uidx_email
  ON users (email ASC);
  ```

- 可包含非键列以支持查询覆盖：

  ```sql
  CREATE UNIQUE INDEX uidx_email
  ON users (email ASC) INCLUDE (first_name, last_name);
  ```

#### 复合索引（多键索引，例如包含两个或多个列）

复合索引（或多列索引）涵盖多个键，适用于基于列组合进行过滤/连接的查询。列的顺序很重要——应将选择性最高的列放在首位。

**语法：**

```sql
CREATE INDEX 索引名称
ON 表名 (列1 [ASC | DESC], 列2 [ASC | DESC], ...);
```

**示例（双键索引）：**

```sql
CREATE INDEX idx_order_date_customer
ON orders (order_date ASC, customer_id DESC);
```

- 此索引可优化类似 `SELECT * FROM orders WHERE order_date > '2023-01-01' AND customer_id = 123;` 的查询
- 创建唯一复合索引：添加 `UNIQUE` 关键字（例如 `CREATE UNIQUE INDEX ...`）

#### 补充建议

- **验证索引：** 使用 `SELECT * FROM SYSCAT.INDEXES WHERE TABSCHEMA = '您的模式名' AND TABNAME = '您的表名';`
- **删除索引：** `DROP INDEX 索引名称;`
- 索引会占用存储空间并降低插入/更新速度——请审慎使用
- 对于分区表或高级选项（如聚簇索引），请参考 DB2 官方文档

[Db2 CREATE INDEX 语句](https://www.ibm.com/docs/en/db2-for-zos/12.0.0?topic=statements-create-index)
[Db2 唯一索引](https://www.ibm.com/docs/en/db2-for-zos/12.0.0?topic=attributes-unique-indexes)
[Db2 复合索引示例](https://stackoverflow.com/questions/21597015/composite-index-creation-in-db2)
[Db2 唯一索引教程](https://www.db2tutorial.com/db2-index/db2-unique-index/)
