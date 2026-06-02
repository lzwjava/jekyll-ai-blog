---
audio: false
generated: true
lang: en
layout: post
title: Identify Tables with Data in Oracle DB
translated: false
type: note
---

In Oracle Database, if you’re exploring schemas and finding that some tables appear "empty" when you click on them (e.g., via a GUI tool like SQL Developer or Toad), it doesn’t necessarily mean they have no data. There could be several reasons: permissions, filters, or you’re simply looking at the wrong tables. To systematically find out which tables in a schema contain data, you can query the database metadata or inspect the tables directly. Here’s how to do it:

#### 1. **Check Your Permissions**
   - If you’re seeing empty tables, you might lack privileges to view the data. Ensure you have `SELECT` privileges on the tables in the schema.
   - Run this to check your privileges on a specific table:
     ```sql
     SELECT privilege
     FROM dba_tab_privs
     WHERE grantee = UPPER('your_username')
     AND table_name = UPPER('table_name');
     ```
     Replace `'your_username'` and `'table_name'` accordingly. If nothing shows up, ask the schema owner or DBA to grant you access.

#### 2. **Query the Number of Rows in Tables**
   - Oracle maintains statistics about tables, including row counts, in the `USER_TABLES`, `ALL_TABLES`, or `DBA_TABLES` views (depending on your access level).
   - To see tables with data in the current schema:
     ```sql
     SELECT table_name, num_rows
     FROM user_tables
     WHERE num_rows > 0
     ORDER BY num_rows DESC;
     ```
     - `USER_TABLES`: Shows tables owned by the current user.
     - `NUM_ROWS`: Approximate number of rows (based on last statistics update).

   - If you have access to another schema (e.g., via `ALL_TABLES`):
     ```sql
     SELECT owner, table_name, num_rows
     FROM all_tables
     WHERE num_rows > 0
     AND owner = UPPER('schema_name')
     ORDER BY num_rows DESC;
     ```
     Replace `'schema_name'` with the schema you’re investigating.

   **Note**: `NUM_ROWS` might be outdated if statistics haven’t been recently gathered. See Step 5 to update them.

#### 3. **Manually Check Specific Tables**
   - If you suspect `NUM_ROWS` is unreliable or want to verify, run a `COUNT(*)` on individual tables:
     ```sql
     SELECT table_name
     FROM user_tables;
     ```
     This lists all tables in your schema. Then, for each table:
     ```sql
     SELECT COUNT(*) FROM table_name;
     ```
     If the count is greater than 0, the table has data. Be cautious with large tables—`COUNT(*)` can be slow.

#### 4. **Use a Script to Automate Checking**
   - To avoid manually querying each table, use a PL/SQL script to check row counts across all tables in a schema:
     ```sql
     BEGIN
         FOR t IN (SELECT table_name FROM user_tables)
         LOOP
             EXECUTE IMMEDIATE 'SELECT COUNT(*) FROM ' || t.table_name INTO v_count;
             IF v_count > 0 THEN
                 DBMS_OUTPUT.PUT_LINE(t.table_name || ' has ' || v_count || ' rows');
             END IF;
         END LOOP;
     EXCEPTION
         WHEN OTHERS THEN
             DBMS_OUTPUT.PUT_LINE('Error on table ' || t.table_name || ': ' || SQLERRM);
     END;
     /
     ```
     - Enable output in your tool (e.g., `SET SERVEROUTPUT ON` in SQL*Plus or SQL Developer).
     - This prints only tables with data. Adjust `user_tables` to `all_tables` and add `owner` filtering if checking another schema.

#### 5. **Update Table Statistics (if Necessary)**
   - If `NUM_ROWS` in `USER_TABLES` or `ALL_TABLES` shows 0 or seems wrong, the statistics might be stale. To update them:
     ```sql
     EXEC DBMS_STATS.GATHER_SCHEMA_STATS(ownname => 'schema_name');
     ```
     Replace `'schema_name'` with the schema name (use your username for your own schema). Then rerun the `USER_TABLES` query from Step 2.

#### 6. **Check for Partitioned Tables**
   - If the schema uses partitioned tables, the data might be spread across partitions, and a simple query might not reflect this. Check for partitions:
     ```sql
     SELECT table_name, partition_name, num_rows
     FROM user_tab_partitions
     WHERE num_rows > 0
     ORDER BY table_name, partition_name;
     ```
     This shows which partitions contain data.

#### 7. **GUI Tool Tips (e.g., SQL Developer)**
   - If you’re using a GUI like Oracle SQL Developer:
     1. Right-click the schema in the Connections pane.
     2. Expand the "Tables" node.
     3. Right-click a table, select "Count Rows," or open the "Data" tab to preview contents (if permitted).
     - If the "Data" tab is empty, it could be a permissions issue or the table genuinely has no rows.

---

### Practical Example
Suppose you’re in a schema called `HR`. You’d:
1. Run:
   ```sql
   SELECT table_name, num_rows
   FROM user_tables
   WHERE num_rows > 0;
   ```
   Output might look like:
   ```
   TABLE_NAME   NUM_ROWS
   ----------   --------
   EMPLOYEES    107
   DEPARTMENTS  27
   ```
   This tells you `EMPLOYEES` and `DEPARTMENTS` have data.

2. If you suspect stale stats, update them:
   ```sql
   EXEC DBMS_STATS.GATHER_SCHEMA_STATS('HR');
   ```
3. Recheck with the same query.

---

### Why Tables Might Appear Empty
- **No Data**: The table genuinely has no rows.
- **Permissions**: You can see the table structure but not the data.
- **Filters**: Your GUI tool might have filters hiding rows (e.g., a `WHERE` clause).
- **Truncated/Deleted Data**: Data might have been recently removed.
- **Synonyms/Views**: You might be looking at a synonym or view pointing to an empty or inaccessible table.

If you’re still stuck, let me know your specific setup (e.g., schema name, tool used), and I can tailor the advice further!
