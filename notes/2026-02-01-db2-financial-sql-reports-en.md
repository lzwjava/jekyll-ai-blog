---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: DB2 Financial Reports With SQL Procedures
translated: false
type: note
---

Question: How to design financial reports using DB2 stored procedures in SQL? Please provide some examples, including aggregations for daily, weekly, monthly, etc.

Answer:

Designing financial report stored procedures in **DB2** typically involves:

- Accepting parameters (e.g. date range, account ID, report type/period)
- Using date functions to group/truncate dates (common functions: `DATE`, `YEAR`, `MONTH`, `DAY`, `WEEK`, `TRUNC`, `VARCHAR_FORMAT`)
- Aggregating financial metrics (SUM, COUNT, AVG, etc.)
- Returning result sets directly (most common for reporting)
- Optionally using dynamic SQL or output parameters

### Common Design Patterns

1. Single flexible procedure → one `@period` parameter ('DAY', 'WEEK', 'MONTH', 'YTD', 'QTR')
2. Separate procedures for each granularity (cleaner maintenance in large systems)
3. Materialized summary tables + procedure (best performance for very large volumes)
4. Date-range + grouping logic inside procedure

### Example 1: General-purpose financial summary by period

```sql
CREATE OR REPLACE PROCEDURE FIN_REPORT_BY_PERIOD (
    IN  p_start_date    DATE,
    IN  p_end_date      DATE,
    IN  p_period        VARCHAR(10),     -- 'DAY', 'WEEK', 'MONTH', 'QUARTER', 'YEAR'
    IN  p_account_id    INTEGER DEFAULT NULL
)
SPECIFIC FIN_RPT_PERIOD
DYNAMIC RESULT SETS 1
LANGUAGE SQL
BEGIN

    DECLARE v_sql VARCHAR(4000);
    DECLARE c1 CURSOR WITH RETURN FOR s1;

    SET v_sql = '
    SELECT
        period_start,
        period_end,
        SUM(debit)          AS total_debit,
        SUM(credit)         AS total_credit,
        SUM(debit - credit) AS net_amount,
        COUNT(*)            AS transaction_count
    FROM financial_transactions t
    WHERE t.trx_date BETWEEN ? AND ?
    ';

    IF p_account_id IS NOT NULL THEN
        SET v_sql = v_sql || ' AND t.account_id = ? ';
    END IF;

    -- Choose grouping expression
    SET v_sql = v_sql || ' GROUP BY ';

    IF p_period = 'DAY' THEN
        SET v_sql = v_sql || ' DATE(t.trx_date) ';
        SET v_sql = REPLACE(v_sql, 'period_start', 'DATE(t.trx_date) AS period_start');
        SET v_sql = REPLACE(v_sql, 'period_end',   'DATE(t.trx_date) AS period_end');
    ELSEIF p_period = 'WEEK' THEN
        SET v_sql = v_sql || ' TRUNC(t.trx_date - DAYOFWEEK(t.trx_date) + 1, ''DD'') ';
        SET v_sql = REPLACE(v_sql, 'period_start',
            'TRUNC(t.trx_date - DAYOFWEEK(t.trx_date) + 1, ''DD'') AS period_start');
        SET v_sql = REPLACE(v_sql, 'period_end',
            'TRUNC(t.trx_date - DAYOFWEEK(t.trx_date) + 7, ''DD'') AS period_end');
    ELSEIF p_period = 'MONTH' THEN
        SET v_sql = v_sql || ' DATE_TRUNC(''MONTH'', t.trx_date) ';
        SET v_sql = REPLACE(v_sql, 'period_start', 'DATE_TRUNC(''MONTH'', t.trx_date) AS period_start');
        SET v_sql = REPLACE(v_sql, 'period_end',
            'LAST_DAY(t.trx_date) AS period_end');
    ELSEIF p_period = 'QUARTER' THEN
        SET v_sql = v_sql || ' DATE_TRUNC(''QUARTER'', t.trx_date) ';
        SET v_sql = REPLACE(v_sql, 'period_start', 'DATE_TRUNC(''QUARTER'', t.trx_date) AS period_start');
        SET v_sql = REPLACE(v_sql, 'period_end',
            'DATE_TRUNC(''QUARTER'', t.trx_date) + 3 MONTHS - 1 DAY AS period_end');
    ELSEIF p_period = 'YEAR' THEN
        SET v_sql = v_sql || ' YEAR(t.trx_date) ';
        SET v_sql = REPLACE(v_sql, 'period_start', 'YEAR(t.trx_date) AS period_start');
        SET v_sql = REPLACE(v_sql, 'period_end',   'YEAR(t.trx_date) AS period_end');
    ELSE
        SIGNAL SQLSTATE '75000' SET MESSAGE_TEXT = 'Invalid period type';
    END IF;

    SET v_sql = v_sql || ' ORDER BY period_start';

    PREPARE s1 FROM v_sql;

    IF p_account_id IS NOT NULL THEN
        OPEN c1 USING p_start_date, p_end_date, p_account_id;
    ELSE
        OPEN c1 USING p_start_date, p_end_date;
    END IF;

END
```

