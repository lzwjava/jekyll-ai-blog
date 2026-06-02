---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 将 DB2 表导出到文件
translated: true
type: note
---

问题：如何使用 DB2 命令将表（或其数据）导出到文件？

答案：

在 DB2（Linux/Unix/Windows 或 z/OS 上），用于导出表数据的主要命令行工具是 **EXPORT** 命令。它可以通过 DB2 命令行处理器 (CLP) 或 db2cmd (Windows) 运行。

### 基本语法

```
db2 "EXPORT TO filename OF export_format [options] SELECT_statement"
```

### 常用导出格式

| 格式 | 文件扩展名 | 用例 |
|------|----------------|----------|
| DEL  | .del 或 .csv   | 分隔符 ASCII（最常见，类似于 CSV） |
| IXF  | .ixf           | IBM DB2 原生格式（最适合导入回 DB2） |
| WSF  | .wsf           | 工作表格式（用于 Lotus/Excel） |

### 示例

1. **将整个表导出到类似 CSV 的分隔文件中**

   ```
   db2 "EXPORT TO /path/employees.del OF DEL SELECT * FROM SCHEMA.EMPLOYEES"
   ```

2. **使用自定义分隔符并包含列名进行导出**

   ```
   db2 "EXPORT TO employees.csv OF DEL MODIFIED BY COLDEL, DECPLUSBLANK MESSAGES msgs.txt SELECT * FROM MYSCHEMA.EMPLOYEES"
   ```

   - `COLDEL,` → 使用逗号作为列分隔符
   - `DECPLUSBLANK` → 为正小数保留加号
   - 第一行将包含列标题

3. **仅导出选定列或带 WHERE 子句的导出**

   ```
   db2 "EXPORT TO active_emps.del OF DEL SELECT EMPNO, FIRSTNME, LASTNAME, SALARY FROM EMPLOYEE WHERE SALARY > 50000 ORDER BY SALARY DESC"
   ```

4. **以 IXF 格式导出（计划导入回 DB2 时推荐）**

   ```
   db2 "EXPORT TO employee.ixf OF IXF MESSAGES msgs.txt SELECT * FROM EMPLOYEE"
   ```

5. **导出带 LOB 的大型表（添加 LOBINFILE 选项）**

   ```
   db2 "EXPORT TO data.del OF DEL LOBINFILE lobdata MODIFIED BY CODEPAGE=1208 SELECT * FROM DOCUMENTS"
   ```

   这将为 LOB 列创建单独的文件。

6. **在 Windows 命令提示符 (db2cmd) 中**

   ```
   db2 connect to MYDB
   db2 "EXPORT TO C:\temp\data.del OF DEL SELECT * FROM MYTABLE"
   ```

### 常用 MODIFIED BY 选项（用于 DEL 格式）

| 选项              | 效果 |
|---------------------|--------|
| `COLDEL;`           | 使用分号作为分隔符 |
| `COLDEL,`           | 使用逗号（标准 CSV） |
| `CHARDEL""`         | 双引号作为字符分隔符 |
| `DECIMAL.`          | 使用点作为小数点 |
| `CODEPAGE=1208`     | UTF-8 编码 |
| `NOCHARDEL`         | 不对字符字段加引号 |
| `STRIPBLANKS`       | 删除尾随空格 |

### 替代方法

- **db2look** – 仅导出表结构 (DDL)
  `db2look -d MYDB -t SCHEMA.TABLE -e > table_ddl.sql`
- **db2move** – 一次导出多个/所有表（IXF 格式）
  `db2move MYDB EXPORT`

参考资料：

- [IBM DB2 EXPORT command documentation](https://www.ibm.com/docs/en/db2/11.5?topic=commands-export)
- [db2move utility](https://www.ibm.com/docs/en/db2/11.5?topic=commands-db2move)
