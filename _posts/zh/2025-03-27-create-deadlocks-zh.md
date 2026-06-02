---
audio: false
generated: true
lang: zh
layout: post
title: 死锁生成
translated: true
type: note
---

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class DeadlockGenerator {

    private static final String DB_URL = "jdbc:sqlite:deadlock_example.db"; // 使用SQLite简化实现
    private static final String CREATE_TABLE_SQL = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, value TEXT)";
    private static final String INSERT_ITEM_SQL = "INSERT OR IGNORE INTO items (id, value) VALUES (?, ?)";
    private static final String UPDATE_ITEM_SQL = "UPDATE items SET value = ? WHERE id = ?";

    public static void main(String[] args) throws InterruptedException {
        createTableAndInitialData();

        ExecutorService executor = Executors.newFixedThreadPool(2);
        executor.submit(new UpdateTask(1, "Updated Value 1 - Thread 1", 2, "Updated Value 2 - Thread 1"));
        executor.submit(new UpdateTask(2, "Updated Value 2 - Thread 2", 1, "Updated Value 1 - Thread 2"));

        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);

        printFinalData();
    }

    private static void createTableAndInitialData() {
        try (Connection conn = DriverManager.getConnection(DB_URL);
             java.sql.Statement stmt = conn.createStatement()) {
            stmt.execute(CREATE_TABLE_SQL);
            try (PreparedStatement pstmt = conn.prepareStatement(INSERT_ITEM_SQL)) {
                pstmt.setInt(1, 1);
                pstmt.setString(2, "Value 1");
                pstmt.executeUpdate();
                pstmt.setInt(1, 2);
                pstmt.setString(2, "Value 2");
                pstmt.executeUpdate();
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    private static void printFinalData() {
        System.out.println("\n数据表最终状态:");
        try (Connection conn = DriverManager.getConnection(DB_URL);
             java.sql.Statement stmt = conn.createStatement();
             java.sql.ResultSet rs = stmt.executeQuery("SELECT * FROM items")) {
            while (rs.next()) {
                System.out.println("ID: " + rs.getInt("id") + ", Value: " + rs.getString("value"));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    static class UpdateTask implements Runnable {
        private final int id1;
        private final String value1;
        private final int id2;
        private final String value2;

        public UpdateTask(int id1, String value1, int id2, String value2) {
            this.id1 = id1;
            this.value1 = value1;
            this.id2 = id2;
            this.value2 = value2;
        }

        @Override
        public void run() {
            Connection conn = null;
            try {
                conn = DriverManager.getConnection(DB_URL);
                conn.setAutoCommit(false); // 开始事务

                System.out.println(Thread.currentThread().getName() + ": 锁定id为 " + id1 + " 的行");
                try (PreparedStatement pstmt1 = conn.prepareStatement(UPDATE_ITEM_SQL)) {
                    pstmt1.setString(1, value1);
                    pstmt1.setInt(2, id1);
                    pstmt1.executeUpdate();
                }
                Thread.sleep(100); // 引入短暂延迟

                System.out.println(Thread.currentThread().getName() + ": 锁定id为 " + id2 + " 的行");
                try (PreparedStatement pstmt2 = conn.prepareStatement(UPDATE_ITEM_SQL)) {
                    pstmt2.setString(1, value2);
                    pstmt2.setInt(2, id2);
                    pstmt2.executeUpdate();
                }

                conn.commit();
                System.out.println(Thread.currentThread().getName() + ": 事务提交成功");

            } catch (SQLException e) {
                if (conn != null) {
                    try {
                        conn.rollback();
                        System.err.println(Thread.currentThread().getName() + ": 事务因错误回滚: " + e.getMessage());
                    } catch (SQLException rollbackException) {
                        rollbackException.printStackTrace();
                    }
                } else {
                    e.printStackTrace();
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                if (conn != null) {
                    try {
                        conn.setAutoCommit(true); // 重置自动提交
                        conn.close();
                    } catch (SQLException e) {
                        e.printStackTrace();
                    }
                }
            }
        }
    }
}
```

**代码说明:**

1. **数据库设置:**
    * `DB_URL`: 指定SQLite数据库文件的连接URL (`deadlock_example.db`)
    * `CREATE_TABLE_SQL`, `INSERT_ITEM_SQL`, `UPDATE_ITEM_SQL`: 定义创建表、插入初始数据和更新行的SQL语句
    * `createTableAndInitialData()`: 如果`items`表不存在则创建，并插入ID为1和2的两个初始行

2. **并发更新:**
    * `ExecutorService`: 创建固定大小为2的线程池，模拟两个任务的并发执行
    * `UpdateTask`: 此内部类实现`Runnable`接口，每个实例代表一个尝试更新两行数据的事务
        * 构造函数接收要更新的两行的ID和新值
        * `run()`方法执行以下操作:
            * 建立数据库连接
            * 设置`conn.setAutoCommit(false)`开始显式事务
            * **首次更新:** 对第一行(`id1`)执行`UPDATE`语句
            * `Thread.sleep(100)`: 引入短暂延迟以增加死锁概率，让第一个线程在第二个线程尝试获取锁之前先锁定第一行
            * **第二次更新:** 对第二行(`id2`)执行`UPDATE`语句
            * `conn.commit()`: 尝试提交事务
            * **错误处理:** 包含`try-catch`块处理`SQLException`，如果发生异常（可能是死锁），则通过`conn.rollback()`尝试回滚事务
            * **Finally块:** 确保连接关闭并将`autoCommit`重置为`true`

3. **冲突顺序:**
    * 在`main`方法中，向执行器提交两个`UpdateTask`实例:
        * 第一个任务尝试先更新行1再更新行2
        * 第二个任务尝试先更新行2再更新行1
    * 这种对相同资源（`items`表中的行）获取锁的顺序冲突是可能导致死锁的条件

4. **执行与输出:**
    * `executor.shutdown()`和`executor.awaitTermination()`: 确保执行器等待两个任务完成
    * `printFinalData()`: 线程完成后，此方法打印`items`表的最终内容以观察结果

**运行方法:**

1. **保存:** 将代码保存为`DeadlockGenerator.java`
2. **编译:** 使用Java编译器编译代码: `javac DeadlockGenerator.java`
3. **运行:** 执行编译后的代码: `java DeadlockGenerator`

**预期结果:**

运行此代码时，可能会看到类似以下输出（具体输出可能因时序和数据库系统的死锁检测机制而略有不同）:

```
Thread-0: 锁定id为 1 的行
Thread-1: 锁定id为 2 的行
Thread-0: 锁定id为 2 的行
Thread-1: 锁定id为 1 的行
Thread-1: 事务因错误回滚: database is locked
Thread-0: 事务提交成功

数据表最终状态:
ID: 1, Value: Updated Value 1 - Thread 0
ID: 2, Value: Updated Value 2 - Thread 0
```

有时也可能是Thread-0被回滚。关键观察点是其中一个线程会遇到指示锁冲突或死锁的`SQLException`，其事务将被回滚，而另一个线程通常会成功。

**重要注意事项:**

* **数据库系统:** 此示例为简化使用SQLite，其他数据库系统如PostgreSQL、MySQL等的行为和错误消息可能不同，可能需要调整JDBC驱动URL和SQL语句
* **隔离级别:** 数据库的默认事务隔离级别会影响死锁概率，较高的隔离级别可能使死锁更频繁发生
* **延迟:** `Thread.sleep()`对演示死锁至关重要，没有它一个事务可能在另一个事务获取第一个锁之前就已完成
* **错误处理:** 在实际应用中，应有健壮的错误处理机制，并可能需要对因死锁失败的事务实现重试机制
