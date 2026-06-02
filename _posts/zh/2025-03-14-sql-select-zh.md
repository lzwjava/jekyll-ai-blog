---
audio: false
generated: true
lang: zh
layout: post
title: SQL SELECT语句
translated: true
type: note
---

关于如何在SQL中使用`SELECT`、`LEFT JOIN`、`RIGHT JOIN`、复杂`SELECT`、`FROM`、`GROUP BY`、`WHERE NOT IN`和`IN`的查询，我将清晰解释每个组成部分并提供实际示例。这些都是用于从数据库检索和操作数据的基础SQL操作。让我们逐步解析，并使用统一的简单数据库模式：

- **数据表：**
  - `employees`（字段：`employee_id`, `employee_name`, `department_id`, `salary`）
  - `departments`（字段：`department_id`, `department_name`）
  - `projects`（字段：`project_id`, `project_name`, `employee_id`）

---

### 1. SELECT
`SELECT`子句用于指定要从数据库表中检索的列。它是所有SQL查询的基础。

- **用途：** 选择要显示的数据
- **示例：**
  ```sql
  SELECT employee_name, salary
  FROM employees;
  ```
  这将从`employees`表中检索`employee_name`和`salary`列

---

### 2. FROM
`FROM`子句标识要从中提取数据的表（或多个表）。它总是与`SELECT`一起使用。

- **用途：** 指定数据源
- **示例：**
  ```sql
  SELECT employee_name
  FROM employees;
  ```
  这里，`employees`是被查询的表

---

### 3. LEFT JOIN
`LEFT JOIN`（或`LEFT OUTER JOIN`）组合两个表的行。它返回左表的所有记录和右表的匹配记录。如果没有匹配项，结果将包含右表列的`NULL`值。

- **用途：** 包含左表的所有行，无论右表是否有匹配项
- **示例：**
  ```sql
  SELECT e.employee_name, d.department_name
  FROM employees e
  LEFT JOIN departments d
  ON e.department_id = d.department_id;
  ```
  这将列出所有员工及其部门名称。如果员工未分配部门，`department_name`将为`NULL`

---

### 4. RIGHT JOIN
`RIGHT JOIN`（或`RIGHT OUTER JOIN`）与`LEFT JOIN`类似，但返回右表的所有记录和左表的匹配记录。不匹配的左表行将产生`NULL`值。

- **用途：** 包含右表的所有行，无论左表是否有匹配项
- **示例：**
  ```sql
  SELECT e.employee_name, d.department_name
  FROM employees e
  RIGHT JOIN departments d
  ON e.department_id = d.department_id;
  ```
  这将显示所有部门及其员工。没有员工的部门将在`employee_name`中显示`NULL`

---

### 5. 复杂SELECT
"复杂`SELECT`"不是正式的SQL术语，但通常指结合了多个子句、连接、子查询或聚合函数以执行高级数据检索的`SELECT`语句。

- **用途：** 处理涉及多个操作的复杂查询
- **示例：**
  ```sql
  SELECT d.department_name, COUNT(e.employee_id) AS employee_count
  FROM departments d
  LEFT JOIN employees e
  ON d.department_id = e.department_id
  GROUP BY d.department_name
  HAVING COUNT(e.employee_id) > 5;
  ```
  这将查找员工数超过5人的部门，按部门统计员工数并筛选结果

---

### 6. GROUP BY
`GROUP BY`子句将具有指定列相同值的行分组为汇总行，通常与`COUNT`、`SUM`或`AVG`等聚合函数一起使用。

- **用途：** 基于列值聚合数据
- **示例：**
  ```sql
  SELECT department_id
