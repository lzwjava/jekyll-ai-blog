---
audio: false
generated: true
lang: zh
layout: post
title: PostgreSQL 数据库管理指南
translated: true
type: note
---

以下是使用 PostgreSQL（一款强大的开源关系型数据库管理系统）的逐步指南：

### 1. **安装**

- **Windows**：从 [postgresql.org/download](https://www.postgresql.org/download/) 下载（包含 pgAdmin 图形界面）
- **macOS**：使用 Homebrew（`brew install postgresql`）或下载安装程序
- **Linux**（Debian/Ubuntu）：

  ```bash
  sudo apt update
  sudo apt install postgresql postgresql-contrib
  sudo systemctl start postgresql.service
  ```

### 2. **连接 PostgreSQL**

- 默认管理员用户：`postgres`

  ```bash
  sudo -u postgres psql  # Linux/macOS
  psql -U postgres       # Windows（通过 PSQL 命令行）
  ```

- 连接到指定数据库：

  ```bash
  psql -U username -d dbname -h localhost -p 5432
  ```

### 3. **基础数据库操作**

- **创建用户/角色**：

  ```sql
  CREATE USER myuser WITH PASSWORD 'mypassword';
  ALTER ROLE myuser WITH CREATEDB;
  ```

- **创建数据库**：

  ```sql
  CREATE DATABASE mydb;
  GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
  ```

- **基础 SQL 命令**：

  ```sql
  -- 创建表
  CREATE TABLE users (
      id SERIAL PRIMARY KEY,
      name VARCHAR(50),
      email VARCHAR(100) UNIQUE
  );

  -- 插入数据
  INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');

  -- 查询数据
  SELECT * FROM users WHERE name LIKE 'A%';

  -- 更新数据
  UPDATE users SET email = 'new@email.com' WHERE id = 1;

  -- 删除数据
  DELETE FROM users WHERE id = 2;
  ```

### 4. **高级功能**

- **表连接**：

  ```sql
  SELECT orders.id, users.name
  FROM orders
  INNER JOIN users ON orders.user_id = users.id;
  ```

- **JSON 支持**：

  ```sql
  CREATE TABLE products (
      id SERIAL PRIMARY KEY,
      details JSONB
  );
  ```

- **全文搜索**：

  ```sql
  SELECT * FROM documents
  WHERE to_tsvector('english', content) @@ to_tsquery('search & term');
  ```

### 5. **维护**

- **备份**：

  ```bash
  pg_dump mydb > backup.sql
  pg_dumpall > all_databases.sql
  ```

- **恢复**：

  ```bash
  psql -U username -d mydb -f backup.sql
  ```

- **清理存储空间**：

  ```sql
  VACUUM ANALYZE;
  ```

### 6. **安全**

- 创建只读用户：

  ```sql
  CREATE USER readonly WITH PASSWORD 'readpass';
  GRANT CONNECT ON DATABASE mydb TO readonly;
  GRANT USAGE ON SCHEMA public TO readonly;
  GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;
  ```

### 7. **实用命令**

- 列出数据库：`\l`
- 切换数据库：`\c dbname`
- 列出表：`\dt`
- 查看表结构：`\d tablename`
- 显示用户：`\du`
- 退出 psql：`\q`

### 8. **图形界面工具**

- **pgAdmin**：Windows 安装包自带
- **DBeaver**：流行的跨平台图形界面
- **TablePlus**：具有原生体验的现代界面

### 9. **学习资源**

- 官方文档：[postgresql.org/docs](https://www.postgresql.org/docs/)
- 交互式教程：[postgresqltutorial.com](https://www.postgresqltutorial.com/)
- 练习平台：[pgexercises.com](https://pgexercises.com/)

**提示**：在生产环境应用更改前，务必在开发环境中进行测试。关键操作请使用事务（`BEGIN`/`COMMIT`）。
