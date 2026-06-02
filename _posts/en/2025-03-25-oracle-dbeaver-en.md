---
audio: false
generated: true
lang: en
layout: post
title: Steps to Use DBeaver to Check Oracle DB Tables for Data
translated: false
type: note
---

I assume you're asking how to use DBeaver to check which Oracle Database tables contain data, based on your previous question about finding tables with data in Oracle DB. DBeaver is a popular, free, multi-platform database tool that works well with Oracle and other databases. Below, I’ll walk you through how to use DBeaver to inspect your Oracle schemas and identify tables with data.

---

#### 1. **Set Up a Connection to Your Oracle Database**

- **Install DBeaver**: If you haven’t already, download and install DBeaver (Community Edition is fine) from [dbeaver.io](https://dbeaver.io/).
- **Create a New Connection**:
     1. Open DBeaver and click **Database** > **New Database Connection** in the menu.
     2. Select **Oracle** from the list and click **Next**.
     3. Enter your connection details:
        - **Host**: Your Oracle server’s hostname or IP.
        - **Port**: Typically 1521 (default for Oracle).
        - **Database/SID or Service Name**: Depending on your setup (e.g., SID = `XE` for Express Edition or a service name).
        - **Username** and **Password**: Your Oracle credentials.
     4. Click **Test Connection** to verify it works. You may need to download the Oracle JDBC driver if prompted (DBeaver can do this automatically).
     5. Click **Finish** to save the connection.

#### 2. **Explore Schemas in the Database Navigator**

- In the **Database Navigator** (left-hand pane), expand your Oracle connection.
- You’ll see a list of schemas (e.g., your username or others you have access to). Expand the schema you want to inspect.
- Under each schema, expand the **Tables** node to see all tables.

#### 3. **Check Tables for Data Using the GUI**

- **View Table Data**:
     1. Double-click a table name or right-click it and select **Edit Table**.
     2. Switch to the **Data** tab in the editor that opens.
     3. If the table has data, you’ll see rows displayed. If it’s empty, you’ll see no rows (or a message like "No data").
  - By default, DBeaver fetches up to 200 rows. To fetch all rows, click the **Fetch All Rows** button (a small arrow icon) in the bottom toolbar of the Data tab.
- **Count Rows Quickly**:
     1. Right-click the table in the Database Navigator.
     2. Select **Navigate** > **Row Count**.
     3. DBeaver runs a `SELECT COUNT(*)` query and shows the result in a pop-up. If it’s 0, the table is empty.

#### 4. **Run SQL Queries to Check Multiple Tables**

- If you want to check many tables at once (more efficient than clicking each one), use the SQL Editor:
     1. Click **SQL Editor** > **New SQL Script** (or press `Ctrl + [`).
     2. Set the schema context:
        - Use the dropdown at the top of the SQL Editor to select your schema, or run:

          ```sql
          ALTER SESSION SET CURRENT_SCHEMA = schema_name;
          ```

          Replace `schema_name` with your target schema (e.g., `HR`).
     3. Query row counts for all tables:
        - Use this SQL to list tables with data (similar to my previous answer):

          ```sql
          SELECT table_name, num_rows
          FROM user_tables
          WHERE num_rows > 0
          ORDER BY num_rows DESC;
          ```

        - Run it by pressing `Ctrl + Enter`. Results appear in the **Results** tab below.
        - `USER_TABLES` shows tables in your schema. Use `ALL_TABLES` for tables you can access across schemas:

          ```sql
          SELECT owner, table_name, num_rows
          FROM all_tables
          WHERE num_rows > 0
          AND owner = UPPER('schema_name');
          ```

     4. **Note**: `NUM_ROWS` is an estimate from the last statistics update. If it’s inaccurate, update stats with:

        ```sql
        EXEC DBMS_STATS.GATHER_SCHEMA_STATS('schema_name');
        ```
