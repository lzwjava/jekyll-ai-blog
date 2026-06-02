---
audio: false
generated: true
lang: zh
layout: post
title: Oracle数据库 - 用户账户
translated: true
type: note
---

`ORA-28000: The account is locked` 错误在尝试连接 Oracle 数据库（例如通过瘦 JDBC 驱动程序）时发生，表示您尝试使用的用户账户已被锁定。这通常由多次登录失败、管理员手动锁定或账户过期策略导致。要解决此问题，您需要解锁账户，并在必要时重置密码或检查账户状态。以下是连接 Oracle 数据库时解决此问题的步骤。

---

### 解决 ORA-28000 的步骤

#### 1. **确认错误信息**
   在 JDBC 连接中遇到此错误时，可能显示如下：
   ```
   java.sql.SQLException: ORA-28000: The account is locked
   ```
   这证实问题出在数据库账户本身，而非 JDBC 配置（如 URL、驱动程序或 WebSphere 数据源设置）。

#### 2. **以特权用户身份登录**
   要解锁账户，您需要具有管理权限的数据库用户（如 `SYS`、`SYSTEM` 或具有 `DBA` 角色的用户）。使用 SQL*Plus、SQL Developer 或 JDBC 客户端连接数据库：
   ```bash
   sqlplus / as sysdba
   ```
   或
   ```bash
   sqlplus system/<密码>@<服务名>
   ```
   请将 `<密码>` 和 `<服务名>` 替换为实际凭据和数据库服务名称（例如 `ORCL`）。

#### 3. **检查账户状态**
   执行以下 SQL 查询检查被锁定账户的状态：
   ```sql
   SELECT username, account_status, lock_date
   FROM dba_users
   WHERE username = '您的用户名';
   ```
   - 将 `您的用户名` 替换为您尝试连接的用户名（如 `myuser`）。
   - 查看 `ACCOUNT_STATUS` 列。若显示 `LOCKED` 或 `LOCKED(TIMED)`，说明账户已被锁定。

   示例输出：
   ```
   USERNAME   ACCOUNT_STATUS   LOCK_DATE
   ---------- ---------------- -------------------
   MYUSER     LOCKED           2025-03-24 10:00:00
   ```

#### 4. **解锁账户**
   以特权用户身份执行以下 SQL 命令解锁账户：
   ```sql
   ALTER USER 您的用户名 ACCOUNT UNLOCK;
   ```
   示例：
   ```sql
   ALTER USER myuser ACCOUNT UNLOCK;
   ```

#### 5. **（可选）重置密码**
   如果密码可能已过期或被怀疑错误，可同时重置：
   ```sql
   ALTER USER 您的用户名 IDENTIFIED BY 新密码;
   ```
   示例：
   ```sql
   ALTER USER myuser IDENTIFIED BY mynewpass123;
   ```
   - 重置后，请在 WebSphere 的 `server.xml`（或 JDBC 数据源配置位置）更新密码，并按需重新加密（关于 AES 编码步骤请参考您之前的问题）。

#### 6. **提交更改（如需要）**
   多数情况下，`ALTER USER` 命令会立即生效且无需 `COMMIT`。但若处于事务密集型环境，请通过重启会话或数据库确保无回滚发生。

#### 7. **测试连接**
   重新通过 JDBC 应用程序或简单测试进行连接：
   ```java
   import java.sql.Connection;
   import java.sql.DriverManager;

   public class TestJDBC {
       public static void main(String[] args) throws Exception {
           String url = "jdbc:oracle:thin:@//localhost:1521/ORCL";
           String user = "myuser";
           String password = "mynewpass123";
           Connection conn = DriverManager.getConnection(url, user, password);
           System.out.println("连接成功！");
           conn.close();
       }
   }
   ```
   - 请根据实际环境更新 `url`、`user` 和 `password`。
   - 若测试成功，请相应更新 WebSphere 数据源配置。

#### 8. **检查配置文件策略（防止再次锁定）**
   账户锁定可能源于用户配置文件的安策策略（如 `FAILED_LOGIN_ATTEMPTS` 或 `PASSWORD_LOCK_TIME`）。检查对应用户的配置文件：
   ```sql
   SELECT profile
   FROM dba_users
   WHERE username = '您的用户名';
   ```
   随后查看配置文件的限制：
   ```sql
   SELECT resource_name, limit
   FROM dba_profiles
   WHERE profile = '您的配置文件名';
   ```
   重点关注：
   - `FAILED_LOGIN_ATTEMPTS`：锁定前的失败尝试次数（如 `10`）。
   - `PASSWORD_LOCK_TIME`：锁定时长（如 `1` 天）。

   如需放宽这些设置（若适用），可修改配置文件：
   ```sql
   ALTER PROFILE 您的配置文件名 LIMIT
       FAILED_LOGIN_ATTEMPTS UNLIMITED
       PASSWORD_LOCK_TIME UNLIMITED;
   ```
   示例：
   ```sql
   ALTER PROFILE DEFAULT LIMIT FAILED_LOGIN_ATTEMPTS UNLIMITED;
   ```

#### 9. **重启 WebSphere（如需要）**
   若您使用 WebSphere 并更新了数据源密码，请重启应用服务器以确保更改生效：
   - Liberty：执行 `./bin/server stop` 与 `./bin/server start`。
   - 传统 WebSphere：使用管理控制台或 `stopServer.sh`/`startServer.sh`。

---

### ORA-28000 常见原因
- **多次登录失败**：检查应用程序日志或 WebSphere 日志（如 `SystemOut.log`）中先前的连接错误。
- **手动锁定**：管理员可能有意锁定账户（`ALTER USER myuser ACCOUNT LOCK`）。
- **账户过期**：部分环境在密码过期时会锁定账户。请检查 `dba_users` 中的 `EXPIRY_DATE`。

---

### 故障排除提示
- 若无 `SYS` 或 `SYSTEM` 访问权限，请联系数据库管理员解锁账户。
- 重试前请确认 `server.xml` 中的 JDBC URL、用户名和密码正确无误。
- 若问题持续，请验证 Oracle 监听器是否运行：
  ```bash
  lsnrctl status
  ```

若遇到其他错误或需要具体步骤的帮助，请随时告知！
