---
audio: false
generated: true
lang: zh
layout: post
title: 创建PostgreSQL数据库
translated: true
type: note
---

您已经以 `postgres` 用户身份进入了 PostgreSQL 交互式终端 (`psql`)，这很好！要在 PostgreSQL 中创建数据库，您可以使用 `CREATE DATABASE` 命令。以下是分步指南：

1. **确保您在 `psql` 中**：
   您已经在其中了，如 `postgres=#` 提示符所示。

2. **创建数据库**：
   使用以下命令创建一个新数据库。将 `mydatabase` 替换为您想要的数据库名称：

   ```sql
   CREATE DATABASE mydatabase;
   ```

   这将创建一个名为 `mydatabase` 的数据库。

3. **验证数据库是否创建成功**：
   列出所有数据库以确认：

   ```sql
   \l
   ```

   这将显示一个包含所有数据库的表格，包括 `mydatabase`。

4. **连接到新数据库**：
   要开始在新数据库中工作，请使用以下命令连接到它：

   ```sql
   \c mydatabase
   ```

   这将把您的会话切换到 `mydatabase`。

5. **可选：创建用户并授予权限**：
   如果您希望特定用户管理此数据库，请创建一个用户并授予权限：

   ```sql
   CREATE USER myuser WITH ENCRYPTED PASSWORD 'mypassword';
   GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
   ```

   将 `myuser` 和 `mypassword` 替换为您想要的用户名和密码。

6. **退出 `psql`**：
   完成后，使用以下命令退出：

   ```sql
   \q
   ```

### 注意

- 您看到的 `Permission denied` 错误（`could not change directory to "/home/lzw/projects/lzwjava.github.io"`）是因为 `postgres` 用户无权访问您的主目录。这不会影响数据库创建，但在从受限目录运行 `psql` 时可能会出现。您可以通过从 `postgres` 用户可以访问的目录运行 `psql` 或不更改目录（例如，从 `/tmp` 运行 `sudo -u postgres psql`）来避免此问题。
- 您在 `psql` 中尝试的 `ls` 命令无效。请使用 `\l` 列出数据库，或使用 `\dt` 列出数据库中的表。
- 确保 PostgreSQL 服务正在运行（`sudo systemctl start postgresql.service`），您已经这样做了。

### 示例会话

```sql
postgres=# CREATE DATABASE mydatabase;
CREATE DATABASE
postgres=# \l
                                  数据库列表
   名称     |  所有者  | 编码 |    排序规则     |     类型     |   访问权限
------------+----------+----------+-------------+-------------+-----------------------
 mydatabase  | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 postgres    | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 template0   | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
             |          |          |             |             | postgres=CTc/postgres
 template1   | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
             |          |          |             |             | postgres=CTc/postgres
(4 行记录)

postgres=# \c mydatabase
您现在已连接到数据库 "mydatabase"，用户 "postgres"。
mydatabase=# \q
```

如果您需要进一步的帮助（例如，设置表、用户或从应用程序连接），请告诉我！
