---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 使用 MagicMock 模拟 IBM DB2 游标
translated: true
type: note
---

要使用 `unittest.mock.MagicMock` 模拟 IBM DB2 cursor（通常用于单元测试中以避免真实的数据库连接），你可以模拟 `ibm_db_dbi` 连接和 cursor 对象的行为。`ibm_db_dbi` 库遵循 Python DB-API 2.0 规范，因此 cursor 支持标准方法，如 `.execute()`、`.fetchone()`、`.fetchall()`、`.fetchmany()` 以及属性如 `.description`。

### 基础手动 Mocking（不使用 `@patch`）

直接创建 mock 对象并将其注入到代码中（如果你的函数接受 connection 或 cursor 作为参数，这种方法非常有用）。

```python
from unittest.mock import MagicMock

# 模拟查询返回的数据
mock_rows = [
    (1, 'Alice', 100.0),
    (2, 'Bob', 200.0)
]
mock_description = [
    ('ID',), ('NAME',), ('BALANCE',)
]

# 创建 mock cursor
mock_cursor = MagicMock()
mock_cursor.fetchall.return_value = mock_rows          # 用于 cursor.fetchall()
mock_cursor.fetchone.return_value = mock_rows[0]       # 用于 cursor.fetchone()
mock_cursor.fetchmany.return_value = mock_rows[:1]     # 用于 cursor.fetchmany(size)
mock_cursor.description = mock_description              # 列信息
mock_cursor.rowcount = len(mock_rows)                  # 受影响/返回的行数

# 创建 mock connection (cursor() 返回 mock cursor)
mock_conn = MagicMock()
mock_conn.cursor.return_value = mock_cursor

# 使用 ibm_db_dbi 的示例函数
def query_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM accounts")
    results = cur.fetchall()
    cur.close()
    return results

# 使用 mocks 进行测试
results = query_data(mock_conn)
print(results)  # [(1, 'Alice', 100.0), (2, 'Bob', 200.0)]

# 断言 (Assertions)
mock_cursor.execute.assert_called_once_with("SELECT * FROM accounts")
mock_cursor.fetchall.assert_called_once()
```

### 使用 `@patch` 进行自动 Mocking

如果你的代码直接调用 `ibm_db_dbi.connect()`，可以使用 patch 来返回你的 mock connection。

```python
import unittest
from unittest.mock import patch, MagicMock

def get_data_from_db():
    import ibm_db_dbi as db2
    conn = db2.connect()  # 这里将被 patched
    cur = conn.cursor()
    cur.execute("SELECT id, name, balance FROM accounts WHERE active = ?", (1,))
    rows = cur.fetchall()
    conn.close()
    return rows

class TestDBQuery(unittest.TestCase):
    @patch('your_module.ibm_db_dbi.connect')  # 将 'your_module' 替换为实际的模块路径
    def test_get_data_from_db(self, mock_connect):
        # 设置 mock 数据
        expected_rows = [(1, 'Alice', 100.0), (2, 'Bob', 200.0)]

        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = expected_rows

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        mock_connect.return_value = mock_conn

        # 运行函数
        result = get_data_from_db()

        # 断言
        self.assertEqual(result, expected_rows)
        mock_cursor.execute.assert_called_once_with(
            "SELECT id, name, balance FROM accounts WHERE active = ?", (1,)
        )
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
```

### 处理 Context Managers（例如 `with conn.cursor() as cur:`）

如果你的代码使用了上下文管理器：

```python
mock_cursor = MagicMock()
mock_cursor.fetchall.return_value = expected_rows

mock_conn = MagicMock()
mock_conn.cursor.return_value.__enter__.return_value = mock_cursor  # 处理 'with ... as cur'
mock_conn.cursor.return_value.__exit__.return_value = None
```

### 提示

- 对于多次调用，使用 `side_effect`：`mock_cursor.fetchall.side_effect = [row1_list, row2_list]`。
- 对于无结果的情况：`mock_cursor.fetchall.return_value = []` 且 `mock_cursor.fetchone.return_value = None`。
- 作为良好的实践，务必在真实代码中关闭 cursor/connection。
- 这种方法之所以有效，是因为 `ibm_db_dbi` 符合 DB-API 规范，类似于模拟 `psycopg2`、`pyodbc` 或 `sqlite3` 的 cursors。

通过这种方式，可以在测试中避免真实的数据库连接，同时验证查询语句并处理结果。