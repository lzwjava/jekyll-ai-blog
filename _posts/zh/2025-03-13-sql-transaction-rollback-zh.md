---
audio: false
generated: true
lang: zh
layout: post
title: Spring中的SQL事务回滚异常
translated: true
type: note
---

针对您关于捕获`SqlTransactionRollbackException`的问题——该异常在`DataSourceUtils.java`从`DataSource`获取JDBC连接后发生，以及对该异常相关数据库锁的详细分析，让我们系统地分解这个问题。

### 捕获 SqlTransactionRollbackException

在基于Spring的应用程序中，`DataSourceUtils.java`是Spring框架内的一个实用工具类，用于促进从`DataSource`获取和管理JDBC连接。具体来说，`DataSourceUtils.getConnection(DataSource)`方法获取一个连接，要么从连接池中获取一个新连接，要么如果当前线程的事务上下文中已经关联了一个现有的事务性连接，则复用该连接。

您描述的场景表明，在成功获取连接后，抛出了`SqlTransactionRollbackException`。由于`SqlTransactionRollbackException`不是Spring异常层次结构中的标准异常（Spring通常使用`TransactionException`、`UnexpectedRollbackException`或`DeadlockLoserDataAccessException`等异常），我假设它是一个自定义的、应用程序特定的异常，在事务由于数据库相关问题（如锁冲突）而回滚时抛出。

此异常很可能不是在连接检索本身期间发生的（如果连接检索失败，通常会抛出`CannotGetJdbcConnectionException`），而是在事务内后续的数据库操作期间——例如执行SQL语句时——遇到了需要回滚的问题。

要捕获此异常，您需要将启动事务操作的代码包装在`try-catch`块中。以下是操作方法：

#### 使用声明式事务管理的示例
如果您使用Spring的`@Transactional`注解来管理事务，异常将从定义事务的方法中抛出。例如：

```java
@Service
public class MyService {
    @Autowired
    private MyDao myDao;

    @Transactional
    public void performDatabaseOperation() {
        myDao.updateData(); // 假设这由于锁问题导致回滚
    }
}
```

在调用此服务方法时，您可以捕获`SqlTransactionRollbackException`：

```java
@Autowired
private MyService myService;

public void executeOperation() {
    try {
        myService.performDatabaseOperation();
    } catch (SqlTransactionRollbackException e) {
        // 处理异常
        System.err.println("事务因以下原因回滚: " + e.getMessage());
        // 可选择重试操作或通知用户
    }
}
```

#### 使用编程式事务管理的示例
如果您使用`TransactionTemplate`或`PlatformTransactionManager`以编程方式管理事务，您需要在事务执行周围捕获异常：

```java
@Autowired
private TransactionTemplate transactionTemplate;

public void executeOperation() {
    try {
        transactionTemplate.execute(status -> {
            // 执行数据库操作
            myDao.updateData();
            return null;
        });
    } catch (SqlTransactionRollbackException e) {
        // 处理异常
        System.err.println("事务因以下原因回滚: " + e.getMessage());
    }
}
```

#### 注意事项
- **异常层次结构**：如果`SqlTransactionRollbackException`是自定义异常，请验证其超类。如果它扩展了Spring的`DataAccessException`，您可以改为捕获`DataAccessException`并检查具体类型：
  ```java
  catch (DataAccessException e) {
      if (e instanceof SqlTransactionRollbackException) {
          // 专门处理 SqlTransactionRollbackException
      }
  }
  ```
- **事务上下文**：异常很可能在连接获取之后，当事务管理器或JDBC驱动程序检测到问题（例如，回滚仅状态或数据库错误）时出现。因此，在服务层或调用者层捕获它是合适的。

### 数据库锁的详细分析

您的查询中提到的“这种数据库锁”，结合回滚异常，强烈暗示与**死锁**有关——这是一种常见的数据库锁定问题，可能导致事务回滚。让我们对此进行详细分析。

#### 什么是死锁？
当两个或多个事务无法继续进行时，数据库中会发生死锁，因为每个事务都持有另一个事务需要的锁，从而创建了循环依赖。例如：

