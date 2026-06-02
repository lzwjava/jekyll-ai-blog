---
audio: false
generated: true
lang: en
layout: post
title: Oracle Database - User Account
translated: false
type: note
---

The `ORA-28000: The account is locked` error occurs when attempting to connect to an Oracle database (e.g., via a thin JDBC driver) and the user account you’re trying to use has been locked. This typically happens due to too many failed login attempts, manual locking by an administrator, or an account expiration policy. To resolve this, you need to unlock the account, and if necessary, reset the password or check the account status. Below are the steps to fix this issue when connecting to an Oracle database.

---

### Steps to Fix ORA-28000

#### 1. **Verify the Error**
   When you encounter this error in a JDBC connection, it might look like this:
   ```
   java.sql.SQLException: ORA-28000: The account is locked
   ```
   This confirms the issue is with the database account, not the JDBC configuration itself (e.g., URL, driver, or WebSphere datasource settings).

#### 2. **Log in as a Privileged User**
   To unlock the account, you need access to a database user with administrative privileges (e.g., `SYS`, `SYSTEM`, or a user with `DBA` role). Connect to the database using a tool like SQL*Plus, SQL Developer, or a JDBC client:
   ```bash
   sqlplus / as sysdba
   ```
   OR
   ```bash
   sqlplus system/<password>@<service_name>
   ```
   Replace `<password>` and `<service_name>` with your actual credentials and database service name (e.g., `ORCL`).

#### 3. **Check the Account Status**
   Run the following SQL query to check the status of the locked account:
   ```sql
   SELECT username, account_status, lock_date
   FROM dba_users
   WHERE username = 'YOUR_USERNAME';
   ```
   - Replace `YOUR_USERNAME` with the username you’re trying to connect with (e.g., `myuser`).
   - Look at the `ACCOUNT_STATUS` column. If it says `LOCKED` or `LOCKED(TIMED)`, the account is locked.

   Example output:
   ```
   USERNAME   ACCOUNT_STATUS   LOCK_DATE
   ---------- ---------------- -------------------
   MYUSER     LOCKED           24-MAR-25 10:00:00
   ```

#### 4. **Unlock the Account**
   To unlock the account, execute this SQL command as the privileged user:
   ```sql
   ALTER USER your_username ACCOUNT UNLOCK;
   ```
   Example:
   ```sql
   ALTER USER myuser ACCOUNT UNLOCK;
   ```

#### 5. **(Optional) Reset the Password**
   If the password might have expired or you suspect it’s incorrect, reset it while you’re at it:
   ```sql
   ALTER USER your_username IDENTIFIED BY new_password;
   ```
   Example:
   ```sql
   ALTER USER myuser IDENTIFIED BY mynewpass123;
   ```
   - After resetting, update the password in your WebSphere `server.xml` (or wherever the JDBC datasource is configured) and re-encrypt it if necessary (see your previous question for AES encoding steps).

#### 6. **Commit Changes (If Required)**
   In most cases, `ALTER USER` commands take effect immediately and don’t require a `COMMIT`. However, if you’re in a transaction-heavy environment, ensure no rollback occurs by restarting the session or the database if needed.

#### 7. **Test the Connection**
   Try connecting again using your JDBC application or a simple test:
   ```java
   import java.sql.Connection;
   import java.sql.DriverManager;

   public class TestJDBC {
       public static void main(String[] args) throws Exception {
           String url = "jdbc:oracle:thin:@//localhost:1521/ORCL";
           String user = "myuser";
           String password = "mynewpass123";
           Connection conn = DriverManager.getConnection(url, user, password);
           System.out.println("Connection successful!");
           conn.close();
       }
   }
   ```
   - Update the `url`, `user`, and `password` to match your environment.
   - If this works, update your WebSphere datasource configuration accordingly.

#### 8. **Check for Profile Policies (Prevent Future Locks)**
   The account might have locked due to a security policy in the user’s profile (e.g., `FAILED_LOGIN_ATTEMPTS` or `PASSWORD_LOCK_TIME`). Check the profile assigned to the user:
   ```sql
   SELECT profile
   FROM dba_users
   WHERE username = 'YOUR_USERNAME';
   ```
   Then, inspect the profile’s limits:
   ```sql
   SELECT resource_name, limit
   FROM dba_profiles
   WHERE profile = 'YOUR_PROFILE_NAME';
   ```
   Look for:
   - `FAILED_LOGIN_ATTEMPTS`: Number of failed attempts before locking (e.g., `10`).
   - `PASSWORD_LOCK_TIME`: Duration of the lock (e.g., `1` day).

   To relax these settings (if appropriate), modify the profile:
   ```sql
   ALTER PROFILE your_profile_name LIMIT
       FAILED_LOGIN_ATTEMPTS UNLIMITED
       PASSWORD_LOCK_TIME UNLIMITED;
   ```
   Example:
   ```sql
   ALTER PROFILE DEFAULT LIMIT FAILED_LOGIN_ATTEMPTS UNLIMITED;
   ```

#### 9. **Restart WebSphere (If Needed)**
   If you’re using WebSphere and updated the datasource password, restart the application server to ensure the changes take effect:
   - For Liberty: `./bin/server stop` and `./bin/server start`.
   - For traditional WebSphere: Use the Admin Console or `stopServer.sh`/`startServer.sh`.

---

### Common Causes of ORA-28000
- **Too Many Failed Login Attempts**: Check application logs or WebSphere logs (e.g., `SystemOut.log`) for prior connection errors.
- **Manual Lock**: An admin might have locked the account intentionally (`ALTER USER myuser ACCOUNT LOCK`).
- **Expired Account**: Some environments lock accounts when passwords expire. Check `EXPIRY_DATE` in `dba_users`.

---

### Troubleshooting Tips
- If you don’t have `SYS` or `SYSTEM` access, contact your database administrator to unlock the account.
- Ensure the JDBC URL, username, and password in `server.xml` are correct before retrying.
- If the issue persists, verify the Oracle listener is running:
  ```bash
  lsnrctl status
  ```

Let me know if you encounter additional errors or need help with a specific step!
