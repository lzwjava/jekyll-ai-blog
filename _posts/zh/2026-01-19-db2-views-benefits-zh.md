---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 深入理解 DB2 视图及其优势
translated: true
type: note
---

Question: What is a view in DB2, and why do we use views?

Answer:

In DB2 中，**view** 是一个 **virtual table**（也称为命名查询），它代表了一个存储好的 SELECT statement 的结果。它不是物理表，本身不存储任何数据。当你查询一个 view 时，DB2 会针对 base tables（一个或多个真实表，甚至可以是其他 views）执行底层的 SELECT statement，并将结果像真实表一样返回。

### Basic Syntax to Create a View

```sql
CREATE VIEW view_name [(column_list)]
AS
    SELECT_statement
    [WITH [CASCADED | LOCAL] CHECK OPTION];
```

Example:

```sql
CREATE VIEW active_employees AS
SELECT emp_id, first_name, last_name, department, hire_date
FROM employees
WHERE status = 'ACTIVE'
  AND hire_date > '2020-01-01';
```

### Main Reasons to Use Views in DB2

Views 被广泛使用，因为它们提供了几个重要的好处：

- **Simplify complex queries**
  你可以隐藏 joins、subqueries、aggregations、calculations 或复杂的 WHERE clauses。用户只需查询一个简单的 view 名称，而不需要反复编写冗长的 SQL。

- **Enhance security and data protection**
  仅授予对 view 的 SELECT 权限（而不是对 base tables 的权限）。
  你可以只显示特定的列或特定的行（row-level security）。
  例如：仅向 HR 用户显示薪资信息，对其他用户隐藏。

- **Provide data abstraction / logical data independence**
  底层的表结构可以更改（列名、拆分表等），但只要相应地更新 view 定义，应用程序就可以继续使用相同的 view 名称而无需更改代码。

- **Present data in a user-friendly or business-oriented way**
  将列重命名为更有意义的名称。
  将来自多个表的数据组合成一个逻辑上的 "business view"。
  格式化或派生新列（例如：`CONCAT(first_name, ' ', last_name) AS full_name`）。

- **Improve consistency**
  每个人都对 "本年销售额"、"活跃客户"、"库存状态" 等使用相同的定义，从而避免不同的人编写略有不同（且可能错误）的查询。

- **Logical data organization without duplication**
  不需要额外的存储空间（除了 view 定义本身）。
  数据保留在 base tables 中 —— views 只是为相同的数据提供了不同的 "窗口"。

- **Support some updatable views** (with restrictions)
  简单的 views（通常针对一张表，没有 joins，没有 aggregates 等）可以允许 INSERT、UPDATE、DELETE 操作透传到 base table。

### Summary Table: Key Advantages of Views

| Benefit                  | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| Simplicity               | 隐藏 joins、filters、calculations 的复杂性                                     |
| Security                 | Column-level 和 row-level 的访问控制                                          |
| Data abstraction         | 保护应用程序免受底层表更改的影响                                                   |
| Consistency              | 在用户/应用程序之间标准化常用查询                                                  |
| No storage overhead      | 虚拟的 —— 仅存储定义                                                          |
| Readability              | 为终端用户提供更有意义的列名和结构                                                 |

Views 是 DB2（以及通用的关系型数据库）中最强大且最常用的功能之一，用于构建可维护、安全且对用户友好的数据库应用程序。

References:  

- [DB2 Views - db2tutorial.com](https://www.db2tutorial.com/db2-view)
- [IBM Db2 Documentation - CREATE VIEW](https://www.ibm.com/docs/en/db2/11.5?topic=statements-create-view)
- [Tutorialspoint - DB2 Views](https://www.tutorialspoint.com/db2/db2_views.htm)
- [Mainframe Tech Help - DB2 View](https://www.mainframestechhelp.com/tutorials/db2/view.htm)