- **事务 T1**：
  1. 获取`TableA`上的排他锁。
  2. 尝试获取`TableB`上的排他锁（等待，因为T2持有它）。
- **事务 T2**：
  1. 获取`TableB`上的排他锁。
  2. 尝试获取`TableA`上的排他锁（等待，因为T1持有它）。

在这里，T1等待T2释放`TableB`，T2等待T1释放`TableA`，导致死锁。

#### 死锁如何导致回滚
大多数关系数据库（例如MySQL、PostgreSQL、Oracle）都有死锁检测机制。当识别出死锁时：
1. 数据库选择一个“受害者”事务（通常是完成工作最少的事务或基于可配置的策略）。
2. 受害者事务被回滚，释放其锁。
3. 数据库向应用程序抛出一个带有特定错误代码的`SQLException`（例如，MySQL错误1213，PostgreSQL错误40P01）。
4. 在Spring中，此`SQLException`通常被转换为`DeadlockLoserDataAccessException`。如果您的应用程序抛出`SqlTransactionRollbackException`，它可能是围绕此类事件的自定义包装器。

在您的场景中，在`DataSourceUtils`获取连接之后，事务内的数据库操作遇到死锁，导致回滚并抛出`SqlTransactionRollbackException`。

#### 涉及的锁类型
- **共享锁**：用于读操作；多个事务可以在同一资源上持有共享锁。
- **排他锁**：用于写操作；只有一个事务可以持有排他锁，并且它与其他人持有的共享锁和排他锁冲突。
死锁通常涉及排他锁，因为它们更具限制性。

#### 死锁发生的原因
死锁由于以下原因产生：
- **不一致的锁定顺序**：事务以不同的顺序访问资源（例如，表、行）。
- **长事务**：长时间持有锁会增加冲突的机会。
- **高并发性**：多个事务同时操作相同的数据。

#### 示例场景
假设您的应用程序中有两个方法更新两个表：

```java
@Transactional
public void updateUserAndOrder1() {
    jdbcTemplate.update("UPDATE users SET name = ? WHERE id = ?", "Alice", 1); // 锁定 users 行
    jdbcTemplate.update("UPDATE orders SET status = ? WHERE user_id = ?", "Shipped", 1); // 锁定 orders 行
}

@Transactional
public void updateUserAndOrder2() {
    jdbcTemplate.update("UPDATE orders SET status = ? WHERE user_id = ?", "Processed", 1); // 锁定 orders 行
    jdbcTemplate.update("UPDATE users SET name = ? WHERE id = ?", "Bob", 1); // 锁定 users 行
}
```

如果这些方法并发运行，`updateUserAndOrder1`可能在等待`orders`时锁定`users`，而`updateUserAndOrder2`可能在等待`users`时锁定`orders`，从而导致死锁。

#### 处理和预防死锁
1. **捕获异常**：
   如前所示，使用`try-catch`块处理`SqlTransactionRollbackException`。您可能：
   - 记录错误以进行调试。
   - 重试操作（谨慎操作以避免无限循环）：
     ```java
     int retries = 3;
     for (int i = 0; i < retries; i++) {
         try {
             myService.performDatabaseOperation();
             break;
         } catch (SqlTransactionRollbackException e) {
             if (i < retries - 1) {
                 Thread.sleep(1000 * (i + 1)); // 指数退避
                 continue;
             }
             throw e; // 在最大重试次数后重新抛出
         }
     }
     ```

2. **确保一致的锁定顺序**：
   修改代码以相同的顺序访问表（例如，始终在`orders`之前锁定`users`）。

3. **最小化锁持有时间**：
   通过将非事务逻辑移到`@Transactional`边界之外来保持事务简短。

4. **使用适当的事务隔离级别**：
   如果应用程序需求允许，调整事务隔离级别（例如，使用`READ_COMMITTED`而不是`SERIALIZABLE`），尽管这不能完全消除死锁。

5. **数据库特定功能**：
   - 启用死锁检测日志记录（例如，MySQL的`innodb_print_all_deadlocks`）。
   - 尽可能使用行级锁定，尽管死锁仍然可能在行级发生。

