---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: DB2 聚合函数指南
translated: true
type: note
---

**Question:** 如何在 DB2 中使用 SUM、AVG 等聚合函数以及其他常见的统计函数？

**Answer:**

以下是 DB2 中最常用的聚合（统计）函数及其应用实例：

### Basic Syntax

```sql
SELECT 
    function_name(column) 
FROM table 
[WHERE ...]
[GROUP BY ...]
[HAVING ...]
```

### DB2 中最常用的 Aggregate Functions

| Function       | Meaning                          | Ignores NULL? | Typical Data Type | Example                                   |
|----------------|----------------------------------|---------------|-------------------|-------------------------------------------|
| `COUNT(*)`     | 行总数                           | No            | -                 | `COUNT(*)`                                |
| `COUNT(col)`   | 非 NULL 值的数量                 | Yes           | any               | `COUNT(salary)`                           |
| `SUM(col)`     | 数值总和                         | Yes           | numeric           | `SUM(sales_amount)`                       |
| `AVG(col)`     | 平均值 (算术平均)                | Yes           | numeric           | `AVG(price)`                              |
| `MIN(col)`     | 最小值                           | Yes           | numeric/string/date | `MIN(order_date)`                      |
| `MAX(col)`     | 最大值                           | Yes           | numeric/string/date | `MAX(salary)`                          |
| `STDDEV(col)`  | 标准差 (样本)                    | Yes           | numeric           | `STDDEV(salary)`                          |
| `STDDEV_SAMP`  | 等同于 STDDEV (样本)             | Yes           | numeric           | `STDDEV_SAMP(score)`                      |
| `STDDEV_POP`   | 总体标准差                       | Yes           | numeric           | `STDDEV_POP(weight)`                      |
| `VARIANCE`     | 样本方差                         | Yes           | numeric           | `VARIANCE(temperature)`                   |
| `VAR_SAMP`     | 等同于 VARIANCE                  | Yes           | numeric           | `VAR_SAMP(sales)`                         |
| `VAR_POP`      | 总体方差                         | Yes           | numeric           | `VAR_POP(income)`                         |

### 实用示例

```sql
-- 1. 简单的总和与平均值
SELECT 
    SUM(salary)          AS total_salary,
    AVG(salary)          AS avg_salary,
    ROUND(AVG(salary), 2) AS avg_salary_rounded,
    COUNT(*)             AS employee_count,
    COUNT(salary)        AS employees_with_salary
FROM employees;


-- 2. 按部门分组 (Group by)
SELECT 
    dept_id,
    dept_name,
    COUNT(*)               AS headcount,
    SUM(salary)            AS dept_salary,
    ROUND(AVG(salary), 0)  AS avg_salary,
    MIN(salary)            AS min_salary,
    MAX(salary)            AS max_salary
FROM employees
GROUP BY dept_id, dept_name
ORDER BY avg_salary DESC;


-- 3. 统计分布 (方差与标准差)
SELECT 
    department,
    AVG(salary)            AS mean_salary,
    STDDEV(salary)         AS stddev_salary,
    VARIANCE(salary)       AS variance_salary,
    STDDEV_POP(salary)     AS population_stddev
FROM employees
GROUP BY department
HAVING COUNT(*) >= 5
ORDER BY stddev_salary DESC;


-- 4. 结合过滤与四舍五入
SELECT 
    product_category,
    ROUND(SUM(sales_amount), 2)          AS total_sales,
    ROUND(AVG(sales_amount), 2)          AS avg_sale_per_order,
    ROUND(AVG(sales_amount), 2) * 1.1    AS avg_with_10pct_buffer
FROM sales
WHERE sale_date >= '2025-01-01'
GROUP BY product_category
HAVING SUM(sales_amount) > 100000
ORDER BY total_sales DESC;


-- 5. 组合多个具有不同精度的聚合
SELECT 
    region,
    COUNT(DISTINCT customer_id)     AS unique_customers,
    SUM(order_total)                AS total_revenue,
    ROUND(AVG(order_total), 2)      AS avg_order_value,
    MIN(order_date)                 AS first_order,
    MAX(order_date)                 AS last_order
FROM orders
GROUP BY region;
```

### DB2 中的注意事项

- `AVG()`、`SUM()` 以及统计函数会忽略 NULL 值
- `COUNT(*)` 会计算所有行（包括 NULL）
- 在使用 `AVG`、`STDDEV` 等函数时，使用 `DECIMAL`、`DOUBLE`、`DECFLOAT` 或 `REAL` 类型可以获得更好的精度
- `ROUND(AVG(salary), 2)` 是非常常用的组合操作
- 为了在大表上获得更好的性能，建议在 `GROUP BY` 的列上创建适当的 indexes 

您目前尝试在查询中使用哪种模式？

**References:**

- [IBM Db2 Documentation - Aggregate functions](https://www.ibm.com/docs/en/db2/11.5?topic=functions-aggregate)
- [IBM Db2 Documentation - AVG](https://www.ibm.com/docs/en/db2/11.5?topic=functions-avg)
- [IBM Db2 Documentation - Variance & Standard Deviation functions](https://www.ibm.com/docs/en/db2/11.5?topic=functions-variance-stddev)