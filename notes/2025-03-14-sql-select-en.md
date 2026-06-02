---
audio: false
generated: true
lang: en
layout: post
title: SQL SELECT Statements
translated: false
type: note
---

To answer your query about how to use `SELECT`, `LEFT JOIN`, `RIGHT JOIN`, complex `SELECT`, `FROM`, `GROUP BY`, `WHERE NOT IN`, and `IN` in SQL, I’ll explain each component clearly and provide practical examples. These are fundamental SQL operations used to retrieve and manipulate data from databases. Let’s break them down step by step, using a simple database schema for consistency:

- **Tables:**
  - `employees` (columns: `employee_id`, `employee_name`, `department_id`, `salary`)
  - `departments` (columns: `department_id`, `department_name`)
  - `projects` (columns: `project_id`, `project_name`, `employee_id`)

---

### 1. SELECT

The `SELECT` clause is used to specify the columns you want to retrieve from a database table. It forms the foundation of any SQL query.

- **Purpose:** Choose which data to display.
- **Example:**

  ```sql
  SELECT employee_name, salary
  FROM employees;
  ```

  This retrieves the `employee_name` and `salary` columns from the `employees` table.

---

### 2. FROM

The `FROM` clause identifies the table (or tables) from which to pull the data. It’s always used with `SELECT`.

- **Purpose:** Specify the data source.
- **Example:**

  ```sql
  SELECT employee_name
  FROM employees;
  ```

  Here, `employees` is the table being queried.

---

### 3. LEFT JOIN

A `LEFT JOIN` (or `LEFT OUTER JOIN`) combines rows from two tables. It returns all records from the left table and the matching records from the right table. If there’s no match, the result includes `NULL` values for the right table’s columns.

- **Purpose:** Include all rows from the left table, regardless of matches in the right table.
- **Example:**

  ```sql
  SELECT e.employee_name, d.department_name
  FROM employees e
  LEFT JOIN departments d
  ON e.department_id = d.department_id;
  ```

  This lists all employees and their department names. If an employee isn’t assigned to a department, `department_name` will be `NULL`.

---

### 4. RIGHT JOIN

A `RIGHT JOIN` (or `RIGHT OUTER JOIN`) is similar to a `LEFT JOIN`, but it returns all records from the right table and the matching records from the left table. Non-matching left table rows result in `NULL` values.

- **Purpose:** Include all rows from the right table, regardless of matches in the left table.
- **Example:**

  ```sql
  SELECT e.employee_name, d.department_name
  FROM employees e
  RIGHT JOIN departments d
  ON e.department_id = d.department_id;
  ```

  This shows all departments and their employees. Departments with no employees will have `NULL` in `employee_name`.

---

### 5. Complex SELECT

A “complex `SELECT`” isn’t a formal SQL term but typically refers to a `SELECT` statement that combines multiple clauses, joins, subqueries, or aggregate functions to perform advanced data retrieval.

- **Purpose:** Handle intricate queries involving multiple operations.
- **Example:**

  ```sql
  SELECT d.department_name, COUNT(e.employee_id) AS employee_count
  FROM departments d
  LEFT JOIN employees e
  ON d.department_id = e.department_id
  GROUP BY d.department_name
  HAVING COUNT(e.employee_id) > 5;
  ```

  This finds departments with more than 5 employees, counting employees per department and filtering the results.

---

### 6. GROUP BY

The `GROUP BY` clause groups rows that have the same values in specified columns into summary rows, often used with aggregate functions like `COUNT`, `SUM`, or `AVG`.

- **Purpose:** Aggregate data based on column values.
- **Example:**

  ```sql
  SELECT department_id, COUNT(employee_id) AS employee_count
  FROM employees
  GROUP BY department_id;
  ```

  This counts the number of employees in each department.

---

### 7. WHERE NOT IN

The `WHERE NOT IN` clause filters rows where a column’s value is not present in a specified list or subquery result. Be cautious: if the list/subquery includes `NULL`, no rows may return.

- **Purpose:** Exclude rows based on a set of values.
- **Example:**

  ```sql
  SELECT employee_name
  FROM employees
  WHERE department_id NOT IN (1, 2);
  ```

  This retrieves employees not in departments 1 or 2.

- **With Subquery:**

  ```sql
  SELECT employee_name
  FROM employees
  WHERE department_id NOT IN (SELECT department_id FROM departments WHERE department_name = 'Inactive');
  ```

  This finds employees not in departments marked as ‘Inactive’.

---

### 8. IN

The `IN` clause filters rows where a column’s value matches any value in a list or subquery. It’s a shorthand for multiple `OR` conditions.

- **Purpose:** Include rows based on a set of values.
- **Example:**

  ```sql
  SELECT employee_name
  FROM employees
  WHERE department_id IN (3, 4);
  ```

  This retrieves employees in departments 3 or 4.

- **With Subquery:**

  ```sql
  SELECT employee_name
  FROM employees
  WHERE department_id IN (
      SELECT department_id
      FROM employees
      GROUP BY department_id
      HAVING COUNT(employee_id) > 5
  );
  ```

  This finds employees in departments with more than 5 employees.

---

### Putting It All Together

Here’s an example combining several of these operations:

```sql
SELECT d.department_name, COUNT(e.employee_id) AS employee_count
FROM departments d
LEFT JOIN employees e
ON d.department_id = e.department_id
WHERE e.department_id NOT IN (1, 2)
GROUP BY d.department_name;
```

- **Explanation:**
  - `FROM departments d`: Starts with the `departments` table.
  - `LEFT JOIN employees e`: Includes all departments, even those without employees.
  - `WHERE NOT IN (1, 2)`: Excludes employees from departments 1 and 2.
  - `GROUP BY d.department_name`: Groups results by department name.
  - `SELECT ... COUNT`: Counts employees per department.

---

### Key Tips

- **Joins:** Choose `LEFT JOIN` or `RIGHT JOIN` based on which table’s rows you want to keep fully (left or right).
- **NULLs with NOT IN:** If a subquery returns `NULL`, `NOT IN` may exclude all rows unexpectedly. Consider `NOT EXISTS` as an alternative.
- **Complex Queries:** Break them into parts (e.g., test joins separately) to ensure correctness.
- **Order Matters:** Place `WHERE` before `GROUP BY`, and use `HAVING` after `GROUP BY` for group-level filters.

By understanding and combining these SQL components—`SELECT`, `FROM`, `LEFT JOIN`, `RIGHT JOIN`, `GROUP BY`, `WHERE NOT IN`, and `IN`—you can craft queries to retrieve and analyze data effectively from any relational database.