#### 分析死锁
要诊断具体的死锁：
- **数据库日志**：检查数据库服务器日志以获取死锁详细信息（例如，涉及的事务、锁定的资源）。
- **Spring调试**：启用Spring事务日志记录（`logging.level.org.springframework.transaction=DEBUG`）以跟踪事务事件。
- **应用程序跟踪**：记录导致异常的操作序列。

### 结论
要捕获`SqlTransactionRollbackException`，请在调用事务操作（例如标记为`@Transactional`的服务方法）的代码周围放置一个`try-catch`块。对于数据库锁——很可能是死锁——确保事务以一致的顺序访问资源，保持事务简短，并考虑对瞬时故障使用重试逻辑。死锁是由于循环锁依赖而发生的，虽然数据库通过回滚受害者事务来解决它们，但主动设计可以最大限度地减少它们的发生。

---

在处理Spring应用程序中的`SqlTransactionRollbackException`时——特别是在另一个事务持有锁，导致连接获取失败并在大约20次失败尝试后抛出异常的情况下——您可以采用几种策略来处理并可能缓解此问题。此异常通常发生在事务回滚期间，当数据库锁或并发问题阻止操作成功完成时。下面，我概述了一个全面的方法来处理此问题，侧重于预防、处理和恢复。

---

### 理解问题
`SqlTransactionRollbackException`（或者在Spring中更可能是`TransactionRollbackException`，因为前者不是标准的Spring异常）表明事务无法回滚，可能是因为另一个事务持有所需数据库资源的锁。这种锁争用导致事务管理器在获取连接时失败，重试多次（在您的情况下大约20次），并最终在回滚无法完成时抛出异常。这表明存在并发问题，例如锁争用或死锁，并因Spring事务管理在放弃前内部重试而加剧。

---

### 处理异常的策略

#### 1. 通过短事务最小化锁争用
长时间运行的事务会增加锁争用的可能性，因为它们长时间持有数据库锁，阻塞其他事务。为降低此风险：

- **设计短生命周期事务**：确保您的`@Transactional`方法快速执行其数据库操作并及时提交或回滚。避免在事务范围内包含耗时的业务逻辑或外部调用。
- **分解大事务**：如果单个事务涉及多个操作，请考虑在可能的情况下将其拆分为更小的独立事务。这减少了锁持有的持续时间。

#### 2. 优化数据库查询
优化不佳的查询会因持有锁的时间超过必要时间而加剧锁争用。为解决此问题：

- **分析和优化查询**：使用数据库分析工具识别慢查询。添加适当的索引，避免不必要的表扫描，并最小化锁定行的范围（例如，使用精确的`WHERE`子句）。
- **避免过于宽泛的锁**：谨慎使用像`SELECT ... FOR UPDATE`这样的语句，它们会显式锁定行并可能阻塞其他事务。仅在必要时使用，并确保它们影响尽可能少的行。

#### 3. 调整事务设置
Spring的`@Transactional`注解提供了用于微调事务行为的属性。虽然这些不能直接解决回滚失败，但它们可以帮助管理并发：

- **隔离级别**：默认隔离级别（`DEFAULT`）通常映射到数据库的默认级别（通常是`READ_COMMITTED`）。将其增加到`REPEATABLE_READ`或`SERIALIZABLE`可能会确保数据一致性，但可能加剧锁争用。相反，坚持使用`READ_COMMITTED`或更低（如果支持）可能会减少锁定问题，具体取决于您的用例。仔细测试以找到正确的平衡点。
- **传播行为**：默认的`REQUIRED`加入现有事务或启动新事务。使用`REQUIRES_NEW`挂起当前事务并启动一个新事务，可能避免与锁定事务的冲突。但是，这可能无法解决回滚特定的问题。
- **超时**：在`@Transactional(timeout = 10)`中设置`timeout`值（以秒为单位），以便在锁持续存在时快速使事务失败。这可以防止长时间重试，但不能解决根本原因。

示例：
```java
@Transactional(timeout = 5, propagation = Propagation.REQUIRES_NEW)
public void performDatabaseOperation() {
    // 您的代码在这里
}
```

