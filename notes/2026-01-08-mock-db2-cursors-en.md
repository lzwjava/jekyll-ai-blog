---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Mocking IBM DB2 Cursors with MagicMock
translated: false
type: note
---

To mock an IBM DB2 cursor using `unittest.mock.MagicMock` (typically in unit tests to avoid real database connections), you can simulate the behavior of `ibm_db_dbi` connection and cursor objects. The `ibm_db_dbi` library follows the Python DB-API 2.0 specification, so the cursor supports standard methods like `.execute()`, `.fetchone()`, `.fetchall()`, `.fetchmany()`, and attributes like `.description`.

### Basic Manual Mocking (Without `@patch`)
Create mock objects directly and inject them into your code (useful if your function accepts a connection or cursor as a parameter).

```python
from unittest.mock import MagicMock

# Mock data to return from queries
mock_rows = [
    (1, 'Alice', 100.0),
    (2, 'Bob', 200.0)
]
mock_description = [
    ('ID',), ('NAME',), ('BALANCE',)
]

# Create mock cursor
mock_cursor = MagicMock()
mock_cursor.fetchall.return_value = mock_rows          # For cursor.fetchall()
mock_cursor.fetchone.return_value = mock_rows[0]       # For cursor.fetchone()
mock_cursor.fetchmany.return_value = mock_rows[:1]     # For cursor.fetchmany(size)
mock_cursor.description = mock_description              # Column info
mock_cursor.rowcount = len(mock_rows)                  # Rows affected/returned

# Create mock connection (cursor() returns the mock cursor)
mock_conn = MagicMock()
mock_conn.cursor.return_value = mock_cursor

# Example function using ibm_db_dbi
def query_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM accounts")
    results = cur.fetchall()
    cur.close()
    return results

# Test it with mocks
results = query_data(mock_conn)
print(results)  # [(1, 'Alice', 100.0), (2, 'Bob', 200.0)]

# Assertions
mock_cursor.execute.assert_called_once_with("SELECT * FROM accounts")
mock_cursor.fetchall.assert_called_once()
```

### Using `@patch` for Automatic Mocking
If your code calls `ibm_db_dbi.connect()` directly, patch it to return your mock connection.

```python
import unittest
from unittest.mock import patch, MagicMock

def get_data_from_db():
    import ibm_db_dbi as db2
    conn = db2.connect()  # This will be patched
    cur = conn.cursor()
    cur.execute("SELECT id, name, balance FROM accounts WHERE active = ?", (1,))
    rows = cur.fetchall()
    conn.close()
    return rows

class TestDBQuery(unittest.TestCase):
    @patch('your_module.ibm_db_dbi.connect')  # Replace 'your_module' with the actual module path
    def test_get_data_from_db(self, mock_connect):
        # Setup mock data
        expected_rows = [(1, 'Alice', 100.0), (2, 'Bob', 200.0)]

        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = expected_rows

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        mock_connect.return_value = mock_conn

        # Run the function
        result = get_data_from_db()

        # Assertions
        self.assertEqual(result, expected_rows)
        mock_cursor.execute.assert_called_once_with(
            "SELECT id, name, balance FROM accounts WHERE active = ?", (1,)
        )
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
```

### Handling Context Managers (e.g., `with conn.cursor() as cur:`)
If your code uses context managers:

```python
mock_cursor = MagicMock()
mock_cursor.fetchall.return_value = expected_rows

mock_conn = MagicMock()
mock_conn.cursor.return_value.__enter__.return_value = mock_cursor  # Handles 'with ... as cur'
mock_conn.cursor.return_value.__exit__.return_value = None
```

### Tips
- Use `side_effect` for multiple calls: `mock_cursor.fetchall.side_effect = [row1_list, row2_list]`.
- For no results: `mock_cursor.fetchall.return_value = []` and `mock_cursor.fetchone.return_value = None`.
- Always close the cursor/connection in your real code for good practice.
- This approach works because `ibm_db_dbi` is DB-API compliant, similar to mocking `psycopg2`, `pyodbc`, or `sqlite3` cursors.

This avoids real DB connections in tests while verifying queries and handling results.
