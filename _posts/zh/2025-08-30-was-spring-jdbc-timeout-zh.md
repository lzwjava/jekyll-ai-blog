---
audio: false
generated: true
image: false
lang: zh
layout: post
title: WAS Spring JDBC超时故障排查指南
translated: true
type: note
---

以下是心智模型和快速排查指南。

# 工作原理 (WAS + Spring + JDBC)

1. **DataSource 存在于 WAS 中**

   * 您在 WAS 管理控制台中定义 JDBC Provider 和 **DataSource**（通常全局事务使用 `XA`，或非 XA）。
   * WAS 管理 **JCA 连接池** 并分配 JDBC 连接。

2. **Spring 通过 JNDI 获取 DataSource**

   * 您的 Spring 应用查找服务器的 DataSource（例如 `java:comp/env/jdbc/MyDS`）并对其进行包装：

     * 纯 JDBC：`JdbcTemplate` 使用该 DataSource。
     * JPA/Hibernate：`EntityManagerFactory` 使用它。
   * 事务通常为 **容器 JTA**（`WebSphereUowTransactionManager` 或标准 JTA）。Spring 的 `@Transactional` 会加入容器事务。

3. **调用路径**

   * Web 请求 → WebContainer 线程 → Spring 服务 → 事务开始（JTA）→ 从 **WAS 池** 调用 `DataSource.getConnection()` → 通过驱动程序执行 SQL → 数据库。
   * 超时可能在多个层面触发（Spring、JPA、WAS 池、JTA 事务、JDBC 驱动程序/数据库、网络）。

# 发生超时 — 识别类型

从四个方面考虑。消息/堆栈跟踪通常会告诉您是哪种。

1. **连接获取超时**
   症状：等待池化连接。
   查找关于池耗尽或 `J2CA0086W / J2CA0030E` 的消息。
   典型调节参数：*最大连接数*、*连接超时*、*老化超时*、*清理策略*。

2. **事务超时 (JTA)**
   症状：`WTRN`/`Transaction` 消息；异常如 *“事务在 xxx 秒后超时”*。
   典型调节参数：**总事务生命周期超时**。即使数据库仍在工作，也可能终止长时间运行的数据库操作。

3. **查询/语句超时**
   症状：`java.sql.SQLTimeoutException`、Hibernate/JPA "查询超时" 或 Spring `QueryTimeoutException`。
   调节参数：

   * Spring：`JdbcTemplate.setQueryTimeout(...)`、Hibernate `javax.persistence.query.timeout` / `hibernate.jdbc.timeout`。
   * WAS DataSource 自定义属性（DB2 示例）：`queryTimeout`、`queryTimeoutInterruptProcessingMode`。
   * 驱动程序/数据库端语句超时。

4. **Socket/读取超时 / 网络**
   症状：在长时间获取过程中的某些空闲时间后；低级 `SocketTimeoutException` 或供应商代码。
   调节参数：驱动程序 `loginTimeout`/`socketTimeout`、防火墙/NAT 空闲超时、数据库保活设置。

# 检查位置（按层）

**WAS 管理控制台路径（传统 WAS）**

* JDBC Provider / DataSource：
  资源 → JDBC → 数据源 → *YourDS* →

  * *连接池属性*：**连接超时**、**最大连接数**、**回收时间**、**未使用超时**、**老化超时**、**清理策略**。
  * *自定义属性*：供应商特定属性（例如，DB2 的 `queryTimeout`、`currentSQLID`、`blockingReadConnectionTimeout`、`queryTimeoutInterruptProcessingMode`）。
  * *JAAS – J2C*（如果认证别名相关）。
* 事务：
  应用程序服务器 → *server1* → 容器设置 → **容器服务 → 事务服务** → **总事务生命周期超时**、**最大事务超时**。
* WebContainer：
  线程池大小（如果请求堆积）。

**日志和跟踪**

* 传统 WAS：`<profile_root>/logs/<server>/SystemOut.log` 和 `SystemErr.log`。
  关键组件：`RRA`（资源适配器）、`JDBC`、`ConnectionPool`、`WTRN`（事务）。
  启用跟踪（简洁起始配置）：

  ```
  RRA=all:WTRN=all:Transaction=all:JDBC=all:ConnectionPool=all
  ```

  查找：

  * `J2CA0086W`、`J2CA0114W`（池/连接问题）
  * `WTRN0037W`、`WTRN0124I`（事务超时/回滚）
  * 带有供应商 SQL 代码的 `DSRA`/`SQL` 异常。
* Liberty：`messages.log`，位于 `wlp/usr/servers/<server>/logs/` 下。

