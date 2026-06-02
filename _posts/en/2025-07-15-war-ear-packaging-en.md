---
audio: false
generated: true
image: false
lang: en
layout: post
title: WAR vs EAR Packaging Guide
translated: false
type: note
---

Here’s a practical, no-table comparison of Maven **WAR** vs **EAR** packaging and how you’d use each in real projects.

# What each packaging is for

* **WAR (`packaging: war`)** – A single web application: servlets/Jakarta REST, JSP/JSF, Spring MVC/Boot (as WAR), etc. Deployed to a servlet container (Tomcat/Jetty) or a full app server’s web tier.
* **EAR (`packaging: ear`)** – A bundle of multiple modules deployed together to a full Java EE/Jakarta EE app server (WildFly/JBoss EAP, WebLogic, WebSphere). Typically contains one or more WARs, EJB JARs, and shared libraries with one deployment unit.

# Typical when-to-choose

* Choose **WAR** if you have a single web app or Spring Boot app and don’t need EJBs or multi-module server features.
* Choose **EAR** if you must deploy several modules together (e.g., EJBs + multiple WARs + shared libs), need app-server services (XA, centralized security realms, JMS, distributed transactions) across modules, or your organization mandates EARs.

# What’s inside the artifact

* **WAR** contents: `/WEB-INF/classes`, `/WEB-INF/lib`, optional `web.xml` (or annotations), static assets. One classloader per WAR in most servers.
* **EAR** contents: `*.war`, `*.jar` (EJBs/utility), `META-INF/application.xml` (or annotations/skinny config), and optional `lib/` for libraries shared across modules. Provides an EAR-level classloader visible to all modules.

# Dependency & classloading considerations

* **WAR**: Declare servlet/Jakarta EE APIs as `provided`; everything else goes under `/WEB-INF/lib`. Isolation is simpler; fewer version clashes.
* **EAR**: Put common libs in the EAR’s `lib/` (via `maven-ear-plugin`), so all modules share one version. Watch for conflicts between module libs and server-provided APIs; align versions and use `provided` where appropriate.

# Maven plugins you’ll use

* **WAR projects**: `maven-war-plugin`
* **EAR aggregator**: `maven-ear-plugin`
* **EJB modules (if any)**: `maven-ejb-plugin`
* Parent/aggregator often uses `packaging: pom` to tie modules together.

# Minimal examples

Single webapp (WAR):

```xml
<!-- pom.xml -->
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId><artifactId>my-web</artifactId><version>1.0.0</version>
  <packaging>war</packaging>

  <dependencies>
    <!-- Use provided for server APIs -->
    <dependency>
      <groupId>jakarta.platform</groupId><artifactId>jakarta.jakartaee-web-api</artifactId>
      <version>10.0.0</version><scope>provided</scope>
    </dependency>
    <!-- Your app deps -->
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <artifactId>maven-war-plugin</artifactId>
        <version>3.4.0</version>
        <!-- Optional: configure webResources, warName, filtering -->
      </plugin>
    </plugins>
  </build>
</project>
```

Multi-module EAR with a WAR and an EJB:

```xml
<!-- parent/pom.xml -->
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId><artifactId>my-app</artifactId><version>1.0.0</version>
  <packaging>pom</packaging>
  <modules>
    <module>ejb-module</module>
    <module>web-module</module>
    <module>ear-assembly</module>
  </modules>
</project>
```

```xml
<!-- ejb-module/pom.xml -->
<project>
  <parent>…</parent>
  <artifactId>ejb-module</artifactId>
  <packaging>ejb</packaging>
  <dependencies>
    <dependency>
      <groupId>jakarta.platform</groupId><artifactId>jakarta.jakartaee-api</artifactId>
      <version>10.0.0</version><scope>provided</scope>
    </dependency>
  </dependencies>
</project>
```

```xml
<!-- web-module/pom.xml -->
<project>
  <parent>…</parent>
  <artifactId>web-module</artifactId>
  <packaging>war</packaging>
  <dependencies>
    <dependency>
      <groupId>jakarta.platform</groupId><artifactId>jakarta.jakartaee-web-api</artifactId>
      <version>10.0.0</version><scope>provided</scope>
    </dependency>
    <dependency>
      <groupId>com.example</groupId><artifactId>ejb-module</artifactId><version>1.0.0</version>
      <type>ejb</type> <!-- allows @EJB injection -->
    </dependency>
  </dependencies>
</project>
```

```xml
<!-- ear-assembly/pom.xml -->
<project>
  <parent>…</parent>
  <artifactId>ear-assembly</artifactId>
  <packaging>ear</packaging>

  <dependencies>
    <dependency>
      <groupId>com.example</groupId><artifactId>web-module</artifactId><version>1.0.0</version>
      <type>war</type>
    </dependency>
    <dependency>
      <groupId>com.example</groupId><artifactId>ejb-module</artifactId><version>1.0.0</version>
      <type>ejb</type>
    </dependency>
    <!-- Libraries to put in EAR/lib shared by all modules -->
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId><artifactId>jackson-databind</artifactId>
      <version>2.17.2</version>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-ear-plugin</artifactId>
        <version>3.4.0</version>
        <configuration>
          <defaultLibBundleDir>lib</defaultLibBundleDir>
          <modules>
            <webModule>
              <groupId>com.example</groupId>
              <artifactId>web-module</artifactId>
              <contextRoot>/myapp</contextRoot>
            </webModule>
            <ejbModule>
              <groupId>com.example</groupId>
              <artifactId>ejb-module</artifactId>
            </ejbModule>
          </modules>
          <!-- Optional: generate application.xml, or provide a custom one -->
          <generateApplicationXml>true</generateApplicationXml>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
```

Build results:

* `mvn -pl web-module -am clean package` → `web-module-1.0.0.war`
* `mvn -pl ear-assembly -am clean package` → `ear-assembly-1.0.0.ear` containing the WAR, EJB, and `lib/`.

# Operational differences that matter

* **Deployment target**

  * WAR: servlet container or app server web tier.
  * EAR: full app server; deploys all modules atomically.
* **Transactions & messaging**

  * WAR alone uses what the container exposes; complex XA/JMS setups often live in EJBs within EARs.
* **Versioning & rollout**

  * WAR: simple to rebuild and redeploy a single app.
  * EAR: coordinates versions of many modules; one deployment unit for consistency.
* **Start-up time & local dev**

  * WAR: fast feedback, lighter runtime.
  * EAR: heavier; IDE/server integration helps but cycles are slower.
* **Modern Spring Boot note**

  * Boot prefers executable **JAR**; WAR is supported if you deploy to an external container.
  * Boot does **not** target EAR; if you must use an app server, deploy Boot as WAR, and avoid EAR unless your platform requires it.

# Common pitfalls & tips

* Use `provided` for server APIs to avoid bundling them.
* For EARs, put shared libs in `defaultLibBundleDir` to prevent duplicate copies inside each WAR/EJB.
* Align Jakarta EE versions across modules; mismatches cause classloading errors.
* On WebLogic/WebSphere, mind classloader policies (parent-first vs parent-last); sometimes you need vendor-specific descriptors.
* If you don’t need EJBs/XA, a plain WAR (or Boot JAR) is simpler and usually more portable.

If you tell me your app server (Tomcat vs WildFly/WebLogic/etc.) and whether you have EJBs or multiple webapps, I can sketch the exact POMs and deployment descriptors you’ll need.
