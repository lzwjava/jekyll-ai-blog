---
audio: false
generated: true
lang: en
layout: post
title: Counting Rows in Scrollable ResultSet
translated: false
type: note
---

In Java, when you are working with a `ResultSet` (e.g., through `Statement.executeQuery()`), counting the rows can be tricky if the `fetchSize` is set to `0` (which means that the JDBC driver will fetch rows as needed). Moreover, using a scrollable result set (using `ResultSet.TYPE_SCROLL_INSENSITIVE` or `ResultSet.TYPE_SCROLL_SENSITIVE`) allows you to navigate through the result set but requires more memory as the rows are loaded into the memory.

Here's a strategy you can use to count rows in a `ResultSet` without requiring a complete traversal of the result set. It uses the `scrollable` feature of the `ResultSet` and the ability to "go to the last row" and "get the row number".

### Steps to count rows using a scrollable `ResultSet`:

1. **Create a scrollable ResultSet**: Make sure to use a `Statement` that can generate scrollable result sets by setting the appropriate cursor type.
2. **Move to the last row**: The scrollable result set allows you to go to the last row using `last()`.
3. **Get the row number**: After moving to the last row, you can call `getRow()` to determine the number of rows.
4. **Optional**: If you need to iterate through the result set, move back to the first row using `first()`.

Here is an example implementation in Java:

```java
import java.sql.*;

public class RowCountExample {
    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/your_database";
        String username = "your_username";
        String password = "your_password";

        Connection conn = null;
        Statement stmt = null;
        ResultSet rs = null;

        try {
            conn = DriverManager.getConnection(url, username, password);
            stmt = conn.createStatement(
                    ResultSet.TYPE_SCROLL_INSENSITIVE,
                    ResultSet.CONCUR_READ_ONLY);
            rs = stmt.executeQuery("SELECT * FROM your_table");

            // Move to the last row to count the total number of rows
            if (rs.last()) {
                int rowCount = rs.getRow();
                System.out.println("Total rows: " + rowCount);

                // Optionally, move back to the first row
                rs.first();
            }
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            try {
                if (rs != null) rs.close();
                if (stmt != null) stmt.close();
                if (conn != null) conn.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }
}
```

### Key Points:

* **Scrollable ResultSet**: We create a scrollable `ResultSet` using `ResultSet.TYPE_SCROLL_INSENSITIVE`. This type of result set allows you to move to the last row and get the row count.
* **Row Count**: The `rs.getRow()` method returns the current row number when the cursor is positioned at the last row. This value is effectively the total number of rows in the result set.
* **Fetch Size**: If the `fetchSize` is `0`, the driver fetches rows dynamically, but using a scrollable result set allows us to navigate the rows efficiently.

### Best Practice:

* **Memory Efficiency**: While scrollable result sets are useful for counting rows, be aware that they may consume more memory, as all rows need to be loaded into the memory. If you're working with a large dataset, consider using a different approach (like iterating over the result set without `last()` to count rows incrementally) if memory usage is a concern.
* **Alternative Approach**: If memory is an issue and you only need the row count, you can execute a `SELECT COUNT(*)` query instead of retrieving the entire result set. This is often more efficient.

```sql
SELECT COUNT(*) FROM your_table;
```

Let me know if you need further clarification!
