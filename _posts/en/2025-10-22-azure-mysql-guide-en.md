---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Azure Database for MySQL Flexible Server Guide
translated: false
type: note
---

Azure Database for MySQL is a fully managed relational database service powered by the MySQL community edition. It handles routine tasks like backups, patching, and monitoring, allowing you to focus on your application. The recommended deployment option is **Flexible Server**, which offers more configuration options and better performance than the older Single Server (which is being retired).

This guide covers creating a server, connecting to it, and performing basic operations. It's based on the Azure portal for simplicity.

## Prerequisites

- An active Azure subscription (create one at [azure.microsoft.com](https://azure.microsoft.com/free/) if needed).
- Access to the Azure portal (portal.azure.com).
- Basic familiarity with MySQL concepts.
- Outbound network access on port 3306 (default for MySQL).
- MySQL Workbench installed for connection (download from [mysql.com](https://dev.mysql.com/downloads/workbench/)).

## Step 1: Create a Flexible Server in the Azure Portal

Follow these steps to provision your server.

1. Sign in to the [Azure portal](https://portal.azure.com).

2. Search for "Azure Database for MySQL Flexible Servers" in the top search bar and select it.

3. Click **Create** to start the wizard.

4. On the **Basics** tab, configure:
   - **Subscription**: Select your subscription.
   - **Resource group**: Create a new one (e.g., `myresourcegroup`) or choose existing.
   - **Server name**: Unique name (e.g., `mydemoserver`), 3-63 characters, lowercase letters/numbers/hyphens. Full hostname will be `<name>.mysql.database.azure.com`.
   - **Region**: Choose closest to your users.
   - **MySQL version**: 8.0 (latest major version).
   - **Workload type**: Development (for testing; use Small/Medium for production).
   - **Compute + storage**: Burstable tier, Standard_B1ms (1 vCore), 10 GiB storage, 100 IOPS, 7-day backups. Adjust for needs (e.g., increase IOPS for migrations).
   - **Availability zone**: No preference (or match your app's zone).
   - **High availability**: Disabled for starters (enable zone-redundant for production).
   - **Authentication**: MySQL and Microsoft Entra (for flexibility).
   - **Admin username**: e.g., `mydemouser` (not root/admin/etc., max 32 chars).
   - **Password**: Strong password (8-128 chars, mix of uppercase/lowercase/numbers/symbols).

5. Switch to the **Networking** tab:
   - **Connectivity method**: Public access (for simplicity; private VNet for production security).
   - **Firewall rules**: Add current client IP (or allow Azure services). You can't change this later.

6. Review settings on **Review + create**, then click **Create**. Deployment takes 5-10 minutes. Monitor via notifications.

7. Once done, pin to dashboard and go to the resource's **Overview** page. Default databases include `information_schema`, `mysql`, etc.

## Step 2: Connect to Your Server

Use MySQL Workbench for a GUI connection. (Alternatives: Azure Data Studio, mysql CLI, or Azure Cloud Shell.)

1. In the portal, go to your server's **Overview** and note:
   - Server name (e.g., `mydemoserver.mysql.database.azure.com`).
   - Admin username.
   - Reset password if needed.

2. Open MySQL Workbench.

3. Click **New Connection** (or edit existing).

4. In the **Parameters** tab:
   - **Connection Name**: e.g., `Demo Connection`.
   - **Connection Method**: Standard (TCP/IP).
   - **Hostname**: Full server name.
   - **Port**: 3306.
   - **Username**: Admin username.
   - **Password**: Enter and store in vault.

5. Click **Test Connection**. If it fails:
   - Verify details from portal.
   - Ensure firewall allows your IP.
   - TLS/SSL is enforced (TLS 1.2); download CA cert from [DigiCert](https://dl.cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem) and bind in Workbench if needed (under SSL tab: Use SSL > Require and specify CA file).

6. Click **OK** to save. Double-click the connection tile to open a query editor.

## Step 3: Create and Manage Databases

Once connected, manage databases via portal or client.

### Via Azure Portal

1. On your server's page, select **Databases** from the left menu.
2. Click **+ Add**:
   - **Database name**: e.g., `testdb`.
   - **Charset**: utf8 (default).
   - **Collation**: utf8_general_ci.
3. Click **Save**.

To delete: Select database(s), click **Delete**.

### Via MySQL Workbench (SQL Queries)

Run these in the query editor:

- Create database: `CREATE DATABASE testdb CHARACTER SET utf8 COLLATE utf8_general_ci;`
- List databases: `SHOW DATABASES;`
- Use database: `USE testdb;`
- Create table: `CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50));`
- Insert data: `INSERT INTO users (name) VALUES ('Alice');`
- Query: `SELECT * FROM users;`

Commit changes with `COMMIT;` if not auto-committing.

## Basic Usage Tips

- **Scaling**: From **Overview** > **Compute + storage**, adjust vCores/storage/IOPS (no downtime for most changes).
- **Backups**: Automated daily; point-in-time restore up to 35 days (configure in **Backup** settings).
- **Monitoring**: Use **Metrics** for CPU/storage insights; set alerts.
- **Security**: Always use SSL (enforced). For production, enable HA, private networking, and Entra ID auth.
- **Migration**: Use mysqldump for small DBs; DMS for large ones.
- **Costs**: Pay for compute/storage; start small and scale. Use calculator at [azure.microsoft.com](https://azure.microsoft.com/pricing/calculator/).
- **Cleanup**: Delete resource group to remove server and avoid charges.

For advanced features like read replicas or server parameters, explore the portal's left menu.

## References

- [Quickstart: Create a Flexible Server Using the Azure Portal](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/quickstart-create-server-portal)
- [Connect Using MySQL Workbench](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/connect-workbench)
- [Create and Manage Databases](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/how-to-create-manage-databases)
- [Azure Database for MySQL Documentation](https://learn.microsoft.com/en-us/azure/mysql/)