**Usage examples:**

```sql
CALL FIN_REPORT_BY_PERIOD('2025-01-01', '2025-12-31', 'MONTH');
CALL FIN_REPORT_BY_PERIOD(CURRENT DATE - 30 DAYS, CURRENT DATE, 'DAY');
CALL FIN_REPORT_BY_PERIOD('2025-01-01', '2025-12-31', 'WEEK', 10045);
```

### Example 2: Simple monthly P&L style report

```sql
CREATE OR REPLACE PROCEDURE MONTHLY_FINANCIAL_SUMMARY (
    IN  p_year  SMALLINT
)
SPECIFIC MONTH_FIN_SUM
DYNAMIC RESULT SETS 1
LANGUAGE SQL
BEGIN

    DECLARE c1 CURSOR WITH RETURN FOR
        SELECT
            MONTH(trx_date)               AS month_number,
            VARCHAR_FORMAT(trx_date, 'Month') AS month_name,
            SUM(CASE WHEN type = 'REVENUE'  THEN amount ELSE 0 END) AS revenue,
            SUM(CASE WHEN type = 'EXPENSE'  THEN amount ELSE 0 END) AS expenses,
            SUM(CASE WHEN type = 'REVENUE'  THEN amount
                     WHEN type = 'EXPENSE'  THEN -amount
                     ELSE 0 END)           AS profit
        FROM financial_transactions
        WHERE YEAR(trx_date) = p_year
        GROUP BY MONTH(trx_date), VARCHAR_FORMAT(trx_date, 'Month')
        ORDER BY MONTH(trx_date);

    OPEN c1;

END
```

### Example 3: Daily balance / running total style (very common in banking)

```sql
CREATE OR REPLACE PROCEDURE DAILY_ACCOUNT_BALANCE (
    IN p_account_id  INTEGER,
    IN p_from_date   DATE,
    IN p_to_date     DATE
)
SPECIFIC DLY_ACCT_BAL
DYNAMIC RESULT SETS 1
LANGUAGE SQL
BEGIN

    DECLARE c1 CURSOR WITH RETURN FOR
        WITH running AS (
            SELECT
                trx_date,
                SUM(amount) OVER (
                    ORDER BY trx_date
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                ) AS balance
            FROM financial_transactions
            WHERE account_id = p_account_id
              AND trx_date BETWEEN p_from_date AND p_to_date
        )
        SELECT
            trx_date,
            balance
        FROM running
        ORDER BY trx_date;

    OPEN c1;

END
```

### Quick Reference – DB2 Date Grouping Techniques

| Period   | Grouping expression (most common)                     | Start of period trick                     |
|----------|-------------------------------------------------------|--------------------------------------------|
| Day      | `DATE(trx_date)`                                      | —                                          |
| Week     | `TRUNC(trx_date - DAYOFWEEK(trx_date)+1,'DD')`        | Monday start (ISO-like)                    |
| Month    | `DATE_TRUNC('MONTH', trx_date)`                       | `LAST_DAY(trx_date)` for end               |
| Quarter  | `DATE_TRUNC('QUARTER', trx_date)`                     | `+ 3 MONTHS - 1 DAY`                       |
| Year     | `YEAR(trx_date)`                                      | —                                          |

These patterns cover most financial reporting needs in DB2 environments (LUW or z/OS).

References:

- <https://www.ibm.com/docs/en/db2-for-zos/12.0.0?topic=procedures-example-simple-stored-procedure>
- <https://medium.com/@lomso.dzingwa/automating-financial-reporting-with-sql-stored-procedures-cae13bf98d35>
- <https://www.experts-exchange.com/questions/24573782/AS400-DB2-Query-To-Group-Date-By-Year-Month-and-Day.html>
