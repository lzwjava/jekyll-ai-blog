---
audio: false
generated: true
lang: en
layout: post
title: Create a PostgreSQL Database
translated: false
type: note
---

You're already in the PostgreSQL interactive terminal (`psql`) as the `postgres` user, which is great! To create a database in PostgreSQL, you can use the `CREATE DATABASE` command. Here's a step-by-step guide:

1. **Ensure you're in `psql`**:
   You already are, as shown by the `postgres=#` prompt.

2. **Create a database**:
   Use the following command to create a new database. Replace `mydatabase` with your desired database name:

   ```sql
   CREATE DATABASE mydatabase;
   ```

   This creates a database named `mydatabase`.

3. **Verify the database was created**:
   List all databases to confirm:

   ```sql
   \l
   ```

   This will display a table of all databases, including `mydatabase`.

4. **Connect to the new database**:
   To start working in the new database, connect to it with:

   ```sql
   \c mydatabase
   ```

   This switches your session to `mydatabase`.

5. **Optional: Create a user and grant permissions**:
   If you want a specific user to manage this database, create one and grant privileges:

   ```sql
   CREATE USER myuser WITH ENCRYPTED PASSWORD 'mypassword';
   GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
   ```

   Replace `myuser` and `mypassword` with your desired username and password.

6. **Exit `psql`**:
   When done, exit with:

   ```sql
   \q
   ```

### Notes

- The `Permission denied` error you saw (`could not change directory to "/home/lzw/projects/lzwjava.github.io"`) is because the `postgres` user doesn't have access to your home directory. This doesn't affect database creation but might show up when running `psql` from a restricted directory. You can avoid this by running `psql` from a directory the `postgres` user can access or by not changing directories (e.g., run `sudo -u postgres psql` from `/tmp`).
- The `ls` command you tried in `psql` isn't valid. Use `\l` to list databases or `\dt` to list tables within a database.
- Ensure the PostgreSQL service is running (`sudo systemctl start postgresql.service`), which you already did.

### Example Session

```sql
postgres=# CREATE DATABASE mydatabase;
CREATE DATABASE
postgres=# \l
                                  List of databases
   Name      |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges
-------------+----------+----------+-------------+-------------+-----------------------
 mydatabase  | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 postgres    | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 template0   | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
             |          |          |             |             | postgres=CTc/postgres
 template1   | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
             |          |          |             |             | postgres=CTc/postgres
(4 rows)

postgres=# \c mydatabase
You are now connected to database "mydatabase" as user "postgres".
mydatabase=# \q
```

If you need further help (e.g., setting up tables, users, or connecting from an application), let me know!
