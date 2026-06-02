---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Exporting DB2 Tables to Files
translated: false
type: note
---

Question: How do I use DB2 commands to export a table (or its data) to a file?

Answer:

In DB2 (on Linux/Unix/Windows or z/OS), the primary command-line tool for exporting table data is the **EXPORT** command. It can be run from the DB2 Command Line Processor (CLP) or db2cmd (Windows).

### Basic Syntax

```
db2 "EXPORT TO filename OF export_format [options] SELECT_statement"
```

### Common Export Formats

| Format | File Extension | Use Case |
|------|----------------|----------|
| DEL  | .del or .csv   | Delimited ASCII (most common, works like CSV) |
| IXF  | .ixf           | IBM DB2 native format (best for importing back into DB2) |
| WSF  | .wsf           | Worksheet format (for Lotus/Excel) |

### Examples

1. **Export entire table to a CSV-like delimited file**

   ```
   db2 "EXPORT TO /path/employees.del OF DEL SELECT * FROM SCHEMA.EMPLOYEES"
   ```

2. **Export with custom delimiters and include column names**

   ```
   db2 "EXPORT TO employees.csv OF DEL MODIFIED BY COLDEL, DECPLUSBLANK MESSAGES msgs.txt SELECT * FROM MYSCHEMA.EMPLOYEES"
   ```

   - `COLDEL,` → uses comma as column delimiter
   - `DECPLUSBLANK` → keeps plus sign for positive decimals
   - First row will contain column headings

3. **Export only selected columns or with a WHERE clause**

   ```
   db2 "EXPORT TO active_emps.del OF DEL SELECT EMPNO, FIRSTNME, LASTNAME, SALARY FROM EMPLOYEE WHERE SALARY > 50000 ORDER BY SALARY DESC"
   ```

4. **Export in IXF format (recommended when you plan to import back into DB2)**

   ```
   db2 "EXPORT TO employee.ixf OF IXF MESSAGES msgs.txt SELECT * FROM EMPLOYEE"
   ```

5. **Export large tables with LOBs (add LOBINFILE option)**

   ```
   db2 "EXPORT TO data.del OF DEL LOBINFILE lobdata MODIFIED BY CODEPAGE=1208 SELECT * FROM DOCUMENTS"
   ```

   This creates separate files for LOB columns.

6. **From Windows command prompt (db2cmd)**

   ```
   db2 connect to MYDB
   db2 "EXPORT TO C:\temp\data.del OF DEL SELECT * FROM MYTABLE"
   ```

### Common MODIFIED BY Options (for DEL format)

| Option              | Effect |
|---------------------|--------|
| `COLDEL;`           | Use semicolon as delimiter |
| `COLDEL,`           | Use comma (standard CSV) |
| `CHARDEL""`         | Double-quote as character delimiter |
| `DECIMAL.`          | Use period as decimal point |
| `CODEPAGE=1208`     | UTF-8 encoding |
| `NOCHARDEL`         | No quoting of character fields |
| `STRIPBLANKS`       | Trim trailing blanks |

### Alternative Methods

- **db2look** – to export table structure (DDL) only
  `db2look -d MYDB -t SCHEMA.TABLE -e > table_ddl.sql`
- **db2move** – to export multiple/all tables at once (IXF format)
  `db2move MYDB EXPORT`

References:

- [IBM DB2 EXPORT command documentation](https://www.ibm.com/docs/en/db2/11.5?topic=commands-export)
- [db2move utility](https://www.ibm.com/docs/en/db2/11.5?topic=commands-db2move)
