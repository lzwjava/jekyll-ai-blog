---
audio: false
generated: true
image: false
lang: en
layout: post
title: WAS Spring JDBC Timeout Triage Guide
translated: false
type: note
---

Here’s the mental model and a quick triage playbook.

# How it works (WAS + Spring + JDBC)

1. **DataSource lives in WAS**

   * You define a JDBC Provider and a **DataSource** (usually `XA` for global tx, or non-XA) in the WAS admin console.
   * WAS manages the **JCA connection pool** and hands out JDBC Connections.

2. **Spring gets the DataSource via JNDI**

   * Your Spring app looks up the server’s DataSource (e.g., `java:comp/env/jdbc/MyDS`) and wraps it:

     * Plain JDBC: `JdbcTemplate` uses that DataSource.
     * JPA/Hibernate: the `EntityManagerFactory` uses it.
   * Transactions are typically **container JTA** (`WebSphereUowTransactionManager` or standard JTA). Spring’s `@Transactional` joins the container tx.

3. **Call path**

   * Web request → WebContainer thread → Spring service → tx begins (JTA) → `DataSource.getConnection()` from **WAS pool** → SQL via driver → DB.
   * Timeouts can fire at multiple layers (Spring, JPA, WAS pool, JTA tx, JDBC driver/DB, network).

# When a timeout happens — identify which kind

Think in four buckets. The message/stack usually tells you which.

1. **Connection acquisition timeout**
   Symptom: waiting for a pooled connection.
   Look for messages about pool exhaustion or `J2CA0086W / J2CA0030E`.
   Typical knobs: *Maximum Connections*, *Connection Timeout*, *Aged Timeout*, *Purge Policy*.

2. **Transaction timeout (JTA)**
   Symptom: `WTRN`/`Transaction` messages; exception like *“Transaction timed out after xxx seconds”*.
   Typical knob: **Total transaction lifetime timeout**. Can kill long DB ops even if DB is still working.

3. **Query/statement timeout**
   Symptom: `java.sql.SQLTimeoutException`, Hibernate/JPA “query timeout”, or Spring `QueryTimeoutException`.
   Knobs:

   * Spring: `JdbcTemplate.setQueryTimeout(...)`, Hibernate `javax.persistence.query.timeout` / `hibernate.jdbc.timeout`.
   * WAS DataSource custom properties (DB2 examples): `queryTimeout`, `queryTimeoutInterruptProcessingMode`.
   * Driver/DB-side statement timeout.

4. **Socket/read timeout / network**
   Symptom: after some idle time during a long fetch; low-level `SocketTimeoutException` or vendor code.
   Knobs: driver `loginTimeout`/`socketTimeout`, firewall/NAT idles, DB keepalives.

# Where to check (by layer)

**WAS Admin Console paths (traditional WAS)**

* JDBC Provider / DataSource:
  Resources → JDBC → Data sources → *YourDS* →

  * *Connection pool properties*: **Connection timeout**, **Maximum connections**, **Reap time**, **Unused timeout**, **Aged timeout**, **Purge policy**.
  * *Custom properties*: vendor-specific (e.g., DB2 `queryTimeout`, `currentSQLID`, `blockingReadConnectionTimeout`, `queryTimeoutInterruptProcessingMode`).
  * *JAAS – J2C* if auth aliases matter.
* Transactions:
  Application servers → *server1* → Container Settings → **Container Services → Transaction Service** → **Total transaction lifetime timeout**, **Maximum transaction timeout**.
* WebContainer:
  Thread pool size (if requests pile up).

**Logs & traces**

* Traditional WAS: `<profile_root>/logs/<server>/SystemOut.log` and `SystemErr.log`.
  Key components: `RRA` (resource adapters), `JDBC`, `ConnectionPool`, `WTRN` (transactions).
  Enable trace (concise starter):

  ```
  RRA=all:WTRN=all:Transaction=all:JDBC=all:ConnectionPool=all
  ```

  Look for:

  * `J2CA0086W`, `J2CA0114W` (pool/connection issues)
  * `WTRN0037W`, `WTRN0124I` (tx timeouts/rollbacks)
  * `DSRA`/`SQL` exceptions with vendor SQL codes.
* Liberty: `messages.log` under `wlp/usr/servers/<server>/logs/`.

