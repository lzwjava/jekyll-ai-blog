---
audio: false
generated: true
lang: zh
layout: post
title: 可滚动结果集的行数统计
translated: true
type: note
---

在 Java 中，当您处理 `ResultSet`（例如通过 `Statement.executeQuery()`）时，如果 `fetchSize` 设置为 `0`（这意味着 JDBC 驱动程序会根据需要获取行），统计行数可能会比较棘手。此外，使用可滚动的结果集（使用 `ResultSet.TYPE_SCROLL_INSENSITIVE` 或 `ResultSet.TYPE_SCROLL_SENSITIVE`）允许您在结果集中导航，但需要更多内存，因为行会被加载到内存中。

以下是一种无需完全遍历结果集即可统计 `ResultSet` 行数的策略。它利用了 `ResultSet` 的可滚动特性以及“跳到最后一行”和“获取行号”的能力。

### 使用可滚动 `ResultSet` 统计行数的步骤

1. **创建可滚动结果集**：通过设置适当的游标类型，确保使用能够生成可滚动结果集的 `Statement`。
2. **移动到最后一行**：可滚动结果集允许您使用 `last()` 跳到最后一行。
3. **获取行号**：移动到最后一行后，可以调用 `getRow()` 来确定行数。
4. **可选**：如果需要遍历结果集，使用 `first()` 移回第一行。

以下是 Java 中的示例实现：

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

            // 移动到最后一行以统计总行数
            if (rs.last()) {
                int rowCount = rs.getRow();
                System.out.println("总行数: " + rowCount);

                // 可选操作：移回第一行
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

### 关键点

* **可滚动结果集**：我们使用 `ResultSet.TYPE_SCROLL_INSENSITIVE` 创建可滚动 `ResultSet`。这种类型的结果集允许您移动到最后一行并获取行数。
* **行数统计**：当游标位于最后一行时，`rs.getRow()` 方法返回当前行号。该值实际上就是结果集中的总行数。
* **获取大小**：如果 `fetchSize` 为 `0`，驱动程序会动态获取行，但使用可滚动结果集允许我们高效地导航行。

### 最佳实践

* **内存效率**：虽然可滚动结果集对于统计行数很有用，但请注意它们可能会消耗更多内存，因为所有行都需要加载到内存中。如果您处理的是大型数据集，并且内存使用是一个问题，请考虑使用不同的方法（例如在不使用 `last()` 的情况下遍历结果集以递增方式统计行数）。
* **替代方法**：如果内存有限且只需要行数，可以执行 `SELECT COUNT(*)` 查询而不是检索整个结果集。这通常更高效。

```sql
SELECT COUNT(*) FROM your_table;
```

如果您需要进一步说明，请告诉我！
