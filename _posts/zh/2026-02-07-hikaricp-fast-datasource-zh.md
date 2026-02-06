---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: HikariCP 快速数据源实现指南
translated: true
type: note
---

HikariCP (HikariDataSource) 是 `javax.sql.DataSource` 接口的一项 **具体实现 (specific implementation)**。以下是它们之间的关系说明：

## javax.sql.DataSource

这是一个 **标准 Java 接口** (JDBC 的一部分)，代表了数据库连接的工厂。它仅仅是一个定义了如下方法的契约 (contract)：
- `getConnection()` - 获取数据库连接
- `getConnection(String username, String password)` - 使用凭据获取连接

它不提供任何具体的实现——仅仅是规范。

## HikariDataSource

这是由 HikariCP 库提供的 `DataSource` 的 **具体实现 (concrete implementation)**。它是一个连接池 (connection pool)，用于管理一组可重用的数据库连接，以提高性能。

**主要区别：**

1. **性质**：`DataSource` 是一个接口；`HikariDataSource` 是一个实现了该接口的类

2. **连接池 (Connection pooling)**：原始的 `DataSource` 实现可能每次都会创建新连接。而 HikariCP 维护一个预先建立的连接池，极大地提高了性能

3. **特性 (Features)**：HikariCP 增加了：
   - 极速的 connection pooling (通常被认为是 Java 中最快的连接池)
   - 自动 connection leak 检测
   - Connection 验证
   - 可配置的 pool sizing
   - Metrics 和监控

**实际应用中：**

```java
// 使用接口 (解耦 - 推荐方式)
DataSource dataSource = new HikariDataSource(config);

// 或者直接使用实现类
HikariDataSource hikariDataSource = new HikariDataSource(config);
```

其他常见的 `DataSource` 实现还包括 Apache DBCP、C3P0 和 Tomcat JDBC Pool，但 HikariCP 被广泛认为是速度最快且最可靠的实现，这也是它成为 Spring Boot 默认连接池的原因。