**PMI / Monitoring**

* Enable **PMI** for JDBC Connection Pools and Transaction metrics. Watch:

  * Pool size, in-use count, waiters, wait time, timeouts.
  * Transaction timeouts/rollback counts.

**Spring/JPA app logs**

* Turn on SQL + timing in your app (`org.hibernate.SQL`, `org.hibernate.type`, Spring JDBC debug) to correlate durations vs. timeouts.

**Database & driver**

* DB2: `db2diag.log`, `MON_GET_PKG_CACHE_STMT`, activity event monitors, statement-level timeouts.
* Driver properties in the WAS DataSource or `DriverManager` if you’re not using container DS (not typical on WAS).

**Network**

* Middleboxes with idle timeouts. OS keepalive / driver keepalive settings.

# Quick triage flow

1. **Classify the timeout**

   * *Connection wait?* Look for `J2CA` pool warnings. If yes, increase **Maximum connections**, fix leak, tune pool, set **Purge Policy = EntirePool** for poison events.
   * *Tx timeout?* `WTRN` messages. Increase **Total transaction lifetime timeout** or reduce work per tx; avoid wrapping huge batch jobs in one tx.
   * *Query timeout?* `SQLTimeoutException` or Spring/Hibernate `QueryTimeout`. Align **Spring/Hibernate** timeouts with **WAS DS** and **DB** timeouts; avoid conflicting settings.
   * *Socket/read timeout?* Network/driver messages. Check driver’s `socketTimeout`/`loginTimeout`, DB keepalives, and firewalls.

2. **Correlate timings**

   * Compare the failing duration with the configured thresholds (e.g., “fails at \~30s” → find any 30s setting: Spring query timeout 30s? tx lifetime 30s? pool wait 30s?).

3. **Check pooling health**

   * PMI: are **waiters** > 0? Is **in-use** near **max**? Long-running holders? Consider enabling **connection leak detection** (RRA trace shows who took the connection).

4. **DB visibility**

   * Confirm on the DB: was the statement still running? Was it cancelled? Any lock waits? If locks → consider lock timeout vs. statement timeout.

# Useful knobs & gotchas (WAS + DB2 examples)

* **Total transaction lifetime timeout** (server level) will kill long queries even if you set a higher Spring/Hibernate timeout. Keep these consistent.
* **queryTimeoutInterruptProcessingMode** (DataSource custom property for DB2): controls how DB2 should interrupt a timed-out query (cooperative/forceful). Helps avoid threads stuck past timeouts.
* **Purge policy**: `EntirePool` can recover faster from fatal SQL states (e.g., DB restart) at the cost of a blip.
* **Aged/Unused timeout**: retire stale connections to dodge firewall/NAT idles.
* **Validation**: enable **validation by SQL** or **validation timeout** so dead connections are detected before use.
* **Thread pools**: if WebContainer threads are saturated, *symptoms look like timeouts*. Ensure WebContainer and Default thread pools are sized appropriately.

# Minimal Spring wiring examples

**JNDI DataSource (XML)**

```xml
<jee:jndi-lookup id="dataSource" jndi-name="java:comp/env/jdbc/MyDS" expected-type="javax.sql.DataSource"/>
<bean id="txManager" class="org.springframework.transaction.jta.JtaTransactionManager"/>
<tx:annotation-driven transaction-manager="txManager"/>
```

**JdbcTemplate query timeout (Java)**

```java
@Bean JdbcTemplate jdbcTemplate(DataSource ds) {
  JdbcTemplate jt = new JdbcTemplate(ds);
  jt.setQueryTimeout(60); // seconds
  return jt;
}
```

**Hibernate/JPA timeout**

```properties
javax.persistence.query.timeout=60000  # ms
hibernate.jdbc.timeout=60              # seconds
```

# What to capture when you escalate

* Exact exception text + stack trace.
* Timestamps: request start, tx begin, query start, error time.
* WAS DS pool config (screenshot or values), Transaction Service timeouts.
* PMI snapshot (pool waiters, in-use, timeout counts).
* DB view of the session/statement at failure time.
* Network topology notes (firewalls, proxies, idle timers).

If you paste a specific exception snippet (J2CA/WTRN/SQL state), I can pinpoint the exact layer and the matching setting to adjust.
