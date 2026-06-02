---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Using Amazon RDS for MySQL
translated: false
type: note
---

Amazon RDS (Relational Database Service) for MySQL is a managed database service that makes it easy to set up, operate, and scale MySQL databases in the cloud. It handles routine tasks like backups, patching, and scaling, so you can focus on your application. This guide walks you through the basics: creating a MySQL DB instance, connecting to it, and performing simple operations. We'll use the AWS Management Console for simplicity.

**Note on Costs:** AWS Free Tier offers limited usage for new accounts, but you'll incur charges for resources beyond that. Always delete resources when done to avoid unexpected bills. For production, follow security best practices like using VPCs, encryption, and least-privilege access.

## Prerequisites

- An AWS account (sign up at [aws.amazon.com](https://aws.amazon.com) if needed).
- Basic familiarity with AWS console and MySQL.
- For secure connection testing, we'll create an EC2 instance in the same VPC (Virtual Private Cloud). Determine your public IP address (e.g., via [checkip.amazonaws.com](https://checkip.amazonaws.com)) for SSH access.
- Choose an AWS Region close to you (e.g., US East (N. Virginia)).

**Best Practice:** Use a private DB instance in a VPC to restrict access to trusted resources only. Enable SSL/TLS for encrypted connections.

## Step 1: Create an EC2 Instance for Connection

This sets up a simple Linux server to connect to your private DB instance.

1. Sign in to the [AWS Management Console](https://console.aws.amazon.com) and open the EC2 console.
2. Select your Region.
3. Click **Launch instance**.
4. Configure:
   - **Name:** `ec2-database-connect`.
   - **AMI:** Amazon Linux 2023 (free tier eligible).
   - **Instance type:** t3.micro (free tier eligible).
   - **Key pair:** Create or select an existing one for SSH access.
   - **Network settings:** Edit > Allow SSH traffic from **My IP** (or your specific IP, e.g., `192.0.2.1/32`). Avoid `0.0.0.0/0` for security.
   - Leave defaults for storage and tags.
5. Click **Launch instance**.
6. Note the instance ID, Public IPv4 DNS, and key pair name from the instance details.
7. Wait for the status to show **Running** (2-5 minutes).

**Security Tip:** Restrict SSH to your IP only. Download the key pair (.pem file) securely.

## Step 2: Create a MySQL DB Instance

Use "Easy create" for quick setup with defaults.

1. Open the [RDS console](https://console.aws.amazon.com/rds/).
2. Select the same Region as your EC2 instance.
3. In the navigation pane, click **Databases** > **Create database**.
4. Select **Easy create**.
5. Under **Configuration**:
   - Engine type: **MySQL**.
   - Templates: **Free tier** (or **Sandbox** for paid accounts).
   - DB instance identifier: `database-test1` (or your choice).
   - Master username: `admin` (or custom).
   - Master password: Auto-generate or set a strong one (record it securely).
6. (Optional) Under **Connectivity**, select **Connect to an EC2 compute resource** and choose your EC2 instance for easier setup.
7. Click **Create database**.
8. View the credentials popup (username/password)—save them, as the password isn't retrievable later.
9. Wait for the status to change to **Available** (up to 10-20 minutes). Note the **Endpoint** (DNS name) and port (default: 3306) from the **Connectivity & security** tab.

**Best Practice:** For production, use "Standard create" to customize VPC, backups (enable automated), and storage. Enable deletion protection and multi-AZ for high availability.

## Step 3: Connect to the DB Instance

Connect from your EC2 instance using the MySQL client.

1. SSH into your EC2 instance:

   ```
   ssh -i /path/to/your-key-pair.pem ec2-user@your-ec2-public-dns
   ```

   (Replace with your details; e.g., `ssh -i ec2-database-connect-key-pair.pem ec2-user@ec2-12-345-678-90.compute-1.amazonaws.com`.)

2. On the EC2 instance, update packages:

   ```
   sudo dnf update -y
   ```

3. Install the MySQL client:

   ```
   sudo dnf install mariadb105 -y
   ```

4. Connect to the DB:

   ```
   mysql -h your-db-endpoint -P 3306 -u admin -p
   ```

   Enter the master password when prompted.

If successful, you'll see the MySQL prompt (`mysql>`).

**Troubleshooting:** Ensure security groups allow inbound traffic on port 3306 from the EC2 instance. For external connections, make the DB public (not recommended) or use bastion hosts/VPN.

**Security Tip:** Use `--ssl-mode=REQUIRED` for encrypted connections: `mysql -h endpoint -P 3306 -u admin -p --ssl-mode=REQUIRED`.

## Step 4: Basic Usage

Once connected, you can run SQL commands. Examples:

- Show databases: `SHOW DATABASES;`
- Create a sample database: `CREATE DATABASE myapp;`
- Use it: `USE myapp;`
- Create a table:

  ```
  CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100)
  );
  ```

- Insert data: `INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');`
- Query: `SELECT * FROM users;`
- Exit: `EXIT;`

From applications (e.g., Python, Node.js), use standard MySQL drivers with the endpoint, port, username, and password as connection strings.

**Best Practice:** Monitor performance via CloudWatch, enable automated backups, and scale vertically (instance size) or horizontally (read replicas) as needed.

## Cleanup: Delete Resources

To stop charges:

1. **Delete EC2 instance:** EC2 console > Select instance > **Instance state** > **Terminate** > Confirm.
2. **Delete DB instance:** RDS console > Select DB > **Actions** > **Delete** > Uncheck snapshot creation > Confirm.

Check the AWS Billing console for any running resources.

For more advanced topics like migrations, performance tuning, or API/CLI usage, refer to the AWS documentation.

## References

- [Creating and connecting to a MySQL DB instance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.MySQL.html)
- [Amazon RDS for MySQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MySQL.html)
- [Getting started with Amazon RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.html)