#### 4. 实施重试逻辑（需谨慎）
由于异常在多次内部重试（大约20次）后发生，Spring的事务管理器很可能已经在尝试处理该问题。但是，您可以在更高级别实现自定义重试逻辑：

- **使用Spring Retry**：
  使用`@Retryable`注解服务方法，以在`TransactionRollbackException`上重试。指定尝试次数和重试之间的延迟。将其与`@Recover`方法配对，以在重试耗尽后处理失败。
  ```java
  import org.springframework.retry.annotation.Backoff;
  import org.springframework.retry.annotation.Retryable;
  import org.springframework.retry.annotation.Recover;
  import org.springframework.transaction.annotation.Transactional;

  @Service
  public class MyService {

      @Retryable(value = TransactionRollbackException.class, maxAttempts = 3, backoff = @Backoff(delay = 1000))
      public void executeOperation() {
          performTransactionalWork();
      }

      @Transactional
      private void performTransactionalWork() {
          // 可能失败的数据库操作
      }

      @Recover
      public void recover(TransactionRollbackException e) {
          // 记录错误、通知管理员或采取纠正措施
          System.err.println("所有重试均失败: " + e.getMessage());
      }
  }
  ```
  **注意**：每次重试都会启动一个新事务，如果跨重试需要原子性，这可能不理想。如果可能，在`@Transactional`方法之外应用此注解。

- **使用 TransactionTemplate 手动重试**：
  为了更多控制，使用`TransactionTemplate`将您的事务代码包装在重试循环中：
  ```java
  import org.springframework.transaction.PlatformTransactionManager;
  import org.springframework.transaction.TransactionStatus;
  import org.springframework.transaction.support.TransactionCallbackWithoutResult;
  import org.springframework.transaction.support.TransactionTemplate;

  @Service
  public class MyService {
      private final TransactionTemplate transactionTemplate;
      private static final int MAX_RETRIES = 3;
      private static final long RETRY_DELAY_MS = 1000;

      public MyService(PlatformTransactionManager transactionManager) {
          this.transactionTemplate = new TransactionTemplate(transactionManager);
      }

      public void executeWithRetry() {
          for (int i = 0; i < MAX_RETRIES; i++) {
              try {
                  transactionTemplate.execute(new TransactionCallbackWithoutResult() {
                      @Override
                      protected void doInTransactionWithoutResult(TransactionStatus status) {
                          // 事务代码在这里
                      }
                  });
                  return; // 成功，退出循环
              } catch (TransactionRollbackException e) {
                  if (i == MAX_RETRIES - 1) {
                      throw e; // 在最大重试次数后重新抛出
                  }
                  try {
                      Thread.sleep(RETRY_DELAY_MS);
                  } catch (InterruptedException ie) {
                      Thread.currentThread().interrupt();
                  }
              }
          }
      }
  }
  ```
  **注意**：如果锁持续存在，重试可能无法解决问题，并且如果在回滚失败之前应用了部分更改，可能导致状态不一致。确保重试是幂等的或安全的。

#### 5. 优雅地处理异常
如果由于持久锁导致回滚失败，数据库状态可能变得不一致，需要仔细处理：

- **捕获并记录**：
  将事务调用包装在try-catch块中，记录异常，并通知管理员：
  ```java
  try {
      myService.performTransactionalWork();
  } catch (TransactionRollbackException e) {
      // 记录错误
      logger.error("重试后事务回滚失败: " + e.getMessage(), e);
      // 通知管理员（例如，通过电子邮件或监控系统）
      alertSystem.notify("严重：事务回滚失败");
      // 优雅地失败或进入安全状态
      throw new RuntimeException("由于事务问题导致操作失败", e);
  }
  ```

- **安全失败**：如果事务状态不确定，停止依赖它的进一步操作，并发出需要手动干预的信号。

#### 6. 利用数据库特性
调整数据库设置以缓解锁相关问题：