**PMI / 监控**

* 为 JDBC 连接池和事务指标启用 **PMI**。关注：

  * 池大小、使用中计数、等待者、等待时间、超时。
  * 事务超时/回滚计数。

**Spring/JPA 应用日志**

* 在应用中开启 SQL + 计时（`org.hibernate.SQL`、`org.hibernate.type`、Spring JDBC 调试）以关联持续时间与超时。

**数据库和驱动程序**

* DB2：`db2diag.log`、`MON_GET_PKG_CACHE_STMT`、活动事件监视器、语句级超时。
* WAS DataSource 或 `DriverManager` 中的驱动程序属性（如果在 WAS 上不使用容器 DataSource，这不典型）。

**网络**

* 具有空闲超时的中间设备。操作系统保活 / 驱动程序保活设置。

# 快速排查流程

1. **分类超时类型**

   * *连接等待？* 查找 `J2CA` 池警告。如果是，增加 **最大连接数**，修复泄漏，调整池，为中毒事件设置 **清理策略 = EntirePool**。
   * *事务超时？* `WTRN` 消息。增加 **总事务生命周期超时** 或减少每个事务的工作量；避免将巨大的批处理作业包装在一个事务中。
   * *查询超时？* `SQLTimeoutException` 或 Spring/Hibernate `QueryTimeout`。将 **Spring/Hibernate** 超时与 **WAS DS** 和 **数据库** 超时对齐；避免设置冲突。
   * *Socket/读取超时？* 网络/驱动程序消息。检查驱动程序的 `socketTimeout`/`loginTimeout`、数据库保活设置和防火墙。

2. **关联时间**

   * 比较失败持续时间与配置的阈值（例如，“大约 30 秒失败” → 查找任何 30 秒的设置：Spring 查询超时 30 秒？事务生命周期 30 秒？池等待 30 秒？）。

3. **检查池健康状况**

   * PMI：**等待者** > 0？**使用中** 接近 **最大值**？有长时间运行的持有者？考虑启用 **连接泄漏检测**（RRA 跟踪显示谁获取了连接）。

4. **数据库可见性**

   * 在数据库上确认：语句是否仍在运行？是否被取消？有任何锁等待？如果是锁 → 考虑锁超时与语句超时。

# 有用的调节参数和注意事项 (WAS + DB2 示例)

* **总事务生命周期超时**（服务器级别）将终止长时间运行的查询，即使您设置了更高的 Spring/Hibernate 超时。保持这些设置一致。
* **queryTimeoutInterruptProcessingMode**（DB2 的 DataSource 自定义属性）：控制 DB2 应如何中断超时的查询（协作式/强制式）。有助于避免线程在超时后卡住。
* **清理策略**：`EntirePool` 可以更快地从致命 SQL 状态（例如，数据库重启）中恢复，代价是出现一个短暂波动。
* **老化/未使用超时**：淘汰陈旧连接以避免防火墙/NAT 空闲超时。
* **验证**：启用 **通过 SQL 验证** 或 **验证超时**，以便在使用前检测到失效连接。
* **线程池**：如果 WebContainer 线程饱和，*症状看起来像超时*。确保 WebContainer 和 Default 线程池大小设置适当。

# 最小 Spring 配置示例

**JNDI DataSource (XML)**

```xml
<jee:jndi-lookup id="dataSource" jndi-name="java:comp/env/jdbc/MyDS" expected-type="javax.sql.DataSource"/>
<bean id="txManager" class="org.springframework.transaction.jta.JtaTransactionManager"/>
<tx:annotation-driven transaction-manager="txManager"/>
```

**JdbcTemplate 查询超时 (Java)**

```java
@Bean JdbcTemplate jdbcTemplate(DataSource ds) {
  JdbcTemplate jt = new JdbcTemplate(ds);
  jt.setQueryTimeout(60); // 秒
  return jt;
}
```

**Hibernate/JPA 超时**

```properties
javax.persistence.query.timeout=60000  # 毫秒
hibernate.jdbc.timeout=60              # 秒
```

# 上报问题时需要收集的信息

* 确切的异常文本 + 堆栈跟踪。
* 时间戳：请求开始、事务开始、查询开始、错误时间。
* WAS DS 池配置（截图或数值）、事务服务超时设置。
* PMI 快照（池等待者、使用中计数、超时计数）。
* 失败时数据库会话/语句的视图。
* 网络拓扑说明（防火墙、代理、空闲计时器）。

如果您粘贴特定的异常片段（J2CA/WTRN/SQL 状态），我可以精确定位到具体层面及需要调整的对应设置。
