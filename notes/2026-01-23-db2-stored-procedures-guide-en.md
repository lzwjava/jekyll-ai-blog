---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Creating DB2 Stored Procedures Guide
translated: false
type: note
---

**Question:** How to define a DB2 stored procedure with IN VARCHAR parameters, OUT parameters, result sets, etc.?

**Answer:**

Here are the most common and practical ways to define stored procedures in **IBM DB2** (both LUW and z/OS flavors — with the most frequently used syntax first).

### 1. Modern recommended style (DB2 LUW & recent z/OS) — SQL PL with RESULT SETS

```sql
CREATE OR REPLACE PROCEDURE GET_CUSTOMER_INFO
    (IN  p_customer_id    VARCHAR(20),
     IN  p_region         VARCHAR(10),
     OUT p_customer_name   VARCHAR(100),
     OUT p_status          CHAR(1),
     OUT p_found_rows      INTEGER)
    SPECIFIC GET_CUST_INFO
    DYNAMIC RESULT SETS 2
    LANGUAGE SQL
    READS SQL DATA
BEGIN
    DECLARE c1 CURSOR WITH RETURN FOR
        SELECT customer_name, status, country
        FROM customers
        WHERE cust_id = p_customer_id
          AND region  = p_region;

    DECLARE c2 CURSOR WITH RETURN FOR
        SELECT order_id, order_date, total_amount
        FROM orders
        WHERE cust_id = p_customer_id
        ORDER BY order_date DESC
        FETCH FIRST 10 ROWS ONLY;

    -- OUT parameters
    SELECT customer_name, status
    INTO p_customer_name, p_status
    FROM customers
    WHERE cust_id = p_customer_id
    FETCH FIRST 1 ROW ONLY;

    GET DIAGNOSTICS p_found_rows = ROW_COUNT;

    -- If no row found → set default
    IF p_customer_name IS NULL THEN
        SET p_customer_name = 'NOT FOUND';
        SET p_status = 'N';
    END IF;

    -- Open cursors → become result sets
    OPEN c1;
    OPEN c2;

END
```

### 2. Calling the procedure (examples)

```sql
-- (1) Consume both result sets + OUT parameters
CALL GET_CUSTOMER_INFO('CUST123', 'APAC', ?, ?, ?);

-- (2) In a client that supports multiple result sets (JDBC, .NET, etc.)
-- Usually you get:
--   ResultSet 1 → customer master data
--   ResultSet 2 → recent orders
--   then OUT parameters
```

### 3. Classic style — only one result set (very common in older code)

```sql
CREATE PROCEDURE LIST_ORDERS_BY_DATE
    (IN  p_start_date   DATE,
     IN  p_end_date     DATE)
    SPECIFIC ORD_BY_DATE
    DYNAMIC RESULT SETS 1
    LANGUAGE SQL
BEGIN
    DECLARE c_orders CURSOR WITH RETURN TO CALLER FOR
        SELECT order_id, customer_id, order_date, total_amount
        FROM orders
        WHERE order_date BETWEEN p_start_date AND p_end_date
        ORDER BY order_date DESC;

    OPEN c_orders;
END
```

### 4. INOUT parameter example

```sql
CREATE OR REPLACE PROCEDURE UPDATE_BALANCE
    (IN    p_account_id     VARCHAR(15),
     INOUT p_amount         DECIMAL(15,2))
    LANGUAGE SQL
BEGIN
    UPDATE accounts
    SET balance = balance + p_amount
    WHERE account_id = p_account_id;

    -- Return the new balance in the same parameter
    SELECT balance
    INTO p_amount
    FROM accounts
    WHERE account_id = p_account_id;
END
```

### Quick reference — most important clauses

| Clause                     | Meaning / Typical values                                 | Mandatory? |
|----------------------------|-------------------------------------------------------------------|------------|
| `IN`                       | Input only parameter                                              | —          |
| `OUT`                      | Output only parameter                                             | —          |
| `INOUT`                    | Can be read and written (input + output)                          | —          |
| `DYNAMIC RESULT SETS n`    | How many result sets (cursors) the procedure may return (0–n)     | Usually yes when returning result sets |
| `LANGUAGE SQL`             | Written in SQL PL (most common)                                   | Yes        |
| `DETERMINISTIC`            | Same inputs → always same output (helps optimizer)                | Optional   |
| `READS SQL DATA`           | Can read tables, no modification                                  | Recommended|
| `MODIFIES SQL DATA`        | Can do INSERT/UPDATE/DELETE                                       | When needed|
| `CONTAINS SQL`             | No table access (only variables, etc.)                            | —          |
| `SPECIFIC name`            | Unique internal name (useful when dropping/overloading)           | Recommended|
| `WITH RETURN TO CALLER`    | Cursor stays open after procedure ends (for result set)           | For result sets |

### Summary — most common patterns in 2024/2025

Pattern                            | Use case
-----------------------------------|-----------------------------------------------
1 IN(s) + 1–2 cursors             | Search / reporting procedures
1–2 IN + several OUT              | Get single row + status/flags
IN + INOUT                        | Modify value and return new value
IN(s) + OUT(s) + 1 cursor         | Get header + detail list

Hope this gives you a practical starting point.

**References:**

- [https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-procedure](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-procedure)
- [https://www.ibm.com/docs/en/db2-for-zos/13?topic=procedures-creating-sql](https://www.ibm.com/docs/en/db2-for-zos/13?topic=procedures-creating-sql)