- **锁超时**：配置数据库以在锁等待时快速超时（例如，在SQL Server中使用`SET LOCK_TIMEOUT 5000`或在MySQL中使用`innodb_lock_wait_timeout`）。这会使事务更早失败，允许Spring更早地处理异常。
- **死锁检测**：确保数据库的死锁检测已启用并配置为通过自动回滚一个事务来解决冲突。
- **乐观锁**：如果使用JPA，对实体应用`@Version`以使用乐观锁，减少物理锁争用：
  ```java
  @Entity
  public class MyEntity {
      @Id
      private Long id;
      @Version
      private Integer version;
      // 其他字段
  }
  ```
  这将冲突检测转移到提交时间，但可能不直接解决回滚失败。

#### 7. 监控和调查
此异常的频繁发生表明存在潜在问题：

- **添加监控**：使用Spring Boot Actuator或日志框架等工具跟踪这些异常及其频率。
- **分析日志**：检查数据库和应用程序日志以查找模式（例如，导致锁的特定查询或事务）。
- **调整并发性**：如果争用持续存在，重新审视应用程序的并发模型或数据库设计。

---

### 回滚失败的原因
在20次尝试后回滚失败表明，当Spring的事务管理器遇到锁定资源或丢失连接时，会重试回滚操作，最终放弃。这可能源于：

- **持久锁**：另一个事务持有的锁在重试窗口内未释放。
- **连接问题**：数据库连接池（例如HikariCP）在获取连接时耗尽了其重试次数。
- **数据库配置错误**：数据库或连接池中的超时或重试设置过于激进或不足。

---

### 推荐方法
以下是结合上述策略的实用解决方案：

1. **优化事务和查询**：保持事务简短，查询高效，以减少锁持有时间。
2. **设置事务超时**：使用`@Transactional(timeout = 5)`在锁持续存在时快速失败。
3. **使用重试和恢复处理**：
   ```java
   @Service
   public class MyService {
       @Autowired
       private MyRepository repository;

       public void executeOperationWithRetry() {
           int maxAttempts = 3;
           for (int i = 0; i < maxAttempts; i++) {
               try {
                   performTransactionalWork();
                   return;
               } catch (TransactionRollbackException e) {
                   if (i == maxAttempts - 1) {
                       logger.error("在 {} 次尝试后失败: {}", maxAttempts, e.getMessage(), e);
                       alertSystem.notify("事务回滚失败");
                       throw e;
                   }
                   try {
                       Thread.sleep(1000); // 重试前等待
                   } catch (InterruptedException ie) {
                       Thread.currentThread().interrupt();
                   }
               }
           }
       }

       @Transactional
       private void performTransactionalWork() {
           // 数据库操作
           repository.save(someEntity);
       }
   }
   ```
4. **监控和调整**：记录异常，设置警报，并调查锁争用的原因。

---

### 结论
要在Spring中处理`SqlTransactionRollbackException`，当另一个事务持有锁导致连接获取失败和重复尝试时，重点是通过短事务和优化查询来最小化锁争用，根据需要调整事务设置，在更高级别实施谨慎的重试逻辑，并通过记录和适当通知来处理异常。这确保了系统稳定性和数据完整性，同时通过监控和调整随时间推移解决根本原因。

---

在使用IBM DB2 Java驱动程序（特别是JDBC驱动程序）时，处理事务回滚场景对于健壮的数据库交互至关重要。查询中提到的`SqlTransactionRollbackException`似乎是一个轻微的拼写错误。在标准JDBC中，特别是从版本4.0开始（受现代IBM DB2驱动程序如`db2jcc4.jar`支持），正确的异常是**`SQLTransactionRollbackException`**。此异常是`SQLException`的子类，在数据库事务自动回滚时抛出，例如在死锁或超时的情况下。

以下是在使用IBM DB2 JDBC驱动程序时，在Java代码中有效处理`SQLTransactionRollbackException`的方法：

### 处理异常的方法

1. **使用 Try-Catch 块**：将您的事务性数据库操作包装在`try`块中，并捕获`SQLTransactionRollbackException`以处理数据库回滚事务的情况。
2. **采取适当措施**：根据您的应用程序需求，您可能记录错误、重试事务（如果问题是瞬态的，如死锁）或通知用户失败。
3. **确保资源清理**：在`finally`块中正确管理数据库资源（例如，关闭连接）以避免资源泄漏。
4. **对旧驱动程序的回退**：如果您使用的旧版DB2驱动程序不支持JDBC 4.0，您可能需要捕获`SQLException`并检查错误代码（例如，在DB2中，死锁导致的回滚错误代码为`-911`）。

