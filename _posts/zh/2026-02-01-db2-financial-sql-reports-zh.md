---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 使用 SQL 过程编写 DB2 财务报表
translated: true
type: note
---

问题：如何使用 SQL 中的 DB2 存储过程设计财务报表？请提供一些示例，包括按日、周、月等进行的聚合。

回答：

在 **DB2** 中设计财务报表存储过程通常涉及以下步骤：

- 接收参数（例如日期范围、账户 ID、报表类型/周期）
- 使用日期函数对日期进行分组或截断（常用函数：`DATE`、`YEAR`、`MONTH`、`DAY`、`WEEK`、`TRUNC`、`VARCHAR_FORMAT`）
- 聚合财务指标（SUM、COUNT、AVG 等）
- 直接返回结果集（报表最常用的方式）
- 可选：使用动态 SQL 或输出参数

### 常见设计模式

1. 单个灵活的过程 → 一个 `@period` 参数（'DAY'、'WEEK'、'MONTH'、'YTD'、'QTR'）
2. 为每个粒度设置独立的过程（大型系统中更易于维护）
3. 物化汇总表 + 存储过程（针对海量数据的最佳性能方案）
4. 在过程内部包含日期范围 + 分组逻辑

### 示例 1：按周期生成的通用财务汇总

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

    -- 选择分组表达式
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

**使用示例：**

```sql
CALL FIN_REPORT_BY_PERIOD('2025-01-01', '2025-12-31', 'MONTH');
CALL FIN_REPORT_BY_PERIOD(CURRENT DATE - 30 DAYS, CURRENT DATE, 'DAY');
CALL FIN_REPORT_BY_PERIOD('2025-01-01', '2025-12-31', 'WEEK', 10045);
```

### 示例 2：简单的月度损益表（P&L）风格报表

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

### 示例 3：每日余额 / 累计余额风格（银行业常见）

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

### 快速参考 – DB2 日期分组技巧

| 周期     | 分组表达式（最常用）                                     | 周期起始技巧                                     |
|----------|-------------------------------------------------------|--------------------------------------------|
| 日       | `DATE(trx_date)`                                      | —                                          |
| 周       | `TRUNC(trx_date - DAYOFWEEK(trx_date)+1,'DD')`        | 周一作为起始 (类似 ISO 标准)                    |
| 月       | `DATE_TRUNC('MONTH', trx_date)`                       | 使用 `LAST_DAY(trx_date)` 获取结束日期         |
| 季度     | `DATE_TRUNC('QUARTER', trx_date)`                     | `+ 3 MONTHS - 1 DAY`                       |
| 年       | `YEAR(trx_date)`                                      | —                                          |

这些模式涵盖了 DB2 环境（LUW 或 z/OS）中大多数财务报表的需求。

参考文献：

- https://www.ibm.com/docs/en/db2-for-zos/12.0.0?topic=procedures-example-simple-stored-procedure
- https://medium.com/@lomso.dzingwa/automating-financial-reporting-with-sql-stored-procedures-cae13bf98d35
- https://www.experts-exchange.com/questions/24573782/AS400-DB2-Query-To-Group-Date-By-Year-Month-and-Day.html