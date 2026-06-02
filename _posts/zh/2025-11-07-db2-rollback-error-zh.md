---
audio: false
generated: true
image: false
lang: zh
layout: post
model: moonshotai/kimi-k2-thinking
title: DB2事务回滚与错误检测
translated: true
type: note
---

## 当 DB2 因系统错误执行回滚时

IBM DB2 在遇到危及数据完整性的严重系统错误时会自动回滚事务。常见场景包括：

- **死锁或超时**：SQLCODE -911 且 SQLSTATE 40001，原因码 "2" 表示事务因死锁被回滚
- **进程异常终止**：在所有 DB2 环境中，进程终止会触发隐式回滚
- **系统资源故障**：内存、磁盘或网络故障导致事务无法完成
- **时间戳冲突**：当模块与 DBRM 之间的内部时间戳不匹配时出现 SQLCODE -818
- **连接池安全机制**：某些实现在释放连接时自动回滚，防止未提交事务导致锁问题

## 如何检测详细错误信息

### 1. 主要错误检测机制

**SQLCODE 和 SQLSTATE**
每条 SQL 语句执行后，DB2 会设置这些变量：

```sql
-- 在语句执行后立即检查
IF SQLCODE < 0 THEN
    -- 发生错误
    ROLLBACK;
END IF;
```

SQLSTATE 分类代码专门标识错误类型：

- **58 类**：系统错误（如资源不可用、操作员干预）
- **40 类**：事务回滚
- **25 类**：无效事务状态

**GET DIAGNOSTICS 语句**
在 SQL PL 存储过程中获取详细错误信息：

```sql
DECLARE v_sqlcode INTEGER;
DECLARE v_sqlstate CHAR(5);
DECLARE v_sqlmessage VARCHAR(256);

GET DIAGNOSTICS CONDITION 1
    v_sqlcode = DB2_RETURNED_SQLCODE,
    v_sqlstate = RETURNED_SQLSTATE,
    v_sqlmessage = MESSAGE_TEXT;
```

### 2. 命令行错误检测

通过 `db2` 命令行执行脚本时，检查退出代码：

- **退出代码 8**：系统错误
- **退出代码 4**：DB2 错误（约束违规、对象未找到）
- **退出代码 2**：DB2 警告
- **退出代码 1**：未找到行

**推荐的脚本模式**：

```bash
db2 -l migration.log +c -stf migration.sql
if [ $? -ge 4 ]; then
    db2 rollback
    tail -10 migration.log  # 查看详细错误
else
    db2 commit
fi
```

### 3. 存储过程错误处理

在 SQL PL 中使用声明的处理器进行全面的错误检测：

```sql
CREATE PROCEDURE my_procedure()
BEGIN
    DECLARE v_sqlcode INTEGER DEFAULT 0;
    DECLARE v_sqlstate CHAR(5) DEFAULT '00000';
    DECLARE v_error_message VARCHAR(256);

    -- 为任何异常声明退出处理器
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        GET DIAGNOSTICS CONDITION 1
            v_sqlcode = DB2_RETURNED_SQLCODE,
            v_sqlstate = RETURNED_SQLSTATE,
            v_error_message = MESSAGE_TEXT;

        -- 将错误详情记录到表或文件
        INSERT INTO error_log (sqlcode, sqlstate, message, timestamp)
        VALUES (v_sqlcode, v_sqlstate, v_error_message, CURRENT_TIMESTAMP);

        ROLLBACK;
    END;

    -- 您的事务逻辑在此
    UPDATE employee SET salary = salary + 1000 WHERE job = 'MANAGER';
    INSERT INTO audit_log VALUES (CURRENT_TIMESTAMP, 'Salary update');

    COMMIT;
END
```

### 4. DB2 诊断日志文件

对于系统级错误，始终检查：

- **db2diag.log**：包含详细系统错误信息的主要诊断日志
- **通知日志**：包含错误摘要
- **命令行日志**：使用 `-l logfile.txt` 选项捕获错误

## 错误检测最佳实践

1. **关键操作后立即检查 SQLCODE/SQLSTATE**
2. **在存储过程中使用 GET DIAGNOSTICS** 获取丰富的错误上下文
3. **实施事务回滚百分比监控** - 超过 1% 即需调查
4. **启用脚本执行的命令选项**：

   ```bash
   db2 +c -s -v -l error.log -f script.sql
   ```

   其中 `+c` 禁用自动提交，`-s` 在错误时停止
5. **在复杂事务中使用保存点** 进行部分回滚
6. **回滚前将错误详情记录** 到持久化表中以保留诊断信息

## 需要监控的关键系统错误 SQLSTATE

| SQLSTATE | 描述 | 应对措施 |
|----------|------|----------|
| **58004** | 系统错误（多种原因） | 立即检查 db2diag.log |
| **58008** | 通信错误 | 验证网络/连接性 |
| **HY000** | 通用驱动程序错误 | 检查 ODBC/JDBC 驱动程序日志 |
| **40001** | 死锁/超时 | 使用退避策略重试事务 |

对于生产环境，监控工具应在 **SQLCODE < 0** 和 **58 类 SQLSTATE** 时发出警报，以便在系统级问题级联之前主动检测到它们。
