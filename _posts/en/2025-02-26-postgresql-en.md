---
audio: false
generated: true
lang: en
layout: post
title: 'PostgreSQL: Database Management Guide'
translated: false
type: note
---

Here's a step-by-step guide to using PostgreSQL, a powerful open-source relational database management system:

### 1. **Installation**

- **Windows**: Download from [postgresql.org/download](https://www.postgresql.org/download/) (includes pgAdmin GUI)
- **macOS**: Use Homebrew (`brew install postgresql`) or download the installer
- **Linux** (Debian/Ubuntu):

  ```bash
  sudo apt update
  sudo apt install postgresql postgresql-contrib
  sudo systemctl start postgresql.service
  ```

### 2. **Connect to PostgreSQL**

- Default admin user: `postgres`

  ```bash
  sudo -u postgres psql  # Linux/macOS
  psql -U postgres       # Windows (via PSQL command line)
  ```

- Connect to a specific database:

  ```bash
  psql -U username -d dbname -h localhost -p 5432
  ```

### 3. **Basic Database Operations**

- **Create User/Role**:

  ```sql
  CREATE USER myuser WITH PASSWORD 'mypassword';
  ALTER ROLE myuser WITH CREATEDB;
  ```

- **Create Database**:

  ```sql
  CREATE DATABASE mydb;
  GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
  ```

- **Basic SQL Commands**:

  ```sql
  -- Create table
  CREATE TABLE users (
      id SERIAL PRIMARY KEY,
      name VARCHAR(50),
      email VARCHAR(100) UNIQUE
  );

  -- Insert data
  INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');

  -- Query data
  SELECT * FROM users WHERE name LIKE 'A%';

  -- Update data
  UPDATE users SET email = 'new@email.com' WHERE id = 1;

  -- Delete data
  DELETE FROM users WHERE id = 2;
  ```

### 4. **Advanced Features**

- **Joins**:

  ```sql
  SELECT orders.id, users.name
  FROM orders
  INNER JOIN users ON orders.user_id = users.id;
  ```

- **JSON Support**:

  ```sql
  CREATE TABLE products (
      id SERIAL PRIMARY KEY,
      details JSONB
  );
  ```

- **Full-Text Search**:

  ```sql
  SELECT * FROM documents
  WHERE to_tsvector('english', content) @@ to_tsquery('search & term');
  ```

### 5. **Maintenance**

- **Backup**:

  ```bash
  pg_dump mydb > backup.sql
  pg_dumpall > all_databases.sql
  ```

- **Restore**:

  ```bash
  psql -U username -d mydb -f backup.sql
  ```

- **Vacuum** (reclaim storage):

  ```sql
  VACUUM ANALYZE;
  ```

### 6. **Security**

- Create read-only user:

  ```sql
  CREATE USER readonly WITH PASSWORD 'readpass';
  GRANT CONNECT ON DATABASE mydb TO readonly;
  GRANT USAGE ON SCHEMA public TO readonly;
  GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;
  ```

### 7. **Useful Commands**

- List databases: `\l`
- Switch database: `\c dbname`
- List tables: `\dt`
- Describe table: `\d tablename`
- Show users: `\du`
- Exit psql: `\q`

### 8. **GUI Tools**

- **pgAdmin**: Included with Windows installer
- **DBeaver**: Popular cross-platform GUI
- **TablePlus**: Modern interface with native feel

### 9. **Learning Resources**

- Official Documentation: [postgresql.org/docs](https://www.postgresql.org/docs/)
- Interactive Tutorial: [postgresqltutorial.com](https://www.postgresqltutorial.com/)
- Practice: [pgexercises.com](https://pgexercises.com/)

**Tip**: Always test changes in a development environment before applying to production. Use transactions (`BEGIN`/`COMMIT`) for critical operations.
