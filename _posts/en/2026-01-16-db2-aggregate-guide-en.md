---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Guide to DB2 Aggregate Functions
translated: false
type: note
---

**Question:** How to use DB2 aggregate functions like SUM, AVG, and other common statistical functions?

**Answer:**

Here are the most commonly used aggregate (statistics) functions in DB2 with practical examples:

### Basic Syntax
```sql
SELECT 
    function_name(column) 
FROM table 
[WHERE ...]
[GROUP BY ...]
[HAVING ...]
```

### Most Common Aggregate Functions in DB2

| Function       | Meaning                          | Ignores NULL? | Typical Data Type | Example                                   |
|----------------|----------------------------------|---------------|-------------------|-------------------------------------------|
| `COUNT(*)`     | Total number of rows             | No            | -                 | `COUNT(*)`                                |
| `COUNT(col)`   | Number of non-NULL values        | Yes           | any               | `COUNT(salary)`                           |
| `SUM(col)`     | Sum of values                    | Yes           | numeric           | `SUM(sales_amount)`                       |
| `AVG(col)`     | Average (arithmetic mean)        | Yes           | numeric           | `AVG(price)`                              |
| `MIN(col)`     | Smallest value                   | Yes           | numeric/string/date | `MIN(order_date)`                      |
| `MAX(col)`     | Largest value                    | Yes           | numeric/string/date | `MAX(salary)`                          |
| `STDDEV(col)`  | Standard deviation (sample)      | Yes           | numeric           | `STDDEV(salary)`                          |
| `STDDEV_SAMP`  | Same as STDDEV (sample)          | Yes           | numeric           | `STDDEV_SAMP(score)`                      |
| `STDDEV_POP`   | Population standard deviation    | Yes           | numeric           | `STDDEV_POP(weight)`                      |
| `VARIANCE`     | Sample variance                  | Yes           | numeric           | `VARIANCE(temperature)`                   |
| `VAR_SAMP`     | Same as VARIANCE                 | Yes           | numeric           | `VAR_SAMP(sales)`                         |
| `VAR_POP`      | Population variance              | Yes           | numeric           | `VAR_POP(income)`                         |

### Practical Examples

```sql
-- 1. Simple totals and averages
SELECT 
    SUM(salary)          AS total_salary,
    AVG(salary)          AS avg_salary,
    ROUND(AVG(salary), 2) AS avg_salary_rounded,
    COUNT(*)             AS employee_count,
    COUNT(salary)        AS employees_with_salary
FROM employees;


-- 2. Group by department
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


-- 3. Statistical distribution (variance & standard deviation)
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


-- 4. With filter + rounding
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


-- 5. Combining multiple aggregates with different precision
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

### Important Notes in DB2

- `AVG()`, `SUM()` and statistical functions ignore NULL values
- `COUNT(*)` counts all rows (including NULLs)
- Use `DECIMAL`, `DOUBLE`, `DECFLOAT` or `REAL` for better precision with `AVG`, `STDDEV`, etc.
- `ROUND(AVG(salary), 2)` is very commonly used
- For better performance on large tables → create appropriate indexes on `GROUP BY` columns

Which of these patterns are you trying to use in your current query?

**References:**

- [IBM Db2 Documentation - Aggregate functions](https://www.ibm.com/docs/en/db2/11.5?topic=functions-aggregate)
- [IBM Db2 Documentation - AVG](https://www.ibm.com/docs/en/db2/11.5?topic=functions-avg)
- [IBM Db2 Documentation - Variance & Standard Deviation functions](https://www.ibm.com/docs/en/db2/11.5?topic=functions-variance-stddev)