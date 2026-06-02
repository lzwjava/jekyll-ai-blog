---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Creating Indexes in IBM DB2
translated: false
type: note
---

### Creating Indexes in IBM DB2

IBM DB2 supports indexes to optimize query performance by allowing faster data retrieval. Indexes can be created on one or more columns of a table. Below, I'll cover the basics, including unique indexes and multi-column (composite) indexes. Note that "union index" isn't a standard term in DB2 documentation— it might refer to a composite index (covering multiple keys) or a misunderstanding of union operations in queries. If you meant something else, provide more details!

#### Basic Index Creation
Use the `CREATE INDEX` statement to build a simple index on a single column. This speeds up searches, sorts, and joins on that column.

**Syntax:**
```sql
CREATE INDEX index_name
ON table_name (column_name [ASC | DESC]);
```

**Example:**
```sql
CREATE INDEX idx_employee_id
ON employees (employee_id ASC);
```

- `ASC` sorts in ascending order (default); use `DESC` for descending.
- Indexes are non-unique by default, allowing duplicate values.

#### Unique Index (Enforcing Unique Keys)
A unique index ensures no duplicate values in the indexed column(s), similar to a unique constraint. DB2 automatically creates a unique index when you define a primary key or unique constraint.

**Syntax:**
```sql
CREATE UNIQUE INDEX index_name
ON table_name (column_name [ASC | DESC]);
```

**Example:**
```sql
CREATE UNIQUE INDEX uidx_email
ON users (email ASC);
```

- This prevents inserting duplicate emails.
- For partial uniqueness (e.g., ignore NULLs), add `WHERE NOT NULL`:
  ```sql
  CREATE UNIQUE WHERE NOT NULL INDEX uidx_email
  ON users (email ASC);
  ```
- You can include non-key columns for query coverage:
  ```sql
  CREATE UNIQUE INDEX uidx_email
  ON users (email ASC) INCLUDE (first_name, last_name);
  ```

#### Composite Index (Multiple Keys, e.g., Two or More Columns)
A composite (or multi-column) index covers multiple keys, useful for queries filtering/joining on combinations of columns. The order of columns matters—place the most selective column first.

**Syntax:**
```sql
CREATE INDEX index_name
ON table_name (column1 [ASC | DESC], column2 [ASC | DESC], ...);
```

**Example (Two Keys):**
```sql
CREATE INDEX idx_order_date_customer
ON orders (order_date ASC, customer_id DESC);
```

- This optimizes queries like `SELECT * FROM orders WHERE order_date > '2023-01-01' AND customer_id = 123;`.
- For unique composite: Add `UNIQUE` (e.g., `CREATE UNIQUE INDEX ...`).

#### Additional Tips
- **Verify Index:** Use `SELECT * FROM SYSCAT.INDEXES WHERE TABSCHEMA = 'YOUR_SCHEMA' AND TABNAME = 'YOUR_TABLE';`.
- **Drop Index:** `DROP INDEX index_name;`.
- Indexes consume storage and slow inserts/updates—use them judiciously.
- For partitioned tables or advanced options (e.g., clustering), refer to DB2 docs.

[Db2 CREATE INDEX Statement](https://www.ibm.com/docs/en/db2-for-zos/12.0.0?topic=statements-create-index)
[Db2 Unique Indexes](https://www.ibm.com/docs/en/db2-for-zos/12.0.0?topic=attributes-unique-indexes)
[Db2 Composite Indexes Example](https://stackoverflow.com/questions/21597015/composite-index-creation-in-db2)
[Db2 Unique Index Tutorial](https://www.db2tutorial.com/db2-index/db2-unique-index/)
