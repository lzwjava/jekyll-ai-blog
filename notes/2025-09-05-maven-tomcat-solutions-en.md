---
audio: false
generated: true
image: false
lang: en
layout: post
title: Solutions for Maven Tomcat Plugin Issues
translated: false
type: note
---

You got the key clue right in your own log:

> `[INFO] Skipping non-war project`

Nothing started because the **tomcat7-maven-plugin only runs webapps packaged as a WAR** with the classic `src/main/webapp` layout. Your project is almost certainly packaged as a JAR right now, so the plugin just exits after the build.

There’s a second gotcha: you’re running **Tomcat 11** (Jakarta `jakarta.*` APIs), but your dependencies are **Spring 5.2.x** (uses `javax.*`). That mismatch means even if Tomcat started, a plain deploy to Tomcat 11 would fail without a migration. Use Tomcat 9 (javax) for Spring 5, or upgrade the app to Spring 6/Jakarta for Tomcat 10/11.

Here are clean paths you can choose—pick one and it’ll work:

### Path 1 — Keep Spring 5, run locally with Jetty plugin (fastest)

No WAR needed; good for hacking.

1. Add plugin:

   ```xml
   <plugin>
     <groupId>org.eclipse.jetty</groupId>
     <artifactId>jetty-maven-plugin</artifactId>
     <version>9.4.54.v20240208</version>
   </plugin>
   ```
2. Run:

   ```bash
   mvn jetty:run -Djetty.port=8080
   ```

This uses `javax.*`, matching Spring 5.

### Path 2 — Keep Spring 5, build a WAR, and use the Tomcat7 plugin

1. In `pom.xml` set WAR packaging:

   ```xml
   <packaging>war</packaging>
   ```
2. Ensure webapp layout exists:

   ```
   src/main/webapp/
   src/main/webapp/WEB-INF/web.xml   # optional if you have a Servlet 3 initializer
   ```
3. (Optional) Add plugin config:

   ```xml
   <plugin>
     <groupId>org.apache.tomcat.maven</groupId>
     <artifactId>tomcat7-maven-plugin</artifactId>
     <version>2.2</version>
     <configuration>
       <path>/</path>
       <port>8080</port>
     </configuration>
   </plugin>
   ```
4. Run:

   ```bash
   mvn tomcat7:run            # for exploded webapp
   # or
   mvn package && mvn tomcat7:run-war
   ```

### Path 3 — Keep Spring 5, deploy to a standalone Tomcat 9

This matches `javax.*` without changing code.

```bash
brew install tomcat@9
/opt/homebrew/opt/tomcat@9/bin/catalina start
```

Build and drop your WAR into `.../tomcat@9/libexec/webapps/`.

### Path 4 — Upgrade the app to Spring 6/Jakarta, stick with Tomcat 11

If you want modern Tomcat:

* Upgrade to Spring Framework 6.x / Spring Boot 3.x.
* Change imports from `javax.*` to `jakarta.*`.
* Then Tomcat 10/11 is fine.

---

#### Why `mvn tomcat7:run` printed success but “nothing happened”

* Maven phases completed successfully, but the plugin saw **non-WAR packaging**, so it **didn’t start** an embedded Tomcat. That’s exactly what “Skipping non-war project” means.

---

If you tell me which path you prefer, I’ll give you the exact `pom.xml` and minimal files for that setup (including a tiny controller and how to hit it at `http://localhost:8080/hello`).
