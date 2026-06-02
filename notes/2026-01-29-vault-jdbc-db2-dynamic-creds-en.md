---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Vault JDBC DB2 Dynamic Credentials Guide
translated: false
type: note
---

I'll help you integrate a JDBC datasource with HashiCorp Vault to dynamically fetch database credentials for IBM DB2. Here's a comprehensive guide:

## Overview

The integration involves configuring your application to retrieve DB2 credentials from Vault at runtime instead of hardcoding them in configuration files.

## Prerequisites

- HashiCorp Vault server running and accessible
- IBM DB2 database
- DB2 JDBC driver (db2jcc4.jar)
- Spring Boot application (most common scenario)

## Implementation Approaches

### Approach 1: Spring Boot with Spring Cloud Vault

**1. Add Dependencies (Maven)**

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

**2. Configure Vault Connection (application.yml)**

```yaml
spring:
  application:
    name: myapp
  cloud:
    vault:
      uri: http://localhost:8200
      token: your-vault-token
      # Or use other authentication methods like AppRole
      authentication: TOKEN
      kv:
        enabled: true
        backend: secret
        profile-separator: '/'
  datasource:
    url: jdbc:db2://localhost:50000/MYDB
    driver-class-name: com.ibm.db2.jcc.DB2Driver
    # Username and password will be fetched from Vault
```

**3. Store Credentials in Vault**

```bash
# Using Vault CLI
vault kv put secret/myapp spring.datasource.username=db2user
vault kv put secret/myapp spring.datasource.password=db2password

# Or as a single command
vault kv put secret/myapp \
  spring.datasource.username=db2user \
  spring.datasource.password=db2password
```

**4. DataSource Configuration (Optional - for custom configuration)**

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

This approach is more secure as Vault generates temporary credentials dynamically.

**1. Enable Database Secrets Engine in Vault**

```bash
vault secrets enable database
```

**2. Configure DB2 Connection in Vault**

```bash
vault write database/config/mydb2 \
    plugin_name=db2-database-plugin \
    connection_url="jdbc:db2://localhost:50000/MYDB" \
    allowed_roles="myapp-role" \
    username="vaultadmin" \
    password="vaultadminpass"
```

**3. Create a Role for Dynamic Credentials**

{% raw %}
```bash
vault write database/roles/myapp-role \
    db_name=mydb2 \
    creation_statements="CREATE USER {{name}} IDENTIFIED BY {{password}}; GRANT CONNECT, RESOURCE TO {{name}};" \
    default_ttl="1h" \
    max_ttl="24h"
```
{% endraw %}

**4. Spring Boot Configuration**

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

**Java Code Example:**

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
        // Initialize Vault client
        VaultConfig config = new VaultConfig()
            .address(VAULT_ADDR)
            .token(VAULT_TOKEN)
            .build();

        Vault vault = new Vault(config);

        // Fetch credentials from Vault
        LogicalResponse response = vault.logical().read(SECRET_PATH);
        String username = response.getData().get("username");
        String password = response.getData().get("password");

        // Create DB2 DataSource
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

**Maven Dependencies for Manual Approach:**

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

1. **Use AppRole Authentication** instead of tokens in production:
```yaml
spring:
  cloud:
    vault:
      authentication: APPROLE
      app-role:
        role-id: your-role-id
        secret-id: your-secret-id
```

2. **Enable SSL/TLS** for Vault communication
3. **Use Dynamic Credentials** when possible for better security
4. **Set appropriate TTL** values for credentials
5. **Rotate credentials** regularly
6. **Use Kubernetes authentication** if running in Kubernetes

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

This setup ensures your DB2 credentials are securely managed by Vault and never hardcoded in your application. The Spring Cloud Vault approach (Approach 1) is the simplest for Spring Boot applications, while the dynamic credentials approach (Approach 2) provides the highest security.
