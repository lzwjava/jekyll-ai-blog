---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast:free
title: IBM DB2 Sequence Usage Guide
translated: false
type: note
---

### IBM DB2 Sequence Usage with NEXT VALUE FOR

In IBM DB2, `NEXT VALUE FOR` is used to retrieve the next value from a sequence, which generates unique, incrementing numbers. Sequences are useful for generating primary keys or other unique identifiers.

#### Example: Creating and Using a Sequence

1. **Create the sequence** (run this once in your DB2 environment):

   ```sql
   CREATE SEQUENCE my_sequence
   START WITH 1
   INCREMENT BY 1
   NO CYCLE;
   ```

   - This creates a sequence named `my_sequence` starting at 1, incrementing by 1 each time.

2. **Use the sequence in an INSERT statement** to get the next value:

   ```sql
   INSERT INTO employees (id, name, department)
   VALUES (NEXT VALUE FOR my_sequence, 'Alice Johnson', 'Engineering');
   ```

   - This inserts a new row with `id` as the next sequence value (e.g., 1 for the first use, 2 for the next, etc.).

#### Key Notes

- You can also use it in SELECT queries: `SELECT NEXT VALUE FOR my_sequence FROM SYSIBM.SYSDUMMY1;`
- Sequences are separate from tables and can be shared across multiple tables if needed.
- For more details, refer to the IBM DB2 documentation on sequences. If you need examples for other sequence functions like `PREVIOUS VALUE FOR`, let me know!
