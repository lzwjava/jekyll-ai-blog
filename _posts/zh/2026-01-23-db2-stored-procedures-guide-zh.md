---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: DB2 存储过程创建指南
translated: true
type: note
---

**Question:** 如何定义一个带有 IN VARCHAR 参数、OUT 参数、result sets 等的 DB2 stored procedure？

**Answer:**

以下是在 **IBM DB2**（包括 LUW 和 z/OS 版本）中定义 stored procedures 最常用且实用的方法（按最常用的语法排序）。

### 1. 现代推荐风格 (DB2 LUW & 近期 z/OS) — 带有 RESULT SETS 的 SQL PL

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

    -- 如果未找到行 → 设置默认值
    IF p_customer_name IS NULL THEN
        SET p_customer_name = 'NOT FOUND';
        SET p_status = 'N';
    END IF;

    -- 打开 cursors → 成为 result sets
    OPEN c1;
    OPEN c2;

END
```

### 2. 调用 procedure (示例)

```sql
-- (1) 使用两个 result sets + OUT 参数
CALL GET_CUSTOMER_INFO('CUST123', 'APAC', ?, ?, ?);

-- (2) 在支持多个 result sets 的客户端中 (JDBC, .NET 等)
-- 通常你会得到：
--   ResultSet 1 → customer 主数据
--   ResultSet 2 → 最近订单
--   然后是 OUT 参数
```

### 3. 经典风格 — 仅一个 result set (在旧代码中非常常见)

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

### 4. INOUT 参数示例

```sql
CREATE OR REPLACE PROCEDURE UPDATE_BALANCE
    (IN    p_account_id     VARCHAR(15),
     INOUT p_amount         DECIMAL(15,2))
    LANGUAGE SQL
BEGIN
    UPDATE accounts
    SET balance = balance + p_amount
    WHERE account_id = p_account_id;

    -- 在同一个参数中返回新的 balance
    SELECT balance
    INTO p_amount
    FROM accounts
    WHERE account_id = p_account_id;
END
```

### 快速参考 — 最重要的子句

| 子句 | 含义 / 典型值 | 是否强制？ |
|----------------------------|-------------------------------------------------------------------|------------|
| `IN` | 仅输入参数 | — |
| `OUT` | 仅输出参数 | — |
| `INOUT` | 可读可写（输入 + 输出） | — |
| `DYNAMIC RESULT SETS n` | procedure 可能返回多少个 result sets (cursors) (0–n) | 返回 result sets 时通常需要 |
| `LANGUAGE SQL` | 使用 SQL PL 编写（最常见） | 是 |
| `DETERMINISTIC` | 相同的输入 → 总是相同的输出（有助于 optimizer） | 可选 |
| `READS SQL DATA` | 可以读取表，不能修改 | 推荐 |
| `MODIFIES SQL DATA` | 可以执行 INSERT/UPDATE/DELETE | 需要时使用 |
| `CONTAINS SQL` | 不访问表（仅变量等） | — |
| `SPECIFIC name` | 唯一的内部名称（在 dropping/overloading 时有用） | 推荐 |
| `WITH RETURN TO CALLER` | procedure 结束后 cursor 保持打开（用于 result set） | 用于 result sets |

### 总结 — 2024/2025 年最常见的模式

模式 | 使用场景
-----------------------------------|-----------------------------------------------
1 IN(s) + 1–2 cursors | 查询 / 报表 procedures
1–2 IN + 多个 OUT | 获取单行 + 状态/标志位
IN + INOUT | 修改数值并返回新值
IN(s) + OUT(s) + 1 cursor | 获取 Header + Detail 列表

希望这能为你提供一个实用的起点。

**References:**

- [https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-procedure](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-procedure)
- [https://www.ibm.com/docs/en/db2-for-zos/13?topic=procedures-creating-sql](https://www.ibm.com/docs/en/db2-for-zos/13?topic=procedures-creating-sql)