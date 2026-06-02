---
audio: false
generated: true
lang: en
layout: post
title: Deadlock Creations
translated: false
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

    private static final String DB_URL = "jdbc:sqlite:deadlock_example.db"; // Using SQLite for simplicity
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
        System.out.println("\nFinal state of the table:");
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
                conn.setAutoCommit(false); // Start transaction

                System.out.println(Thread.currentThread().getName() + ": Locking row with id " + id1);
                try (PreparedStatement pstmt1 = conn.prepareStatement(UPDATE_ITEM_SQL)) {
                    pstmt1.setString(1, value1);
                    pstmt1.setInt(2, id1);
                    pstmt1.executeUpdate();
                }
                Thread.sleep(100); // Introduce a small delay

                System.out.println(Thread.currentThread().getName() + ": Locking row with id " + id2);
                try (PreparedStatement pstmt2 = conn.prepareStatement(UPDATE_ITEM_SQL)) {
                    pstmt2.setString(1, value2);
                    pstmt2.setInt(2, id2);
                    pstmt2.executeUpdate();
                }

                conn.commit();
                System.out.println(Thread.currentThread().getName() + ": Transaction committed successfully.");

            } catch (SQLException e) {
                if (conn != null) {
                    try {
                        conn.rollback();
                        System.err.println(Thread.currentThread().getName() + ": Transaction rolled back due to error: " + e.getMessage());
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
                        conn.setAutoCommit(true); // Reset auto-commit
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

**Explanation:**

1. **Database Setup:**
    * `DB_URL`: Specifies the connection URL for the SQLite database file (`deadlock_example.db`).
    * `CREATE_TABLE_SQL`, `INSERT_ITEM_SQL`, `UPDATE_ITEM_SQL`: Define the SQL statements for creating the table, inserting initial data, and updating rows.
    * `createTableAndInitialData()`: Creates the `items` table if it doesn't exist and inserts two initial rows with IDs 1 and 2.

2. **Concurrent Updates:**
    * `ExecutorService`: An `ExecutorService` with a fixed thread pool of 2 is created to simulate concurrent execution of two tasks.
    * `UpdateTask`: This inner class implements the `Runnable` interface. Each instance of `UpdateTask` represents a transaction that will attempt to update two rows.
        * The constructor takes the IDs and the new values for the two rows to be updated.
        * The `run()` method performs the following:
            * Establishes a database connection.
            * Sets `conn.setAutoCommit(false)` to start an explicit transaction.
            * **First Update:** Executes an `UPDATE` statement for the first row (`id1`).
            * `Thread.sleep(100)`: Introduces a small delay to increase the chance of a deadlock. This allows the first thread to acquire a lock on the first row before the second thread tries to acquire it.
            * **Second Update:** Executes an `UPDATE` statement for the second row (`id2`).
            * `conn.commit()`: Attempts to commit the transaction.
            * **Error Handling:** Includes a `try-catch` block to handle `SQLException`. If an exception occurs (which could be a deadlock), it attempts to roll back the transaction using `conn.rollback()`.
            * **Finally Block:** Ensures that the connection is closed and `autoCommit` is reset to `true`.

3. **Conflicting Order:**
    * In the `main` method, two `UpdateTask` instances are submitted to the executor:
        * The first task tries to update row 1 and then row 2.
        * The second task tries to update row 2 and then row 1.
    * This conflicting order of acquiring locks on the same resources (the rows in the `items` table) is the condition that can lead to a deadlock.

4. **Execution and Output:**
    * `executor.shutdown()` and `executor.awaitTermination()`: Ensure that the executor waits for both tasks to complete.
    * `printFinalData()`: After the threads have finished, this method prints the final contents of the `items` table to observe the outcome.

**How to Run:**

1. **Save:** Save the code as `DeadlockGenerator.java`.
2. **Compile:** Compile the code using a Java compiler: `javac DeadlockGenerator.java`
3. **Run:** Execute the compiled code: `java DeadlockGenerator`

**Expected Outcome:**

When you run this code, you will likely see output similar to this (the exact output might vary slightly depending on the timing and the database system's deadlock detection):

```
Thread-0: Locking row with id 1
Thread-1: Locking row with id 2
Thread-0: Locking row with id 2
Thread-1: Locking row with id 1
Thread-1: Transaction rolled back due to error: database is locked
Thread-0: Transaction committed successfully.

Final state of the table:
ID: 1, Value: Updated Value 1 - Thread 0
ID: 2, Value: Updated Value 2 - Thread 0
```

Or sometimes, Thread-0 might be rolled back instead. The key observation is that one of the threads will encounter an `SQLException` indicating a lock conflict or deadlock, and its transaction will be rolled back. The other thread will usually succeed.

**Important Notes:**

* **Database System:** This example uses SQLite for simplicity. The behavior and error messages might differ with other database systems like PostgreSQL, MySQL, etc. You might need to adjust the JDBC driver URL and potentially the SQL statements.
* **Isolation Levels:** The default transaction isolation level of your database can influence the likelihood of deadlocks. Higher isolation levels might make deadlocks more frequent.
* **Delay:** The `Thread.sleep()` is crucial for demonstrating the deadlock. Without it, one transaction might complete before the other has a chance to acquire the first lock.
* **Error Handling:** In a real-world application, you should have robust error handling and potentially retry mechanisms for transactions that fail due to deadlocks.
