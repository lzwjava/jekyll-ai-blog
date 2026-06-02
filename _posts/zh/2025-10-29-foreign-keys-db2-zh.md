---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 在 Db2 中创建外键
translated: true
type: note
---

### 在 IBM Db2 中创建外键

外键在 Db2 中通过将一个表（子表）中的列（或列集）与另一个表（父表）中的主键或唯一键相关联，来强制实施参照完整性。这确保了子表中的值与父表中的现有值匹配，防止出现孤立记录。

您可以在建表时使用 `CREATE TABLE` 定义外键，也可以通过 `ALTER TABLE` 将其添加到现有表中。该语法是标准 SQL，可在所有 Db2 平台（例如 LUW、z/OS）上使用。

#### 1. 在建表时定义外键 (`CREATE TABLE`)

在列定义内或表定义末尾使用 `FOREIGN KEY` 子句。

**基本语法：**

```
CREATE TABLE child_table (
    child_column1 datatype,
    foreign_key_column datatype,
    -- 其他列...
    CONSTRAINT constraint_name
    FOREIGN KEY (foreign_key_column)
    REFERENCES parent_table (parent_key_column)
);
```

**示例：**
假设您有一个包含主键 `dept_id` 的 `departments` 表：

```
CREATE TABLE departments (
    dept_id INTEGER NOT NULL PRIMARY KEY,
    dept_name VARCHAR(50)
);
```

现在创建一个 `employees` 表，其中包含一个引用 `dept_id` 的外键：

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

这将在 `employees` 表的 `dept_id` 上创建一个名为 `fk_emp_dept` 的外键。

#### 2. 向现有表添加外键 (`ALTER TABLE`)

使用 `ALTER TABLE` 在表存在后添加约束。父键必须已存在。

**基本语法：**

```
ALTER TABLE child_table
ADD CONSTRAINT constraint_name
FOREIGN KEY (foreign_key_column)
REFERENCES parent_table (parent_key_column);
```

**示例：**
要向现有的 `employees` 表添加相同的外键：

```
ALTER TABLE employees
ADD CONSTRAINT fk_emp_dept
FOREIGN KEY (dept_id)
REFERENCES departments (dept_id);
```

#### 附加选项

您可以指定在更新或删除父行时执行的操作：

- `ON DELETE CASCADE`：删除父行时同时删除子行。
- `ON DELETE SET NULL`：删除父行时将子行中的外键设置为 NULL。
- `ON UPDATE CASCADE`：父键更改时更新子键。
- `ON UPDATE SET NULL`：父键更新时设置为 NULL。

**带选项的示例：**

```
ALTER TABLE employees
ADD CONSTRAINT fk_emp_dept
FOREIGN KEY (dept_id)
REFERENCES departments (dept_id)
ON DELETE CASCADE
ON UPDATE RESTRICT;
```

#### 关键规则与注意事项

- 外键列的数据类型和长度必须与父键列匹配。
- 在创建外键之前，父表必须已定义主键或唯一键。
- 外键可以引用同一个表（自引用）。
- 多个列可以组成复合外键：`FOREIGN KEY (col1, col2) REFERENCES parent (pk1, pk2)`。
- 删除外键：`ALTER TABLE child_table DROP CONSTRAINT constraint_name;`。
- 建议在外键列上创建索引以提高性能。

请在开发环境中进行测试，因为如果现有数据违反约束（例如，存在孤立行），添加约束可能会失败。

#### 参考资料

- [外键（参照）约束 - Db2 11.5](https://www.ibm.com/docs/en/db2/11.5.x?topic=constraints-foreign-key-referential)
- [CREATE TABLE 语句 - Db2 11.5](https://www.ibm.com/docs/en/db2/11.5.x?topic=statements-create-table)
- [ALTER TABLE 语句 - Db2 11.5](https://www.ibm.com/docs/en/db2/11.5.x?topic=statements-alter-table)
- [在 Db2 中添加外键 - Stack Overflow](https://stackoverflow.com/questions/59370149/adding-a-foreign-key-with-db2-of-ibm)
