---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Creating Foreign Keys in Db2
translated: false
type: note
---

### Creating Foreign Keys in IBM Db2

Foreign keys in Db2 enforce referential integrity by linking a column (or set of columns) in one table (the child table) to the primary key or unique key in another table (the parent table). This ensures that values in the child table match existing values in the parent table, preventing orphaned records.

You can define foreign keys either during table creation using `CREATE TABLE` or by adding them to an existing table using `ALTER TABLE`. The syntax is standard SQL and works across Db2 platforms (e.g., LUW, z/OS).

#### 1. Defining a Foreign Key During Table Creation (`CREATE TABLE`)

Use the `FOREIGN KEY` clause within the column definitions or at the end of the table definition.

**Basic Syntax:**

```
CREATE TABLE child_table (
    child_column1 datatype,
    foreign_key_column datatype,
    -- Other columns...
    CONSTRAINT constraint_name
    FOREIGN KEY (foreign_key_column)
    REFERENCES parent_table (parent_key_column)
);
```

**Example:**
Assume you have a `departments` table with a primary key `dept_id`:

```
CREATE TABLE departments (
    dept_id INTEGER NOT NULL PRIMARY KEY,
    dept_name VARCHAR(50)
);
```

Now create an `employees` table with a foreign key referencing `dept_id`:

```
CREATE TABLE employees (
    emp_id INTEGER NOT NULL PRIMARY KEY,
    emp_name VARCHAR(100),
    dept_id INTEGER,
    CONSTRAINT fk_emp_dept
    FOREIGN KEY (dept_id)
    REFERENCES departments (dept_id)
);
```

This creates a foreign key named `fk_emp_dept` on `dept_id` in `employees`.

#### 2. Adding a Foreign Key to an Existing Table (`ALTER TABLE`)

Use `ALTER TABLE` to add the constraint after the table exists. The parent key must already exist.

**Basic Syntax:**

```
ALTER TABLE child_table
ADD CONSTRAINT constraint_name
FOREIGN KEY (foreign_key_column)
REFERENCES parent_table (parent_key_column);
```

**Example:**
To add the same foreign key to an existing `employees` table:

```
ALTER TABLE employees
ADD CONSTRAINT fk_emp_dept
FOREIGN KEY (dept_id)
REFERENCES departments (dept_id);
```

#### Additional Options

You can specify actions for what happens when a parent row is updated or deleted:

- `ON DELETE CASCADE`: Deletes child rows when the parent is deleted.
- `ON DELETE SET NULL`: Sets the foreign key to NULL in child rows.
- `ON UPDATE CASCADE`: Updates child keys when the parent key changes.
- `ON UPDATE SET NULL`: Sets to NULL on parent key update.

**Example with Options:**

```
ALTER TABLE employees
ADD CONSTRAINT fk_emp_dept
FOREIGN KEY (dept_id)
REFERENCES departments (dept_id)
ON DELETE CASCADE
ON UPDATE RESTRICT;
```

#### Key Rules and Considerations

- The foreign key columns must match the data type and length of the parent key columns.
- The parent table must have a primary or unique key defined before creating the foreign key.
- Foreign keys can reference the same table (self-referential).
- Multiple columns can form a composite foreign key: `FOREIGN KEY (col1, col2) REFERENCES parent (pk1, pk2)`.
- To drop a foreign key: `ALTER TABLE child_table DROP CONSTRAINT constraint_name;`.
- It's recommended to create an index on the foreign key columns for performance.

Test in a development environment, as adding constraints may fail if existing data violates them (e.g., orphaned rows).

#### References

- [Foreign key (referential) constraints - Db2 11.5](https://www.ibm.com/docs/en/db2/11.5.x?topic=constraints-foreign-key-referential)
- [CREATE TABLE statement - Db2 11.5](https://www.ibm.com/docs/en/db2/11.5.x?topic=statements-create-table)
- [ALTER TABLE statement - Db2 11.5](https://www.ibm.com/docs/en/db2/11.5.x?topic=statements-alter-table)
- [Adding a foreign key with Db2 - Stack Overflow](https://stackoverflow.com/questions/59370149/adding-a-foreign-key-with-db2-of-ibm)
