---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Setting Delimiters in DBeaver
translated: false
type: note
---

**Question:** How to set the delimiter in DBeaver? Sometimes for BEGIN/END stored procedure calls, I need to use @ as the end delimiter.

**Answer:**

In DBeaver, the most common and reliable way to handle stored procedures (especially in MySQL/MariaDB) that contain internal semicolons is to include `DELIMITER` commands directly in your script and execute the whole script properly.

### Recommended Method (Works in most cases)

Write your script like this in the SQL Editor:

```sql
DELIMITER @

CREATE PROCEDURE your_procedure_name()
BEGIN
    SELECT 'Hello';
    INSERT INTO log VALUES ('test');
    -- any statements with ; inside
END @

DELIMITER ;
```

**How to execute it:**

- Select the entire script (from the first `DELIMITER @` to the final `DELIMITER ;`)
- Press **Alt+X** (or right-click → Execute → Execute Script)
  - This runs the whole block as a script, allowing DBeaver to respect the `DELIMITER` changes
- Alternatively, use **Ctrl+Enter** on the selected block, but **Alt+X** is usually more reliable for multi-statement scripts with delimiter changes

### Alternative: Change the default statement delimiter in DBeaver settings

If you very frequently use `@` (or another character) instead of `;`, you can change DBeaver's parsing delimiter:

1. Go to **Window → Preferences** (or **DBeaver → Settings** on macOS)
2. Navigate to **Editors → SQL Editor → SQL Processing → Delimiters**
3. Set **Statements delimiter** to `@`
4. (Optional) Check/uncheck **Ignore native delimiter** depending on your needs
5. Click **Apply and Close**

After this change:

- DBeaver will treat `@` as the end of each statement
- You no longer need to write `DELIMITER @` — just end your procedure with `@`
- But you must be careful: this setting affects **all** queries in that editor/connection

```sql
CREATE PROCEDURE your_procedure_name()
BEGIN
    SELECT 'Hello';
    -- statements
END @
```

**Warning:** Changing the global/default delimiter to `@` can cause confusion with normal queries that use `;`. Most users prefer the first method (using `DELIMITER` + Alt+X) because it keeps the change local to that script only.

### Quick Summary – What usually works best

- Use `DELIMITER @` ... `END @` ... `DELIMITER ;`
- **Select all** → **Alt+X** (Execute as Script)
- This is the standard approach for MySQL/MariaDB stored procedures in DBeaver

This method avoids changing global settings and works consistently across different connections.

**References:**

- [DBeaver SQL Execution Documentation](https://dbeaver.com/docs/dbeaver/SQL-Execution)
- [MySQL DELIMITER usage](https://www.mysqltutorial.org/mysql-stored-procedure/mysql-delimiter)
