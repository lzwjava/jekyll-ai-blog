---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Vault JDBC DB2 动态凭据指南
translated: true
type: note
---

我将帮助你将 JDBC datasource 与 HashiCorp Vault 集成，以便为 IBM DB2 动态获取数据库凭据。以下是详细指南：

## Overview

该集成涉及配置应用程序在运行时从 Vault 获取 DB2 凭据，而不是将其硬编码在配置文件中。

## Prerequisites

- HashiCorp Vault server 已运行且可访问
- IBM DB2 数据库
- DB2 JDBC driver (db2jcc4.jar)
- Spring Boot 应用程序（最常见场景）

## Implementation Approaches

### Approach 1: Spring Boot with Spring Cloud Vault

**1. 添加依赖 (Maven)**

```xml
<dependencies>
    <!-- Spring Cloud Vault -->
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-vault-config</artifactId>
    </dependency>
    
    <!-- DB2 JDBC Driver -->
    <dependency>
        <groupId>com.ibm.db2</groupId>
        <artifactId>jcc</artifactId>
        <version>11.5.8.0</version>
    </dependency>
    
    <!-- Spring Boot JDBC -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-jdbc</artifactId>
    </dependency>
</dependencies>
```

**2. 配置 Vault Connection (application.yml)**

```yaml
spring:
  application:
    name: myapp
  cloud:
    vault:
      uri: http://localhost:8200
      token: your-vault-token
      # 或使用其他身份验证方法，如 AppRole
      authentication: TOKEN
      kv:
        enabled: true
        backend: secret
        profile-separator: '/'
  datasource:
    url: jdbc:db2://localhost:50000/MYDB
    driver-class-name: com.ibm.db2.jcc.DB2Driver
    # 用户名和密码将从 Vault 中获取
```

**3. 在 Vault 中存储凭据**

```bash
# 使用 Vault CLI
vault kv put secret/myapp spring.datasource.username=db2user
vault kv put secret/myapp spring.datasource.password=db2password

# 或作为单个命令
vault kv put secret/myapp \
  spring.datasource.username=db2user \
  spring.datasource.password=db2password
```

**4. DataSource 配置 (可选 - 用于自定义配置)**

```java
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.jdbc.DataSourceBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import javax.sql.DataSource;

@Configuration
public class DataSourceConfig {
    
    @Bean
    @ConfigurationProperties(prefix = "spring.datasource")
    public DataSource dataSource() {
        return DataSourceBuilder.create().build();
    }
}
```

### Approach 2: Using Vault's Database Secrets Engine (Dynamic Credentials)

这种方法更安全，因为 Vault 会动态生成临时凭据。

**1. 在 Vault 中启用 Database Secrets Engine**

```bash
vault secrets enable database
```

**2. 在 Vault 中配置 DB2 Connection**

```bash
vault write database/config/mydb2 \
    plugin_name=db2-database-plugin \
    connection_url="jdbc:db2://localhost:50000/MYDB" \
    allowed_roles="myapp-role" \
    username="vaultadmin" \
    password="vaultadminpass"
```

**3. 为 Dynamic Credentials 创建映射角色**

```bash
vault write database/roles/myapp-role \
    db_name=mydb2 \
    creation_statements="CREATE USER {{name}} IDENTIFIED BY {{password}}; GRANT CONNECT, RESOURCE TO {{name}};" \
    default_ttl="1h" \
    max_ttl="24h"
```

**4. Spring Boot 配置**

```yaml
spring:
  cloud:
    vault:
      uri: http://localhost:8200
      token: your-vault-token
      database:
        enabled: true
        role: myapp-role
        backend: database
  datasource:
    url: jdbc:db2://localhost:50000/MYDB
    driver-class-name: com.ibm.db2.jcc.DB2Driver
```

### Approach 3: Manual Integration (Without Spring Cloud Vault)

**Java 代码示例：**

```java
import com.bettercloud.vault.Vault;
import com.bettercloud.vault.VaultConfig;
import com.bettercloud.vault.VaultException;
import com.bettercloud.vault.response.LogicalResponse;
import com.ibm.db2.jcc.DB2SimpleDataSource;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.SQLException;

public class VaultDB2Integration {
    
    private static final String VAULT_ADDR = "http://localhost:8200";
    private static final String VAULT_TOKEN = "your-vault-token";
    private static final String SECRET_PATH = "secret/data/myapp";
    
    public static DataSource createDataSource() throws VaultException {
        // 初始化 Vault 客户端
        VaultConfig config = new VaultConfig()
            .address(VAULT_ADDR)
            .token(VAULT_TOKEN)
            .build();
        
        Vault vault = new Vault(config);
        
        // 从 Vault 获取凭据
        LogicalResponse response = vault.logical().read(SECRET_PATH);
        String username = response.getData().get("username");
        String password = response.getData().get("password");
        
        // 创建 DB2 DataSource
        DB2SimpleDataSource dataSource = new DB2SimpleDataSource();
        dataSource.setServerName("localhost");
        dataSource.setPortNumber(50000);
        dataSource.setDatabaseName("MYDB");
        dataSource.setDriverType(4);
        dataSource.setUser(username);
        dataSource.setPassword(password);
        
        return dataSource;
    }
    
    public static void main(String[] args) {
        try {
            DataSource ds = createDataSource();
            Connection conn = ds.getConnection();
            System.out.println("Successfully connected to DB2!");
            conn.close();
        } catch (VaultException | SQLException e) {
            e.printStackTrace();
        }
    }
}
```

**手动集成方式的 Maven 依赖：**

```xml
<dependencies>
    <dependency>
        <groupId>com.bettercloud</groupId>
        <artifactId>vault-java-driver</artifactId>
        <version>5.1.0</version>
    </dependency>
    <dependency>
        <groupId>com.ibm.db2</groupId>
        <artifactId>jcc</artifactId>
        <version>11.5.8.0</version>
    </dependency>
</dependencies>
```

## Security Best Practices

1. **使用 AppRole Authentication**：在生产环境中代替 token。
```yaml
spring:
  cloud:
    vault:
      authentication: APPROLE
      app-role:
        role-id: your-role-id
        secret-id: your-secret-id
```

2. **启用 SSL/TLS**：用于 Vault 通信。
3. **使用 Dynamic Credentials**：尽可能提高安全性。
4. **设置适当的 TTL**：为凭据设置合理的生存周期。
5. **定期轮换凭据** (Rotate credentials)。
6. **使用 Kubernetes authentication**：如果在 Kubernetes 中运行。

## Testing the Connection

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import javax.sql.DataSource;
import java.sql.Connection;

@Component
public class DatabaseConnectionTest implements CommandLineRunner {
    
    @Autowired
    private DataSource dataSource;
    
    @Override
    public void run(String... args) throws Exception {
        try (Connection conn = dataSource.getConnection()) {
            System.out.println("Database connected successfully!");
            System.out.println("Catalog: " + conn.getCatalog());
        }
    }
}
```

此设置可确保你的 DB2 凭据由 Vault 安全管理，且永远不会在应用程序中硬编码。Spring Cloud Vault 方案（方案 1）是 Spring Boot 应用程序最简单的方法，而动态凭据方案（方案 2）提供了最高的安全性。