### 示例代码

以下是一个演示如何处理`SQLTransactionRollbackException`的实用示例：

```java
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.SQLTransactionRollbackException;
import javax.sql.DataSource;

public class DB2TransactionExample {
    public void performTransaction(DataSource dataSource) {
        Connection conn = null;
        try {
            // 获取连接并禁用自动提交以启动事务
            conn = dataSource.getConnection();
            conn.setAutoCommit(false);

            // 在此处执行您的数据库操作
            // 例如，执行 INSERT、UPDATE 等语句

            // 如果所有操作成功，提交事务
            conn.commit();
        } catch (SQLTransactionRollbackException e) {
            // 处理数据库回滚事务的情况
            System.err.println("数据库回滚了事务: " + e.getMessage());
            System.err.println("SQL 状态: " + e.getSQLState() + ", 错误代码: " + e.getErrorCode());
            // 示例：SQL状态 '40001' 和错误代码 -911 表示 DB2 中的死锁或超时
            // 可选择重试事务或通知用户
        } catch (SQLException e) {
            // 处理其他 SQL 异常
            System.err.println("SQL 错误: " + e.getMessage());
            // 如果事务仍处于活动状态，尝试手动回滚
            if (conn != null) {
                try {
                    conn.rollback();
                    System.out.println("手动回滚事务。");
                } catch (SQLException rollbackEx) {
                    System.err.println("回滚失败: " + rollbackEx.getMessage());
                }
            }
        } finally {
            // 清理资源
            if (conn != null) {
                try {
                    conn.setAutoCommit(true); // 恢复默认行为
                    conn.close();
                } catch (SQLException closeEx) {
                    System.err.println("关闭连接失败: " + closeEx.getMessage());
                }
            }
        }
    }
}
```

### 代码中的关键点

- **捕获 `SQLTransactionRollbackException`**：这专门捕获DB2回滚事务的情况（例如，由于死锁，由错误代码`-911`或SQL状态`40001`指示）。
- **通用 `SQLException` 捕获**：这作为其他数据库错误的回退，确保更广泛的错误处理。
- **手动回滚**：如果发生`SQLException`且事务尚未自动回滚，您可以尝试手动回滚。
- **资源管理**：`finally`块确保连接被关闭，防止资源泄漏。

### 其他注意事项

- **驱动程序版本**：确保您使用的是符合JDBC 4.0的IBM DB2驱动程序（例如，`db2jcc4.jar`）。旧版驱动程序（例如，`db2jcc.jar`）可能仅抛出`SQLException`，要求您手动检查错误代码。例如：
  ```java
  catch (SQLException e) {
      if (e.getErrorCode() == -911) {
          // 处理由于死锁或超时导致的事务回滚
      }
  }
  ```
- **SQL 状态和错误代码**：DB2对序列化失败（如死锁）使用SQL状态`40001`，错误代码`-911`表示事务自动回滚。错误代码`-913`表示由于死锁导致的语句失败，但除非显式回滚，否则事务仍处于活动状态。
- **重试逻辑**：对于瞬态问题（如死锁），您可以实施重试机制：
  ```java
  int maxRetries = 3;
  for (int attempt = 1; attempt <= maxRetries; attempt++) {
      try {
          performTransaction(dataSource);
          break; // 成功，退出循环
      } catch (SQLTransactionRollbackException e) {
          if (attempt == maxRetries) {
              throw e; // 在最大重试次数后重新抛出
          }
          Thread.sleep(1000 * attempt); // 重试前退避
      }
  }
  ```

### 结论

要在IBM DB2 Java驱动程序中处理`SQLTransactionRollbackException`（正确的`SQLTransactionRollbackException`），使用`try-catch`块捕获此特定异常以处理事务回滚场景。将其与适当的资源管理结合，并在必要时通过检查错误代码（如`-911`）为旧驱动程序提供回退逻辑。这种方法确保您的应用程序优雅地处理事务回滚，同时保持数据库完整性和用户体验。
