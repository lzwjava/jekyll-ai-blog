---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: Python连接IBM DB2指南
translated: true
type: note
---

### 概述
IBM DB2 是一款关系型数据库管理系统，Python 可通过 `ibm_db` 包与其交互，该包提供底层接口；另有 `ibm_db_dbi` 作为符合 DB-API 2.0 规范的封装层，基于 `ibm_db` 构建，提供更简便、更符合 Python 风格的用法。`ibm_db` 更直接且功能强大，但需要更深入的知识；而 `ibm_db_dbi` 模仿 Python 的 `sqlite3` 模块，简化了标准数据库操作。两者均属于 IBM DB2 Python 驱动程序。

### 安装
使用 pip 安装包：
```
pip install ibm_db
pip install ibm_db_dbi
```
注意：这些包需要 DB2 客户端库。在 Windows/Linux 上，请从 IBM 网站下载并安装 IBM Data Server Driver Package。在 macOS 上可能需要额外配置。确保 DB2 服务器可访问（例如在具有凭据的主机上运行）。

### 使用 ibm_db
`ibm_db` 提供连接、执行语句和处理结果的函数。它不符合 DB-API 规范，但提供更多控制权。

#### 基本连接与查询
```python
import ibm_db

# 连接字符串格式：DATABASE=<数据库名>;HOSTNAME=<主机>;PORT=<端口>;PROTOCOL=TCPIP;UID=<用户>;PWD=<密码>;
conn_str = "DATABASE=mydb;HOSTNAME=192.168.1.100;PORT=50000;PROTOCOL=TCPIP;UID=myuser;PWD=mypassword;"

# 连接
conn = ibm_db.connect(conn_str, "", "")

# 执行查询
stmt = ibm_db.exec_immediate(conn, "SELECT * FROM MYTABLE")

# 获取结果（逐行获取）
row = ibm_db.fetch_assoc(stmt)
while row:
    print(row)  # 返回字典
    row = ibm_db.fetch_assoc(stmt)

# 关闭连接
ibm_db.close(conn)
```
- **关键函数**：`connect()`、`exec_immediate()`（用于简单查询）、`prepare()` 和 `execute()`（用于参数化查询以防止注入）。
- **预处理语句**：使用 `prepare()` 编译查询，并使用 `execute()` 传入参数。

#### 错误处理
```python
try:
    conn = ibm_db.connect(conn_str, "", "")
except Exception as e:
    print(f"连接失败：{str(e)}")
```

### 使用 ibm_db_dbi
`ibm_db_dbi` 实现了 DB-API 2.0，使其可与 `sqlite3` 或 `psycopg2` 等模块互换使用。

#### 基本连接与查询
```python
import ibm_db_dbi

# 连接字符串与 ibm_db 类似
conn_str = "DATABASE=mydb;HOSTNAME=192.168.1.100;PORT=50000;PROTOCOL=TCPIP;UID=myuser;PWD=mypassword;"

# 连接
conn = ibm_db_dbi.connect(conn_str)

# 创建游标
cursor = conn.cursor()

# 执行查询
cursor.execute("SELECT * FROM MYTABLE")

# 获取结果
rows = cursor.fetchall()  # 返回元组列表
for row in rows:
    print(row)

# 关闭
cursor.close()
conn.close()
```
- **参数化查询**：`cursor.execute("SELECT * FROM MYTABLE WHERE ID = ?", (id_value,))` – 使用 ? 作为占位符。
- **事务**：`conn.commit()` 或 `conn.rollback()`；默认关闭自动提交。

### 主要差异及使用场景

| 特性               | ibm_db                          | ibm_db_dbi                      |
|--------------------|---------------------------------|---------------------------------|
| 规范符合性         | 非 DB-API（底层）               | 符合 DB-API 2.0 规范           |
| 易用性             | 需要更多代码；直接访问           | 语法更简单，类似 Python 风格    |
| 性能               | 复杂操作可能更快                 | 封装层带来开销                 |
| 功能               | 完整的 DB2 功能                 | 通过 DB-API 接口提供功能子集   |
| 使用场景           | 需要原始控制的自定义应用         | 标准 CRUD 操作                 |

若习惯其他 DB-API 驱动程序，可选用 `ibm_db_dbi` 以保持熟悉度。如需使用存储过程或批量操作等高级 DB2 特定功能，可切换至 `ibm_db`。

### 最佳实践
- 始终在 `try-finally` 或 `with` 块中处理异常并关闭连接，以避免资源泄漏。
- 对于大型结果集，使用 `fetchmany(size)` 而非 `fetchall()` 以限制内存使用。
- 检查 DB2 版本兼容性；这些包支持 DB2 LUW、z/OS、iSeries。
- 有关 SSL 连接或 CLPPlus 集成等高级主题，请参阅 IBM 文档。

更多示例请访问 [IBM db2 Python 驱动程序仓库](https://github.com/ibmdb/python-ibmdb)。若遇到问题，请确保 DB2 实例正在运行且凭据正确。
