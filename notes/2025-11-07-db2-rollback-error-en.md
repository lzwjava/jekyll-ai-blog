---
audio: false
generated: true
image: false
lang: en
layout: post
model: moonshotai/kimi-k2-thinking
title: DB2 Transaction Rollback and Error Detection
translated: false
type: note
---

## When DB2 Performs Rollback Due to System Errors

IBM DB2 automatically rolls back transactions when encountering critical system errors that threaten data integrity. Common scenarios include:

- **Deadlocks or timeouts**: SQLCODE -911 with SQLSTATE 40001, Reason code "2" indicates transaction rolled back due to deadlock
- **Process abend (abnormal end)**: In all DB2 environments, process termination triggers implicit rollback
- **System resource failures**: Memory, disk, or network failures that prevent transaction completion
- **Timestamp conflicts**: SQLCODE -818 occurs when internal timestamps don't match between module and DBRM
- **Connection pooling safety nets**: Some implementations automatically roll back connections when released to prevent uncommitted transactions from causing locking issues

## How to Detect Detailed Error Information

### 1. Primary Error Detection Mechanisms

**SQLCODE and SQLSTATE**
After each SQL statement, DB2 sets these variables:

```sql
-- Check immediately after statement execution
IF SQLCODE < 0 THEN
    -- Error occurred
    ROLLBACK;
END IF;
```

SQLSTATE class codes specifically identify error types :
- **Class 58**: System error (e.g., resource unavailable, operator intervention)
- **Class 40**: Transaction rollback
- **Class 25**: Invalid transaction state

**GET DIAGNOSTICS Statement**
For detailed error information in SQL PL stored procedures:

```sql
DECLARE v_sqlcode INTEGER;
DECLARE v_sqlstate CHAR(5);
DECLARE v_sqlmessage VARCHAR(256);

GET DIAGNOSTICS CONDITION 1
    v_sqlcode = DB2_RETURNED_SQLCODE,
    v_sqlstate = RETURNED_SQLSTATE,
    v_sqlmessage = MESSAGE_TEXT;
```

### 2. Command-Line Error Detection

When executing scripts via `db2` command line, check exit codes :

- **Exit code 8**: System error
- **Exit code 4**: DB2 error (constraint violation, object not found)
- **Exit code 2**: DB2 warning
- **Exit code 1**: No rows found

**Recommended script pattern**:
```bash
db2 -l migration.log +c -stf migration.sql
if [ $? -ge 4 ]; then
    db2 rollback
    tail -10 migration.log  # Review detailed error
else
    db2 commit
fi
```

### 3. Stored Procedure Error Handling

For comprehensive error detection in SQL PL, use declared handlers :

```sql
CREATE PROCEDURE my_procedure()
BEGIN
    DECLARE v_sqlcode INTEGER DEFAULT 0;
    DECLARE v_sqlstate CHAR(5) DEFAULT '00000';
    DECLARE v_error_message VARCHAR(256);

    -- Declare exit handler for any exception
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        GET DIAGNOSTICS CONDITION 1
            v_sqlcode = DB2_RETURNED_SQLCODE,
            v_sqlstate = RETURNED_SQLSTATE,
            v_error_message = MESSAGE_TEXT;

        -- Log error details to table or file
        INSERT INTO error_log (sqlcode, sqlstate, message, timestamp)
        VALUES (v_sqlcode, v_sqlstate, v_error_message, CURRENT_TIMESTAMP);

        ROLLBACK;
    END;

    -- Your transactional logic here
    UPDATE employee SET salary = salary + 1000 WHERE job = 'MANAGER';
    INSERT INTO audit_log VALUES (CURRENT_TIMESTAMP, 'Salary update');

    COMMIT;
END
```

### 4. DB2 Diagnostic Log Files

For system-level errors, always check:

- **db2diag.log**: Primary diagnostic log with detailed system error information
- **Notification log**: Contains error summaries
- **Command-line logs**: Use `-l logfile.txt` option to capture errors

## Best Practices for Error Detection

1. **Always check SQLCODE/SQLSTATE immediately** after critical operations
2. **Use GET DIAGNOSTICS** for rich error context in stored procedures
3. **Implement transaction rollback percentage monitoring** - anything over 1% warrants investigation
4. **Enable command options** for script execution:
   ```bash
   db2 +c -s -v -l error.log -f script.sql
   ```
   Where `+c` disables autocommit and `-s` stops on error
5. **Use savepoints** for partial rollbacks within complex transactions
6. **Log error details** to persistent tables before rollback to preserve diagnostic information

## Key System Error SQLSTATEs to Monitor

| SQLSTATE | Description | Action |
|----------|-------------|--------|
| **58004** | System error (various causes) | Check db2diag.log immediately |
| **58008** | Communication error | Verify network/connectivity |
| **HY000** | General driver error | Check ODBC/JDBC driver logs  |
| **40001** | Deadlock/timeout | Retry transaction with backoff  |

For production environments, monitoring tools should alert on **SQLCODE < 0** and **Class 58 SQLSTATEs** to proactively detect system-level issues before they cascade.
