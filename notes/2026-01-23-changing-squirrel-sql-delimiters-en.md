---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Changing Squirrel SQL Delimiters
translated: false
type: note
---

**Question:** How to set/change the delimiter in Squirrel SQL Client (especially for stored procedures using BEGIN … END that need a different delimiter like @@ or @)?

**Answer:**

In **Squirrel SQL Client**, the default statement delimiter is `;`.
When creating or calling stored procedures / functions / triggers that contain `;` inside their body (BEGIN … END blocks), you must temporarily change the delimiter.

Here are the main ways to do it in Squirrel-SQL:

### Recommended & Most Common Method (2024–2026 style)

1. Go to the **SQL worksheet** (where you write your script)
2. At the very top of your script, write:

```sql
--#SET TERMINATOR @@

DELIMITER @@

CREATE PROCEDURE my_proc()
BEGIN
    INSERT INTO log VALUES(NOW(), 'start');
    -- many statements using normal ;
    INSERT INTO log VALUES(NOW(), 'end');
END@@

DELIMITER ;
```

3. Then execute the whole script (Ctrl+Enter or the running man icon)

The `--#SET TERMINATOR xx` is a **SQuirreL special comment** that changes the delimiter **for the current session/tab**.

Popular choices people use:

```sql
--#SET TERMINATOR @@        ← most popular
--#SET TERMINATOR $
--#SET TERMINATOR //
--#SET TERMINATOR \G
--#SET TERMINATOR @          ← what you mentioned
```

### Alternative ways that also work

**Method 2 – Use the Session Properties menu**

- Right-click your session in the left panel → **Session Properties**
- Go to tab **SQL Execution** → **Delimiters**
- Change "Statement separator" from `;` to whatever you want (e.g. `@@` or `@`)
- → OK
- → This changes it for the whole session (until you change it back)

**Method 3 – Quick one-liner style (MySQL/MariaDB friendly)**

Many people still write it the "classic" way:

```sql
DELIMITER @@

CREATE PROCEDURE example()
BEGIN
    SELECT 1;
    SELECT 2;
END @@

DELIMITER ;
```

SQuirreL understands this syntax correctly **as long as** you have not disabled the "Process SQL comments" or "Allow # as comment" settings.

### Quick rule of thumb – what most people do in 2025/2026

```sql
--#SET TERMINATOR @@

DROP PROCEDURE IF EXISTS my_proc@@

CREATE PROCEDURE my_proc(IN p_id INT)
BEGIN
    DECLARE v_name VARCHAR(100);
    SET v_name = 'test';
    INSERT INTO t1 (id, name) VALUES (p_id, v_name);
    -- more business logic with normal semicolons
END@@

--#SET TERMINATOR ;     ← good practice to reset
```

### Summary – Pick one style

Style A (clean & modern)

```sql
--#SET TERMINATOR @@
... your procedure ...
--#SET TERMINATOR ;
```

Style B (classic MySQL workbench style)

```sql
DELIMITER @@
... your procedure ...
DELIMITER ;
```

Both work well in current SQuirreL versions (4.x, 202x builds).

Hope this helps you get rid of the "You have an error in your SQL syntax … near END" problem.

**References:**

- None (information based on SQuirreL SQL client behavior up to 2025 releases and common community usage patterns)
