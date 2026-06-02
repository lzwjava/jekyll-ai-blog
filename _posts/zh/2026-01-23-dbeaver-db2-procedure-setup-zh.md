---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: DBeaver DB2 存储过程与分隔符设置
translated: true
type: note
---

Question: How to use DBeaver to call a stored procedure in DB2, and how to set the delimiter for BEGIN and END blocks?

Answer:

Here’s how to handle **calling stored procedures** and **changing the statement delimiter** in DBeaver when working with **IBM DB2** (works for both LUW and z/OS in most cases).

### 1. Calling a DB2 Stored Procedure in DBeaver

There are two main ways:

**Simple call (no OUT/INOUT parameters or you don't need to see OUT values):**

```sql
CALL YOUR_SCHEMA.YOUR_PROCEDURE_NAME(?, 'input value', 100);
```

Or with named parameters (recommended when there are many):

```sql
CALL YOUR_SCHEMA.YOUR_PROCEDURE_NAME(
    IN_PARAM  => ?,
    OUT_COUNT => ?,
    OUT_LIST  => ?
);
```

**Recommended way — using the context menu (easiest):**

1. In the Database Navigator → find your schema → Procedures
2. Right-click the stored procedure
3. Choose **Execute Stored Procedure** or **Generate SQL → CALL**
4. DBeaver opens a dialog where you can enter input values and see output parameters (if any)
5. Click **OK** or **Execute**

This method usually handles IN, OUT, and INOUT parameters correctly (output values appear in the bottom panel after execution).

**Manual call with variables (useful for OUT parameters):**

```sql
-- Only needed if you want to capture/use output values
CREATE OR REPLACE VARIABLE v_out_count INTEGER;
CREATE OR REPLACE VARIABLE v_out_list  VARCHAR(1000);

CALL YOUR_SCHEMA.YOUR_PROCEDURE_NAME(?, v_out_count, v_out_list);

-- View results
VALUES (v_out_count, v_out_list);
```

### 2. Setting Delimiter for CREATE PROCEDURE / BEGIN ... END blocks

DB2 compound statements (CREATE PROCEDURE, CREATE FUNCTION, BEGIN ... END) contain many `;` characters inside the body. DBeaver (by default) treats `;` as the end of a statement → it fails when you try to run the whole CREATE script.

**Solution: Change the script delimiter in DBeaver**

**Quick per-script method (recommended):**

1. Open your CREATE PROCEDURE script
2. Press **Ctrl + Enter** (or right-click → Execute → Execute SQL Script) **→ no**, better:
3. Click the **gear icon** (SQL Editor preferences) or press **Alt+Enter** on the editor
4. Go to the **SQL Processing** tab (sometimes called "SQL Editor Settings")
5. Set:
   - **Statements delimiter**: `@` (or `//` or `$$` — `@` is very common for DB2)
   - Check **Ignore native delimiter**
   - (Optional) Check **Blank line is statement delimiter** if you like
6. Click **OK**
7. Now write your procedure like this:

```sql
CREATE OR REPLACE PROCEDURE YOUR_SCHEMA.YOUR_PROC (
    IN  p_id    INTEGER,
    OUT p_count INTEGER
)
LANGUAGE SQL
BEGIN
    -- many ; inside are ok now
    SELECT COUNT(*) INTO p_count
    FROM YOUR_TABLE
    WHERE id = p_id;

    -- more logic...
END
@
```

8. Select the whole script (or just put cursor inside) and press **Alt+X** or **Ctrl+Enter** (Execute script mode)

**Global / connection-level change (alternative):**

- Right-click your DB2 connection → **Edit Connection** → **Driver properties** or **Connection settings** → look for SQL delimiter settings (not always available)
- Or go to **Window → Preferences → Editors → SQL Editor → SQL Processing** and change the default delimiter there

**Common DB2 delimiters people use:**

- `@` (most popular in IBM documentation and tools)
- `//`
- `$$`

After you finish creating procedures, you can switch the delimiter back to `;` for normal SELECT/INSERT work.

References:

- [DBeaver SQL Execution Documentation](https://dbeaver.com/docs/dbeaver/SQL-Execution)
- [Stack Overflow – DB2 Stored Procedure IF/ELSE in DBeaver](https://stackoverflow.com/questions/69016820/db2-stored-procedure-if-else-what-am-i-missing)
- [GitHub DBeaver issues on DB2 delimiter](https://github.com/dbeaver/dbeaver/issues/14384)
